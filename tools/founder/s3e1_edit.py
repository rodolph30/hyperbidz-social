"""Season 3 Ep. 1 'Jeddo's tawleh': warm golden re-grade of a flat clip (curves, warm highlights, vignette, light shafts
from the arched windows, drifting dust), a shimmer across the tawleh, memory tags beside his head ('Jeddo's tawleh',
'Teta's ring'), then the worth reveal: 'First offer $40' struck, bids climbing to $680. End card 'What's waiting in your home?'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, GOLD, AMBER = (167, 139, 250), (255, 206, 128), (255, 184, 92)
CAPS = [(0.30, 2.75, ["In every Lebanese home,", "something is [waiting.]"]), (3.10, 4.45, ["Jeddo's [tawleh.]"]),
        (4.55, 5.75, ["Teta's [ring.]"]), (6.00, 7.85, ["It's worth more", "than you [think.]"])]
SHINE1, TAG1, TAG2, OFFER, STRIKE, CLIMB, LAND = 2.05, 3.15, 4.6, 6.05, 6.5, 6.6, 7.25
BIDS = [40, 95, 160, 240, 330, 430, 540, 680]

# ---------- grade ----------
x = np.linspace(0, 1, 256)
def curve(v):
    v = v ** 1.10                                     # a little deeper
    v = 0.5 + (v - 0.5) * 1.14                        # contrast
    v = np.where(v > 0.78, 0.78 + (v - 0.78) * 0.62, v)   # roll off the blown windows
    return np.clip(v, 0, 1)
c = curve(x)
LUT_R = np.clip((c * 1.07 + 0.012) * 255, 0, 255).astype(np.uint8)
LUT_G = np.clip((c * 0.985 + 0.004) * 255, 0, 255).astype(np.uint8)
LUT_B = np.clip((c * 0.84 + 0.035 * (1 - x)) * 255, 0, 255).astype(np.uint8)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.34 * np.clip((((xx - 540) / 760) ** 2 + ((yy - 900) / 1150) ** 2) ** 1.3, 0, 1))[..., None]
GLOW = (np.exp(-(((xx - 540) / 420) ** 2 + ((yy - 760) / 560) ** 2)) * 0.10)[..., None] * np.array([255, 214, 160], np.float32)

def shafts():
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay)
    for wx, a in ((310, 120), (570, 90), (830, 120)):
        d.polygon([(wx - 60, 330), (wx + 60, 330), (wx + 420, 1950), (wx + 40, 1950)], fill=a)
    return np.asarray(lay.filter(ImageFilter.GaussianBlur(46)), np.float32) / 255.0
SHAFT = shafts()[..., None] * np.array([255, 210, 150], np.float32)

rng = np.random.default_rng(5)
MOTES = [(rng.uniform(80, 1000), rng.uniform(300, 1700), rng.uniform(8, 26), rng.uniform(1.5, 3.4), rng.uniform(0, 6.3)) for _ in range(46)]

FR = decode()
def grade(fr, t):
    a = np.asarray(fr)
    g = np.stack([LUT_R[a[..., 0]], LUT_G[a[..., 1]], LUT_B[a[..., 2]]], -1).astype(np.float32)
    breathe = 0.13 + 0.025 * np.sin(t * 1.3)
    g = g * VIG + GLOW + SHAFT * breathe
    lum = g.mean(-1, keepdims=True); g = lum + (g - lum) * 1.08          # a touch more colour
    im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    for mx, my, sp, r, ph in MOTES:                                      # dust drifting up through the light
        yv = (my - sp * t) % 1500 + 250; xv = mx + 14 * np.sin(t * 0.7 + ph)
        al = int(120 * (0.35 + 0.65 * np.sin(t * 1.8 + ph) ** 2))
        d.ellipse((xv - r, yv - r, xv + r, yv + r), fill=(255, 232, 190, al))
    return im

# ---------- the board ----------
KEYS = [(0.5, (290, 1200, 800, 1570)), (3.5, (270, 1210, 810, 1690)), (7.0, (260, 1230, 820, 1730))]
def board_box(t):
    if t <= KEYS[0][0]: return KEYS[0][1]
    for (t0, b0), (t1, b1) in zip(KEYS, KEYS[1:]):
        if t <= t1: k = (t - t0) / (t1 - t0); return tuple(int(p + (q - p) * k) for p, q in zip(b0, b1))
    return KEYS[-1][1]
def shine(im, t, t0, dur=0.75, peak=0.42):
    k = (t - t0) / dur
    if not 0 <= k <= 1: return
    x0, y0, x1, y1 = board_box(t); w, h = x1 - x0, y1 - y0
    band = Image.new("L", (w, h), 0); d = ImageDraw.Draw(band); cx = -w * 0.4 + k * w * 1.8
    d.polygon([(cx - 70, h), (cx + 70, h), (cx + 70 + h * 0.6, 0), (cx - 70 + h * 0.6, 0)], fill=int(255 * peak * np.sin(np.pi * k)))
    band = band.filter(ImageFilter.GaussianBlur(26)); m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=14, fill=255)
    band = Image.fromarray((np.asarray(band, np.float32) * np.asarray(m, np.float32) / 255).astype(np.uint8))
    lay = Image.new("RGBA", (w, h), (255, 244, 220, 0)); lay.putalpha(band); im.alpha_composite(lay, (x0, y0))

# ---------- memory tags ----------
def dice():
    im = Image.new("RGBA", (64, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for ox, pips in ((2, ((10, 10), (26, 26), (18, 18))), (34, ((8, 8), (28, 8), (8, 28), (28, 28)))):
        d.rounded_rectangle((ox, 2, ox + 34, 36), radius=7, fill=(250, 246, 236, 255), outline=(120, 98, 70, 255), width=2)
        for px, py in pips: d.ellipse((ox + px - 3, py - 1, ox + px + 3, py + 5), fill=(70, 50, 34, 255))
    return im
def ring_icon():
    im = Image.new("RGBA", (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((6, 14, 42, 46), outline=(214, 168, 70, 255), width=6); d.ellipse((9, 17, 39, 43), outline=(255, 222, 140, 180), width=1)
    d.polygon([(24, 2), (32, 10), (24, 18), (16, 10)], fill=(232, 240, 255, 255), outline=(150, 170, 210, 255)); return im
def tag(title, line, icon, rot):
    a = R.text_layer(title, R.font(22, mono=True), (110, 84, 52), tracking=2); b = R.text_layer(line, R.font(28, 500), (62, 48, 34))
    w = max(a.width, b.width, icon.width) + 44; h = icon.height + a.height + b.height + 52
    im = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((18, 22, w + 14, h + 18), radius=16, fill=(40, 24, 8, 110)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(card).rounded_rectangle((0, 0, w - 1, h - 1), radius=16, fill=(250, 241, 222, 246), outline=(222, 196, 150, 255), width=2)
    card.alpha_composite(icon, ((w - icon.width) // 2, 18)); y = 18 + icon.height + 10
    card.alpha_composite(a, ((w - a.width) // 2, y)); card.alpha_composite(b, ((w - b.width) // 2, y + a.height + 6))
    im.alpha_composite(card, (15, 15)); return im.rotate(rot, resample=Image.BICUBIC, expand=True)
T1 = tag("JEDDO'S TAWLEH", "since 1968", dice(), 4)
T2 = tag("TETA'S RING", "her wedding, 1959", ring_icon(), -4)
def show_tag(im, t, tg, t0, cx, cy):
    if not t0 <= t < 6.0: return
    k = (t - t0) / 0.6; out = R.clamp((t - 5.65) / 0.35)
    a = R.ease_out(k) * (1 - out); y = cy + (1 - R.ease_out(k)) * 26 + 6 * np.sin((t - t0) * 2.2) - out * 30
    lay = tg if k >= 1 else tg.filter(ImageFilter.GaussianBlur(8 * (1 - R.ease_out(k))))
    R.paste_center(im, lay, cx, y, a)
    sparkle_burst(im, t, t0 + 0.15, cx, y, ((-150, -50, 18), (150, -40, 14), (120, 50, 18)))

# ---------- the worth reveal ----------
def offer_chip(strike):
    tl = R.text_layer("First offer  ·  $40", R.font(40, 700), (60, 40, 10)); w, h = tl.width + 64, tl.height + 30
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(*AMBER, 245))
    im.alpha_composite(tl, (32, 15))
    if strike > 0: ImageDraw.Draw(im).line([(18, h // 2 + 2), (18 + (w - 36) * strike, h // 2 - 4)], fill=(*VIOLET, 255), width=9)
    return im
def bid_pill(v, n):
    a = R.text_layer(f"${v}", R.font(76, 700), WHITE); b = R.text_layer(f"LIVE  ·  {n} bidders", R.font(26, mono=True), (235, 238, 255), tracking=3)
    w, h = max(a.width, b.width) + 96, a.height + b.height + 40
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=36, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(b, ((w - b.width) // 2, 16)); im.alpha_composite(a, ((w - a.width) // 2, 20 + b.height)); return im

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["What's waiting", "in your home?"], END)
    im = grade(FR[min(len(FR) - 1, int(t * FPS))], t)
    shine(im, t, SHINE1); shine(im, t, LAND, 0.8, 0.5)
    show_tag(im, t, T1, TAG1, 175, 520); show_tag(im, t, T2, TAG2, 905, 520)
    if OFFER <= t < CLIMB + 0.2:
        k = (t - OFFER) / 0.3; sk = R.clamp((t - STRIKE) / 0.25) if t >= STRIKE else 0
        shake = 10 * np.sin((t - STRIKE) * 60) * max(0, 1 - (t - STRIKE) / 0.25) if t >= STRIKE else 0
        R.paste_center(im, offer_chip(sk), W / 2 + shake, 190, R.clamp(k * 3) * (1 - R.clamp((t - CLIMB) / 0.2)), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    if t >= CLIMB:
        k = (t - CLIMB) / 0.3; i = min(len(BIDS) - 1, int((t - CLIMB) / ((LAND - CLIMB) / (len(BIDS) - 1))))
        pill = bid_pill(BIDS[i], 4 + i)
        bump = 1.05 if t >= LAND and t < LAND + 0.12 else 1.0
        R.paste_center(im, pill, W / 2, 200, R.clamp(k * 3), (0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0) * bump)
        if t >= LAND: sparkle_burst(im, t, LAND, W / 2, 200, ((-260, -40, 34), (250, -50, 26), (-200, 50, 18), (230, 45, 34)))
    draw_caps(im, t, CAPS, y=1010, size=62)
    if LAND <= t < LAND + 0.07: im = M.flash(im, 0.18, (255, 236, 200))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

def pluck(mx, at, f0, g=0.08, dur=1.6):
    n = int(dur * SR); p = int(SR / f0); buf = mx.rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    mx.fadd(out * np.exp(-np.arange(n) / SR * 1.6), at, g)

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, .32), (220, .22), (293.7, .16), (370, .06)))
        notes = [293.7, 440, 370, 392, 293.7, 440, 349.2, 293.7]                      # a slow, warm arpeggio (D, Hijaz colour)
        for i, f in enumerate(notes): pluck(mx, 0.2 + i * 0.95, f, 0.07)
        mx.shimmer(SHINE1, 1568, 0.05)
        for t0 in (TAG1, TAG2): mx.shimmer(t0, 1174.7, 0.06); mx.ping(t0 + 0.05, 880, 0.06)
        mx.ping(OFFER, 523.3, 0.1); y = mx.tt(0.25); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 3) * np.exp(-y * 14), STRIKE, 0.22)
        for i in range(len(BIDS) - 1): mx.ping(CLIMB + i * (LAND - CLIMB) / (len(BIDS) - 1), 1046.5 * 2 ** (i * 2 / 12), 0.1)
        mx.thud(LAND, 0.45); mx.shimmer(LAND + 0.02, 1318.5, 0.12)
        mx.write("s3e1_audio.wav")
    render(frame, TOTAL, "s3e1_audio.wav", OUT)
