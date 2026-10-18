# Auction lessons: the awareness campaign (owner's brief, 16 Oct 2026)

This file is the complete instructions for the daily lesson run and the posting check. Read it in full before doing anything. `PLAYBOOK.md` "The owner's standing instructions" and "Never" still apply, except where this file is stricter.

## What the owner asked for

- **One educational video every day.** You research, you write the story, it must be catchy and easy to follow.
- The goals: **teach** how auctions work, build **awareness** of auctions (in Lebanon: courts, the state, fish halls, plates; worldwide; stock markets), and show **why auctions are convenient**, so people want to use one.
- **"Did you know" facts**, Lebanon and worldwide, including the link between bidding and stocks.
- **No Higgsfield and no AI video tool.** Every frame is drawn in code with the kit in `tools/lessons/`.
- **The account is new on Instagram.** These lessons are how it earns its first followers, so post every day, regularly, until viewers get used to it: **7:00 pm Beirut Monday to Friday, 11:00 am Beirut on Saturday and Sunday** (owner, 17 Oct 2026). See "Post times" below.
- The owner runs the before/after measurement himself (story surveys). Don't put surveys on the board.

## Post times (owner, 17 Oct 2026)

- **Monday–Friday: 19:00 Beirut. Saturday and Sunday: 11:00 Beirut.** A lesson's "slot" is the post time of its day. Everywhere this file says "the 7 pm slot", read "the day's slot".
- Approval cutoff is 15 minutes before the slot: **6:45 pm** on weekdays, **10:45 am** on weekends.
- Write slots with Beirut's offset for that date: `+03:00` until Sat 24 Oct 2026, `+02:00` from Sun 25 Oct 2026 (clocks go back), e.g. `2026-10-18T11:00:00+03:00`, `2026-10-25T11:00:00+02:00`, `2026-10-26T19:00:00+02:00`.

## Rules for this campaign (owner, 16 Oct 2026; these override anything else)

