# akhbarmazad (أخبار مزاد): the auction news page (owner's brief, 23 Oct 2026)

This file is the complete instructions for the akhbarmazad daily story run and its posting check. Read it in full before doing anything. The HyperBidz standing rules in `PLAYBOOK.md` ("Never") still apply where they fit.

## What the owner asked for

"I have another Instagram account and it's called akhbarmazad. This Instagram will be like a news page for auction wins, it will only post images with songs, and not motion graphics videos. Your aim is to share auction news around the Middle East: Dubai, Riyadh, KSA, UAE, Qatar, Kuwait, and make sure they are insane stories. Just post who won what at what price, with a headline. Research the internet for interesting auction wins, something that will attract people and let them follow this page, so that this page later on becomes a marketing tool for HyperBidz."

His choices (23 Oct 2026):
- **Arabic only**: image text and caption.
- **Static news images only**, no video, no animation ("I want static images and not motion graphics… just the news").
- **Real photos from the internet**, fetched from the news coverage and credited ("with real images from the internet that you fetch and use"). This replaces the designed-card option he first picked.
- **A breaking-news song** behind each post ("the ones they use for breaking news"). On a photo post Instagram only lets the song be added in the app, so for now he adds it when he posts (see "The song").
- The look: a TV breaking-news frame (his reference image, 23 Oct 2026).
- **One story a day**, 9 pm Riyadh. Metricool isn't connected for akhbarmazad (its free plan allows one brand and he can't pay yet), so he posts approved stories himself from the desk.

## Rules

1. **No HyperBidz** for now: no name, logo, app, link or hint, on the card or in the caption. The page earns trust as a news page first; the owner decides when it starts promoting HyperBidz.
2. **Only the Gulf and the Middle East**: UAE (Dubai, Abu Dhabi, Sharjah…), Saudi Arabia (Riyadh, Jeddah, Qassim…), Qatar, Kuwait, Bahrain, Oman. A record bought by a Gulf buyer elsewhere only if the buyer's origin is publicly reported.
3. **Insane, or skip it.** Every story must make someone stop and send it to a friend: an absurd price, an unexpected item (a number, a sheep, a falcon, a fish), a record, a bidding war. A dull result isn't news for this page.
4. **Facts only.** Every name, price, date and place comes from sources you opened: one official (the organiser, WAM, SPA, QNA, KUNA, the auction house) or two reputable outlets. If sources disagree, use the official figure. Never round a price up; "نحو" (about) for conversions.
5. **The winner.** Name the buyer only if a reputable outlet named them publicly. Otherwise "مزايد لم يُكشف اسمه". Never guess, never imply.
6. **Real news photos, credited.** Use the photo of the actual item from the coverage (see "Getting the photo"). Prefer the organiser's or a news agency's own press photo (WAM, SPA, QNA, KUNA, the auction house) or the outlet's own photo; never a watermarked image, never a Getty/Reuters/AFP/AP image (they enforce aggressively), never a photo where a child is the subject. Always put "الصورة: <outlet>" on the photo. If no usable photo exists, fall back to the drawn visual (plates and phone numbers typeset exactly; other items as the MIT-licensed 3D emoji in `assets/emoji/`).
7. **No politics, religion, war, or a private person's misfortune** (no seized homes of named people, no court cases about individuals).
8. **No AI tag** (`isAiGenerated: false`); the cards are designed, not generated. No boosts.
9. **Neutral, newsy tone.** Excitement comes from the facts. No mockery of buyers. Royal or official bidders: state the fact only if it was officially reported, with no comment.
10. **Credit the source** on the card (small line) and in the caption: "المصدر: …".

## The image

- **The look (owner, 23 Oct 2026: "it should look like news")**: a TV breaking-news frame. Red slanted "عاجل" banner, the أخبار مزاد mark, a big white headline with a gold second line, a red rule and a dateline, a red price bar, a gold-framed panel with the item, a ticker (who won · which auction · when), the source. Navy background with red light streaks.
- `tools/card.py story.json` renders `card.jpg`: a static 1080x1350 (4:5) image for an Instagram photo post, with the real photo in the gold frame (`photo`, `photo_credit`, `photo_pos`, and `tag_side: "left"` when the stamp would cover a face). Side margins stay wide enough for the profile grid's 3:4 crop.
- `story.json` fields are documented at the top of `card.py`:
  - `headline` (white, about 18 characters, one line) + `highlight` (gold, the punch: usually the price in words, about 18 characters). Example: "لوحة سيارة في دبي" / "بـ 55 مليون درهم".
  - `dateline`: "مزاد الأرقام المميزة · دبي · أبريل 2023".
  - `price`: digits with commas, Western digits (`55,000,000`); `currency` (درهم، ريال، دينار، ريال قطري); `usd`: "نحو 15 مليون دولار".
  - ticker: `winner` ("لم يُكشف اسمه" or the publicly reported name, short), `event` (organiser, short), `date`.
  - `tag` (red stamp, optional): رقم قياسي، مزاد خيري، أغلى …، لأول مرة. Only when true.
- Look at the JPG once before uploading: nothing clipped, Latin/number runs in the right order, ticker text not cut off (keep each item under about 16 characters).
- Keep plate codes on the plate, not in the headline: Arabic text mixed with Latin codes reorders badly.

## Getting the photo

