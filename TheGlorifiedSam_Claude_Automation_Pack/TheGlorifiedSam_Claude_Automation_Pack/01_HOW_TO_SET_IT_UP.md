# Setting it up

1. Install the tools (from the Starter Kit): `brew install ffmpeg yt-dlp whisper-cpp`
2. Install **Claude in Chrome** (the browser extension) and sign in with the **same Claude account** as your app. A different account, like an Apple "Hide My Email" one, won't connect.
3. Sign in to YouTube, TikTok and Content Rewards yourself in that Chrome. Never give Claude passwords.
4. Put this pack's `scripts/`, `runbooks/` and `schedules/` folders in your workspace.
5. Test by hand once: *"Shrink finished/clip1.mp4 with make_upload_copy.sh, then follow runbooks/UPLOAD_YOUTUBE_SHORTS.md. Stop before Publish and show me."*
6. When that works, make the scheduled tasks from `schedules/POST_AT_PEAK_TIMES.md`.

## If something breaks
- **"File too heavy" / upload fails:** shrink it first. It must be under 10 MB.
- **Claude opens a file picker and gets stuck:** tell it to use `file_upload` on the hidden file input instead of clicking the button.
- **"Chrome not connected":** open Chrome, click the Claude extension and reconnect.
- **Your stream lags while Claude works:** downloads are speed-capped in `grab_clip.sh`, and renders use `nice -n 19`. Also close heavy pages (like dashboards with videos) in Claude's tab.
