# Founder series: Rodolph on camera (strategy and episode bible)

The owner, Rodolph, appears on camera as himself: bald, full dark beard, round black sunglasses, black crew-neck t-shirt, a thin gold chain. His face, beard and sunglasses stay the same in every season; each season has its own dressed character image (see Seasons). Generate him in Google Flow from his photo, which the owner keeps; never publish the photo to this public repo.

## Positioning (never name competitors)

HyperBidz is the fair way to buy and sell in Lebanon: buyers compete live, so the price goes up instead of down.

The enemy is "the old way" of classifieds, never named:
- posting and waiting
- "Is it still available?"
- lowball offers
- haggling
- people who never show up
- one buyer setting the price

Only claim features the owner has confirmed. Known from the app's design: live bidding, a countdown, the "Going once… Going twice…" and "Hammer falling" moments, and time added when someone bids at the last second.

## Formats (rotate them, 20 to 30 s each, founder plus pop-ups)

1. **The Old Way.** A problem the old way causes, then how bidding fixes it. Chat-bubble pop-ups act out the problem, bid pop-ups act out the fix.
2. **How it works in 20 seconds.** One mechanic per episode: listing, live bids, time added, winning, getting paid.
3. **What's it worth?** He presents one item (a watch, a vintage camera, sneakers, a bag), viewers guess the price in the comments, and the item goes into the first live auction. This builds the community and the first listings.
4. **The Luxury Drop.** A weekly teaser of one premium item for the luxury community: close-ups, provenance, the starting bid, and a launch-day auction.
5. **Myths.** "Auctions are only for the rich." "Auctions are rigged." "My stuff isn't worth anything."
6. **Fiction episodes** for reach: "The Last One", "Pulled In".

## Community mechanics

- **One call to action in every episode:** comment, follow, or "DM us the item you'd sell first". The best DMs become featured items in later episodes.
- **Recurring lines** the audience learns: "Don't sell it. Let them bid for it." and "Find out the second price."
- **Cadence:** about 3 founder episodes a week, plus fiction or carousels in between.

## Approval (owner's rule)

No episode of this series goes to Instagram until the owner approves it on the Approval Board. Finished cuts go on the board as `waiting`, and the approval check posts them only once they are `approved`.

## Production rules for the founder clips (owner's rule: one prompt per episode)

- **One prompt and one 8-second clip per episode.** The owner attaches only his photo as the character reference in Veo. No first-frame images, no multi-clip episodes.
- **Each prompt describes:**
  - where he stands
  - exactly what is in the frame
  - what he says: at most about 20 words, with timestamps
  - at most 1 or 2 simple actions, with timestamps
- **Anti-hallucination lines:**
  - his hands are empty unless a prop is named
  - the sunglasses stay on his face
  - nothing else enters the frame
  - static camera, a clean picture with no text anywhere
- **Voice line in every prompt:** English with a light Lebanese accent, calm, confident, warm, medium-low.
- **Keep prompts simple,** in the style of the Ep. 1 prompt, which the owner called perfect: a short setting, a short "only these things in the frame" line, his lines with timestamps, and at most 2 actions.
- **Always end the prompt with:** "No captions, no subtitles, no text or writing anywhere on the video."
- **From Season 7 E2 on (owner, 14 Oct 2026):** the character image he attaches already carries the room, the ambience and how he looks. So the prompt says only "Use the attached character". Never describe the room, the lighting, his clothes or his looks. List only the objects that must be in the shot (e.g. the envelope and the watch box), then the timed lines, the actions, the voice, the sound and the anti-hallucination lines.
- **Hold the last shot (owner, 14 Oct 2026):** before the end card, let the last shot breathe for about 1.4 s, frozen on its last frame with a slow push-in (`hold_zoom` in founder_common.py: start the push about 1 s before the clip ends, zoom to about 1.08 toward his face), keeping the last caption and pop-ups on screen. Viewers need time to take in the final moment.
- **The edit makes it an episode:** captions, pop-ups acting out the line, sound design, and the end card.

## Seasons (owner's plan, 14 Oct 2026)

Each season targets one audience and is shot in one place, with the same setting text in every prompt of that season.

