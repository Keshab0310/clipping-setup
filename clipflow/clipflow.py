"""Approval queue and upload prep for finished vertical clips.

    python clipflow.py ingest
    python clipflow.py list
    python clipflow.py approve c001 --date 2026-11-22 --slot 5pm --title "..." --description "... #shorts" --rights "Campaign name"
    python clipflow.py reject c002
    python clipflow.py due --date 2026-11-22 --slot 5pm
    python clipflow.py posted c001 --platform youtube --url https://www.youtube.com/shorts/ID
    python clipflow.py submitted c001

Nothing here publishes. Posting happens through the runbooks, with a final human confirmation.
"""

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

HOME = Path(os.environ.get("CLIPFLOW_HOME", Path(__file__).resolve().parent))
CAPTURES = Path(os.environ.get("CLIPFLOW_CAPTURES", r"D:\Clipping\gtavi-claudecode\captures"))
CONFIG = HOME / "config.json"
QUEUE = HOME / "queue.json"
LOG = HOME / "content_log.csv"
SLOTS = ("noon", "5pm", "8pm")
PLATFORMS = ("youtube", "tiktok", "instagram", "facebook")
DEFAULTS = {
    "accounts": {"youtube": "", "tiktok": "", "instagram": "", "facebook": ""},
    "default_platforms": ["youtube"],
    "max_posts_per_day": 2,
    "upload_limit_mb": 9.5,
    "campaign_submit_minutes": 30,
}


class FlowError(Exception):
    pass


def load_config():
    if not CONFIG.exists():
        return json.loads(json.dumps(DEFAULTS))
    return {**DEFAULTS, **json.loads(CONFIG.read_text(encoding="utf-8"))}


def load_queue():
    return json.loads(QUEUE.read_text(encoding="utf-8")) if QUEUE.exists() else []


def save_queue(items):
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    staged = QUEUE.with_suffix(".tmp")
    staged.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(staged, QUEUE)


def find_item(items, clip_id):
    for item in items:
        if item["id"] == clip_id:
            return item
    raise FlowError(f"No clip named {clip_id}.")


