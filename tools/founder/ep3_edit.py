"""Founder Ep. 3 'Be in the room': glowing watch case, shop-window tag struck out, LIVE + watchers,
ONE AUCTION · ONE WINNER, sparkle burst on 'Be in the room'."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.20, 1.80, ["The [rarest pieces]", "in Lebanon"]), (1.80, 3.50, ["won't sit in a", "shop window."]),
        (4.05, 5.20, ["They'll go [live.]"]), (5.55, 6.40, ["[Once.]"]), (6.85, 7.80, ["[Be in the room.]"])]
STRIKE, LIVE, ONCE, ROOM = 3.0, 4.1, 5.65, 6.9
WATCH = (840, 1530)
rng = np.random.default_rng(9)
MOTES = [(rng.uniform(560, 1060), rng.uniform(1250, 1800), rng.uniform(30, 90), rng.uniform(1.5, 4), rng.uniform(0, 6)) for _ in range(40)]

def glow_layer(strength):
    y = np.arange(H)[:, None]; x = np.arange(W)[None, :]
    g = np.exp(-(((x - WATCH[0]) / 260.0) ** 2 + ((y - WATCH[1]) / 200.0) ** 2)) * strength
    a = np.zeros((H, W, 4), dtype=np.uint8); a[..., 0] = 140; a[..., 1] = 110; a[..., 2] = 255; a[..., 3] = np.clip(g * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(a, "RGBA")
GLOWS = {s: glow_layer(s) for s in (0.18, 0.25, 0.32, 0.45, 0.6)}

def motes(im, t, boost=1.0):
    d = ImageDraw.Draw(im)
    for x, y, sp, r, ph in MOTES:
        yy = y - (sp * t) % 600; a = int(150 * boost * (0.4 + 0.6 * np.sin(t * 2.5 + ph) ** 2) * max(0, 1 - (y - yy) / 600))
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(205, 195, 255, a))

def chip(line1, line2=None, hot=False):
    a = R.text_layer(line1, R.font(26, mono=True), WHITE if hot else (205, 210, 235), tracking=4)
    b = R.text_layer(line2, R.font(46, 700), WHITE) if line2 else None
    w = max(a.width, b.width if b else 0) + 70; h = a.height + (b.height + 6 if b else 0) + 40
    if hot:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=28, fill=255)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    else:
        im = M.glass(w, h, 28, fill=(16, 16, 30, 225), border=(167, 139, 250, 200))
    im.alpha_composite(a, (35, 20))
    if b: im.alpha_composite(b, (35, 26 + a.height))
    return im
SHOP = chip("IN A SHOP WINDOW", "$ 4,200")
ONE = chip("ONE AUCTION", "ONE WINNER", hot=True)

def live_chip(t, viewers):
    tl = R.text_layer(f"LIVE  ·  {viewers} watching", R.font(30, mono=True), WHITE, tracking=3)
    w, h = tl.width + 92, tl.height + 32; im = M.glass(w, h, h // 2, fill=(16, 16, 30, 225), border=(167, 139, 250, 220))
    a = int(160 + 95 * (0.5 + 0.5 * np.sin(t * 7))); ImageDraw.Draw(im).ellipse((28, h // 2 - 11, 50, h // 2 + 11), fill=(167, 139, 250, a))
    im.alpha_composite(tl, (64, 16)); return im

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Be in the room."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, True, 420, 130); M.scrim(im, False, 360, 110)
    pulse = 0.5 + 0.5 * np.sin(t * 2.2)
    s = 0.18 + 0.07 * pulse
    if t >= ROOM: s = 0.32 + 0.28 * max(0, 1 - (t - ROOM) / 0.8)
    key = min(GLOWS, key=lambda v: abs(v - s)); im.alpha_composite(GLOWS[key])
    motes(im, t, 1.6 if t >= ROOM else 1.0)
    # shop window tag gets struck through
    if 1.85 <= t < 4.0:
        k = (t - 1.85) / 0.3; a = R.clamp(k * 3) * (1 - R.clamp((t - 3.7) / 0.3)) * (0.6 if t >= STRIKE + 0.3 else 1)
        tag = SHOP.copy()
        if t >= STRIKE:
            sk = R.clamp((t - STRIKE) / 0.25); d = ImageDraw.Draw(tag); y = tag.height // 2
            d.line([(20, y), (20 + (tag.width - 40) * sk, y)], fill=(167, 139, 250, 255), width=8)
        R.paste_center(im, tag, W - 40 - tag.width / 2, 900, a, 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    # LIVE + watchers climbing
    if t >= LIVE:
        k = (t - LIVE) / 0.3; viewers = int(120 + 380 * R.clamp((t - LIVE) / 3.5) ** 1.3)
        lc = live_chip(t, viewers); R.paste_center(im, lc, W - 40 - lc.width / 2, 900, R.clamp(k * 3), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    if t >= ONCE:
        k = (t - ONCE) / 0.32; R.paste_center(im, ONE, W - 40 - ONE.width / 2, 755, R.clamp(k * 3), 1.6 - 0.6 * R.stamp(k) if k < 1 else 1.0)
    if t >= ROOM:
        sparkle_burst(im, t, ROOM, WATCH[0], WATCH[1] - 60, ((-160, -80, 34), (150, -120, 26), (-90, 90, 18), (170, 60, 34), (0, -170, 26)))
    draw_caps(im, t, CAPS, y=150, size=62)
    if ONCE <= t < ONCE + 0.07: im = M.flash(im, 0.25)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((130.8, .35), (196, .25), (261.6, .2), (392, .08)))
        mx.shimmer(0.25, 1046.5, 0.05)
        mx.ping(1.9, 990, 0.12); y = mx.tt(0.25); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 3) * np.exp(-y * 14), STRIKE, 0.3)   # strike scratch
        mx.ping(LIVE, 1318.5, 0.18); mx.shimmer(LIVE + 0.02, 1568, 0.05)
        for i in range(8): mx.ping(LIVE + 0.4 + i * 0.3, 2093 + 60 * i, 0.04)       # watcher ticks
        mx.thud(ONCE, 0.6); mx.shimmer(ONCE + 0.03, 1046.5, 0.06)
        mx.whoosh(ROOM - 0.15, 0.4, 0.25); mx.shimmer(ROOM, 1318.5, 0.12)
        mx.write("ep3_audio.wav")
    render(frame, TOTAL, "ep3_audio.wav", OUT)