1. **Never mention HyperBidz.** No name, no logo or Z mark, no wordmark, no "coming soon", no handle on screen, no app screens or app UI. Captions don't mention it either. The videos only talk about auctions: how they work and why they're convenient.
2. **No tags on screen.** No "Lesson NN" label, no chapter chips, no progress bar.
3. **A narrator speaks the whole video** in a calm, clear, teacher-like voice (`narration.py`: Kokoro voice `am_michael`, speed 1.0; don't change it without the owner). Every on-screen idea is spoken. Since lesson 03 (v3 style) the words appear on screen word by word as they're spoken (`motion.KCaps`), instead of a subtitle pill. Speed 1.07 for v3 lessons. Say Nour as `{Nour|Nuur}` (the voice mispronounces "Nour").
4. **Easy to follow.** One idea on screen at a time. Few words on screen besides the captions: at most one short headline, one number or one card at a time. Nothing else moving while the key point lands. If a frame has more than three things competing for attention, simplify it.
5. **Music stays quietly in the background** (`music.mix`, bed about −21 dB under the voice, ducked further while the narrator speaks) and is **different every video**: use the style and seed given in `QUEUE.md` (styles rotate keys → marimba → ambient → pluck → lofi; seed = lesson number).
6. **App colours** (`cast.py`): near-black stage #0B0E14, electric blue #2F7BFF, violet #7C5CFF, lilac #A78BFA, green #00A364, white. No warm/orange palettes.
7. **The same characters every time** (`cast.py`): **Sami** the seller (blue, small moustache), **Nour** the buyer (lilac, hair bun), and **the bidders** (violet, green, silver, with numbered paddles). Reuse them; don't invent new characters. Real people in stories are never drawn as faces (show objects, screens, places instead).
8. **Professional, not niche.** No family-nostalgia props or words (no "jeddo's…", "teta's…"), no inside jokes. Plain, confident, explanatory.
9. **Facts only.** Every number, date, name and quote must come from a source you opened (the research file's links, re-checked). Write numbers for the voice in words with `{shown|spoken}` markup, e.g. `{$14.83|fourteen dollars and eighty-three cents}`. Cartoon prices (Sami's radio) are illustrations and must look like it.
10. **Neutral on Lebanon.** Explain how things work; never blame or name a bank, judge, official, party or person; no crisis jokes; no politics. No legal or financial advice ("this is how it works", never "you should buy").
11. No slogan "Ma fi ekher se3er…", no "last price?/akher se3er".
12. No AI content tag on Instagram (`isAiGenerated: false`) and no on-screen AI label.

## Format

- 1080x1920, 30 fps, H.264, under 19 MB (re-encode at a higher CRF if larger; the board's upload cap is 20 MB).
- **What these are (owner, 16 Oct 2026): viral, animated, informative shorts about auctions.** Every one must be built to stop the scroll, hold to the end and get shared, while still teaching one true thing. Judge each script against the viral checklist below before you build it.
- **Length and pace.** Shorts win on retention, so keep them tight. Two paces, mixed (owner: "lesson 01 was slow; good, but quick things can be catchy, so be both"); the pace for each lesson is in `QUEUE.md`.
  - **Quick (most lessons):** 20–35 s, 55–90 words, one fact, one takeaway, narrator speed 1.08 (`Timeline(LINES, speed=1.08)`), pauses 0.1–0.25 s, 3–6 scenes.
  - **Standard:** 40–55 s (never over 60), 110–150 words, narrator speed 1.03, pauses 0.2–0.5 s, up to 9 scenes.
  - Cut every pause and every line that isn't doing work. Lesson 01 (70 s) is the upper limit we'll never reach again.

### Viral checklist (every lesson)

1. **The first second is the whole game.** The first frame shows the most surprising thing in the story (the $3.24M fish, the emperor's crown with a price tag), with the narrator starting on word one and the kinetic caption showing the hook as it's said. No setup, no "today we'll learn". The first frame doubles as the cover.
2. **Hook formulas that work:** a shocking number ("This fish sold for $3.24 million."), a paradox ("Haggling costs sellers money."), a "you didn't know" ("Rome was once sold at an auction."), a direct challenge ("You've been selling things wrong.").
3. **Open a loop early, pay it off late.** Tease the best part in the first 5 seconds ("…and the winner's reply is the best part") so people stay.
4. **Something changes every 2 to 3 seconds:** a cut, a zoom, a number counting, a stamp, a character reaction, a sound accent. Still one idea on screen at a time: change the picture, don't pile things up.
5. **Big, readable numbers** drawn into the scene (counters, price tags, stamps). Subtitles always on, so it works with the sound off.
6. **A twist or payoff near the end**, then a **loop line**: the last line flows back into the first frame so the replay feels seamless (e.g. ends on the same object the video opened on).
7. **Give people a reason to share or save:** a takeaway that makes them look smart, or a line they'd send a friend ("Send this to someone who still haggles"). Captions open with the hook and end with a question that invites comments.
8. **Energy:** the narrator sounds curious and confident (quick pace), music bed with a light pulse (marimba, pluck or lofi for quick lessons), sound accents on every reveal.
9. **Recurring cast for recognition:** Sami and Nour appear in every lesson, even briefly, so followers start to recognise the series.
- Arc (one idea per beat; a quick lesson keeps hook → story/number → takeaway → end card): **hook** (a paradox, a surprising number or a question, spoken in the first 2 s, with the subject already on screen) → **the idea** (one teaching device: a definition card, a simple diagram, a step list of at most 4 steps, or a chart) → **the true story** (props + the number) → **the lesson** (one sentence on a card) → **callback** to the hook with the answer → **end card**: the follow line "Follow for more special auction stories." (owner, 18 Oct 2026; no brand).
- Text and transitions: see "Style v3" below.

### Style v3: the level to hit (owner, 18 Oct 2026)

The owner shared a reference reel ("Steal 100 users from your competitor", Ben Zogby) as **the level** these shorts must reach. What makes it work, and how to do it with the kit (`motion.py`, reference implementation `lesson03.py`):

1. **Word-by-word kinetic captions at the top** (`KCaps(TL).draw(im, t, dark)`, y≈250): each word appears the moment the narrator says it (real word timings from `TL.words`), the newest word is strong, earlier words go grey, `[emphasis]` words get a lilac highlight, numbers also get a design-tool selection box. No bottom subtitle pill in v3.
2. **Clean UI cards are the visual language**: windows, phones, dashboards, order books, stat cards with big counters, rows with avatars, pills, chips, a cursor that clicks with a ripple, selection boxes, strikethroughs, big stamps (RECORD, SOLD). Generic UIs only: never HyperBidz screens, and made-up names say so in a footnote ("Company names are made up", "Bar heights are illustrative").
3. **Light and dark scenes alternate with the mood** (`bg(False)` grid paper, `bg(True)` near-black with stars), in the app colours.
4. **Something moves every 1 to 2 seconds**: cards spring in (`spring`, `settle`), numbers roll (`roll`), rows tick, a stamp lands, the cursor clicks. Still one idea at a time.
5. **Whip transitions with motion blur** between scenes (`whip`, 0.32 s), plus a slow camera push inside a scene.
6. **Concrete, specific, a little funny**: real numbers, a precise time ("exactly 4 p.m."), a relatable detail. The story runs hook → relatable setup → twist → how it works → proof number → payoff → loop/CTA.
7. **Sami and Nour live inside the UIs** as avatars (`head("sami")`, `head("nour")`): Nour bids, Sami asks, they appear in rows, chats and grids, and they close every video on the end card.
8. **End card**: paddles, Sami and Nour, a "+ Follow" pill that the cursor clicks, while the narrator says the follow line: **"Follow for more special auction stories."** (owner, 18 Oct 2026: not "follow to learn how auctions work"). No brand.
9. **Sound**: a whoosh on every whip, ticks on counters, pops on cards, a soft ding on reveals, thuds on stamps; the music bed stays low.

## The kit (`tools/lessons/`)

- **`lesson03.py` + `lesson03_lines.py` are the reference lesson (style v3).** Copy both to `lessonNN.py` / `lessonNN_lines.py` and rewrite the lines and scenes. Scenes are timed from the narration: `TL.t(key)` gives a line's start/end and `TL.wt(key, "word")` the exact moment a word is spoken (from `TL.words`). Never hard-code times. (`lesson01.py` is the older cartoon style; don't copy it.)
- `motion.py` (v3): `bg`, `KCaps`, `card`, `window`, `phone`, `pill`, `chip`, `stat`, `head`, `cursor`, `ripple`, `select_box`, `strike`, `big_stamp`, `stamp_at`, `roll`, `money`, `footnote`, `spring`, `settle`, `lift`, `whip`, and the text cache `T(text, size, colour, weight, mono)`.
- `narration.py`: `Timeline(LINES, speed=…)`, `speak()`, `TL.words(key)` exact word times (offline zipformer recogniser), `TL.wt(key, word)`, `asr_check()`. Lines are `(key, text, pause_after)`; `[word]` is highlighted in the subtitles; `{shown|spoken}` splits what's shown from what's said.
- `cast.py`: palette, `app_stage()`, `table()`, `radio()`, `tag()`, `sami()`, `nour()`, `bidder()`, `bidder_with_paddle()`, `chip_label()`, `subtitle()`.
- `ex_kit.py`: text (`serif`, `sans`, `mono`, `tl`, `rich_c`), layout (`put`, `shadowed`), easing (`ease`, `eout`, `pop`, `fade`), `camera`, `zoom_through`, props (`bubble`, `price_tag`, `stamp`, `paddle`, `pedestal`, `plaque`, `crt`, `paper`, `laser_pointer`), `Snd` sound effects.
- `music.py`: `make(total, style, seed)` and `mix(voice, bed, speaking, sfx)`.
- Setup in a fresh session: `bash tools/lessons/setup_tts.sh` (installs kokoro-onnx and sherpa-onnx, downloads the voice model and the speech models from GitHub, ~500 MB). Stills: `python3 tools/lessons/peek.py tools/lessons/lessonNN.py /tmp/p.png 1,5,9`. Render: `python3 tools/lessons/lessonNN.py /abs/path/out.mp4` (about 5 minutes).

## Lessons board

`https://claude.ai/artifact/1y9fTB5thL1iwc2versHBa` ("HyperBidz Lessons"; the board itself is internal and can carry the name). Database:
- `lessons/<id>` (id like `L02`, a redo `L02-v2`): `lesson` (number), `title` (`[word]` = emphasis), `topic`, `hook`, `learn` (one line: what viewers learn), `caption`, `captionAlt`, `quiz` `{question, options[4], answer (index), extra}`, `sources` `[{label, url}]`, `script` (the narration lines as plain text), `video` and `cover` (asset ids), `duration`, `status` (`waiting` → owner sets `approved` or `changes` with `note` → you set `scheduled` → `published`; `manual` when Metricool's monthly limit is full and the owner posts it himself, then he taps "I posted it" → `published`; `failed` if Metricool refuses), `slot` (ISO time: 19:00 Beirut on weekdays, 11:00 on Sat/Sun), `revision`, `createdAt`, `mediaUrl`, `metricoolId`, `igUrl`, `metrics` `{reach, plays, saves, shares, quizCorrect}`.
- `campaign/plan` `{total, titles[]}` (titles from `QUEUE.md`; update it when you add lessons to the queue).
- Upload media with the Artifact tool (`url` = the board, `file_path`, `asset: true`) and store the returned ids. Write documents with the ArtifactData tool.

## Procedure L: the daily lesson run (every morning)

1. `git pull`. Read `tools/lessons/QUEUE.md`; take the first lesson with `status: todo`. Read the owner's change notes on the board (`lessons` with `status: changes`): **a lesson with changes comes first** (redo it as `-v2`, same lesson number) before making a new one.
2. Research: open each source for the lesson's items in `research/auction_facts.md`, re-check every fact, find one vivid detail if thin. Unverifiable → drop it.
3. Write `tools/lessons/lessonNN_lines.py` (the narration, 140–175 words) and `posts/lessons/LNN-<slug>/script.md`. Check: hook surprising in 2 s? one clear thing learned? ends on why auctions are convenient? no HyperBidz?
4. Build `tools/lessons/lessonNN.py` from `lesson03.py` (style v3). Generate the narration and run `narration.asr_check()` on the voice track: fix any line that the transcript gets wrong (except brand names the small recogniser can't spell, like eBay).
5. Stills: look at the start, the key moment and the end of every scene. Fix overlaps, clipped text, crowded frames (rule 4).
6. Render to `posts/lessons/LNN-<slug>/lesson-NN.mp4`; ffprobe it (duration, 1080x1920, 30 fps, audio); loudness-normalise to −15 LUFS (`ffmpeg -c:v copy -af loudnorm=I=-15:TP=-1.5:LRA=11`); keep it under 19 MB. Extract `cover.jpg` (a frame with the hook).
7. Write `caption.md` (hook line, 3 to 5 short teaching lines, "Source: …", a CTA like "Follow for more special auction stories" or "Send this to someone who still haggles", 3 to 6 hashtags such as #auction #Lebanon #Beirut #learnoninstagram + topic; two options; no HyperBidz), `quiz.md`, `sources.md`.
8. Commit and push (`git add posts/lessons/LNN-* tools/lessons/lessonNN*.py tools/lessons/QUEUE.md`; set the lesson `status: made` with today's date in `QUEUE.md`; `git fetch -q origin main && git rebase -q FETCH_HEAD && git push -q origin HEAD:main`).
9. Board: upload the mp4 and the cover as assets, write `lessons/LNN` with `status: waiting`, `mediaUrl` (`https://raw.githubusercontent.com/rodolph30/hyperbidz-social/<full commit hash>/posts/lessons/LNN-<slug>/lesson-NN.mp4`; check with curl that it returns 200), and `slot` = the first day from today whose slot (19:00 Beirut on weekdays, 11:00 on Sat/Sun; see "Post times" for the offset) is still at least 1 hour away and isn't already held by another lesson that is waiting, approved or scheduled. Also add the lesson's title to `campaign/plan` if it isn't there.
10. **Notify the owner** with SendUserMessage: "Lesson NN is ready: <title>. Approve it on the Lessons board before <cutoff> and it posts at <time> on <day>. <board link>" (6:45 pm / 7 pm on weekdays, 10:45 am / 11 am on weekends). Also send the mp4 with SendUserFile so he can watch it right away. Never publish or schedule in this run.

## Procedure P: the posting check (09:45, 10:45, 12:45, 15:45, 17:45 and 18:45 Beirut, every day)

The 09:45 and 10:45 runs exist for the weekend 11:00 slot; on weekdays they only schedule what is approved and otherwise end quietly.

1. Read `lessons` on the board.
2. For each `approved` lesson without `metricoolId`:
   - **Its slot is still at least 10 minutes away:** schedule it for its own `slot`.
   - **Its slot has passed (or is under 10 minutes away): post it immediately** (owner, 18 Oct 2026: "whenever something is approved after its schedule, it should post immediately once it's approved"). Schedule it in Metricool for about 5 minutes from now and set `slot` to that time. Never push it to another day.
   - The board starts this check the moment the owner taps Approve (it fires the "Lesson posting check" scheduled task with a note naming the lesson), so approvals are scheduled within minutes; the timed runs are the backup.
   - **Never post twice:** before creating a post, look in Metricool (`getScheduledPosts` around the slot) for one with the same caption; if it exists, just record its id. If the lesson has `metricoolDraft` `{id, uuid}`, update that draft (`draft: false`, the right date) instead of creating a new post.
   - Use Metricool brand `7343454`, Instagram Reel, timezone Asia/Beirut, the lesson's `mediaUrl` (Metricool copies the mp4 from it when the post is created) and caption option 1. `isAiGenerated: false`: **never add the AI content tag to lessons** (owner, 16 Oct 2026). Check the monthly cap (`PLAYBOOK.md`). Then set `status: scheduled`, `slot`, `metricoolId`.
   - If the owner moves a lesson back to `waiting` (Undo) after you scheduled it, turn its Metricool post into a draft (`draft: true`) and keep its ids in `metricoolDraft`.
3. **Monthly limit (owner, 16 Oct 2026: "schedule up to the limit, and tell me when the limit hits").** Metricool's free plan allows 20 posts a month, counted as in `PLAYBOOK.md` (everything published or scheduled in Metricool that month).
   - If scheduling a lesson uses the **last** slot of the month, tell the owner right away: "Heads-up: Metricool's limit for <month> is now full (20/20). From <next lesson's date> until <1st of next month>, lessons won't post by themselves; I'll mark them 'Post it yourself' on the board."
   - If the month is **already full**, don't schedule. Set the lesson to `status: manual` (keep its `slot`) and message the owner: "Metricool's monthly limit is full, so Lesson NN won't post by itself. At <slot time>, open the board, tap Save video and Copy caption, post it, then tap 'I posted it'." The board shows a "Post it yourself" card for it.
   - On the 1st of a month the count resets: approved lessons go back to normal scheduling.
4. Scheduled lessons whose time has passed: confirm in Metricool, set `published` (+ `igUrl` if available). From the day after, record metrics when available. Lessons the owner marked "I posted it" are already `published` (`postedBy: owner`).
5. Reminders. **Weekdays (19:00 slot):** in the **17:45** run, if today's lesson is still `waiting`, send the owner one line: "Lesson NN is still waiting. Approve it before 6:45 pm to post at 7: <board link>". If today's lesson is `manual`, remind him to post it at 7 from the board. In the **18:45** run, repeat the `manual` reminder only if it's still `manual`. **Saturday and Sunday (11:00 slot):** the same reminders move to the **09:45** run ("…Approve it before 10:45 am to post at 11…") and the **10:45** run (`manual` only); no lesson reminders in the 17:45 and 18:45 runs on weekends.
6. If you scheduled something or a message above is due, tell the owner in one or two lines. Otherwise end quietly.

## Measurement

The owner runs the before/after surveys himself (16 Oct 2026); don't add surveys to the board. Each lesson still ships an optional story quiz idea in `quiz.md` and the board's Quiz tab. Once lessons are live, record per-lesson results from Metricool in the lesson's `metrics` (reach, plays, average watch time, saves, shares, comments, follows) so we can see which topics and which pace bring followers.