The workspace can't reach news sites, but the Higgsfield sandbox (`mcp__Higgsfield__sandbox_exec`) can:
1. In the sandbox, `curl -sL -A "Mozilla/5.0 …" <article url>` and read the `og:image` / `twitter:image` meta tags (or the article's image list). Prefer the largest version (strip crop parameters or ask for `width=1600`); send a `Referer:` header of the outlet if the image host refuses.
2. Open it with Pillow, convert to RGB, resize to at most 1600 px wide, save as JPEG quality about 86 (it must stay under 500 KB).
3. Return it with `image_paths` on a foreground `sandbox_exec` call. The tool result names a local copy ("source: /root/.claude/projects/…/tool-results/mcp-Higgsfield-blob-….jpg"). Copy that file to `posts/<id>/photo.jpg`. Never relay image bytes as base64 text.
4. Look at the photo: is it the actual item from this sale? Who took it (check the caption or credit near the image in the page)? Credit the outlet on the image.

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

- Every post carries a **breaking-news theme** (owner: "the ones they use for breaking news"). Use the same theme on every post so it becomes the page's sound.
- On a photo post, Instagram only lets the song be added in the app. The owner adds it when he posts: Music → search "Breaking News". Write that in the story's `song` on the desk.
- Later, if akhbarmazad is added to Metricool: the API can attach a song only to Reels, not photos. Ask the owner then whether to auto-post photos without the song, or keep adding the song himself.

## The desk (approval board)

`https://claude.ai/artifact/WXRDeyZMCjBeYC8cbDUpQC` ("Akhbar Mazad Desk"). Database collection `stories/<id>` (ids `M001`, `M002`…; a redo keeps its id with `revision` + 1):
`headline` (Arabic, headline + highlight), `english` (one-line English gloss for the owner), `itemEn`, `priceEn` (e.g. "AED 55,000,000 (≈ $15M)"), `place` (Arabic), `placeEn`, `caption`, `song` `{title, artist}`, `sources` `[{label, url}]`, `confidence`, `check` (one line: what you verified and where), `image` (asset id of `card.jpg`), `mediaUrl` (raw GitHub link to `card.jpg` at a full commit hash), `slot` (ISO, 21:00 Asia/Riyadh = `T21:00:00+03:00`), `status` (`waiting` → owner `approved` / `changes` with `note` → `scheduled` → `published`; `manual` when it can't post by itself; `failed`), `revision`, `createdAt`, `metricoolId`, `igUrl`, `metrics`.

Upload media with the Artifact tool (`url` = the desk, `asset: true`), write documents with ArtifactData.

## Story bank

- `research/auction_wins.md`: verified stories with sources, ranked by "insane factor", plus recurring events to watch. `QUEUE.md`: the posting order and status of each story.
- **Fresh news first.** Each run, search the web for auction results from the last 7 days in the region (plates and numbers auctions, falcon and camel auctions, Sotheby's/Christie's/RM Sotheby's sales in Dubai, Abu Dhabi, Riyadh, Doha). A verified fresh insane result goes before the bank. Add every new verified story to the research file.
- Mix the topics: never two plate stories in a row; rotate countries.

## Procedure A: the daily story run (every morning)

1. `git pull`. Read this file, `QUEUE.md`, and the desk (`stories`): a story with `status: changes` is redone first (same id, `revision` + 1, apply the note).
2. Look for fresh news (above); otherwise take the first `todo` in `QUEUE.md`.
3. Re-open its sources and re-check every fact. Unverifiable → skip it and mark it `dropped` with the reason.
4. Get the photo (see "Getting the photo") into `posts/<id>/photo.jpg`. Write `posts/<id>/story.json`, render with `python3 akhbarmazad/tools/card.py akhbarmazad/posts/<id>/story.json`, look at `card.jpg` once (stamp off faces, nothing clipped), fix, re-render.
5. Write `posts/<id>/caption.md` (caption, song, photo credit, sources).
6. Commit and push (`git add akhbarmazad/posts/<id> akhbarmazad/QUEUE.md akhbarmazad/research`; `git fetch -q origin main && git rebase -q FETCH_HEAD && git push -q origin HEAD:main`); check the raw `card.jpg` link returns 200.
7. Desk: upload `card.jpg` as an asset; write `stories/<id>` with `status: waiting`, `slot` = the next 21:00 Riyadh that is at least 1 hour away and not held by another waiting/approved/scheduled story.
8. Tell the owner (SendUserMessage): "akhbarmazad story <id> is ready: <English gloss>. Approve it on the desk before 8:45 pm Riyadh and it posts at 9 pm. <desk link>", and send `card.jpg` with SendUserFile.

## Procedure B: the posting check

1. Read `stories` on the desk.
2. Find akhbarmazad in Metricool: `getBrandSettings` and look for a brand whose `networksData.instagramData` is `akhbarmazad`. **If there is none** (the case today), every `approved` story becomes `manual` (keep its `slot`), and tell the owner once per story: "Story <id> is approved. Post it yourself at 9 pm Riyadh from the desk: Save image, Copy caption, post it as a photo on @akhbarmazad, add the breaking-news song from Instagram's Music, then tap 'I posted it'."
3. If the brand exists and the owner has said how to handle the song (see "The song"): for each `approved` story without `metricoolId`: slot ≥ 10 minutes away → schedule it for its slot; slot passed or under 10 minutes → post it now (about 5 minutes from now) and update `slot`. Instagram `POST` with the story's `mediaUrl` and caption, `isAiGenerated: false`, timezone Asia/Riyadh. **Never post twice**: check `getScheduledPosts` for the same caption first. Set `status: scheduled`, `metricoolId`.
4. Scheduled stories whose time has passed: confirm, set `published` and `igUrl`. Later runs record metrics (reach, plays, saves, shares, follows).
5. In the 19:46 Riyadh run, if tonight's story is still `waiting`, send one line: "Tonight's akhbarmazad story is still waiting. Approve it before 8:45 pm Riyadh: <desk link>".

## Measurement

Track per story: reach, plays, shares, saves, follows gained. Every Monday, note in `QUEUE.md` which topics (plates, numbers, animals, luxury) and which songs did best, and lean the bank toward them.
