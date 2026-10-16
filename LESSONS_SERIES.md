# Auction lessons: the awareness campaign (owner's brief, 16 Oct 2026)

This file is the complete instructions for the daily lesson run and the posting check. Read it in full before doing anything. `PLAYBOOK.md` "The owner's standing instructions" and "Never" still apply, except where this file is stricter.

## What the owner asked for

- **One educational video every day.** You research, you write the story, it must be catchy and easy to follow.
- The goals: **teach** how auctions work, build **awareness** of auctions (in Lebanon: courts, the state, fish halls, plates; worldwide; stock markets), and show **why auctions are convenient**, so people want to use one.
- **"Did you know" facts**, Lebanon and worldwide, including the link between bidding and stocks.
- **No Higgsfield and no AI video tool.** Every frame is drawn in code with the kit in `tools/lessons/`.
- At the end of the campaign, measure how much people's knowledge and willingness to use auctions increased (see "Measurement").

## Rules for this campaign (owner, 16 Oct 2026; these override anything else)

1. **Never mention HyperBidz.** No name, no logo or Z mark, no wordmark, no "coming soon", no handle on screen, no app screens or app UI. Captions don't mention it either. The videos only talk about auctions: how they work and why they're convenient.
2. **No tags on screen.** No "Lesson NN" label, no chapter chips, no progress bar.
3. **A narrator speaks the whole video** in a calm, clear, teacher-like voice (`narration.py`: Kokoro voice `am_michael`, speed 1.0; don't change it without the owner). Every on-screen idea is spoken. Subtitles follow the voice, a few words at a time (`cast.subtitle`).
4. **Easy to follow.** One idea on screen at a time. Few words on screen besides the subtitles: at most one short headline, one number or one card at a time. Nothing else moving while the key point lands. If a frame has more than three things competing for attention, simplify it.
5. **Music stays quietly in the background** (`music.mix`, bed about −21 dB under the voice, ducked further while the narrator speaks) and is **different every video**: use the style and seed given in `QUEUE.md` (styles rotate keys → marimba → ambient → pluck → lofi; seed = lesson number).
6. **App colours** (`cast.py`): near-black stage #0B0E14, electric blue #2F7BFF, violet #7C5CFF, lilac #A78BFA, green #00A364, white. No warm/orange palettes.
7. **The same characters every time** (`cast.py`): **Sami** the seller (blue, small moustache), **Nour** the buyer (lilac, hair bun), and **the bidders** (violet, green, silver, with numbered paddles). Reuse them; don't invent new characters. Real people in stories are never drawn as faces (show objects, screens, places instead).
8. **Professional, not niche.** No family-nostalgia props or words (no "jeddo's…", "teta's…"), no inside jokes. Plain, confident, explanatory.
9. **Facts only.** Every number, date, name and quote must come from a source you opened (the research file's links, re-checked). Write numbers for the voice in words with `{shown|spoken}` markup, e.g. `{$14.83|fourteen dollars and eighty-three cents}`. Cartoon prices (Sami's radio) are illustrations and must look like it.
10. **Neutral on Lebanon.** Explain how things work; never blame or name a bank, judge, official, party or person; no crisis jokes; no politics. No legal or financial advice ("this is how it works", never "you should buy").
11. No slogan "Ma fi ekher se3er…", no "last price?/akher se3er".

## Format

- 1080x1920, 30 fps, **55 to 75 s**, H.264, under 19 MB (re-encode at a higher CRF if larger; the board's upload cap is 20 MB).
- Arc (one idea per beat): **hook** (a paradox, a surprising number or a question, spoken in the first 2 s, with the subject already on screen) → **the idea** (one teaching device: a definition card, a simple diagram, a step list of at most 4 steps, or a chart) → **the true story** (props + the number) → **the lesson** (one sentence on a card) → **callback** to the hook with the answer → **end card**: a short line like "Follow to learn how auctions really work." (no brand).
- Text: subtitles at y≈1600 via `subtitle(im, t, TL)`; a headline only for the hook; big numbers drawn as part of the scene (counters, marquee years, cards).
- Transitions: `zoom_through` 0.36 s between scenes; gentle camera push inside scenes.

## The kit (`tools/lessons/`)

- `lesson01.py` + `lesson01_lines.py`: the reference lesson. Copy both to `lessonNN.py` / `lessonNN_lines.py` and rewrite the lines and scenes. Scenes are timed from the narration: `TL.t(key)` gives a line's start/end, `TL.word(key, "word")` the moment a word is spoken. Never hard-code times.
- `narration.py`: `Timeline(LINES)`, `speak()`, subtitles chunking, `asr_check()`. Lines are `(key, text, pause_after)`; `[word]` is highlighted in the subtitles; `{shown|spoken}` splits what's shown from what's said.
- `cast.py`: palette, `app_stage()`, `table()`, `radio()`, `tag()`, `sami()`, `nour()`, `bidder()`, `bidder_with_paddle()`, `chip_label()`, `subtitle()`.
- `ex_kit.py`: text (`serif`, `sans`, `mono`, `tl`, `rich_c`), layout (`put`, `shadowed`), easing (`ease`, `eout`, `pop`, `fade`), `camera`, `zoom_through`, props (`bubble`, `price_tag`, `stamp`, `paddle`, `pedestal`, `plaque`, `crt`, `paper`, `laser_pointer`), `Snd` sound effects.
- `music.py`: `make(total, style, seed)` and `mix(voice, bed, speaking, sfx)`.
- Setup in a fresh session: `bash tools/lessons/setup_tts.sh` (installs kokoro-onnx and downloads the voice model from GitHub, ~350 MB). Stills: `python3 tools/lessons/peek.py tools/lessons/lessonNN.py /tmp/p.png 1,5,9`. Render: `python3 tools/lessons/lessonNN.py /abs/path/out.mp4` (about 5 minutes).

## Lessons board

`https://claude.ai/artifact/1y9fTB5thL1iwc2versHBa` ("HyperBidz Lessons"; the board itself is internal and can carry the name). Database:
- `lessons/<id>` (id like `L02`, a redo `L02-v2`): `lesson` (number), `title` (`[word]` = emphasis), `topic`, `hook`, `learn` (one line: what viewers learn), `caption`, `captionAlt`, `quiz` `{question, options[4], answer (index), extra}`, `sources` `[{label, url}]`, `script` (the narration lines as plain text), `video` and `cover` (asset ids), `duration`, `status` (`waiting` → owner sets `approved` or `changes` with `note` → you set `scheduled` → `published`; `failed` if Metricool refuses), `slot` (ISO time, 19:00 Beirut), `revision`, `createdAt`, `metricoolId`, `igUrl`, `metrics` `{reach, plays, saves, shares, quizCorrect}`.
- `campaign/plan` `{total, titles[]}` (titles from `QUEUE.md`), `campaign/survey` `{questions[{text, kind, measures}], baselineFrames[], endlineFrames[], baseline{date, n, results[]}, endline{...}}`.
- Upload media with the Artifact tool (`url` = the board, `file_path`, `asset: true`) and store the returned ids. Write documents with the ArtifactData tool.

## Procedure L: the daily lesson run (every morning)

1. `git pull`. Read `tools/lessons/QUEUE.md`; take the first lesson with `status: todo`. Read the owner's change notes on the board (`lessons` with `status: changes`): **a lesson with changes comes first** (redo it as `-v2`, same lesson number) before making a new one.
2. Research: open each source for the lesson's items in `research/auction_facts.md`, re-check every fact, find one vivid detail if thin. Unverifiable → drop it.
3. Write `tools/lessons/lessonNN_lines.py` (the narration, 140–175 words) and `posts/lessons/LNN-<slug>/script.md`. Check: hook surprising in 2 s? one clear thing learned? ends on why auctions are convenient? no HyperBidz?
4. Build `tools/lessons/lessonNN.py` from `lesson01.py`. Generate the narration and run `narration.asr_check()` on the voice track: fix any line that the transcript gets wrong (except brand names the small recogniser can't spell, like eBay).
5. Stills: look at the start, the key moment and the end of every scene. Fix overlaps, clipped text, crowded frames (rule 4).
6. Render to `posts/lessons/LNN-<slug>/lesson-NN.mp4`; ffprobe it (duration, 1080x1920, 30 fps, audio); loudness-normalise to −15 LUFS (`ffmpeg -c:v copy -af loudnorm=I=-15:TP=-1.5:LRA=11`); keep it under 19 MB. Extract `cover.jpg` (a frame with the hook).
7. Write `caption.md` (hook line, 3 to 5 short teaching lines, "Source: …", a CTA like "Follow to learn how auctions really work" or "Send this to someone who still haggles", 3 to 6 hashtags such as #auction #Lebanon #Beirut #learnoninstagram + topic; two options; no HyperBidz), `quiz.md`, `sources.md`.
8. Commit and push (`git add posts/lessons/LNN-* tools/lessons/lessonNN*.py tools/lessons/QUEUE.md`; set the lesson `status: made` with today's date in `QUEUE.md`; `git fetch -q origin main && git rebase -q FETCH_HEAD && git push -q origin HEAD:main`).
9. Board: upload the mp4 and the cover as assets, write `lessons/LNN` with `status: waiting`, `slot` = today 19:00 Beirut (`YYYY-MM-DDT19:00:00+03:00`; if today's slot already holds an approved or scheduled lesson, the next free day).
10. **Notify the owner** with SendUserMessage: "Lesson NN is ready: <title>. Approve it on the Lessons board before 6:45 pm and it posts at 7. <board link>". Also send the mp4 with SendUserFile so he can watch it right away. Never publish or schedule in this run.

## Procedure P: the posting check (12:50, 15:50, 17:50 and 18:45 Beirut)

1. Read `lessons` on the board.
2. For each `approved` lesson without `metricoolId`: its slot is the next 19:00 Beirut that's at least 10 minutes away and not taken by another scheduled lesson. Check the Metricool monthly cap (`PLAYBOOK.md`). Schedule it in Metricool (brand `7343454`, Instagram Reel, timezone Asia/Beirut) with the mp4's public link from this repo (jsDelivr `https://cdn.jsdelivr.net/gh/rodolph30/hyperbidz-social@<commit>/posts/lessons/...`) and caption option 1. `isAiGenerated`: not decided for this series; ask the owner once and record his answer here. Then set `status: scheduled`, `slot`, `metricoolId`.
3. If the cap is full, don't schedule: set the lesson's `note` to say so and message the owner that he can post it himself from the board (Save video + Copy caption).
4. Scheduled lessons whose time has passed: confirm in Metricool, set `published` (+ `igUrl` if available). From the day after, record metrics when available.
5. Reminder: in the **17:50** run, if today's lesson is still `waiting`, send the owner one line: "Lesson NN is still waiting. Approve it before 6:45 pm to post at 7: <board link>".
6. If you scheduled something, tell the owner in one line. Otherwise end quietly.

## Measurement (owner: measure knowledge and willingness at the end)

- **Baseline** before the first lesson goes live: story frames in `posts/lessons/survey/baseline-*.jpg` (on the board, "Before and after"). The owner posts them with the sticker shown on each frame and screenshots the results after 24 h. Questions: ever bid in an auction (poll); who decides the final price (quiz); Lebanese courts sell seized property at public auction, true/false (quiz); where a share price comes from (quiz); how comfortable buying at auction (slider); would you use a live auction app made for Lebanon (poll).
- **Per lesson:** the quiz from `quiz.md` as a story Quiz sticker the day after; record its correct-answer rate in `metrics.quizCorrect`.
- **Endline** after the last lesson: the same questions plus "Did you watch our auction lessons?" (`posts/lessons/survey/endline-*.jpg`). Compare before/after, and watchers vs non-watchers. Write the results into `campaign/survey`.
- Engagement per lesson from Metricool: reach, plays, average watch time, saves, shares, comments, follows.
