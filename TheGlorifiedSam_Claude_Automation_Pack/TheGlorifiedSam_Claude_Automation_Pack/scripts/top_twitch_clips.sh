#!/bin/bash
# The fastest way to find good moments: a streamer's most-viewed community clips.
# Usage: bash top_twitch_clips.sh channel_name [24hr|7d|30d]
CH="$1"; RANGE="${2:-24hr}"
[ -n "$CH" ] || { echo "Usage: bash top_twitch_clips.sh channel_name [24hr|7d|30d]"; exit 1; }
yt-dlp --flat-playlist --playlist-end 20 --print "%(view_count)s views | %(duration)ss | %(title)s | %(url)s" \
  "https://www.twitch.tv/$CH/clips?filter=clips&range=$RANGE"
