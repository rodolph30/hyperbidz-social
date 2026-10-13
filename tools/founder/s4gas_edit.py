"""Season 4 'Not a crime movie' (gas station). It opens like a thriller: crushed green crime grade, letterbox bars,
film grain, a flickering canopy light, '00:14 · DORA HIGHWAY' typed in the top bar and texts from an unknown number
('I'm at the pump. Silver car.' / 'Bring cash. Only cash.' / 'Come alone.') over a drone and a heartbeat.
After 'to buy a car?' a record scratch freezes the frame, it drains to grey and a red stamp slams: NOT A CRIME MOVIE.
Then a violet ripple sweeps it away, the bars retract and the station turns clean and bright on 'We can do better.'
'See it': a live auction card for the silver sedan. 'Bid on it live': bids tick in, 18 bidders, $5,100.
Last shot held with a slow push-in. End card 'No more midnight deals.' Pump sign and car badge blurred."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s4_common as S

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, RED = S.VIOLET, S.RED
FR = decode()
BLURS = [((178, 730, 366, 799), 12), ((0, 796, 58, 904), 9), ((0, 1388, 44, 1462), 8)]   # Arabic pump sign, pump label, grille badge
for fr in FR:
    for box, r in BLURS: S.blur_region(fr, box, r)

CAPS = [(0.05, 1.15, ["Meeting a [stranger]…"]), (1.15, 2.30, ["at a gas station", "at [midnight?]"]), (2.50, 3.45, ["To buy a [car?]"]),
        (4.05, 5.00, ["We can do [better.]"]), (5.20, 6.10, ["[See it.]"]), (6.15, 9.20, ["Bid on it [live.]"])]
FREEZE, TWIST = 3.45, 4.0
MSGS = [(0.45, "UNKNOWN NUMBER", "I'm at the pump. Silver car.", 420, 300), (1.35, None, "Bring cash. Only cash.", 640, 405), (2.30, None, "Come alone.", 470, 492)]
FLICK = [(0.62, 0.07), (0.74, 0.05), (1.92, 0.10), (2.88, 0.06), (3.02, 0.05)]
CARD_IN, BIDS_AT, DONE = 5.30, [6.25, 6.55, 6.85], 7.15
BIDS = [("Karim", 4500), ("Rita", 4800), ("Jad", 5100)]

MSG_IM = [S.msg_bubble(h, tx, fill=(40, 44, 40, 236), size=34) for _, h, tx, _, _ in MSGS]
TYPE = "00:14  ·  DORA HIGHWAY"

def stamp():
    sub = R.text_layer("PLOT TWIST", R.font(36, mono=True), RED, tracking=8)
    a = R.text_layer("NOT A", R.font(86, 700), RED); b = R.text_layer("CRIME MOVIE.", R.font(86, 700), RED)
    w = max(a.width, b.width, sub.width) + 90; h = sub.height + a.height + b.height + 84
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w - 5, h - 5), radius=18, fill=(12, 8, 10, 120), outline=RED + (255,), width=9)
    im.alpha_composite(sub, ((w - sub.width) // 2, 34)); im.alpha_composite(a, ((w - a.width) // 2, 40 + sub.height)); im.alpha_composite(b, ((w - b.width) // 2, 28 + sub.height + a.height))
    rng = np.random.default_rng(3); al = np.asarray(im.getchannel("A"), np.float32)      # worn rubber-stamp ink
    holes = (rng.random(al.shape) < 0.10).astype(np.float32); holes = np.asarray(Image.fromarray((holes * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    im.putalpha(Image.fromarray(np.clip(al * (1 - 0.6 * holes * (al > 200)) * 0.96, 0, 255).astype(np.uint8)))
    return im.rotate(7, resample=Image.BICUBIC, expand=True)
STAMP = stamp()

def card(price, bidders, watching):
    w, h = 660, 236; im = M.glass(w, h, 34, fill=(14, 14, 24, 228), border=(*VIOLET, 200)); d = ImageDraw.Draw(im)
    d.ellipse((34, 34, 54, 54), fill=RED + (255,)); hd = R.text_layer("LIVE AUCTION", R.font(24, mono=True), (235, 238, 255), tracking=4); im.alpha_composite(hd, (66, 28))
    wt = R.text_layer(f"{watching} watching", R.font(24, mono=True), (190, 194, 210), tracking=1); im.alpha_composite(wt, (w - 34 - wt.width, 28))
    nm = R.text_layer("Silver sedan  ·  2004", R.font(44, 700), WHITE); im.alpha_composite(nm, (34, 70))
    lb = R.text_layer(f"Current bid  ·  {bidders} bidders" if bidders else "Bidding opens now", R.font(26, 500), (190, 194, 210)); im.alpha_composite(lb, (34, 160))
    pr = R.text_layer(f"${price:,}", R.font(64, 700), WHITE); im.alpha_composite(pr, (w - 34 - pr.width, 136))
    return im

def chip(name, amt):
    a = R.text_layer(name, R.font(28, 600), WHITE); b = R.text_layer(f"${amt:,}", R.font(30, 700), WHITE)
    w, h = a.width + b.width + 66, 58
    im = M.glass(w, h, h // 2, fill=(36, 28, 76, 236), border=(*VIOLET, 230))
    im.alpha_composite(a, (22, (h - a.height) // 2 - 2)); im.alpha_composite(b, (w - 22 - b.width, (h - b.height) // 2 - 2)); return im
CHIPS = [chip(n, a) for n, a in BIDS]

def grey(im, k):
    if k <= 0: return im
    g = im.convert("L").convert("RGBA"); return Image.blend(im, g, k)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["No more", "midnight deals."], END)
    ft = FREEZE if FREEZE <= t < TWIST else min(t, SHOT - 0.01)
    fr = FR[min(len(FR) - 1, int(ft * FPS))]
    if t < TWIST:
        im = S.look(fr, "crime")
        dip = max([1 - 0.45 * np.sin(np.pi * R.clamp((t - a) / d)) for a, d in FLICK if a <= t < a + d] + [1.0])   # canopy light flickers
        if dip < 1: im = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), im, dip)
        im = S.grain(im, 9, int(ft * FPS))
        if t >= FREEZE: im = grey(im, R.clamp((t - FREEZE) / 0.12) * 0.9)
    else:
        k = R.clamp((t - TWIST) / 0.35)
        im = S.look(fr, "night") if k >= 1 else Image.blend(S.grain(S.look(fr, "crime"), 9, int(ft * FPS)), S.look(fr, "night"), R.ease_out(k))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (560, 640))
    # --- the thriller ---
    bars = R.ease_out(t / 0.35) if t < TWIST else 1 - R.ease_out((t - TWIST) / 0.35)
    sweep = R.clamp((t - TWIST) / 0.45) if t >= TWIST else 0
    for (at, h, tx, x, y), mi in zip(MSGS, MSG_IM):
        if t < at or sweep >= 1: continue
        k = (t - at) / 0.25; side = -1 if x < 540 else 1
        jit = 3 * np.sin(t * 40 + x) * (1 - R.clamp((t - at) / 0.4))                      # buzzes in
        R.paste_center(im, mi, x + jit + side * sweep ** 2 * 800, y - sweep * 80, R.clamp(k * 3) * (1 - sweep), 0.86 + 0.14 * R.stamp(k) if k < 1 else 1.0)
    S.letterbox(im, bars)
    if bars > 0.5 and t < TWIST:
        n = int(len(TYPE) * R.clamp((t - 0.2) / 1.0)); cur = "_" if (t * 3) % 1 < 0.6 else " "
        tl = R.text_layer(TYPE[:n] + cur, R.font(30, mono=True), (225, 230, 220), tracking=4); im.alpha_composite(tl, (60, int(105 - tl.height / 2)))
    if FREEZE <= t < TWIST + 0.5:
        s = (t - FREEZE - 0.06) / 0.28; fly = R.clamp((t - TWIST) / 0.22)                    # blown away by the ripple
        R.paste_center(im, STAMP, W / 2, 940, R.clamp(s * 3) * (1 - fly), (1.9 - 0.9 * R.stamp(s) if s < 1 else 1.0) + 0.5 * fly)
    if TWIST <= t < TWIST + 0.7:
        for j in range(2): kk = R.clamp((t - TWIST - 0.1 * j) / 0.6); S.ring(im, 560, 700, 80 + 800 * R.ease_out(kk), (1 - kk) * 0.8, VIOLET, 8)
    # --- the HyperBidz way ---
    if t >= CARD_IN:
        k = R.ease_out((t - CARD_IN) / 0.4); nb = sum(t >= b for b in BIDS_AT)
        price = 4200 if nb == 0 else BIDS[nb - 1][1]; bidders = 0 if nb == 0 else (9, 14, 18)[nb - 1]
        c = card(price, bidders, 142 + int((t - CARD_IN) * 37))
        pop = 1.0
        if nb: pop = 1 + 0.05 * (1 - R.clamp((t - BIDS_AT[nb - 1]) / 0.2))
        R.paste_center(im, c, W / 2, 360 + (1 - k) * -60, R.clamp((t - CARD_IN) / 0.2) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), pop)
        for j in range(nb):
            at = BIDS_AT[j]; kk = R.ease_out((t - at) / 0.3); slot = nb - 1 - j
            R.paste_center(im, CHIPS[j], 150 + (1 - kk) * -260, 960 + slot * 70, R.clamp((t - at) / 0.15) * (1 - 0.25 * slot) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)))
    if t >= DONE: sparkle_burst(im, t, DONE, W / 2 + 220, 410, ((-60, -40, 26), (70, -30, 18), (40, 50, 26)))
    draw_caps(im, t, CAPS, y=1640, size=60)
    if TWIST <= t < TWIST + 0.08: im = M.flash(im, 0.35)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

def tone(mx, t0, t1, freqs, g, fade=0.4):
    y = mx.tt(t1 - t0); s = sum(np.sin(2 * np.pi * f * y + i) * a for i, (f, a) in enumerate(freqs))
    env = np.minimum(1, y / fade) * np.minimum(1, (y[-1] - y) / 0.12); mx.fadd(s * env, t0, g)

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, 0.0),))
        S.drone(mx, 0.0, FREEZE + 0.05, 49, 0.16); S.hum(mx, 0.0, FREEZE, 0.035)                   # thriller bed
        for b in (0.25, 1.15, 2.05, 2.95):                                                          # heartbeat
            for o, gg in ((0, 0.30), (0.17, 0.2)): y = mx.tt(0.18); mx.fadd(np.sin(2 * np.pi * 52 * y) * np.exp(-y * 22), b + o, gg)
        for at, *_ in MSGS: y = mx.tt(0.28); mx.fadd(np.sign(np.sin(2 * np.pi * 180 * y)) * (np.sin(2 * np.pi * 9 * y) > 0) * np.exp(-y * 6), at, 0.025)  # phone buzz
        S.scratch(mx, FREEZE, 0.32)
        y = mx.tt(0.5); mx.fadd(np.sin(2 * np.pi * np.cumsum(98 * np.exp(-y * 2.5)) / SR) * np.exp(-y * 3), FREEZE, 0.22)   # tape stop
        mx.thud(FREEZE + 0.08, 0.45)
        mx.whoosh(TWIST - 0.15, 0.45, 0.32); mx.shimmer(TWIST + 0.02, 1174.7, 0.08)
        tone(mx, TWIST, CLIP, ((146.8, .3), (185, .22), (220, .2), (293.7, .1)), 0.05, 0.6)         # D major, bright and calm
        mx.ping(CARD_IN - 0.05, 1318.5, 0.06)
        for i, at in enumerate(BIDS_AT): mx.ping(at + 0.02, 1046.5 * 2 ** (i * 2 / 12), 0.045)
        mx.thud(7.62, 0.35); mx.shimmer(7.64, 1318.5, 0.09)
        mx.write("s4gas_audio.wav")
    render(frame, TOTAL, "s4gas_audio.wav", OUT)
