# Writing realistic video prompts (Veo and Omni in Google Flow)

This is the method for every generation prompt, for any scene, not only auctions. The goal: a stranger watching the clip believes a real phone filmed real people. Only the one deliberate twist (being pulled into a phone, a man flying instead of a drone) may break reality, and everything around it must be strictly real.

## 1. Design the scene like a real shoot, before writing the prompt

1. **Reality check.** Ask: "Could a real phone camera capture this in one take, with real people?" Every person, object and sound needs a reason to be there.
2. **Learn how the real situation works.** Write down three to five facts the scene must respect. For an auction:
   - the auctioneer calls the bids
   - one or two paddles go up at a time
   - prices rise in sensible steps
   - the calls run "Going once… Going twice… Sold!"
   - the gavel strikes once, on "Sold!"

   Do the same for a café, a car showroom, a family dinner, a souk or a phone screen.
3. **Write a story bible for the video:**
   - the characters: look, wardrobe, what each one holds, and whether they speak
   - the location and the key items
   - every number (prices, times, counts)
   - the full script: every line, who says it, when
4. **Make a shot list.** One clip is one shot: one main action plus one reaction. 8 seconds holds two or three beats, no more.
5. **Write each shot's start state and end state:**
   - where each person stands
   - what each one holds
   - where they look

   The end state of shot N is the start state of shot N+1.

## 2. The prompt template (fill every block, in this order)

```
REFERENCES: Using the character reference for Karim. / Starting from this exact frame.
FORMAT: Vertical 9:16, 8 seconds, one continuous handheld shot filmed on a phone by someone in the room, photorealistic, everything moving at real speed.
SETTING: the place, time of day, and the light sources that motivate the lighting (phone glow, LED strips, spotlights, window).
PEOPLE: each person with role, position in frame, look, and "speaks" or "silent, mouth closed throughout".
PROPS: each prop, who holds it or where it rests, "for the whole clip".
TIMELINE:
[00:00–00:02] one action per person, plus the camera move
[00:02–00:04] ...
[00:04–00:06] ...
[00:06–00:08] ... ends with the agreed end state
DIALOGUE: The auctioneer says, fast and clear: "..." (at 00:02). Every other person stays silent.
SOUND: Ambient: ... SFX: each one tied to a visible action at its timestamp.
PALETTE: the brand palette block from PLAYBOOK.md.
REALISM: real skin texture, natural imperfect movement, each background person acts on their own at different moments, varied clothing within the palette, real-world physics, every object stays where it is unless someone moves it.
CLEAN FRAME: screens and signs glow plain violet and blank; objects plain and unbranded; a clean picture without captions or subtitles.
```

## 3. Rules that keep it real

**Logic and continuity**
- **One continuous shot per clip.** Ask for a cut only when the story needs one. Otherwise the model invents cuts, and continuity breaks at each one.
- **Every prop has an owner for the whole clip.** Fixed props are safer than handheld ones: a microphone on a stand, a phone that stays in his left hand.
- **One action at a time per person, with its timestamp.** Each reaction comes after its cause, with a short beat in between.
- **Background people act as individuals.** Write "a man in the third row raises his paddle, a moment later a woman on the left raises hers", never "the crowd raises their paddles". Same for clapping, turning, laughing.
- **Prices, times and procedures must be realistic** for the item, for Lebanon and for the situation.

**Speech**
- **Every spoken line goes in quotes, with the speaker and a timestamp.** Name everyone else as silent with their mouth closed.
- **Short lines:** about 2 to 3 words per second at most, each line under 10 words. Spell numbers the way they're said ("twelve thousand").
- **The spoken numbers are the overlay numbers.** I decide them first, put them in the script, then use the same ones in the edit.
- **Arabic speech.** Write each line in Arabic script and in Arabizi, and specify "Lebanese Arabic, casual Beirut dialect". Keep it to a few short, everyday words (واحد… تنين… تلاتة!, مبروك). AI voices drift to Egyptian or formal Arabic on long lines, and Lebanese viewers notice instantly. If the accent comes out wrong, mute the voice in the edit and let the overlays and sound effects carry the scene.

