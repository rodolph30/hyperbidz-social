# akhbarmazad (أخبار مزاد): the auction news page (owner's brief, 23 Oct 2026)

This file is the complete instructions for the akhbarmazad daily story run and its posting check. Read it in full before doing anything. The HyperBidz standing rules in `PLAYBOOK.md` ("Never") still apply where they fit.

## What the owner asked for

"I have another Instagram account and it's called akhbarmazad. This Instagram will be like a news page for auction wins, it will only post images with songs, and not motion graphics videos. Your aim is to share auction news around the Middle East: Dubai, Riyadh, KSA, UAE, Qatar, Kuwait, and make sure they are insane stories. Just post who won what at what price, with a headline. Research the internet for interesting auction wins, something that will attract people and let them follow this page, so that this page later on becomes a marketing tool for HyperBidz."

His choices (23 Oct 2026):
- **Arabic only**: card text and caption.
- **Designed news cards**, never news photos (they belong to agencies and auction houses).
- **Image Reel with an Instagram song, auto-posted** through Metricool once akhbarmazad is connected there (see "Posting").
- **One story a day.**

## Rules

1. **No HyperBidz** for now: no name, logo, app, link or hint, on the card or in the caption. The page earns trust as a news page first; the owner decides when it starts promoting HyperBidz.
2. **Only the Gulf and the Middle East**: UAE (Dubai, Abu Dhabi, Sharjah…), Saudi Arabia (Riyadh, Jeddah, Qassim…), Qatar, Kuwait, Bahrain, Oman. A record bought by a Gulf buyer elsewhere only if the buyer's origin is publicly reported.
3. **Insane, or skip it.** Every story must make someone stop and send it to a friend: an absurd price, an unexpected item (a number, a sheep, a falcon, a fish), a record, a bidding war. A dull result isn't news for this page.
4. **Facts only.** Every name, price, date and place comes from sources you opened: one official (the organiser, WAM, SPA, QNA, KUNA, the auction house) or two reputable outlets. If sources disagree, use the official figure. Never round a price up; "نحو" (about) for conversions.
5. **The winner.** Name the buyer only if a reputable outlet named them publicly. Otherwise "مزايد لم يُكشف اسمه". Never guess, never imply.
6. **No photos** of the items or people from the news. The card draws the item: plates and phone numbers are typeset exactly; everything else uses the MIT-licensed 3D emoji in `assets/emoji/` (Microsoft Fluent Emoji). Never draw a person.
7. **No politics, religion, war, or a private person's misfortune** (no seized homes of named people, no court cases about individuals).
8. **No AI tag** (`isAiGenerated: false`); the cards are designed, not generated. No boosts.
9. **Neutral, newsy tone.** Excitement comes from the facts. No mockery of buyers. Royal or official bidders: state the fact only if it was officially reported, with no comment.
10. **Credit the source** on the card (small line) and in the caption: "المصدر: …".

## The card and the Reel

