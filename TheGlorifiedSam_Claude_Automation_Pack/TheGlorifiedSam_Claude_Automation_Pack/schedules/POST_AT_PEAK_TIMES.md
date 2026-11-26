# Post at peak times automatically

In the Claude app: Code tab > Scheduled > New task (or tell Claude "create a scheduled task…"). Make one task per time slot. US Shorts peaks are around **12 PM, 5 PM and 8 PM Eastern**.

Each run starts fresh with no memory, so the prompt has to explain everything. Copy this and fill in the blanks:

---
You post my approved clips. Read `schedules/QUEUE.json` in my workspace. Post every item where `date` is today, `slot` is "[noon|5pm|8pm]" and `status` is "queued".
For each item:
- Follow `runbooks/UPLOAD_YOUTUBE_SHORTS.md`. The channel must be [MY CHANNEL NAME/ID]; otherwise stop.
- If it has a `campaign`, submit the link right away with `runbooks/SUBMIT_TO_CAMPAIGN.md`.
- Set its status to "posted" and save the link.
Never post anything that isn't in the queue. Never like, follow or comment. If Chrome isn't connected, stop and tell me.
At the end, report what was posted, with links.
---

## Tips
- The Claude app must be open and Chrome connected at post time. If the app is closed, the task runs when you reopen it.
- Start in a mode that asks before acting. Switch to Auto only once you trust it.
- A separate morning task can build the clips and fill the queue. Have it show you the clips first until you trust it.