**Text, logos and numbers in the picture**
- **Models garble text.** Keep every screen, sign, paper and paddle blank in the footage. Every readable word, price and logo comes from my overlays.
- **Describe what's there, not what isn't.** "Blank screens glowing plain violet" works better than "no text" (Veo responds better to positive descriptions than to negations).

**Acting**
- **Ask for small, specific reactions:** a slow double-take, a nervous swallow, a half-smile he tries to hide. Words like "very excited" or "shocked" alone lead to over-acting.
- **Nobody looks at the camera** unless that's the beat.

**Camera and look**
- **Aim for phone or documentary realism:** handheld, natural exposure, slight grain. Avoid "cinematic", "epic", "8K", "hyper-realistic"; they push the glossy AI look.
- **Light comes from a source you can name.** Everything plays at real speed; use slow motion only when the idea needs it.

**Consistency**
- **Use saved characters** (Karim) and the same wording for them every time.
- **Use a first-frame image** when the location must match an earlier shot exactly. Use reference images for a new location.
- **Describe hero items identically every time,** for example "a glossy white vintage scooter, no logos".

## 4. Never ask one shot to choreograph several people

Video models handle one person doing one clear action well. They fail when several people must take turns with small props in one shot: hands overlap, the order breaks, objects get used wrongly. Real ads aren't filmed that way either. So:
- **Build interplay from short single-action shots,** usually 4 to 6 s, and let the edit create the sequence and the cause and effect:
  - a close-up of two hands reaching
  - an extreme close-up of one face reacting
  - a close-up of a hand placing a bill
  - a medium shot of one person raising a finger
  - a close-up of a knock
- **Reaction close-ups can be stills.** I animate them with push-ins and sound, which is cheap and never breaks.
- **Let overlays carry the rest.** When the interaction is a bidding duel, pop-ups (bids, chats, notifications) can carry it while the footage stays on one person's reactions. That's why "Pulled In" worked.

## 5. Lock the first frame when blocking matters

When a scene has several people in set positions, or the lighting is specific, don't ask a video model to invent the frame. Do it in two steps:
1. **Make a still image of the opening frame** and iterate on it cheaply until the cast, positions, lighting and palette are right.
2. **Animate it with Veo,** using the still as the first frame. The video prompt then only describes motion, dialogue and sound.

Choose a camera position that shows every face and the key hands at once, for example over the shoulder of the person behind a counter. A character who speaks is best seen from behind or off-camera: their voice is heard, but there's no lip-sync to break.

## 6. Model choice and cost

- **A shot continuing an existing frame:** first frame plus Veo. Fast is enough to test the logic.
- **A known character in a new place:** Omni Flash with the character reference. It keeps identity better, and small mistakes can be fixed with an edit to the same clip instead of a new generation.
- **Always 1 output.**
- **Transcribe the speech yourself.** Use `tools/asr/transcribe.py`. Setup: `pip install sherpa-onnx --break-system-packages`, then download and unpack https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 into /home/claude/asr. It prints each phrase with start and end times, in English only. For Arabic, or if it fails, ask the owner for Flow's transcript.

## Pacing (owner's friends' feedback on "The Last Manouche", 13 Oct 2026)

The first cut, at 12 to 16 seconds, was too fast: viewers couldn't read the text or follow the story.
- **Every on-screen line stays up long enough to read twice:** at least 0.4 s per word, and never under 1.5 s for a name tag or caption.
- **Each story beat gets at least 0.8 to 1.2 s;** reaction close-ups get about 0.8 s.
- **A story Reel with text usually lands at 20 to 30 seconds.** Fast cutting is fine for energy, but never faster than the text it carries.

## 7. Review before editing (every clip, every cut)

- **Check the transcript against the script.** Words, numbers, call order and speaker should all match. Overlays follow the transcript; drop any overlay the audio doesn't support.
- **Check the frames at every cut and about every 0.5 s.** Look for:
  - props that vanish or change
  - hands that appear or disappear
  - a silent character who seems to talk
  - a crowd moving in unison
  - garbled text
  - lighting outside the palette
- **Fix what the edit can fix.** Blur text, trim, cover with an overlay.
- **Flag what it can't.** If the story depends on it, ask for an Omni edit or a regeneration, and tell the owner exactly what's wrong.

## 8. Mistakes already seen (do not repeat)