- **The look (owner, 23 Oct 2026: "it should look like news")**: a TV breaking-news frame. Red slanted "عاجل" banner, the أخبار مزاد mark, a big white headline with a gold second line, a red rule and a dateline, a red price bar, a gold-framed panel with the item, a ticker (who won · which auction · when), the source. Navy background with red light streaks.
- `tools/card.py story.json` renders `card.png` (1080x1920) and `reel.mp4` (the card held for 12 s with a silent track; Instagram's song is attached when posting). Everything important sits between y 250 and 1560, so it survives both the profile-grid crop and the Reel's caption and buttons.
- `story.json` fields are documented at the top of `card.py`:
  - `headline` (white, about 18 characters, one line) + `highlight` (gold, the punch: usually the price in words, about 18 characters). Example: "لوحة سيارة في دبي" / "بـ 55 مليون درهم".
  - `dateline`: "مزاد الأرقام المميزة · دبي · أبريل 2023".
  - `price`: digits with commas, Western digits (`55,000,000`); `currency` (درهم، ريال، دينار، ريال قطري); `usd`: "نحو 15 مليون دولار".
  - ticker: `winner` ("لم يُكشف اسمه" or the publicly reported name, short), `event` (organiser, short), `date`.
  - `tag` (red stamp, optional): رقم قياسي، مزاد خيري، أغلى …، لأول مرة. Only when true.
- Look at the PNG once before uploading: nothing clipped, Latin/number runs in the right order, ticker text not cut off (keep each item under about 16 characters).
- Keep plate codes on the plate, not in the headline: Arabic text mixed with Latin codes reorders badly.

## Caption (Arabic)

```
<the headline, one line> 🔨
<2–3 short lines: what it is, who won, the price, where and when, one wow detail>
المصدر: <outlet(s)>
تابعونا لأغرب نتائج المزادات في الخليج 👈 @akhbarmazad
#مزاد #مزادات #<city> #<country> #<topic>
```
At most 3 emojis, 4–7 hashtags (#مزاد #مزادات #دبي #الرياض #السعودية #الامارات #قطر #الكويت #لوحات_مميزة #صقور …).

## The song

- Every Reel carries a popular Instagram song chosen for the mood (Khaleeji or Arabic hits for most stories; an epic or luxurious instrumental for record prices). Vary it: never the same song two days running.
- Record the choice in the story's `song` `{title, artist}` on the desk. Metricool takes a search term (song title and artist) in `instagramData.audioConfiguration.audioId` and resolves it when it matches exactly one track; if it returns several candidates, retry with the right numeric id. Audio only works when the account is an Instagram **Business** account linked to a Facebook Page.
- If the song can't be attached, post without it only if the owner agrees; otherwise mark the story `manual` and tell him which song to add in the app.

## The desk (approval board)

`https://claude.ai/artifact/WXRDeyZMCjBeYC8cbDUpQC` ("Akhbar Mazad Desk"). Database collection `stories/<id>` (ids `M001`, `M002`…; a redo keeps its id with `revision` + 1):
`headline` (Arabic), `english` (one-line English gloss for the owner), `itemEn`, `priceEn` (e.g. "AED 55,000,000 (≈ $15M)"), `place` (Arabic), `placeEn`, `caption`, `song` `{title, artist}`, `sources` `[{label, url}]`, `confidence`, `check` (one line: what you verified and where), `image` and `video` (asset ids), `mediaUrl` (raw GitHub link to `reel.mp4` at a full commit hash), `slot` (ISO, 21:00 Asia/Riyadh = `T21:00:00+03:00`), `status` (`waiting` → owner `approved` / `changes` with `note` → `scheduled` → `published`; `manual` when it can't post by itself; `failed`), `revision`, `createdAt`, `metricoolId`, `igUrl`, `metrics`.

Upload media with the Artifact tool (`url` = the desk, `asset: true`), write documents with ArtifactData.

## Story bank

- `research/auction_wins.md`: verified stories with sources, ranked by "insane factor", plus recurring events to watch. `QUEUE.md`: the posting order and status of each story.
- **Fresh news first.** Each run, search the web for auction results from the last 7 days in the region (plates and numbers auctions, falcon and camel auctions, Sotheby's/Christie's/RM Sotheby's sales in Dubai, Abu Dhabi, Riyadh, Doha). A verified fresh insane result goes before the bank. Add every new verified story to the research file.
- Mix the topics: never two plate stories in a row; rotate countries.

## Procedure A: the daily story run (every morning)

1. `git pull`. Read this file, `QUEUE.md`, and the desk (`stories`): a story with `status: changes` is redone first (same id, `revision` + 1, apply the note).
2. Look for fresh news (above); otherwise take the first `todo` in `QUEUE.md`.
3. Re-open its sources and re-check every fact. Unverifiable → skip it and mark it `dropped` with the reason.
4. Write `posts/<id>/story.json`, render with `python3 akhbarmazad/tools/card.py akhbarmazad/posts/<id>/story.json`, look at the PNG once, fix, re-render.
5. Write `posts/<id>/caption.md` (caption + sources + song choice).
6. Commit and push (`git add akhbarmazad/posts/<id> akhbarmazad/QUEUE.md akhbarmazad/research`; `git fetch -q origin main && git rebase -q FETCH_HEAD && git push -q origin HEAD:main`); check the raw `reel.mp4` link returns 200.
7. Desk: upload `card.png` and `reel.mp4` as assets; write `stories/<id>` with `status: waiting`, `slot` = the next 21:00 Riyadh that is at least 1 hour away and not held by another waiting/approved/scheduled story.
8. Tell the owner (SendUserMessage): "akhbarmazad story <id> is ready: <English gloss>. Approve it on the desk before 8:45 pm Riyadh and it posts at 9 pm. <desk link>", and send `card.png` with SendUserFile.

## Procedure B: the posting check

1. Read `stories` on the desk.
2. Find akhbarmazad in Metricool: `getBrandSettings` and look for a brand whose `networksData.instagramData` is `akhbarmazad`. **If there is none**, every `approved` story becomes `manual` (keep its `slot`), and tell the owner once per story: "Story <id> is approved but akhbarmazad isn't in Metricool yet, so post it yourself at 9 pm from the desk (Save Reel, Copy caption, add the song <song>), then tap 'I posted it'."
3. If the brand exists: for each `approved` story without `metricoolId`: slot ≥ 10 minutes away → schedule it for its slot; slot passed or under 10 minutes → post it now (about 5 minutes from now) and update `slot`. Instagram `REEL`, the story's `mediaUrl`, caption, `audioConfiguration` with the song, `isAiGenerated: false`, timezone Asia/Riyadh. **Never post twice**: check `getScheduledPosts` for the same caption first. Set `status: scheduled`, `metricoolId`.
4. Scheduled stories whose time has passed: confirm, set `published` and `igUrl`. Later runs record metrics (reach, plays, saves, shares, follows).
5. In the 19:46 Riyadh run, if tonight's story is still `waiting`, send one line: "Tonight's akhbarmazad story is still waiting. Approve it before 8:45 pm Riyadh: <desk link>".

## Measurement

Track per story: reach, plays, shares, saves, follows gained. Every Monday, note in `QUEUE.md` which topics (plates, numbers, animals, luxury) and which songs did best, and lean the bank toward them.
