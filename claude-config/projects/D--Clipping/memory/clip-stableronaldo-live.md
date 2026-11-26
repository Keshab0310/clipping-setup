---
name: clip-stableronaldo-live
description: "Clipping source is now stableronaldo (Twitch/YouTube live) instead of Lacy, with no full-stream downloads"
metadata:
  node_type: memory
  type: project
  originSessionId: 5127fe74-c6d5-4367-9b90-2fa4060335d1
  modified: 2026-11-22T04:07:59.678Z
---

As of 2026-11-21 the clipping target is stableronaldo (https://www.twitch.tv/stableronaldo, or their YouTube live), replacing Lacy.

**Why:** The user asked to switch channels and to stop downloading whole videos. Claude should watch the live stream and clip only moments worth posting.

**How to apply:** The user wants every minute of the live reviewed. Run `twitch_auto_clipper.py` with `--watch --every-minute --polish --minutes 30 --buffer-minutes 6` so blocks overlap, only a short rolling buffer stays on disk, and rejected footage is deleted. Keep finished clips in `D:\Clipping\stableronaldo_batch\finished` and follow [[store-clips-local-and-drive]]. Do not post without asking.