From "Pulled In", episode 1 (12 Oct 2026):
- **The prices didn't match.** The auctioneer said "ten thousand, twelve thousand" while the overlays showed $1,100 to $1,350.
- **The call order was wrong.** The gavel struck on "Going once", "Going twice" was skipped, then he said "Sold!".
- **The auctioneer's handheld microphone vanished** mid-clip.
- **Karim's phone was gone** when he landed back on the couch.
- **The whole crowd raised and lowered their paddles together.**
- **Karim seemed to speak the auctioneer's lines** in the first version.
- **Garbled words appeared on the screens** in the hall.

From "The Last One", episode 1, take 1 (Omni Flash, text only, 4 people, 10 s):
- **The blocking was wrong.** The two customers stood side by side with no stare-down.
- **A character turned into another one.** The uncle morphed into the baker halfway through.
- **The room came out bright white, off the palette.**
- **The rolling pin was used to roll the manouche** instead of knocking.

The cause: too many people and beats for a text-only prompt. The fix is a locked first frame plus Veo.

Take 2 (Veo Quality, locked first frame): the look and cast held, but the four-person sequence still broke. The baker fiddled with the manouche and swung the rolling pin overhead, a glass guard blocked the customers from the tray, and the beats overlapped. The lesson is section 4: split the scene into single-action shots.

## 9. Worked example: the auction shot, written with this method

Price ladder: someone else is at $10,000 when Karim arrives. Karim bids $12,000 and wins at $12,000. Overlays: earlier bids $8,000 and $9,000, then "rami_k $10,000" at 00:00.5, "Karim $12,000" at 00:03.6, "Going once…" at 00:04.8, "Going twice…" at 00:05.8, "SOLD." at 00:07.2.

```
Using the character reference for Karim.
Vertical 9:16, 8 seconds, one continuous handheld shot filmed on a phone from the side aisle of an auction hall: Karim in the foreground on the right, the stage with the auctioneer in the background on the left. Photorealistic, real-speed motion.

Setting: a modern auction hall at night, about forty people seated in rows facing a low stage. Near-black walls, glossy black floor, thin blue-violet LED strips along the stage edge, two large screens behind the stage glowing plain violet and blank. On the stage, a glossy white vintage scooter without logos on a low round pedestal, and a black podium with a microphone fixed on a short stand.

People:
- Karim, black hoodie, holding his phone in his left hand for the whole clip, standing in the aisle. Silent, mouth closed throughout.
- The auctioneer, a man in his fifties in a dark suit, behind the podium speaking into the fixed microphone, holding a wooden gavel in his right hand for the whole clip.
- A woman in a grey blazer standing next to Karim, holding a spare white bid paddle with a violet edge.
- The seated crowd in black, white and grey clothes; each person reacts on their own, at different moments.

[00:00–00:02] Karim looks around the hall with a slow, disbelieving blink. A man in the third row raises his paddle, then lowers it.
[00:02–00:04] The woman next to Karim holds the spare paddle out to him. He takes it with his right hand, hesitates one beat, then raises it high at 00:03.5. The auctioneer points at him.
[00:04–00:07] The auctioneer scans the room slowly, gavel raised. One woman in the front row half-lifts her paddle, then changes her mind.
[00:07–00:08] The auctioneer brings the gavel down once on the podium as he says "Sold!". Two people near Karim turn and clap; Karim lowers the paddle slowly with a half-smile he tries to hide.

Dialogue, auctioneer only, fast and clear through the hall speakers:
[00:00.5] "Ten thousand, thank you, sir. Do I hear twelve?"
[00:03.6] "Twelve thousand, the young man in the aisle!"
[00:04.8] "Going once…"
[00:05.8] "Going twice…"
[00:07.2] "Sold!"
Karim, the woman and the crowd do not speak.

Sound: low murmur of the seated crowd, the auctioneer's amplified voice, one sharp wooden gavel knock on "Sold!", scattered applause after it.
Palette: deep near-black (#0B0E14), electric blue (#2F7BFF) blending into violet (#7C5CFF) as the only light colors, soft light-violet highlights (#A78BFA), clean white; cool, modern, high-contrast.
Realism: real skin texture, natural imperfect movement, every object stays where it is unless someone moves it, a clean picture without captions or subtitles.
```
