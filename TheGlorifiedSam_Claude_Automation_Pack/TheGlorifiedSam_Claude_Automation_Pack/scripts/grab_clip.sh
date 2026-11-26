#!/bin/bash
# Download a video, or part of one, at a capped speed so your live stream or Wi-Fi doesn't lag.
# Only download footage you have the rights to clip (your own, or a campaign's official source).
# Usage: bash grab_clip.sh URL output_name [start-end]   e.g. bash grab_clip.sh URL clip1 01:02:10-01:03:00
set -e
URL="$1"; NAME="${2:-clip}"; SECTION="$3"
[ -n "$URL" ] || { echo "Usage: bash grab_clip.sh URL output_name [start-end]"; exit 1; }
ARGS=(--limit-rate 1.5M -f "bv*[height<=1080]+ba/b[height<=1080]" --merge-output-format mp4 -o "$NAME.mp4")
[ -n "$SECTION" ] && ARGS+=(--download-sections "*$SECTION")
nice -n 19 yt-dlp "${ARGS[@]}" "$URL"