**Character image per season:** for each season the owner makes one character image that is already dressed (same face, beard and sunglasses every time; the sunglasses and style may change in later seasons). He attaches that image in Veo. Prompts never describe his clothes: the image decides the outfit. Design the next season's look with the owner, then give him an image prompt for it. A character image should have a plain background so the setting comes only from the prompt.

| Season | Audience | Place | Character image |
|---|---|---|---|
| 1 | Auction awareness (done: Ep. 1–6 below) | Mixed | Owner's photo, black crew-neck tee |
| 2 | Buyers | Rooftop infinity pool, Beirut, night | Owner's S2 character, black short-sleeve button shirt |
| 3 | Sellers | Old Beirut house, triple-arched window, afternoon sun | To design with the owner |
| 4 | Cars | Dark private garage, one classic car under a spotlight | Later |
| 5 | Watches | Dark walnut private vault, one lit glass case | Later (no watch on his wrists unless the episode needs one) |
| 6 | Bags (mainly women) | Bright boutique dressing room | Later (owner to decide: him, or a female co-host) |

Ideas for later seasons: sneakers and streetwear (young crowd), antiques and art (Lebanese heritage).

**Setting texts for the next seasons:**

- **S3 Sellers:** "Setting: inside an old Beirut house. Behind him, a tall triple-arched window with warm afternoon sunlight, pale stone walls and patterned floor tiles. Nothing else in the frame: no furniture, no objects, no other people."
- **S4 Cars:** "Setting: a dark private garage at night. Behind him, one classic silver sports car under a single soft spotlight, its body clean and smooth, with no badges, no logos and no license plate. Nothing else in the frame: no other cars, no objects, no other people."
- **S5 Watches:** "Setting: a quiet private vault with dark walnut walls. Behind him, one small glass display case lit from inside, holding a single steel watch. Nothing else in the frame: no other objects, no other people."
- **S6 Bags:** "Setting: a bright luxury boutique dressing room in soft daylight, cream walls and a warm marble floor. Behind him, one shelf holding three handbags in black, cream and caramel, with plain leather and no logos. Nothing else in the frame: no other objects, no other people."

**Cadence:** Metricool is on the Free plan (20 posts a month), so a 6-episode season takes about a week and a half alongside other posts.

## Episodes

### Ep. 1: "They bid" (The Old Way)

**Line:** "You posted it. Twelve messages. 'Is it still available?' Not one real offer. On HyperBidz, they don't message… they bid."

**Actions:** a small shrug on "not one real offer", then he points at the camera on "they bid".

**Edit:** a message counter and a flood of "Is it still available?" bubbles, the bubbles getting swept away by live bids climbing, then the end card "Don't sell it. Let them bid for it."

### Ep. 2: "Worthless" (Myths)

**Setting:** a Beirut rooftop at blue hour.

**Line:** "Everyone thinks their old stuff is worthless… until three people want it at the same time. That's an auction."

**Actions:** he raises three fingers on "three people", then gives a small confident nod at the end.

**Edit:** a "WORTHLESS?" tag that gets struck through, three bidder avatars popping in one by one, a price ticker jumping, then the end card "Find out the second price."

### Ep. 3: "Be in the room" (Luxury Drop, FOMO)

**Setting:** a dark private gallery, with a glass case holding one steel watch.

**Line:** "The rarest pieces in Lebanon won't sit in a shop window. They'll go live. Once. Be in the room."

**Actions:** a hand on the case, then a nod.

**Edit:** violet light particles rising from the case, a "LIVE ONCE" tag, the bidder count climbing, end card.

### Ep. 4: "Pay attention" (Myths)

**Setting:** a private members' lounge, him seated in a leather armchair.

**Line:** "Auctions were never for the rich. They're for the people who pay attention. Most people don't."

**Actions:** he taps his temple, then leans back with a smile.

**Edit:** a "FOR THE RICH" label stamped "MYTH", then a deal ticker showing smart buyers' wins.

### Ep. 5: "How smart people sell" (How it works)

**Setting:** a Beirut marina terrace at night.

**Line:** "You set the starting price. The market sets the final one. That's not luck. That's how smart people sell."

**Actions:** his palm moves down, then rises.

**Edit:** a "STARTING PRICE $100" chip at his low hand, a "FINAL $640" counter rising with his hand.

### Ep. 6: "Don't hear about it later" (Launch FOMO)

**Setting:** a penthouse at night, him holding his phone with the screen facing him.

