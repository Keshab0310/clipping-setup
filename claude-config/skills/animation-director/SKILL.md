---
name: animation-director
description: Direct and QA professional animated reels, character animation, motion graphics, and video edits made in code. Use whenever the user wants an animated reel, cartoon short, motion design piece, kinetic typography, animated explainer, or asks to improve the animation, editing, timing, or polish of a video. Works alongside faceless-shorts, chalk-talk, and lemo-opuscar as the craft and review layer.
---

# Animation Director

Motion must show intent. Every move answers: who wants what, what caused this, and where should the eye go next?

## 1. Pre-production
Write these before any code:
- **One-line story:** character + want + obstacle + twist. If it has no change, it is a slideshow.
- **Beat sheet with times.** Hook lands by 0.5 s. A new visual idea every 1.5-3 s. One clear payoff. An ending that can loop.
- **Thumbnail storyboard.** Each shot gets a silhouette, focal point, screen direction, and camera move.
- **Style lock.** Max 5 core colors plus 1 accent reserved for the story's key object. One line language. One character model sheet.
- **Safe zones for 1080x1920.** Keep text out of the top 220 px, bottom 340 px, and right 130 px.

## 2. Character animation
Work pose to pose: key storytelling poses, then breakdowns, then ease, then overlap.
- **Anticipation** before every big action, opposite the direction of travel. Length scales with force.
- **Squash and stretch** with preserved volume. Stretch along velocity, squash on contact.
- **Arcs.** Hands, heads, and thrown objects never travel in straight lines.
- **Overlap and follow-through.** Scarves, hair, ears, and tails lag and settle. Simulate them from the body's path.
- **Timing and spacing.** Few frames means heavy or fast. Clustered keys mean ease. Hold key poses long enough to read (6-12 frames).
- **Animate on twos** (12 poses/s at 24 fps) for acting. Use ones for fast actions, impacts, and all camera moves.
- **Eyes lead.** Eyes move first, then head, then body. Blink on head turns and thought changes.
- **Moving holds.** Never freeze a character completely. Breathe, blink, or drift.
- **Secondary action** supports the main action and never competes with it.
- **Model consistency.** One rig or one reference for every shot. An off-model frame is a release blocker.

## 3. Camera and editing
- Motivate each move: follow action, reveal information, or raise tension. Never drift just to hide a still.
- **Cut on action.** Start the motion in shot A and finish it in shot B.
- Keep the eye trace: place the next shot's focal point near the last shot's.
- Keep screen direction unless the turn is the story.
- **Speed ramps** before the important moment. **Hit-stop** of 2-4 frames on the biggest impact.
- Shake decays within about 0.3 s. Use it only on real impacts.
- Parallax needs at least 3 depth layers.

## 4. Light, color, and finish
- Value structure first: the subject must read in grayscale.
- Brightest point and highest contrast sit on the focal point.
- Add contact shadows, rim light from the story's light source, restrained bloom, vignette, and fine grain to prevent banding.
- Save big color shifts for story turns.

## 5. Type
- Animate by letter or word with overshoot and stagger of 2-3 frames.
- One idea at a time, high contrast, never over a face or the key action.

## 6. Sound
Sound is half the animation.
- Design sound from the actions: anticipation, whoosh, impact, tail.
- **Silence is a tool.** Drop the music right before a joke or payoff.
- Land music accents on picture accents.
- Deliver around -14 LUFS integrated with true peak at or below -1.5 dBTP.

## 7. QA gate
Never call it done until all of these are checked:
1. Contact sheet of the whole piece, then full-size frames at each key beat.
2. Silhouette and focal point are clear in each shot.
3. No clipping, floating feet, limbs through bodies, or off-model frames.
4. No unintended freezes (`freezedetect`). Every long hold must be a deliberate acting beat.
5. Text is inside safe zones and readable at phone size.
6. Loudness and true peak are measured.
7. The finished MP4 is probed for resolution, frame rate, duration, and audio.

Report honestly what was verified by frames and measurement, and what still needs human eyes and ears.

## 8. Failure patterns found in real renders
- **Stiff cloth:** a long simulated chain reads as a pole. Use a short tapered ribbon with a traveling wave.
- **Arms over the face:** draw raised arms behind the body and bend elbows outward.
- **Glow rings:** linear falloff shows a visible edge. Use 4-5 eased gradient stops, and threshold bloom high.
- **Tangents:** never let the title, moon, or other large shapes just touch. Overlap them or separate them clearly.
- **Effects over acting:** particles go behind the character so the face stays readable on the key beat.
- **Over-squash:** below about 0.6 scale, a face stops reading. Keep extreme squash to 1-2 frames.
- **Slow hooks:** the subject or its goal must be on screen in frame 1.

## 9. Delivery encode
Canvas JPEG frames arrive full-range. Convert them or colors can shift on phones:
`-vf "scale=in_range=full:out_range=tv:flags=lanczos,format=yuv420p" -c:v libx264 -preset slow -crf 20 -maxrate 14M -bufsize 28M -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart`

Grain makes files large, so cap the bitrate. Measure loudness on the final MP4, not the intermediate mix.
