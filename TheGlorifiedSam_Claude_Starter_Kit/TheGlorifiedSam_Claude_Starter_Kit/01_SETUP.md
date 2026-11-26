# Setup (about 30 min)

## 1. Get Claude Code
- Download the Claude desktop app from https://claude.com/download and open the **Code** tab. Or install the CLI from https://claude.com/claude-code
- Claude Code works on a paid Claude plan (Pro or Max). Check the current plans on claude.com before you buy.

## 2. Make a workspace folder
Make one folder for all your content work, for example `~/Creator`, and open it in Claude Code. Claude can only see what's in the folders you give it.

## 3. Install the free tools (Mac, with Homebrew)
If you don't have Homebrew, install it from https://brew.sh. Then paste this into Terminal:
```
brew install ffmpeg yt-dlp whisper-cpp node python
```
- **ffmpeg**: cuts, crops, encodes and mixes audio. Claude drives it for you.
- **yt-dlp**: downloads videos you have the rights to use (campaign footage, your own streams).
- **whisper-cpp**: local captions and transcripts, free and private.
- **node / python**: lets skills render graphics and run scripts.

On Windows, ask Claude: "Install ffmpeg, yt-dlp and whisper for me on Windows", and it will walk you through it.

## 4. Drop in your brain file
Copy `templates/CLAUDE.md` into your workspace folder and fill in the blanks. This is the single biggest upgrade.

## 5. Install skills
See `02_FREE_SKILLS.md`.

## 6. First test
Ask Claude: *"Read my CLAUDE.md, then tell me 5 things you can automate for my channel this week."*
