# Runbook: post on TikTok (web, TikTok Studio)

1. If the file is over 10 MB, run `scripts/make_upload_copy.sh` first.
2. Open https://www.tiktok.com/tiktokstudio/upload. **Check the account:** run this JavaScript on the page:
   `fetch('/passport/web/account/info/').then(r=>r.json()).then(d=>d.data.username)`
   It must return the account you expect. If it doesn't, STOP.
3. Don't click "Select video". Find the hidden **file input** and send the file to it with `file_upload`.
4. **Caption:** click the description box, press Cmd+A, delete, then type the caption. Press Escape to close the hashtag suggestions.
5. Scroll down and wait for **Music copyright check: "No issues found"**. "Content check lite" can still be running; that's OK.
6. Click **Post**. If it asks "Continue to post?", click **Post now**.
7. Get the link from TikTok Studio > Posts (the first link containing `/video/`).

Notes:
- New TikTok posts can sit in "under review" for up to 12 hours.
- 1–2 posts a day on new accounts. If every post gets 0–5 views, stop and check the account's status in the app.
- Official sounds (for music campaigns) can't be added on the web. Use the phone app for those.