**Line:** "The first HyperBidz auction is coming. First in always gets the best deals. Don't hear about it later."

**Actions:** a glance at the phone, then a nod.

**Edit:** a "FIRST AUCTION · SOON" countdown, a "Turn on notifications" chip, a Follow call to action.

## Season 2: for buyers (all episodes in one place)

**Goal:** make buyers excited to buy through auctions instead of fixed-price marketplaces. The benefits:
- you decide what it's worth to you
- deals below retail
- the thrill of the last seconds
- no "is it still available?"
- every bid is visible and the rules are the same for everyone
- the joy of the first win

**Fixed setting:** use this exact text in every Season 2 prompt.

> Setting: a luxury rooftop terrace in Beirut at night. Behind him, the glowing blue water of an infinity pool and, beyond it, the softly blurred city lights and the dark sea. A thin violet light line runs along the edge of the pool. Nothing else in the frame: no furniture, no objects, no other people.

1. **S2E1 "You decide":** "On other apps, the seller decides the price. Here… you do. Bid what it's worth to you. Not a dollar more."
2. **S2E2 "Full price?":** "Why pay full price? On HyperBidz, the same thing can go for way less… if you're there when it happens."
3. **S2E3 "The rush":** "Ten seconds left. You're winning. Someone bids. Your heart jumps… and you bid again. Nothing else feels like that."
4. **S2E4 "Just bid":** "No 'is it still available?' No waiting for replies. If it's live, it's available. You just bid."
5. **S2E5 "Same chance":** "Every bid is live, in front of everyone. No secret deals. No special prices for friends. Same chance for all."
6. **S2E6 "First win":** "Remember your first win? You will. The first HyperBidz auctions are coming. Be there… and bid."

### Season 1, Ep. 7: "Two prices" (replaces the earlier presenter clip, p010)

**Setting:** a modern Beirut apartment at golden hour, a large window behind him.

**Line:** "Everything you own has two prices. The one you'd sell it for… and the one someone would fight for."

**Actions:** a slight lean toward the camera on "fight for", then a knowing smile and nod.

**Edit:** the two price tags from the first version ("YOUR PRICE $20" and "THEIR PRICE" climbing, then "$ ???"), end card "Find out the second price."

## Season 3: for sellers, "What it's really worth" (old Beirut house)

**Final running order (owner, 14 Oct 2026):** the owner dropped "Jeddo's tawleh" (its files stay in posts/2026-11-03-p022-founder-s3e1 but it is off the board and must not be posted). Season 3 is 5 episodes: 1 Forty years (Nov 3), 2 Not begging (Nov 4), 3 They come to you (Nov 5), 4 Something you love (Nov 6), 5 The very first (Nov 7). The list below keeps the original prompt numbers.

**Feeling:** pride and dignity. Your things carry stories, and selling shouldn't feel like losing. The arc: memory → story → dignity → reversal → pride → call to action.

**Character image:** the owner's "me 3" character in Flow: cream linen shirt, thin gold chain, round sunglasses. Every prompt adds "no bookshelves, no books, no desk" because the portrait has bookshelves behind him.

