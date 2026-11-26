# The Glorified Sam: Claude Automation Pack (free)

This is how I get Claude to download footage, make captions, upload videos and post on a schedule, without babysitting it.

## The "file too heavy" fix (why your Claude refuses to upload)
Claude in Chrome sends files into the browser through its upload tool, and **that tool has a limit of about 10 MB per upload.** Most phone and stream exports are bigger, so Claude says the file is too heavy.

The fix is to shrink the video to under 10 MB before uploading. A 30–60 s vertical short still looks great at that size.
```
bash scripts/make_upload_copy.sh my_video.mp4
```
This makes `my_video_upload.mp4` at about 9.5 MB. Tell Claude to upload that file.

The other common mistake: **Claude must NOT click the "Select files" button.** That opens your Mac's file picker, which Claude can't see. Claude has to send the file straight to the page's hidden file input. The runbooks tell it how.

## What's inside
| File | What it does |
|---|---|
| `scripts/make_upload_copy.sh` | Shrinks any video to under 10 MB for upload (2-pass, keeps the quality) |
| `scripts/grab_clip.sh` | Downloads a clip or VOD section, speed-capped so your stream or Wi-Fi doesn't lag |
| `scripts/captions.sh` | Accurate word-timed captions with whisper (free, runs on your computer) |
| `scripts/top_twitch_clips.sh` | Lists a streamer's most-viewed clips from the last 24 h (the fastest way to find moments) |
| `runbooks/UPLOAD_YOUTUBE_SHORTS.md` | Exact steps Claude follows to post a Short in YouTube Studio |
| `runbooks/UPLOAD_TIKTOK.md` | Exact steps for TikTok Studio on the web |
| `runbooks/SUBMIT_TO_CAMPAIGN.md` | Submitting a clip link to a clipping campaign within the time limit |
| `schedules/POST_AT_PEAK_TIMES.md` | Scheduled-task prompts that post at set times every day |
| `schedules/QUEUE_TEMPLATE.json` | The queue file the scheduled posts read from |
| `01_HOW_TO_SET_IT_UP.md` | Putting it all together |
| `02_SAFETY.md` | How to automate without getting banned |