def media_seconds(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def review_rows(capture):
    report = capture / "review.md"
    if not report.exists():
        return "none", {}
    text = report.read_text(encoding="utf-8")
    reviewer = "claude" if "Reviewer: Claude" in text else "chat ranking"
    rows = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 9 and cells[8].endswith(".mp4"):
            rows[cells[8]] = {"score": cells[4], "hook": cells[6], "reason": cells[7]}
    return reviewer, rows


def source_channel(capture):
    jobs = sorted(p.name for p in (capture / "jobs").glob("*")) if (capture / "jobs").exists() else []
    names = [name.rsplit("-", 1)[0] for name in jobs if not name.lower().startswith("spike")]
    return names[0] if names else "unknown"


def cmd_ingest(args):
    items = load_queue()
    known = {item["origin"] for item in items}
    clips = HOME / "clips"
    clips.mkdir(parents=True, exist_ok=True)
    next_n = max((int(item["id"][1:]) for item in items), default=0) + 1
    added = 0
    for capture in sorted(p for p in CAPTURES.glob("*") if p.is_dir()):
        reviewer, rows = review_rows(capture)
        for draft in sorted((capture / "drafts").glob("*.mp4")):
            origin = f"{capture.name}/{draft.name}"
            if origin in known:
                continue
            clip_id = f"c{next_n:03}"
            master = clips / f"{clip_id}.mp4"
            shutil.copy2(draft, master)
            row = rows.get(draft.name, {})
            items.append({
                "id": clip_id, "origin": origin, "file": str(master), "status": "needs_review",
                "seconds": round(media_seconds(master), 1), "source": source_channel(capture),
                "reviewer": reviewer, "score": row.get("score", "-"), "hook": row.get("hook", ""),
                "reason": row.get("reason", ""), "title": "", "description": "", "rights": "",
                "campaign": "", "date": "", "slot": "", "platforms": [], "posts": {},
            })
            next_n += 1
            added += 1
    save_queue(items)
    print(f"Added {added} clip(s). Queue now holds {len(items)}.")


def cmd_list(args):
    items = [i for i in load_queue() if not args.status or i["status"] == args.status]
    if not items:
        print("Queue is empty.")
    for i in items:
        when = f"{i['date']} {i['slot']}" if i["date"] else "-"
        print(f"{i['id']}  {i['status']:<12} {i['seconds']:>5}s  score {i['score']:<2} {when:<16} "
              f"{i['source']}  {i['title'] or i['hook'] or i['origin']}")


def parse_day(value):
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use a date like 2026-11-22.") from error


def cmd_approve(args):
    config = load_config()
    items = load_queue()
    item = find_item(items, args.id)
    if item["status"] not in {"needs_review", "approved"}:
        raise FlowError(f"{item['id']} is {item['status']} and cannot be approved.")
    if args.date < date.today():
        raise FlowError("The post date is in the past.")
    if not args.rights.strip():
        raise FlowError("--rights must name the campaign or permission that covers this footage.")
    if not Path(item["file"]).is_file():
        raise FlowError(f"Missing clip file: {item['file']}")
    platforms = args.platforms.split(",") if args.platforms else config["default_platforms"]
    unknown = set(platforms) - set(PLATFORMS)
    if unknown:
        raise FlowError(f"Unknown platform: {', '.join(sorted(unknown))}.")
    day = args.date.isoformat()
    for platform in platforms:
        used = sum(1 for other in items if other["id"] != item["id"] and other["date"] == day
                   and other["status"] in {"approved", "posted"} and platform in other["platforms"])
        if used >= config["max_posts_per_day"]:
            raise FlowError(f"{platform} already has {used} post(s) on {day}, the daily limit.")
    item.update(status="approved", date=day, slot=args.slot, title=args.title.strip(),
                description=args.description.strip(), rights=args.rights.strip(),
                campaign=(args.campaign or "").strip(), platforms=platforms)
    save_queue(items)
    print(f"Approved {item['id']} for {day} {args.slot} on {', '.join(platforms)}.")


def cmd_reject(args):
    items = load_queue()
    item = find_item(items, args.id)
    if item["status"] == "posted" or item["posts"]:
        raise FlowError(f"{item['id']} has already been posted.")
    item["status"] = "rejected"
    save_queue(items)
    print(f"Rejected {item['id']}.")


def encode_two_pass(source, target, video_k, audio_k):
    with TemporaryDirectory(prefix="clipflow-") as temp:
        base = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(source), "-c:v", "libx264",
                "-preset", "slow", "-b:v", f"{video_k}k", "-pix_fmt", "yuv420p"]
        subprocess.run([*base, "-pass", "1", "-passlogfile", "pass", "-an", "-f", "null", "-"],
                       cwd=temp, check=True)
        subprocess.run([*base, "-pass", "2", "-passlogfile", "pass", "-c:a", "aac", "-b:a", f"{audio_k}k",
                        "-movflags", "+faststart", str(target)], cwd=temp, check=True)


def prepare_upload(item, config):
    source = Path(item["file"])
    folder = HOME / "upload"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{item['id']}_upload.mp4"
    limit = int(config["upload_limit_mb"] * 1024 * 1024)
    if target.exists() and target.stat().st_size <= limit and target.stat().st_mtime >= source.stat().st_mtime:
        return target
    if source.stat().st_size <= limit:
        shutil.copy2(source, target)
        return target
    audio_k = 128
    seconds = media_seconds(source)
    for margin in (0.97, 0.90):
        video_k = int(config["upload_limit_mb"] * 8192 * margin / seconds) - audio_k
        if video_k < 300:
            raise FlowError(f"{item['id']} is too long to fit the upload limit with usable quality.")
        encode_two_pass(source, target, video_k, audio_k)
        if target.stat().st_size <= limit:
            return target
    target.unlink(missing_ok=True)
    raise FlowError(f"Could not fit {item['id']} under {config['upload_limit_mb']} MB.")


def cmd_due(args):
    config = load_config()
    items = load_queue()
    day = (args.date or date.today()).isoformat()
    due = []
    for item in items:
        if item["status"] != "approved" or item["date"] != day or (args.slot and item["slot"] != args.slot):
            continue
        waiting = [p for p in item["platforms"] if p not in item["posts"]]
        if not waiting:
            continue
        missing = [p for p in waiting if not config["accounts"].get(p)]
        if missing:
            raise FlowError(f"Set the expected account for {', '.join(missing)} in config.json first.")
        upload = prepare_upload(item, config)
        due.append({
            "id": item["id"], "upload_file": str(upload), "size_mb": round(upload.stat().st_size / 1048576, 2),
            "title": item["title"], "description": item["description"], "campaign": item["campaign"],
            "rights": item["rights"], "slot": item["slot"],
            "platforms": {p: {"expected_account": config["accounts"][p]} for p in waiting},
        })
    print(json.dumps(due, indent=2, ensure_ascii=False))


