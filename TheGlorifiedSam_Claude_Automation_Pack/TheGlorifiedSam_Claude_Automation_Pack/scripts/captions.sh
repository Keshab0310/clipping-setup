#!/bin/bash
# Word-timed captions with whisper.cpp. The -dtw flag makes each word line up with when it's said;
# without it, captions show up seconds early.
# One-time model download (about 550 MB):
#   curl -L -o ggml-large-v3-turbo-q5_0.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
# Usage: bash captions.sh video.mp4 path/to/ggml-large-v3-turbo-q5_0.bin
set -e
IN="$1"; MODEL="$2"; BASE="${IN%.*}"
[ -f "$IN" ] && [ -f "$MODEL" ] || { echo "Usage: bash captions.sh video.mp4 model.bin"; exit 1; }
ffmpeg -v error -y -i "$IN" -ar 16000 -ac 1 "$BASE.wav"
nice -n 19 whisper-cli -t 4 -m "$MODEL" -f "$BASE.wav" -l en -nfa -dtw large.v3.turbo -ojf -osrt -of "$BASE"
rm -f "$BASE.wav"
echo "Made $BASE.srt (captions) and $BASE.json (per-word timing)"
