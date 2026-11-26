# Post on TikTok (Windows, Claude in Chrome)

Use only an item returned by `python clipflow.py due`.

1. Confirm the Chrome extension is connected. If it is not, stop and report it.
2. Open https://www.tiktok.com/tiktokstudio/upload and confirm the visible profile matches `expected_account`. If it does not, stop.
3. Do not click "Select video". Find the hidden file input and send `upload_file` with `file_upload`.
4. Click the description box, press Ctrl+A, press Delete, and type `description`. Press Escape to close hashtag suggestions.
5. Wait for the music copyright check to report no issues. If it reports a problem, stop.
6. **Stop before Post.** Show the user the clip ID, account, caption, and file, then wait for a clear yes in chat.
7. After that yes, click Post. If TikTok asks "Continue to post?", click Post now.
8. Copy the link containing `/video/` from TikTok Studio > Posts.
9. Record it: `python clipflow.py posted ID --platform tiktok --url LINK`
10. If the item has a campaign, go straight to `SUBMIT_CAMPAIGN.md`.

New posts can stay under review for up to 12 hours. Never like, follow, comment, or post anything outside the queue.
