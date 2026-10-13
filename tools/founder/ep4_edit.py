"""Founder Ep. 4 'Pay attention': FOR THE RICH? -> MYTH stamp, ripple from the temple tap,
live-deal chips that only the attentive catch, then SOLD $85 to someone who was watching."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.30, 2.20, ["Auctions were never", "for the [rich.]"]), (2.50, 4.45, ["They're for the people", "who [pay attention.]"]),
        (5.15, 6.40, ["[Most people don't.]"])]
MYTH_AT, TAP, CHIPS_AT, FADE_AT, SOLD_AT = 1.65, 2.95, (3.6, 3.85, 4.1), 5.2, 6.5
TEMPLE = (285, 780)

def label(text, fill=(20, 22, 32, 225), border=(255, 255, 255, 60), size=54, mono=False):
    tl = R.text_layer(text, R.font(size, mono=True) if mono else R.font(size, 700), WHITE, tracking=4 if mono else 0)
    w, h = tl.width + 70, tl.height + 34; im = M.glass(w, h, h // 2, fill=fill, border=border); im.alpha_composite(tl, (35, 17)); return im
RICH = label("Auctions are for the rich?", size=50)
def myth():
    tl = R.text_layer("MYTH", R.font(96, 700), WHITE); w, h = tl.width + 80, tl.height + 36
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=20, fill=255)
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); g.paste(M.grad(w, h), (0, 0), m); im.alpha_composite(g, (20, 20)); im.alpha_composite(tl, (60, 36))
    return im.rotate(-10, resample=Image.BICUBIC, expand=True)
MYTH = myth()

def chip(line1, line2):
    a = R.text_layer(line1, R.font(24, mono=True), (205, 210, 235), tracking=3); b = R.text_layer(line2, R.font(40, 700), WHITE)
    w, h = max(a.width, b.width) + 64, a.height + b.height + 40
    im = M.glass(w, h, 26, fill=(20, 18, 40, 225), border=(167, 139, 250, 220)); im.alpha_composite(a, (32, 18)); im.alpha_composite(b, (32, 24 + a.height)); return im
CHIPS = [chip("● LIVE NOW", "Steel watch · 2 bidders"), chip("ENDS IN", "00:09"), chip("CURRENT BID", "$85")]
CHIP_POS = [(540, 225), (330, 385), (760, 385)]
def sold_pill():
    a = R.text_layer("SOLD  ·  $85", R.font(62, 700), NAVY); b = R.text_layer("to someone who was watching.", R.font(34, 500), (60, 50, 120))
    w, h = max(a.width, b.width) + 90, a.height + b.height + 46; im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=36, fill=(255, 255, 255, 245))
    im.alpha_composite(a, ((w - a.width) // 2, 18)); im.alpha_composite(b, ((w - b.width) // 2, 24 + a.height)); return im
SOLD = sold_pill()

def ripple(im, t):
    k = t - TAP
    if not (0 <= k < 1.0): return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for j in range(3):
        kk = k - 0.15 * j
        if 0 < kk < 0.85:
            r = 30 + 340 * R.ease_out(kk / 0.85); a = int(200 * (1 - kk / 0.85))
            d.ellipse((TEMPLE[0] - r, TEMPLE[1] - r, TEMPLE[0] + r, TEMPLE[1] + r), outline=(167, 139, 250, a), width=6)
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1.5)))

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Be the one", "paying attention."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, False, 650, 150); M.scrim(im, True, 360, 110)
    if 0.35 <= t < 2.6:
        k = (t - 0.35) / 0.3; a = R.clamp(k * 3) * (1 - R.clamp((t - 2.35) / 0.25)); dim = 0.55 if t >= MYTH_AT + 0.1 else 1.0
        R.paste_center(im, RICH, W / 2, 250, a * dim, 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
        if t >= MYTH_AT:
            s = (t - MYTH_AT) / 0.3; R.paste_center(im, MYTH, W / 2 + 120, 270, R.clamp(s * 3) * (1 - R.clamp((t - 2.35) / 0.25)), 1.7 - 0.7 * R.stamp(s) if s < 1 else 1.0)
    ripple(im, t)
    if TAP <= t < TAP + 0.6: sparkle_burst(im, t, TAP, TEMPLE[0], TEMPLE[1] - 40)
    for (at, c, (x, y)) in zip(CHIPS_AT, CHIPS, CHIP_POS):
        if t >= at and t < SOLD_AT:
            k = (t - at) / 0.3; a = R.clamp(k * 3)
            if t >= FADE_AT:  # most people don't: the deals drift away
                f = R.clamp((t - FADE_AT) / 0.9); a *= 1 - f; x += 160 * f; y -= 40 * f
            R.paste_center(im, c, x + 8 * np.sin((t - at) * 3), y, a, 0.8 + 0.2 * R.stamp(k) if k < 1 else 1.0)
    if t >= SOLD_AT:
        s = (t - SOLD_AT) / 0.35; R.paste_center(im, SOLD, W / 2, 330, R.clamp(s * 3), 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, SOLD_AT, W / 2, 330, ((-280, -40, 34), (270, -60, 26), (-230, 60, 18), (250, 50, 34)))
    draw_caps(im, t, CAPS)
    if MYTH_AT <= t < MYTH_AT + 0.08: im = M.flash(im, 0.25)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END)
        mx.ping(0.35, 880, 0.12); mx.thud(MYTH_AT, 0.6); mx.shimmer(MYTH_AT + 0.02, 1046.5, 0.05)
        mx.shimmer(TAP, 1568, 0.09); mx.whoosh(TAP - 0.1, 0.4, 0.2)
        for i, at in enumerate(CHIPS_AT): mx.ping(at, 1318.5 + 220 * i, 0.15)
        y = mx.tt(1.0); mx.fadd(np.sin(2 * np.pi * np.cumsum(660 - 220 * y) / SR) * np.exp(-y * 3) * 0.5, FADE_AT, 0.12)   # falling tone: missed
        mx.thud(SOLD_AT, 0.45); mx.shimmer(SOLD_AT + 0.02, 1318.5, 0.11)
        mx.write("ep4_audio.wav")
    render(frame, TOTAL, "ep4_audio.wav", OUT)
