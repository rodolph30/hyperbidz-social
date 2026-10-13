"""Season 4 Ep. 1 'Fought over': cinematic night grade (teal shadows, warm chrome highlights, deep vignette, spotlight
bloom), a light sweep gliding along the silver car on 'doesn't get sold', a rev-counter gauge whose needle climbs into the
red with every bid (engine revs) on 'It gets fought over', and a LIVE badge slamming in on 'it goes live'. Last shot held
with a slow push-in. End card 'Not sold. Fought over.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, RED = (167, 139, 250), (255, 76, 96)
FR = decode()
CAPS = [(0.05, 2.45, ["A car like this", "doesn't get [sold.]"]), (2.50, 4.40, ["It gets [fought over.]"]),
        (5.05, 6.30, ["On HyperBidz…"]), (6.35, 9.20, ["it goes [live.]"])]
SWEEP, GAUGE_IN, BRAND, LIVE = 1.35, 2.45, 5.15, 6.42
BIDS = [(2.75, 61000, "Karim"), (3.05, 68500, "Nadim"), (3.35, 74000, "Rita"), (3.65, 81500, "Karim"), (3.95, 88000, "Jad"), (4.40, 94500, "Rita")]
GX, GY, GR = 885, 320, 150

# ---------- night grade ----------
x = np.linspace(0, 1, 256)
def tone(v): v = np.clip(0.5 + (v - 0.5) * 1.22, 0, 1); return v ** 1.08
c = tone(x)
LUT_R = np.clip((c * 1.02 - 0.02 * (1 - x) ** 2) * 255, 0, 255).astype(np.uint8)
LUT_G = np.clip((c * 1.00 + 0.005) * 255, 0, 255).astype(np.uint8)
LUT_B = np.clip((c * 0.96 + 0.06 * (1 - x) ** 1.5) * 255, 0, 255).astype(np.uint8)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.48 * np.clip((((xx - 540) / 700) ** 2 + ((yy - 860) / 1100) ** 2) ** 1.25, 0, 1))[..., None]
BLOOM = (np.exp(-(((xx - 540) / 260) ** 2 + ((yy - 40) / 320) ** 2)) * 0.22)[..., None] * np.array([255, 236, 210], np.float32)
CONE = (np.clip(1 - np.abs(xx - 540) / (120 + yy * 0.32), 0, 1) ** 2 * np.clip(1 - yy / 1500, 0, 1) * 0.07)[..., None] * np.array([255, 240, 220], np.float32)
FLOOR_DARK = (1 - 0.32 * np.clip((yy - 1450) / 470, 0, 1))[..., None]

def car_band(t):
    k = R.clamp(t / 7.5); return 760 + (900 - 760) * k, 1460 + (1920 - 1460) * k

def grade(fr, t):
    a = np.asarray(fr)
    g = np.stack([LUT_R[a[..., 0]], LUT_G[a[..., 1]], LUT_B[a[..., 2]]], -1).astype(np.float32)
    g = g * VIG * FLOOR_DARK + BLOOM + CONE
    k = (t - SWEEP) / 1.05
    if 0 <= k <= 1:                                     # specular sweep along the silver body
        y0, y1 = car_band(t); lum = a.mean(-1)
        band = np.exp(-(((xx - (-300 + k * 1700)) - (yy - 1000) * 0.55) / 90) ** 2)
        m = band * np.clip((lum - 120) / 80, 0, 1) * ((yy > y0) & (yy < y1)) * np.sin(np.pi * k)
        g = g + (m * 150)[..., None] * np.array([1.0, 0.98, 0.94], np.float32)
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA")

# ---------- rev-counter gauge ----------
A0, A1 = 225, -45                                         # 0 at lower-left, 100k at lower-right (degrees, CCW from +x)
def ang(v): return np.radians(A0 + (A1 - A0) * R.clamp(v / 100000))
def dial():
    s = 2 * GR + 80; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c0 = s / 2
    d.ellipse((c0 - GR - 18, c0 - GR - 18, c0 + GR + 18, c0 + GR + 18), fill=(10, 10, 16, 215), outline=(255, 255, 255, 60), width=2)
    for i in range(0, 101, 5):
        a = ang(i * 1000); r0 = GR - (22 if i % 20 == 0 else 12); col = RED + (255,) if i >= 80 else (235, 238, 245, 255)
        d.line([(c0 + r0 * np.cos(a), c0 - r0 * np.sin(a)), (c0 + GR * np.cos(a), c0 - GR * np.sin(a))], fill=col, width=4 if i % 20 == 0 else 2)
        if i % 20 == 0 and 0 < i < 100:
            tl = R.text_layer(str(i), R.font(24, mono=True), (220, 224, 236)); rr = GR - 48
            im.alpha_composite(tl, (int(c0 + rr * np.cos(a) - tl.width / 2), int(c0 - rr * np.sin(a) - tl.height / 2)))
    d.arc((c0 - GR + 4, c0 - GR + 4, c0 + GR - 4, c0 + GR - 4), -np.degrees(ang(80000)), -np.degrees(ang(100000)), fill=RED + (220,), width=6)   # red zone 80k-100k
    return im
DIAL = dial()

def gauge(im, t, a_):
    cur = [v for at, v, n in BIDS if t >= at]; prev = ([0] + [v for _, v, _ in BIDS])
    if cur:
        i = len(cur) - 1; at = BIDS[i][0]; v0 = prev[i]; v = v0 + (cur[-1] - v0) * R.ease_out((t - at) / 0.22)
        v += 900 * np.sin((t - at) * 40) * max(0, 1 - (t - at) / 0.25)        # needle bounce
    else: v = 18000 * R.ease_out((t - GAUGE_IN) / 0.4)
    lay = DIAL.copy(); d = ImageDraw.Draw(lay); c0 = lay.width / 2; a = ang(v)
    redline = v >= 80000
    d.line([(c0 - 22 * np.cos(a), c0 + 22 * np.sin(a)), (c0 + (GR - 14) * np.cos(a), c0 - (GR - 14) * np.sin(a))], fill=(RED if redline else (255, 160, 90)) + (255,), width=7)
    d.ellipse((c0 - 16, c0 - 16, c0 + 16, c0 + 16), fill=(30, 30, 40, 255), outline=(220, 224, 236, 255), width=3)
    val = R.text_layer(f"${int(round(v / 500) * 500):,}", R.font(36, 700), WHITE); lay.alpha_composite(val, (int(c0 - val.width / 2), int(c0 + 34)))
    if t >= BRAND:
        b = R.text_layer("HYPERBIDZ", R.font(22, mono=True), (200, 190, 255), tracking=5); lay.alpha_composite(b, (int(c0 - b.width / 2), int(c0 - 70)))
    if redline:
        glow = Image.new("RGBA", lay.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((20, 20, lay.width - 20, lay.height - 20), outline=RED + (int(110 + 60 * np.sin(t * 14)),), width=10)
        lay = Image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)), lay)
    R.paste_center(im, lay, GX, GY, a_)

def chip(name, v):
    a = R.text_layer(name, R.font(28, 600), WHITE); b = R.text_layer(f"${v:,}", R.font(30, 700), WHITE)
    w, h = a.width + b.width + 70, 58; im = M.glass(w, h, h // 2, fill=(20, 20, 32, 225), border=(255, 255, 255, 70))
    im.alpha_composite(a, (24, (h - a.height) // 2 - 2)); im.alpha_composite(b, (w - 24 - b.width, (h - b.height) // 2 - 2)); return im
CHIPS = [chip(n, v) for _, v, n in BIDS]

def live_badge():
    tl = R.text_layer("LIVE", R.font(84, 700), WHITE, tracking=6); w, h = tl.width + 150, tl.height + 50
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    ImageDraw.Draw(im).ellipse((40, h // 2 - 18, 76, h // 2 + 18), fill=(255, 255, 255, 255)); im.alpha_composite(tl, (100, 25)); return im
LIVE_IM = live_badge()
def sub_line():
    tl = R.text_layer("23 bidders  ·  $94,500", R.font(30, mono=True), (235, 238, 255), tracking=2); w, h = tl.width + 50, tl.height + 24
    im = M.glass(w, h, h // 2, fill=(14, 14, 24, 220), border=(*VIOLET, 200)); im.alpha_composite(tl, (25, 12)); return im
SUB = sub_line()

def ring(im, cx, cy, rad, a, col=VIOLET, width=6):
    if a <= 0.01: return
    lay = Image.new("RGBA", (int(rad * 2 + 20), int(rad * 2 + 20)), (0, 0, 0, 0)); c = lay.width / 2
    ImageDraw.Draw(lay).ellipse((c - rad, c - rad, c + rad, c + rad), outline=(*col, int(255 * a)), width=width); R.paste_center(im, lay, cx, cy)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Not sold.", "Fought over."], END)
    im = grade(FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))], min(t, SHOT - 0.01))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (480, 620))
    if t >= GAUGE_IN:
        k = (t - GAUGE_IN) / 0.35; gauge(im, t, R.clamp(k * 3))
        shown = [(at, ch) for (at, v, n), ch in zip(BIDS, CHIPS) if t >= at][-3:]
        for j, (at, ch) in enumerate(reversed(shown)):
            kk = R.ease_out((t - at) / 0.25); R.paste_center(im, ch, GX, GY + GR + 60 + j * 66 + (1 - kk) * -20, R.clamp((t - at) / 0.15) * (1 - 0.3 * j) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)))
    if t >= LIVE:
        s = (t - LIVE) / 0.3; R.paste_center(im, LIVE_IM, 250, 250, R.clamp(s * 3), 1.8 - 0.8 * R.stamp(s) if s < 1 else 1.0 + 0.02 * np.sin((t - LIVE) * 6))
        if t >= LIVE + 0.35: s2 = (t - LIVE - 0.35) / 0.3; R.paste_center(im, SUB, 250, 360, R.clamp(s2 * 3), 0.85 + 0.15 * R.stamp(s2) if s2 < 1 else 1.0)
        for j in range(2): kk = R.clamp((t - LIVE - 0.08 * j) / 0.6); ring(im, 250, 250, 60 + 520 * R.ease_out(kk), (1 - kk) * 0.8, VIOLET, 7)
        sparkle_burst(im, t, LIVE, 250, 250, ((-150, -70, 34), (160, -60, 26), (140, 70, 18), (-130, 80, 26)))
    draw_caps(im, t, CAPS, y=1700, size=62)
    if LIVE <= t < LIVE + 0.08: im = M.flash(im, 0.3)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

def rev(mx, at, f0, f1, dur, g):
    y = mx.tt(dur); f = f0 + (f1 - f0) * np.sin(np.pi / 2 * np.minimum(1, y / (dur * 0.6)))
    ph = 2 * np.pi * np.cumsum(f) / SR; sig = sum(np.sin(ph * k) / k for k in range(1, 9)) + 0.25 * mx.lp(mx.rng.normal(0, 1, len(y)), 4)
    env = np.minimum(1, y / 0.04) * np.exp(-np.maximum(0, y - dur * 0.6) * 7); mx.fadd(mx.lp(sig, 3) * env, at, g)

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((73.4, .30), (110, .22), (146.8, .16), (220, .06)))
        mx.shimmer(SWEEP + 0.2, 2093, 0.05)
        rev(mx, GAUGE_IN, 38, 52, 0.5, 0.18)
        for i, (at, v, n) in enumerate(BIDS):
            if 3.15 < at < 4.1: continue                                   # silent under 'It gets fought over'
            rev(mx, at - 0.03, 45 + i * 6, 70 + i * 12, 0.26, 0.09); mx.ping(at + 0.05, 1046.5 * 2 ** (i * 2 / 12), 0.05)
        mx.ping(BRAND, 1318.5, 0.08)
        mx.thud(LIVE, 0.35); mx.shimmer(LIVE + 0.03, 1318.5, 0.06); rev(mx, 7.0, 60, 140, 1.1, 0.26)   # the roar comes after 'live'
        mx.write("s4e1_audio.wav")
    render(frame, TOTAL, "s4e1_audio.wav", OUT)
