---
name: chalk-talk
description: Make an animated explainer video in the hand-drawn "Chalk Talk" style from the Nafay 3D Style Library, with a chalk stick writing on a long green slate, a felt eraser, and synthesized chalk sounds. Use when the user asks for a chalk talk, chalkboard, blackboard, or hand-drawn lesson animation, or invokes /chalk-talk. Storyboards first, then builds a self-contained HTML animation and can render an MP4.
---

# Chalk Talk

Two files in this skill's folder define the work:

- `references/brief.md` is the user's full brief: workflow, style, rules, sound, and rendering. Follow it exactly.
- `references/reference.html` is the complete working animation. It is the ground truth for how the style looks, moves, and sounds.

## Workflow

1. Read `references/brief.md` in full.
2. If the user has not given a topic or script, ask for one and stop. Build nothing yet.
3. Read `references/reference.html` in full.
4. Check the target format. The reference is 16:9 at 1280x720. If the video is for Shorts, TikTok, or Reels, ask whether to recompose for 9:16. Never center-crop the board, because that cuts off the writing.
5. Build the storyboard described in the brief, publish it, and wait for the user's approval.
6. After approval, build the full animation from a copy of the reference, reusing the storyboard's drawing code. Never edit `references/reference.html` itself.
7. Check the result: scrub through it, confirm text sizes and facts, and confirm each frame stays well under 50 ms.
8. If code can run, render the MP4 as the brief describes.

The "MY CONTENT" section of the brief is a placeholder. The user's current request replaces it.
