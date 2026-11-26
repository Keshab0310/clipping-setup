"""Re-transcribe one chosen clip with a stronger model so its burned-in captions are accurate.

The live pipeline keeps the fast `small` model for scanning every minute. This runs only on winners, on the CPU so it
never competes with live transcription for the laptop GPU.
"""
import json
import re
import subprocess
from pathlib import Path

import numpy as np

from common import tool

MODEL = "distil-large-v3"
PROMPT = "Twitch streamer playing GTA 6, talking to chat. Bro, y'all, aim, hit-reg, heals, respawn, clutch, nerf, buff."
HOTWORDS = "GTA, hit-reg, heals, y'all, chat, respawn, clutch"


def tidy(words):
    """Fix gaming homophones and rejoin words Whisper splits at an apostrophe or hyphen (y 'all, dead -ass)."""
    out = []
    for word in words:
        word = dict(word, w=re.sub(r"\bheels\b", lambda m: "Heals" if m[0][0] == "H" else "heals", word["w"], flags=re.I))
        if out and (word["w"][:1] in "'-" or (re.match(r",\d", word["w"]) and out[-1]["w"][-1:].isdigit())):
            out[-1] = dict(out[-1], w=out[-1]["w"] + word["w"], e=word["e"])
        else:
            out.append(word)
    return out


def refine_words(video, start, end, job):
    """Words for [start, end) as [{w, s, e}] in the source video's seconds. Cached per window in the job folder."""
    cache = Path(job) / f"transcript.refined_{start:.2f}_{end:.2f}.json"
    if cache.exists():
        return tidy(json.loads(cache.read_text(encoding="utf-8")))
    pcm = subprocess.run(
        [tool("ffmpeg"), "-v", "error", "-ss", f"{start:.2f}", "-to", f"{end:.2f}", "-i", str(video),
         "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        check=True, capture_output=True,
    ).stdout
    samples = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    from faster_whisper import WhisperModel
    model = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=4)
    segments, _ = model.transcribe(samples, language="en", word_timestamps=True, vad_filter=True,
                                   initial_prompt=PROMPT, hotwords=HOTWORDS, condition_on_previous_text=False)
    words = [{"w": w.word.strip(), "s": round(start + w.start, 2), "e": round(start + w.end, 2)}
             for segment in segments for w in (segment.words or []) if w.word.strip()]
    cache.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    return tidy(words)
