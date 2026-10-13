"""Founder Ep. 5 'How smart people sell': STARTING PRICE $100 set by you, a market gauge climbing to $640,
SOLD with the 6.4x multiplier, end card 'Set the start. Let the market finish.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.25, 1.95, ["You set the", "[starting price.]"]), (2.15, 3.95, ["The [market] sets", "the final one."]),
        (4.45, 5.55, ["That's not luck."]), (5.95, 7.70, ["That's how", "[smart people sell.]"])]
START_AT = 0.9
BIDS = [(2.35, 160), (2.65, 230), (2.95, 310), (3.25, 390), (3.55, 470), (3.85, 560), (4.15, 640)]
SOLD_AT = 6.05
GX, GY0, GY1 = 1005, 1000, 420          # gauge x, bottom y, top y
LO, HI = 100, 640

def start_chip():
    a = R.text_layer("STARTING PRICE", R.font(26, mono=True), (205, 210, 235), tracking=4); b = R.text_layer("$100", R.font(64, 700), WHITE)
    c = R.text_layer("set by you", R.font(30, 500), (190, 195, 215))
    w = max(a.width, b.width, c.width) + 70; h = a.height + b.height + c.height + 50
    im = M.glass(w, h, 28, fill=(20, 22, 32, 225), border=(255, 255, 255, 70))
    im.alpha_composite(a, (35, 18)); im.alpha_composite(b, (35, 22 + a.height)); im.alpha_composite(c, (35, 26 + a.height + b.height)); return im
START = start_chip()

def value_at(t):
    cur = [v for at, v in BIDS if t >= at]
    if not cur: return LO, None
    at = [a for a, v in BIDS if t >= a][-1]; prev = ([LO] + cur)[-2]
    k = R.ease_out((t - at) / 0.22); return prev + (cur[-1] - prev) * k, at

def gauge(im, t, a):
    v, at = value_at(t); frac = (v - LO) / (HI - LO)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.rounded_rectangle((GX - 34, GY1, GX + 34, GY0), radius=34, fill=(16, 16, 30, int(200 * a)), outline=(255, 255, 255, int(70 * a)), width=2)
    top = GY0 - (GY0 - GY1) * max(0.06, frac)
    bar = M.grad(60, int(GY0 - top) + 1); m = Image.new("L", bar.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bar.width - 1, bar.height - 1), radius=30, fill=int(255 * a))
    layer.paste(bar, (GX - 30, int(top)), m)
    im.alpha_composite(layer)
    lab = R.text_layer("MARKET PRICE", R.font(24, mono=True), (205, 210, 235), tracking=4); R.paste_center(im, lab, W - 30 - lab.width / 2, GY1 - 40, a)
    val = R.pill(f"${int(round(v / 5) * 5)}", R.font(48, 700), NAVY, WHITE, pad=(26, 12))
    bump = 1 + 0.12 * (1 - R.clamp((t - at) / 0.2)) if at else 1
    R.paste_center(im, val, GX - 115, top, a, bump)
    for bat, bv in BIDS:  # +$ chips flying into the gauge
        k = (t - bat) / 0.5
        if 0 <= k < 1:
            p = R.pill(f"+${bv - ([LO] + [x for _, x in BIDS])[[x for _, x in BIDS].index(bv)]}", R.font(30, 700), WHITE, (124, 92, 255), pad=(16, 8))
            R.paste_center(im, p, GX - 150 + 110 * R.ease_out(k), top + 120 - 80 * k, (1 - k) ** 0.6)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Set the start.", "Let them bid."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, False, 650, 150); M.scrim(im, True, 300, 90)
    if START_AT <= t < SOLD_AT:
        k = (t - START_AT) / 0.3; a = R.clamp(k * 3) * (0.55 if t >= 2.2 else 1.0)
        R.paste_center(im, START, 50 + START.width / 2, 470, a, 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    if t >= 2.15 and t < SOLD_AT + 0.2:
        a = R.ease_out((t - 2.15) / 0.3) * (1 - R.clamp((t - SOLD_AT) / 0.2)); gauge(im, t, a)
    if t >= SOLD_AT:
        s = (t - SOLD_AT) / 0.35
        sold = R.pill("SOLD  ·  $640", R.font(66, 700), NAVY, WHITE, pad=(48, 24)); R.paste_center(im, sold, W / 2, 300, R.clamp(s * 3), 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0)
        s2 = (t - SOLD_AT - 0.45) / 0.3
        if s2 > 0:
            mult = R.pill("6.4× your starting price", R.font(40, 700), WHITE, (124, 92, 255), pad=(30, 14)); R.paste_center(im, mult, W / 2, 420, R.clamp(s2 * 3), 0.85 + 0.15 * R.stamp(s2) if s2 < 1 else 1.0)
        sparkle_burst(im, t, SOLD_AT, W / 2, 300, ((-300, -40, 34), (290, -60, 26), (-240, 60, 18), (260, 50, 34)))
    draw_caps(im, t, CAPS)
    if SOLD_AT <= t < SOLD_AT + 0.08: im = M.flash(im, 0.3)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END)
        y = mx.tt(0.05); mx.fadd(np.sin(2 * np.pi * 2200 * y) * np.exp(-y * 120), START_AT, 0.3)     # click: you set it
        mx.ping(START_AT + 0.05, 880, 0.12); mx.whoosh(2.05, 0.35, 0.2)
        for i, (at, v) in enumerate(BIDS): mx.ping(at, 1046.5 * (2 ** (i / 12 * 2)), 0.14)          # rising scale with the price
        mx.thud(SOLD_AT, 0.55); mx.shimmer(SOLD_AT + 0.02, 1318.5, 0.11); mx.ping(SOLD_AT + 0.45, 1975.5, 0.12)
        mx.write("ep5_audio.wav")
    render(frame, TOTAL, "ep5_audio.wav", OUT)