def valid_post_url(platform, url):
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.").removeprefix("m.")
    if parsed.scheme != "https":
        return False
    if platform == "youtube":
        return (host == "youtube.com" and bool(re.fullmatch(r"/shorts/[\w-]{6,}/?", parsed.path))) or (
            host == "youtu.be" and bool(re.fullmatch(r"/[\w-]{6,}/?", parsed.path)))
    if platform == "instagram":
        return host == "instagram.com" and bool(
            re.fullmatch(r"(/[\w.]+)?/(reel|reels|p)/[\w-]{5,}/?", parsed.path))
    if platform == "facebook":
        return host == "facebook.com" and bool(re.fullmatch(r"/reel/\d+/?", parsed.path))
    return host == "tiktok.com" and bool(re.fullmatch(r"/@[\w.-]+/video/\d+/?", parsed.path))


def cmd_posted(args):
    config = load_config()
    items = load_queue()
    item = find_item(items, args.id)
    if item["status"] != "approved" or args.platform not in item["platforms"]:
        raise FlowError(f"{item['id']} is not approved for {args.platform}.")
    if args.platform in item["posts"]:
        raise FlowError(f"{item['id']} is already recorded as posted on {args.platform}.")
    if not valid_post_url(args.platform, args.url):
        raise FlowError(f"That does not look like a {args.platform} post link.")
    now = datetime.now(timezone.utc)
    deadline = ""
    if item["campaign"]:
        deadline = (now + timedelta(minutes=config["campaign_submit_minutes"])).isoformat(timespec="seconds")
    item["posts"][args.platform] = {"url": args.url, "posted_at": now.isoformat(timespec="seconds"),
                                    "submit_by": deadline, "submitted_at": ""}
    if all(p in item["posts"] for p in item["platforms"]):
        item["status"] = "posted"
    save_queue(items)
    new_log = not LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new_log:
            writer.writerow(["posted_at", "id", "platform", "title", "campaign", "url"])
        writer.writerow([now.isoformat(timespec="seconds"), item["id"], args.platform, item["title"],
                         item["campaign"], args.url])
    print(f"Recorded {item['id']} on {args.platform}." + (f" Submit to campaign by {deadline}." if deadline else ""))


def cmd_submitted(args):
    items = load_queue()
    item = find_item(items, args.id)
    if not item["campaign"]:
        raise FlowError(f"{item['id']} has no campaign.")
    platforms = [args.platform] if args.platform else list(item["posts"])
    if not platforms or any(p not in item["posts"] for p in platforms):
        raise FlowError(f"{item['id']} has no matching post to mark as submitted.")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for platform in platforms:
        item["posts"][platform]["submitted_at"] = now
    save_queue(items)
    print(f"Marked {item['id']} as submitted to {item['campaign']}.")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("ingest").set_defaults(run=cmd_ingest)
    p = sub.add_parser("list")
    p.add_argument("--status", choices=("needs_review", "approved", "posted", "rejected"))
    p.set_defaults(run=cmd_list)
    p = sub.add_parser("approve")
    p.add_argument("id")
    p.add_argument("--date", type=parse_day, required=True)
    p.add_argument("--slot", choices=SLOTS, required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", required=True)
    p.add_argument("--rights", required=True, help="Campaign or permission covering this footage")
    p.add_argument("--campaign", help="Exact campaign name, if it should be submitted")
    p.add_argument("--platforms", help="Comma-separated: youtube,tiktok,instagram,facebook")
    p.set_defaults(run=cmd_approve)
    p = sub.add_parser("reject")
    p.add_argument("id")
    p.set_defaults(run=cmd_reject)
    p = sub.add_parser("due")
    p.add_argument("--date", type=parse_day)
    p.add_argument("--slot", choices=SLOTS)
    p.set_defaults(run=cmd_due)
    p = sub.add_parser("posted")
    p.add_argument("id")
    p.add_argument("--platform", choices=PLATFORMS, required=True)
    p.add_argument("--url", required=True)
    p.set_defaults(run=cmd_posted)
    p = sub.add_parser("submitted")
    p.add_argument("id")
    p.add_argument("--platform", choices=PLATFORMS)
    p.set_defaults(run=cmd_submitted)
    return parser


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()
    try:
        args.run(args)
    except FlowError as error:
        print(f"Stopped: {error}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(f"Stopped: {error.cmd[0]} failed with exit code {error.returncode}.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
