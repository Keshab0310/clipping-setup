# Clipflow

Turns finished clipper drafts into an approved, upload-ready posting queue.

## Daily flow

1. Capture and edit:
   `python D:\Clipping\twitch_auto_clipper.py https://www.twitch.tv/CHANNEL --repo D:\Clipping\gtavi-claudecode --keep 3 --min-score 7`
2. Add the drafts to the queue: `python clipflow.py ingest`
3. See what needs review: `python clipflow.py list --status needs_review`
4. Watch each clip in `clips\`, then approve or reject it:
   `python clipflow.py approve c001 --date 2026-11-22 --slot 5pm --title "Title" --description "Caption #shorts" --rights "Campaign name" --campaign "Campaign name"`
5. At post time: `python clipflow.py due --slot 5pm`
6. Ask Claude to follow the matching guide in `runbooks\`. It stops for your yes before anything goes public.

## Setup

- Put your expected channel and account names in `config.json`. Posting prep refuses to run without them.
- Sign in to YouTube, TikTok, Instagram, Facebook, and your campaign site yourself in Google Chrome, then connect the Claude extension there.

## Limits

- Peak slots are noon, 5 PM, and 8 PM Eastern.
- The default limit is 2 posts per platform per day.
- `clips\` keeps full-quality masters. `upload\` holds copies under 9.5 MB for browser upload.
- Every approval must name the campaign or permission that covers the footage.
