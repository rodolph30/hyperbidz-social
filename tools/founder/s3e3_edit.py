"""Season 3 Ep. 3 'Not begging': the light tells the story. It opens cool, dim and grey ('I know things are hard'),
the seller's own begging messages sink around him ('Any offer is fine…', 'Please, I need to sell', 'I can go lower')
and dissolve on 'isn't begging'. On 'You're not desperate', as he sits up, golden light floods the room and the last
of them burst into golden dust. On 'let them bid' bids rise like lanterns: LIVE · 12 bids · $310.
End card 'Not begging. Bidding.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
from s3_common import Look, pluck

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.4; END = 3.8; TOTAL = CLIP + END   # last shot held + slow push-in
VIOLET, GOLD = (167, 139, 250), (255, 214, 140)
FR = decode()
LOOK = Look(windows=((230, 260, 110), (540, 260, 80), (850, 260, 110)), key=(540, 860))
CAPS = [(0.40, 1.95, ["I know things are [hard.]"]), (2.35, 4.00, ["But selling", "isn't [begging.]"]),
        (4.75, 6.05, ["You're [not desperate.]"]), (6.20, 9.20, ["[Let them bid.]"])]
BEG = [(2.45, "Any offer is fine…", 245, 360), (2.85, "Please, I need to sell", 835, 450), (3.25, "I can go lower", 235, 560)]
FADE_BEG, BURST, WARM0, WARM1, LANTERN, TOP = 3.55, 4.9, 4.75, 5.9, 6.3, 6.95
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
COOL_VIG = (1 - 0.5 * np.clip((((_xx - 540) / 700) ** 2 + ((_yy - 900) / 1050) ** 2) ** 1.3, 0, 1))[..., None]

def cool(fr):
    a = np.asarray(fr, np.float32); lum = a.mean(-1, keepdims=True)
    a = lum + (a - lum) * 0.45; a = a * np.array([0.90, 0.95, 1.04], np.float32) * 0.86
    return Image.fromarray(np.clip(a * COOL_VIG, 0, 255).astype(np.uint8)).convert("RGBA")

def beg_bubble(text):
    tx = R.text_layer(text, R.font(34, 600), (226, 228, 236)); w, h = tx.width + 52, tx.height + 32
    im = Image.new("RGBA", (w, h + 22), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=24, fill=(70, 74, 88, 225)); d.polygon([(w - 64, h - 2), (w - 24, h - 2), (w - 16, h + 18)], fill=(70, 74, 88, 225))
    im.alpha_composite(tx, (26, 14)); return im
BEG_IM = [beg_bubble(t) for _, t, _, _ in BEG]

rng = np.random.default_rng(11)
DUST = []
for (_, _, x, y), b in zip(BEG, BEG_IM):
    for _ in range(70):
        DUST.append((x + rng.uniform(-b.width / 2, b.width / 2), y + rng.uniform(-b.height / 2, b.height / 2), rng.uniform(-160, 160), rng.uniform(-520, -160), rng.uniform(3, 8)))

def lantern(text):
    tl = R.text_layer(text, R.font(38, 700), (60, 38, 6)); w, h = tl.width + 50, tl.height + 26
    im = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((18, 18, w + 42, h + 42), radius=30, fill=(255, 200, 110, 150)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(16)))
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(255, 226, 160, 250))
    c.alpha_composite(tl, (25, 13)); im.alpha_composite(c, (30, 30)); return im
LANTERNS = [(LANTERN, lantern("+$40"), 230, 520), (LANTERN + 0.18, lantern("+$60"), 860, 600), (LANTERN + 0.36, lantern("+$80"), 170, 760), (LANTERN + 0.54, lantern("+$50"), 900, 820), (LANTERN + 0.72, lantern("+$80"), 280, 950)]

def top_pill():
    b = R.text_layer("LIVE  ·  12 BIDS", R.font(24, mono=True), (235, 238, 255), tracking=3); a = R.text_layer("$310", R.font(70, 700), WHITE)
    w, h = max(a.width, b.width) + 100, a.height + b.height + 40
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=32, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(b, ((w - b.width) // 2, 16)); im.alpha_composite(a, ((w - a.width) // 2, 20 + b.height)); return im
TOP_IM = top_pill()

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Not begging.", "Bidding."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    w = R.ease_out((t - WARM0) / (WARM1 - WARM0)) if t >= WARM0 else 0.0     # the light comes back
    if w <= 0: im = cool(fr)
    elif w >= 1: im = LOOK(fr, t)
    else: im = Image.blend(cool(fr), LOOK(fr, t), w)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.08, (540, 720))
    if 0 < w < 1:                                                          # a wash of sunlight sweeping in
        lay = Image.new("RGBA", (W, H), (255, 214, 150, int(70 * np.sin(np.pi * w)))); im.alpha_composite(lay)
    for (at, txt, x, y), b in zip(BEG, BEG_IM):                             # his own begging, sinking
        if t < at or t >= BURST: continue
        k = (t - at) / 0.35; sink = (t - at) * 22; trem = 2.5 * np.sin(t * 31 + x)
        a = R.clamp(k * 3) * (0.85 if t < FADE_BEG else 0.85 - 0.45 * R.clamp((t - FADE_BEG) / 0.4))
        R.paste_center(im, b, x + trem, y + sink, a)
    if FADE_BEG <= t < BURST:                                               # struck through on "isn't begging"
        d = ImageDraw.Draw(im, "RGBA")
        for (at, txt, x, y), b in zip(BEG, BEG_IM):
            sk = R.clamp((t - FADE_BEG - 0.08 * BEG.index((at, txt, x, y))) / 0.25); yy = y + (t - at) * 22
            if sk > 0: d.line([(x - b.width / 2 + 14, yy), (x - b.width / 2 + 14 + (b.width - 28) * sk, yy - 4)], fill=(*VIOLET, 230), width=6)
    if BURST <= t < BURST + 1.3:                                            # ...and burst into golden dust
        k = t - BURST; d = ImageDraw.Draw(im, "RGBA")
        for x0, y0, vx, vy, r in DUST:
            x = x0 + vx * k; y = y0 + vy * k + 120 * k * k; a = int(230 * max(0, 1 - k / 1.3))
            d.ellipse((x - r, y - r, x + r, y + r), fill=(*GOLD, a))
    for at, ln, x, yt in LANTERNS:                                          # bids rising like lanterns, beside him
        if t < at: continue
        k = (t - at) / 1.25; y = 1550 - (1550 - yt) * R.ease_out(min(1, k)); a = R.clamp((t - at) / 0.2) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3))
        R.paste_center(im, ln, x + 18 * np.sin((t - at) * 2.4 + x), y, a)
    if t >= TOP:
        s = (t - TOP) / 0.32; R.paste_center(im, TOP_IM, W / 2, 210, R.clamp(s * 3), 1.4 - 0.4 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, TOP, W / 2, 210, ((-270, -30, 26), (260, -40, 18), (220, 40, 26)))
    draw_caps(im, t, CAPS, y=1700, size=62)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, .30), (174.6, .18), (220, .16), (293.7, .06)))       # D minor, quiet
        for i, f in enumerate([293.7, 349.2, 220, 261.6]): pluck(mx, 0.3 + i * 1.15, f, 0.05)        # sparse, heavy
        for at, *_ in BEG: y = mx.tt(0.3); mx.fadd(np.sin(2 * np.pi * np.cumsum(420 - 120 * y / 0.3) / SR) * np.exp(-y * 8), at, 0.08)   # sinking
        y = mx.tt(0.25); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 3) * np.exp(-y * 14), FADE_BEG, 0.15)
        mx.whoosh(WARM0 - 0.1, 0.8, 0.22)
        for i, f in enumerate([293.7, 370, 440, 587.3, 740]): pluck(mx, BURST + i * 0.11, f, 0.07, 1.8)    # D major: the light comes back
        mx.shimmer(BURST + 0.05, 1174.7, 0.1)
        for i, (at, _, _, _) in enumerate(LANTERNS): mx.ping(at + 0.1, 880 * 2 ** (i * 2 / 12), 0.06)
        mx.thud(7.45, 0.4); mx.shimmer(7.47, 1318.5, 0.11)
        mx.write("s3e3_audio.wav")
    render(frame, TOTAL, "s3e3_audio.wav", OUT)