**What varies per episode (owner's ask, 14 Oct):** a different object in his hands or a different position, and the light moves through the day across the season (afternoon in ep. 1 → sunset in ep. 6). The house stays the same: a tall triple-arched window, pale stone walls, patterned floor tiles.

1. **S3E1 "Jeddo's tawleh"** (afternoon; holds a closed vintage wooden backgammon board with mother-of-pearl inlay): "In every Lebanese home, something is waiting. Jeddo's tawleh. Teta's ring. It's worth more than you think." Starts looking down at the board, raises his eyes at 2.5 s. Replaced the camera version because the owner felt we use cameras too much: keep the camera out of Season 3. *Edit:* warm memory flashes of the tawleh and a ring, then bids climbing on the board.
2. **S3E2 "Forty years"** (afternoon; a vintage watch in his open palm, wrists bare): "This watch has a story. Forty years on one wrist. Don't let a lowball offer write the ending." Closes his hand around it and looks up at 4.8 s. *Edit:* a 1985 → 2026 counter, a lowball message struck out.
3. **S3E3 "Not begging"** (late afternoon; seated on a wooden chair, leaning forward, medium close-up): "I know things are hard. But selling isn't begging. You're not desperate. Let them bid." Head shake at 4.5 s, sits up at 6.3 s. *Edit:* lowball DMs crumble, then LET THEM BID.
4. **S3E4 "They come to you"** (late afternoon; starts looking out the window, turns at 1 s): "For years, you chased buyers. Answered every message. Dropped your price. Now… they come to you." Smile at 6 s. *Edit:* his chat bubbles to buyers flip around, and bidders come to him.
5. **S3E5 "Something you love"** (golden hour; holds a brass Arabic coffee pot): "Selling something you love shouldn't feel like losing. When people compete for it… you walk away proud." Looks at the pot at 3.5 s, proud smile at 5.8 s. *Edit:* bids climbing until SOLD to the 9th bidder.
6. **S3E6 "The very first"** (sunset; seated on the window ledge, medium-wide): "The first HyperBidz auctions need great items. Yours could open the very first one. Send us a message." Points at 3.1 s, nods at 6 s. *Edit:* "Be one of the first sellers"; caption CTA: DM us "SELLER".

**Props:** see VIDEO_PROMPTS.md "Props in hand". The prop stays still in the same grip for the whole clip; the actions are on the head and face only.

Never use "last price?" (or "akher se3er") in any lowball message: too close to the banned slogan.

## Owner's voice (from 14 Oct 2026)

Every founder episode uses the owner's own voice: Higgsfield voice element "Rodolph" (`854d5761-a599-4fc1-9f5b-b1f61cc1632f`, voice_type `element`), about 1 credit per 8-second clip. Workflow:
1. Edit the episode as usual from the raw Veo clip.
2. Put the raw clip in `raw/` in this repo, import it into Higgsfield with `media_import_url` through jsDelivr (`https://cdn.jsdelivr.net/gh/rodolph30/hyperbidz-social@<commit>/raw/<file>`; raw.githubusercontent serves mp4 as octet-stream and is refused), then run `voice_change` on it.
3. `tools/voice/make_bed.py` splits the finished episode into a voice-free bed (`voice/<name>.bed.wav` + `.json`).
4. In the Higgsfield sandbox, `tools/voice/mix_voice.py` puts the new voice on the bed under the untouched video. Run it with stdin from /dev/null inside loops (ffmpeg eats stdin).
5. Bring the result into Higgsfield by serving the sandbox folder (`python3 -m http.server 8000`) and calling `media_import_url` on `https://8000-<E2B_SANDBOX_ID>.e2b.app/<file>`. Use the Higgsfield CDN URL as the post's media URL. This workspace cannot download from Higgsfield.

## Season 4: cars ("the founder's garage")

**Character (owner, 14 Oct 2026):** classy entrepreneur, the owner of the app. A tailored navy two-piece suit, a crisp white shirt open at the collar with no tie, a thin gold chain, the same round black sunglasses, no watch or rings. Flow character info: the host of a private car collection, refined, calm, quietly powerful. The owner rejected a leather-jacket "car guy" look: keep this season classy.

**Place:** a dark private garage at night, one classic car under a single spotlight, a polished concrete floor. Cars never show badges, logos or license plates. Later episodes can move: leaning on the car, behind the wheel at night, a rooftop parking deck over Beirut.

1. **S4E1 "Fought over":** "A car like this doesn't get sold. It gets fought over. On HyperBidz, it goes live." Left hand rests on the roof the whole time; glance at the car at 3 s; half-smile at 5.5 s; slow push-in. *Edit:* night grade, a light sweep on the body, bids on a rev-counter needle with engine revs, a LIVE badge, held last shot.
**Rethink (owner, 14 Oct 2026):** the owner called the first scenes "stereotype, no creativity, poor in context" and asked for twists. Season 4 is now **"The Lebanese car deal"**: each episode drops him (navy suit) into a real Lebanese car-buying ritual; it opens as one thing and turns into another halfway, then lands on the auction. "Fought over" (garage) is on the board as made; the owner decides whether to keep it.

1. **"Not a crime movie"** (empty gas station at midnight): "Midnight. A gas station. Cash in an envelope… No, this isn't a crime movie. It's how we sell cars in Lebanon." Amused smile + head shake at 3.4 s. *Edit:* crime-thriller grade and title card, record scratch + freeze on the twist, flip to brand colours.
2. **"Forty bidders disagree"** (old mechanic's workshop, car on a lift): "I'm sorry. Your mechanic says it's only worth three thousand. Forty bidders disagree." Doctor tone, half-smile at 5.3 s. *Edit:* tight crop on his face + heart-monitor beeps, pull back to reveal the workshop on the twist, the flatline turns into a climbing bid line, 40 bidders.
3. **"Grandma drove it to church"** (used-car lot at dusk): dealer pitch "One owner. Never crashed. Grandma drove it to church." → "Sure… or let real bids tell the truth." *Edit:* a "100% TRUE" stamp cracks.
4. **"Service?"** (driver's seat of an old cream Beirut taxi): "Service? Hamra? Verdun?" → "Just kidding. This old taxi goes live… and collectors are already fighting for it." *Edit:* taxi meter → bid counter.
5. **"Three generations"** (classic white wedding car with flowers, old stone church): "This car drove three generations of brides to the church… and tonight, three generations of collectors will bid for it." *Edit:* zaffe drums.
6. **"Never sell"** (snowy road to Faraya, Sunday): "Everyone in Lebanon has a car they'll never sell… until they see what it's worth. The first car auctions are coming."

### Season 4 as made (14 Oct 2026)

The owner generated these clips; all seven are on the board as `waiting`, in his own voice, one a day from 9 to 15 Nov (10:00 Beirut). The planned eps 3–6 above ("Grandma drove it to church", "Service?", "Three generations", "Never sell") were replaced by what he made.

| Ep | Post | Title | Where | What the edit does |
|---|---|---|---|---|
| 1 | p029 | Not a crime movie | gas station, midnight | Thriller (crime grade, letterbox, "00:14 · DORA HIGHWAY", unknown-number texts) → record scratch, freeze, PLOT TWIST stamp → clean live auction card and bids. Pump sign blurred. |
| 2 | p030 | Forty bidders disagree | mechanic | Doctor's bad news: clinic grade, ECG, diagnosis card "$3,000", flatline → jolt → pull back, 40 bidders, bid line to $7,400. Plate (masked around his head) and badge blurred. |
| 3 | p031 | Auction it once | rooftop, dusk | 100 missed calls, 1,000 lowballs flood in, shake → one wave, ONE LIVE AUCTION, SOLD $38,000. |
| 4 | p028 | Fought over | private garage | (the original opener) rev-counter gauge, LIVE badge. |
| 5 | p032 | Lights on | dark warehouse | Darkness → headlights clack on with flares; search "0 results" → private invitation, one night only, Remind me tapped. |
| 6 | p033 | Drove it home | Corniche, blue hour | 23 bidders → 22 fall away, one drove it home $41,500 → NEXT CAR AUCTION · SOON → YOU + crown. |
| 7 | p034 | You just won (finale) | Raouché, golden hour | 3 · 2 · 1 countdown, gavel strike on "Sold", SOLD stamp, confetti, "You won your first car" notification. Hubcap emblem tracked and blurred. |

Edit scripts: `tools/founder/s4gas_edit.py`, `s4mech_edit.py`, `s4roof_edit.py`, `s4lights_edit.py`, `s4drive_edit.py`, `s4final_edit.py`, shared pieces in `s4_common.py` (looks, letterbox, grain, `blur_unless` for plates behind a moving head, `zcrop`, `tone`). `remux.py` swaps in rebuilt audio without re-rendering; `peek.py` / `cover.py` render single frames.

Sound rule kept: nothing loud under key words (moved the rooftop whoosh off "Auction", nothing under "lowballs"/"once"; the finale's gavel crack is tamed so the voice sits at the usual level).

## Season 5: watches = the HyperBidz Vault (made 14 Oct 2026)

**Look:** the owner's Vault design canvas (https://claude.ai/artifact/QG4bob3hsS82xDNVoEiGFR): black stage `#06070B`, a lit gradient edge (`#2F7BFF → #7C5CFF`, border `#6D4DFF`, blue-violet glow), the Z mark as a members' seal (black disc, `#6D4DFF` ring, Z in `#5C95FF → #A08BFF`), Space Mono labels in `#B9A8FF`, lot card with Place Bid / NEXT, TOP BID and YOU chips, the Won card (`#5B3BE8 → #3A22B8 → #160C46`), Join the Vault in the brand gradient. Kit: `tools/founder/s5_common.py` (Vault grade, `lit_edge`, `seal`, `lot_card`, `bid_chip`, `timer_chip`, `won_panel`/`won_strip`, `vault_end_card`, `VaultMix` with a vault-door end sound, watch ticks, lock, chime). Never show a membership price: the design marks it as an example.

**Character:** black overshirt, white tee, thin gold chain, round sunglasses (owner made the clips himself).

| Ep | Post | Title | Clip | Edit |
|---|---|---|---|---|
| 1 | p035 | Worth the chase | two clips with the same line, cut together (counter → glass case → close-up) | cold open with the seal, timer + TOP BID chips chasing, lit edge on the close-up, YOU lead, hammer falls |
| 2 | p036 | Your move | boutique, seated | frosted doors + BY INVITATION ONLY → lock opens → Place Bid → You're leading → seal |
| 3 | p037 | Want it | boutique ("knowing you want it") | retail tag vs the Watch heart (41 others want it) → Vault lot card, FROM THE VAULT |
| 4 | p038 | How you got it | private showroom | ticking dial, heartbeat edge on "Mmm", spec card flips into provenance |
| 5 | p039 | You know what to do (finale) | hotel entrance, night | Vault profile noticed → last-second win → seal → Join the Vault tapped |

Slots 16–20 Nov, 10:00 Beirut, all `waiting` on the board.

## Season 6: bags, "rooftop nights" (planned 14 Oct 2026)

**Owner's brief:** Seasons 1 and 2 are his favourites because they are cool and the ambiance is nice; Season 6 should have that vibe ("I wanna be vibing"). Audience: mainly women.

**Character:** ivory short-sleeve knit shirt with an open camp collar, relaxed black tailored trousers, thin gold chain, the same round black sunglasses. Relaxed, warm, playful; the host of Beirut's coolest rooftop.

**Place (same text every episode; only the time of day and the bag change):** a seaside rooftop lounge in Beirut, sunset in ep. 1 moving to deep night in ep. 6. String lights, blurred city lights and the sea, a thin violet light line along a low glass railing. One handbag rests on a white stone ledge beside him; he never touches it (props rule). No music in Veo: the groove is added in the edit, so the voice swap stays clean.

| Ep | Title | Bag | Line |
|---|---|---|---|
| 1 | The one that got away | small caramel shoulder bag | "Everyone has that one bag they still think about. The one that got away. On HyperBidz… it comes back." |
| 2 | That bag | cream tote | "That bag you never carry anymore? Someone in Beirut is waiting for exactly that one. Let them bid." |
| 3 | Not full price | glossy black mini top-handle | "Why pay boutique price for the bag everyone has? Bid on the one nobody else has. For less." |
| 4 | Girls' night | red clutch | "Girls' night. Dinner at nine, auction at eleven. Ten seconds left… and your best friend bids against you." |
| 5 | Its next story | vintage tan bucket bag | "This bag has been to weddings, Faraya weekends and three first dates. Now it's ready for its next story." |
| 6 | Bid like you mean it (finale) | pistachio mini bag | "The first bags go live soon. Set your reminder, call your girls… and bid like you mean it." |

**Edit vibe:** warm night grade with soft bokeh and light leaks, a slow deep-house groove under the voice (pads and soft kicks, ducked under every word), pop-ups that pulse gently with the beat, held last shot, end card.

### Season 6 as made (14 Oct 2026)

The owner made all six clips from the prompts above (his character wears a navy oversized tee and navy trousers; the light runs sunset → dusk → blue hour). Owner's note on the edit: "keep the motions classy". All six are on the board as `waiting`, 21–26 Nov, 10:00 Beirut (p040–p045).

Kit: `tools/founder/s6_common.py`: warm `night_grade` with a soft bloom, a slow `light_leak`, frosted `shield`/`panel` cards with hairline borders, champagne mono `tag`s, `hairline_ring`, frosted `captions`, `blur_mark` for embossed logo marks on the bags (episodes 1, 2, 4 and 6), a deep-house `groove` (112 BPM, soft kick, off-beat hats, Rhodes stabs in A minor, sub, gentle pump) ducked under the voice by `GrooveMix`, and an `end_card` on the blurred last frame with drifting bokeh. Motion rule for this season: fades and small rises only; no stamps, bounces, shakes or bursts.

After the owner's note that the E6 ending looked blurry, all six now end on `end_card2` instead: a crisp series gradient with bokeh, the Z mark, the episode line, the wordmark and a Follow pill, reached with a 0.5 s crossfade. The voiced audio was kept (`tools/founder/s6_reend.py`, revision 2 on the board).

## Season 7: "The Envelope" (planned 14 Oct 2026)

**Owner's brief:** set in the HyperBidz HQ office ambience. Create a problem and solve it, or leave people with questions they can't answer; play on psychology; viral, meaningful and hooky. For E1 he asked for "short clips… ecstatic, real, and hooky".

**The hook:** a sealed envelope and a watch in a small glass box sit on his desk. The envelope holds the price he thinks this watch will sell for. Viewers guess in the comments. The envelope stays sealed until launch night, when the first live HyperBidz auction opens it. The payoff is honest: there is no fake sale before launch.

**Place (same every episode):** an office at night, with a dark wall showing only a glowing blue-violet Z (no letters; the wordmark is added in the edit), violet light strips, a shelf with warm LEDs, plants and plain book spines, and a black desk with a closed plain silver laptop (no logo). The envelope (cream, plain dark-violet wax seal) and the glass watch box lie flat in front of him; his hands rest beside them and never pick them up. Black tee, round sunglasses.

| Ep | Title | Line |
|---|---|---|
| 1 | The envelope | "Okay. I sealed a number in this envelope. It's what this watch will sell for. Yalla… guess it." |
| 2 | What's it worth? | "What's your car worth? Not what you paid. Not what you want. What someone would actually pay. You don't know." |
| 3 | Who decides? | "Who decides what something's worth? You? A dealer? Your cousin who 'knows a guy'? No. The buyers do. All at once." |
| 4 | The $1 start | "Why would I start this watch at one dollar? Because the price isn't where you start. It's where they stop." |
| 5 | The last three seconds | "Most auctions are decided in the last three seconds. That's when people finally admit what something's worth to them." |
| 6 | Same watch | "Notice something? You all guessed a different price for the same watch. That's why a fixed price is always wrong." (the edit shows real guesses from the E1 comments) |
| 7 | Launch night | "This envelope stays sealed until launch night. The first HyperBidz auction opens it. Will you be right?" |

**Edit:** a typed question in the first second, a "Part N/7" tag, and a violet seal on the envelope that glows a little brighter each episode. Held last shot with a push-in, the owner's voice, an end card in the series style.

**Open decision (owner):** whether the closest guess wins something, for example first access on launch night.

### Season 7 as made

**E1 "The envelope"** (p046, 27 Nov, `waiting`). The owner's line came out as "Okay, I sealed a number in this envelope. It's what this watch will sell for. I want you to… guess it." The last 0.2 s of the clip (hands lifting) is cut, and the hold freezes at 7.8 s.

Kit: `tools/founder/s7_common.py`:
- **Grade and light:** `hq_grade`, a cool-violet grade that keeps the warm shelf LEDs. `z_glow` flares the wall Z by screen-blending its own blue-violet pixels. `seal_glow` lights the wax seal (base 0.55 in E1; raise it each episode).
- **Overlays:**
  - `typed_lines` for typed hooks with a violet cursor
  - `number_card`: a scrambling amount, then a redaction bar and the SEALED · OPENS LAUNCH NIGHT label
  - `brackets`: focus corners
  - `qmarks`: bobbing $ ? ? ?
  - `composer`: an Instagram-style "Your guess: $" field
  - `part_tag`
  - `pop`: a playful overshoot (this season is fun, unlike S6's classy rule)
- **Sound:** `sneaky`, a 100 BPM pizzicato (Karplus-Strong) groove in D minor with a G#, clock tick-tocks, a soft kick and snaps. `HQMix` ends on a pluck arpeggio and a D major chord.
- **End card:** `end_card7`, a crisp HQ end card: dark wall gradient, violet strips, the envelope icon with a glowing seal, THE ENVELOPE · SEASON 7, the lines, the wordmark and the Follow pill. A 0.45 s crossfade leads into it.

**E2 "What's it worth?"** (p047, 28 Nov, `waiting`). The line came out exactly as written. The hands stayed still from the first frame to the last, so the whole 8 s is used. The seal glows at base 0.62. The end card reads "You don't know. / Not yet."
