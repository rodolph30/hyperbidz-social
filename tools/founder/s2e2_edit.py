"""Season 2 Ep. 2 'Full price?': a swinging FULL PRICE $1,200 shop tag, then the same item LIVE on HyperBidz
with the bid climbing to $540, a 3-2-1 countdown on 'if you're there', SOLD $540. End card 'Be there when it happens.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.20, 1.70, ["Why pay [full price?]"]), (1.90, 3.55, ["On HyperBidz,", "the [same thing]…"]),
        (3.60, 5.60, ["can go for", "[way less.]"]), (5.80, 7.70, ["…if you're [there]", "when it happens."])]
TAG_AT, Q_AT, PARK, LIVE_AT, EQ_AT = 0.3, 1.0, 1.95, 2.05, 3.1
BIDS = [(3.70, 120), (3.95, 190), (4.20, 260), (4.45, 330), (4.70, 410), (4.95, 480), (5.20, 540)]
TICKS = [(5.85, 3), (6.05, 2), (6.25, 1)]
SOLD = 6.45
PIV_Y, L = -100, 300                 # pendulum pivot (off screen) and string length to the tag's hole
TAG_X, CARD_X, EQ_X, ROW_Y = 255, 735, 465, 345
VIOLET = (167, 139, 250)

def paste_clip(base, layer, x, y, alpha=1.0):
    """alpha-composite layer with its top-left at (x, y), cropping whatever falls off the frame."""
    x, y = int(round(x)), int(round(y)); x0, y0 = max(0, -x), max(0, -y)
    x1, y1 = min(layer.width, base.width - x), min(layer.height, base.height - y)
    if x1 <= x0 or y1 <= y0 or alpha <= 0.003: return
    part = layer.crop((x0, y0, x1, y1))
    if alpha < 0.999: a = part.getchannel("A").point(lambda v: int(v * alpha)); part.putalpha(a)
    base.alpha_composite(part, (x + x0, y + y0))

def make_tag():
    w, h = 380, 250; t = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=(246, 240, 228, 255), outline=(214, 204, 186, 255), width=3)
    d.ellipse((w / 2 - 13, 21, w / 2 + 13, 47), fill=(0, 0, 0, 0)); d.ellipse((w / 2 - 13, 21, w / 2 + 13, 47), outline=(200, 190, 172, 255), width=3)
    a = R.text_layer("FULL PRICE", R.font(26, mono=True), (96, 90, 84), tracking=4); t.alpha_composite(a, ((w - a.width) // 2, 62))
    b = R.text_layer("$1,200", R.font(92, 700), (24, 24, 30)); t.alpha_composite(b, ((w - b.width) // 2, 92))
    c = R.text_layer("in store", R.font(28, 500), (120, 112, 104)); t.alpha_composite(c, ((w - c.width) // 2, 196))
    cv = Image.new("RGBA", (600, 600), (0, 0, 0, 0)); cv.alpha_composite(t, (300 - w // 2, 300 - 34))   # hole at the canvas centre
    return cv, 34, h
TAG, HOLE, TAG_H = make_tag()
TAG_CY = TAG_H / 2 - HOLE               # tag centre below the hole

def live_card(v, tick=None, bump=1.0):
    w, h = 440, 232; im = M.glass(w, h, 32, fill=(16, 16, 30, 232), border=(*VIOLET, 210)); d = ImageDraw.Draw(im)
    d.ellipse((30, 30, 50, 50), fill=(*VIOLET, 255))
    hd = "LIVE" if tick is None else f"LIVE  ·  00:0{tick}"
    im.alpha_composite(R.text_layer(hd, R.font(26, mono=True), WHITE if tick is None else (255, 236, 160), tracking=4), (62, 24))
    val = R.text_layer(f"${int(v)}", R.font(88, 700), WHITE)
    if bump > 1.001: val = val.resize((int(val.width * bump), int(val.height * bump)), Image.LANCZOS)
    im.alpha_composite(val, (30, 66 - int((val.height - val.height / bump) / 2)))
    im.alpha_composite(R.text_layer("current bid", R.font(28, 500), (190, 195, 215)), (32, 176))
    return im

def eq_sign():
    im = Image.new("RGBA", (64, 52), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 8, 60, 20), radius=6, fill=(*VIOLET, 255)); d.rounded_rectangle((4, 32, 60, 44), radius=6, fill=(*VIOLET, 255)); return im
EQ = eq_sign()
Q = M.stamp_text("?", 130)

def sold_pill():
    a = R.text_layer("SOLD  ·  $540", R.font(70, 700), WHITE); b = R.text_layer("$660 under full price", R.font(36, 500), (235, 238, 255))
    w, h = max(a.width, b.width) + 100, a.height + b.height + 46
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=38, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(a, ((w - a.width) // 2, 18)); im.alpha_composite(b, ((w - b.width) // 2, 24 + a.height)); return im
SOLD_P = sold_pill()

def bid_value(t):
    done = [(a, v) for a, v in BIDS if t >= a]
    if not done: return 60, None
    at, v = done[-1]; prev = ([60] + [x for _, x in BIDS])[len(done) - 1]
    return prev + (v - prev) * R.ease_out((t - at) / 0.18), at

def draw_tag(im, t):
    """hanging + swinging, then parks as the left cell of the comparison row."""
    k = (t - TAG_AT) / 0.55; drop = (1 - R.stamp(k)) * 420 if k < 1 else 0
    th = 11 * np.exp(-max(0, t - TAG_AT) * 1.3) * np.cos(2 * np.pi * 0.95 * max(0, t - TAG_AT) + 0.6)
    hx, hy, s = W / 2 + L * np.sin(np.radians(th)), PIV_Y + L * np.cos(np.radians(th)) - drop, 1.0
    p = R.ease_out((t - PARK) / 0.42) if t >= PARK else 0.0
    if p > 0:   # fly to the parked spot: no string, upright, smaller
        s = 1 - 0.25 * p; th *= (1 - p)
        px, py = TAG_X, ROW_Y - TAG_CY * s
        hx, hy = hx + (px - hx) * p, hy + (py - hy) * p
    a = R.clamp(k * 4) * (1 - R.clamp((t - SOLD) / 0.2))
    if p < 1:   # the string up to the hole, fading as the tag parks
        sl = Image.new("RGBA", (W, 700), (0, 0, 0, 0))
        ImageDraw.Draw(sl).line([(W / 2, PIV_Y), (hx, hy - 12 * s)], fill=(236, 230, 218, int(210 * a * (1 - p) ** 2)), width=3)
        im.alpha_composite(sl)
    tg = TAG.rotate(th, resample=Image.BICUBIC) if abs(th) > 0.05 else TAG
    if s != 1.0: tg = tg.resize((int(tg.width * s), int(tg.height * s)), Image.LANCZOS)
    paste_clip(im, tg, hx - tg.width / 2, hy - tg.height / 2, a)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Be there when", "it happens."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, True, 600, 150); M.scrim(im, False, 650, 150)
    if TAG_AT <= t < SOLD + 0.25: draw_tag(im, t)
    if Q_AT <= t < PARK + 0.1:
        k = (t - Q_AT) / 0.3; a = R.clamp(k * 3) * (1 - R.clamp((t - (PARK - 0.15)) / 0.2))
        R.paste_center(im, Q, W / 2 + 255, 250 + 6 * np.sin((t - Q_AT) * 9), a, 0.7 + 0.3 * R.stamp(k) if k < 1 else 1.0)
    if LIVE_AT <= t < SOLD + 0.25:
        k = (t - LIVE_AT) / 0.38; a = R.clamp(k * 3) * (1 - R.clamp((t - SOLD) / 0.2))
        v, at = bid_value(t); bump = 1 + 0.12 * (1 - R.clamp((t - at) / 0.2)) if at else 1.0
        tick = [n for tt, n in TICKS if t >= tt]; tick = tick[-1] if tick else None
        x = CARD_X + (1 - R.stamp(k)) * 360 if k < 1 else CARD_X
        card = live_card(v, tick, bump)
        if tick is not None and t - [tt for tt, n in TICKS if t >= tt][-1] < 0.1: card = card.resize((int(card.width * 1.03), int(card.height * 1.03)), Image.LANCZOS)
        R.paste_center(im, card, x, ROW_Y, a)
    if EQ_AT <= t < SOLD + 0.2:
        k = (t - EQ_AT) / 0.3; R.paste_center(im, EQ, EQ_X, ROW_Y, R.clamp(k * 3) * (1 - R.clamp((t - SOLD) / 0.2)), 0.6 + 0.4 * R.stamp(k) if k < 1 else 1.0)
        sparkle_burst(im, t, EQ_AT, EQ_X, ROW_Y, ((-40, -70, 18), (45, 60, 14), (50, -55, 14)))
    if t >= SOLD:
        s = (t - SOLD) / 0.35; R.paste_center(im, SOLD_P, W / 2, ROW_Y, R.clamp(s * 3), 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, SOLD, W / 2, ROW_Y, ((-360, -50, 34), (350, -70, 26), (-300, 60, 18), (330, 55, 34)))
    draw_caps(im, t, CAPS)
    if SOLD <= t < SOLD + 0.08: im = M.flash(im, 0.3)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((123.5, .35), (185, .25), (246.9, .2), (370, .08)))
        mx.whoosh(TAG_AT, 0.3, 0.18); mx.ping(TAG_AT + 0.3, 660, 0.1)                    # tag drops in
        mx.ping(Q_AT, 990, 0.12); mx.ping(Q_AT + 0.09, 880, 0.08)                         # "?"
        mx.whoosh(PARK, 0.4, 0.2); mx.ping(LIVE_AT + 0.2, 1318.5, 0.16); mx.shimmer(LIVE_AT + 0.22, 1568, 0.04)
        mx.ping(EQ_AT, 1046.5, 0.1)
        for i, (at, v) in enumerate(BIDS): mx.ping(at, 1046.5 * (2 ** (i * 2 / 12)), 0.12)  # rising with the bids
        for at, n in TICKS:                                                                 # countdown clicks
            y = mx.tt(0.05); mx.fadd(np.sin(2 * np.pi * 2400 * y) * np.exp(-y * 110), at, 0.35); mx.ping(at, 740, 0.06)
        mx.thud(SOLD, 0.55); mx.shimmer(SOLD + 0.02, 1318.5, 0.12)
        mx.write("s2e2_audio.wav")
    render(frame, TOTAL, "s2e2_audio.wav", OUT)
