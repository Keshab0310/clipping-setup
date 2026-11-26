# Post a YouTube Short (Windows, Claude in Chrome)

Use only an item returned by `python clipflow.py due`.

1. Confirm the Chrome extension is connected. If it is not, stop and report it.
2. Open https://studio.youtube.com and confirm the channel matches `expected_account`. If it does not, stop.
3. Open Create > Upload videos. Do not click "Select files". Find the hidden file input and send `upload_file` with `file_upload`.
4. If the upload tool reports a lost connection, take a screenshot before retrying so the clip is not uploaded twice.
5. Click the title box, press Ctrl+A, and type `title`. Click the description box and type `description`.
6. Select "No, it's not made for kids". Click Next three times to reach Visibility and choose Public.
7. **Stop before Publish.** Show the user the clip ID, channel, title, description, and file, then wait for a clear yes in chat.
8. After that yes, click Publish and copy the `youtube.com/shorts/` link.
9. Record it: `python clipflow.py posted ID --platform youtube --url LINK`
10. If the item has a campaign, go straight to `SUBMIT_CAMPAIGN.md`.

Never like, follow, comment, or post anything outside the queue.
