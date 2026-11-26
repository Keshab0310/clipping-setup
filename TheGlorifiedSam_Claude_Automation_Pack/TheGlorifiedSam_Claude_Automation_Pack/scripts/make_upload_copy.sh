#!/bin/bash
# Shrink a video to under ~9.5 MB (fits Claude in Chrome's ~10 MB upload limit) with 2-pass x264.
# Usage: bash make_upload_copy.sh input.mp4 [target_MB]
set -e
IN="$1"; TARGET_MB="${2:-9.5}"
[ -f "$IN" ] || { echo "Usage: bash make_upload_copy.sh input.mp4 [target_MB]"; exit 1; }
OUT="${IN%.*}_upload.mp4"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
AUDIO_K=128
TOTAL_K=$(echo "$TARGET_MB * 8192 / $DUR" | bc)
VIDEO_K=$(( TOTAL_K - AUDIO_K ))
[ "$VIDEO_K" -lt 300 ] && { echo "Video is too long to fit $TARGET_MB MB nicely. Trim it or raise the target."; exit 1; }
LOG=$(mktemp -t pass)
ffmpeg -v error -y -i "$IN" -c:v libx264 -preset slow -b:v ${VIDEO_K}k -pass 1 -passlogfile "$LOG" -an -f mp4 /dev/null
ffmpeg -v error -y -i "$IN" -c:v libx264 -preset slow -b:v ${VIDEO_K}k -pass 2 -passlogfile "$LOG" \
  -c:a aac -b:a ${AUDIO_K}k -movflags +faststart -pix_fmt yuv420p "$OUT"
rm -f "$LOG"*
ls -lh "$OUT" | awk '{print "Made", $9, "(" $5 ")"}'
