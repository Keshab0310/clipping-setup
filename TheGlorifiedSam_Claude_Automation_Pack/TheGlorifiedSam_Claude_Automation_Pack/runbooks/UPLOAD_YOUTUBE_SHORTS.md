# Runbook: post a YouTube Short (Claude in Chrome)

Paste this to Claude, or point a scheduled task at this file.

1. **Make it uploadable:** if the file is over 10 MB, run `scripts/make_upload_copy.sh` first and use the `_upload.mp4` copy.
2. **Check the channel:** open https://studio.youtube.com and confirm the channel name or ID is the one I expect. If it isn't, STOP and tell me.
3. Click **Upload videos** (or Create > Upload videos).
4. **Don't click "Select files".** Use the `find` tool to locate the hidden **file input** on the page, then send the video to it with `file_upload`.
   - If `file_upload` says the connection was lost, take a screenshot before retrying. The upload usually went through.
5. **Title:** click the title box, press Cmd+A, then type the title.
6. **Description:** click the description box, then type the description and hashtags.
7. Scroll to **"No, it's not made for kids"** and click it.
8. Click **Next** three times to reach Visibility.
9. Choose **Public**, then **Publish**.
10. Get the link: read the first link containing `youtube.com/shorts/` on the page (with JavaScript), or copy it from the share dialog.
11. Add a row to `content_log.csv`: date, title, platform, link.
