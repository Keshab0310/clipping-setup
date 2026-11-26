# Post an Instagram Reel (Windows, Claude in Chrome)

Use only an item returned by `python clipflow.py due`.

1. Confirm the Chrome extension is connected. If it is not, stop and report it.
2. Open https://www.instagram.com/ and confirm the visible profile matches `expected_account`. If it does not, stop.
3. Open Create > Post. Do not click "Select from computer". Find the hidden file input and send `upload_file` with `file_upload`.
4. If Instagram says videos are shared as reels, continue. Choose the original or 9:16 crop, then click Next until the caption screen appears.
5. Click the caption box and type `description`.
6. **Stop before Share.** Show the user the clip ID, account, caption, and file, then wait for a clear yes in chat.
7. After that yes, click Share and wait for the confirmation.
8. Copy the link containing `/reel/` from the profile's Reels tab.
9. Record it: `python clipflow.py posted ID --platform instagram --url LINK`
10. If the item has a campaign, go straight to `SUBMIT_CAMPAIGN.md`.

Never like, follow, comment, or post anything outside the queue.
