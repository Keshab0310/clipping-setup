# Post a Facebook Reel (Windows, Claude in Chrome)

Use only an item returned by `python clipflow.py due`.

1. Confirm the Chrome extension is connected. If it is not, stop and report it.
2. Open https://www.facebook.com/reels/create and confirm the profile or Page posting the reel matches `expected_account`. If it does not, stop.
3. Do not click "Add video". Find the hidden file input and send `upload_file` with `file_upload`.
4. Click Next until the description screen appears, then type `description`.
5. Confirm the audience is Public.
6. **Stop before Publish.** Show the user the clip ID, profile or Page, caption, and file, then wait for a clear yes in chat.
7. After that yes, click Publish and wait for the confirmation.
8. Copy the link containing `/reel/` from the published reel.
9. Record it: `python clipflow.py posted ID --platform facebook --url LINK`
10. If the item has a campaign, go straight to `SUBMIT_CAMPAIGN.md`.

Never like, follow, comment, or post anything outside the queue.
