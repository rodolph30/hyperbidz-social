"""Season 4 (cars) shared pieces: looks (night, dusk, crime, clinic), letterbox, film grain, region blur for stray text
or plates, LIVE badge, bid chips, gradient pills, rings, and sounds (engine rev, record scratch, monitor beep, drone)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
import mhelpers as M
from founder_common import W, H, SR, WHITE

VIOLET, RED, AMBER = (167, 139, 250), (255, 76, 96), (255, 184, 92)
_x = np.linspace(0, 1, 256)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)

def _lut(fr, fg, fb):
    return [np.clip(f(_x) * 255, 0, 255).astype(np.uint8) for f in (fr, fg, fb)]
def _tone(v, c=1.2, gam=1.06): v = np.clip(0.5 + (v - 0.5) * c, 0, 1); return v ** gam

LOOKS = {
    "night": _lut(lambda v: _tone(v) * 1.02 - 0.02 * (1 - v) ** 2, lambda v: _tone(v) + 0.005, lambda v: _tone(v) * 0.96 + 0.06 * (1 - v) ** 1.5),
    "dusk": _lut(lambda v: _tone(v, 1.15) * 1.05 + 0.01, lambda v: _tone(v, 1.15) * 0.99, lambda v: _tone(v, 1.15) * 0.9 + 0.04 * (1 - v)),
    "crime": _lut(lambda v: _tone(v, 1.35, 1.2) * 0.86, lambda v: _tone(v, 1.35, 1.2) * 1.0 + 0.03, lambda v: _tone(v, 1.35, 1.2) * 0.92 + 0.04),
    "clinic": _lut(lambda v: _tone(v, 1.05, 0.95) * 0.95 + 0.05, lambda v: _tone(v, 1.05, 0.95) * 1.0 + 0.05, lambda v: _tone(v, 1.05, 0.95) * 1.04 + 0.06),
}
SAT = {"night": 1.05, "dusk": 1.1, "crime": 0.55, "clinic": 0.45}

def vignette(strength=0.45, cy=860):
    return (1 - strength * np.clip((((_xx - 540) / 700) ** 2 + ((_yy - cy) / 1100) ** 2) ** 1.25, 0, 1))[..., None]
VIG = vignette()

def look(fr, name, vig=VIG, extra=None):
    a = np.asarray(fr); r, g, b = LOOKS[name]
    out = np.stack([r[a[..., 0]], g[a[..., 1]], b[a[..., 2]]], -1).astype(np.float32)
    lum = out.mean(-1, keepdims=True); out = lum + (out - lum) * SAT[name]
    out = out * vig
    if extra is not None: out = out + extra
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")

def blend_looks(fr, a, b, k, **kw):
    if k <= 0: return look(fr, a, **kw)
    if k >= 1: return look(fr, b, **kw)
    return Image.blend(look(fr, a, **kw), look(fr, b, **kw), k)

def grain(im, amount=10, seed=0):
    rng = np.random.default_rng(seed); n = rng.normal(0, amount, (H // 2, W // 2)).astype(np.float32)
    n = np.asarray(Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8)).resize((W, H)), np.float32) - 128
    a = np.asarray(im.convert("RGB"), np.float32) + n[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def letterbox(im, k, h=210):
    if k <= 0: return
    d = ImageDraw.Draw(im); hh = int(h * k); d.rectangle((0, 0, W, hh), fill=(0, 0, 0, 255)); d.rectangle((0, H - hh, W, H), fill=(0, 0, 0, 255))

def blur_region(im, box, r=14):
    reg = im.crop(box).filter(ImageFilter.GaussianBlur(r)); im.paste(reg, box[:2]); return im

def ring(im, cx, cy, rad, a, col=VIOLET, width=6):
    if a <= 0.01: return
    lay = Image.new("RGBA", (int(rad * 2 + 20), int(rad * 2 + 20)), (0, 0, 0, 0)); c = lay.width / 2
    ImageDraw.Draw(lay).ellipse((c - rad, c - rad, c + rad, c + rad), outline=(*col, int(255 * a)), width=width); R.paste_center(im, lay, cx, cy)

def grad_pill(top, big, size=70, sub_size=24):
    b = R.text_layer(top, R.font(sub_size, mono=True), (235, 238, 255), tracking=3) if top else None
    a = R.text_layer(big, R.font(size, 700), WHITE)
    w = max(a.width, b.width if b else 0) + 90; h = a.height + (b.height + 8 if b else 0) + 36
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=min(36, h // 2), fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m); y = 16
    if b: im.alpha_composite(b, ((w - b.width) // 2, y)); y += b.height + 8
    im.alpha_composite(a, ((w - a.width) // 2, y - 4)); return im

def live_badge(size=84):
    tl = R.text_layer("LIVE", R.font(size, 700), WHITE, tracking=6); w, h = tl.width + 150, tl.height + 50
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    ImageDraw.Draw(im).ellipse((40, h // 2 - 18, 76, h // 2 + 18), fill=(255, 255, 255, 255)); im.alpha_composite(tl, (100, 25)); return im

def bid_chip(name, amt, hot=False):
    a = R.text_layer(name, R.font(28, 600), WHITE); b = R.text_layer(amt, R.font(30, 700), WHITE)
    w, h = a.width + b.width + 74, 58
    im = M.glass(w, h, h // 2, fill=(36, 28, 76, 236) if hot else (20, 20, 32, 225), border=(*VIOLET, 230) if hot else (255, 255, 255, 70))
    im.alpha_composite(a, (24, (h - a.height) // 2 - 2)); im.alpha_composite(b, (w - 24 - b.width, (h - b.height) // 2 - 2)); return im

def msg_bubble(head, text, fill=(52, 54, 68, 242), out=False, size=36):
    hd = R.text_layer(head, R.font(20, mono=True), (190, 194, 206), tracking=2) if head else None
    tx = R.text_layer(text, R.font(size, 600), WHITE)
    w = max(tx.width, hd.width if hd else 0) + 56; h = tx.height + (hd.height + 8 if hd else 0) + 34
    im = Image.new("RGBA", (w, h + 22), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=fill)
    if out: d.polygon([(w - 64, h - 2), (w - 24, h - 2), (w - 16, h + 18)], fill=fill)
    else: d.polygon([(40, h - 2), (82, h - 2), (32, h + 18)], fill=fill)
    y = 16
    if hd: im.alpha_composite(hd, (28, y)); y += hd.height + 8
    im.alpha_composite(tx, (28, y - 2)); return im

# ---------- sound ----------
def rev(mx, at, f0, f1, dur, g):
    y = mx.tt(dur); f = f0 + (f1 - f0) * np.sin(np.pi / 2 * np.minimum(1, y / (dur * 0.6)))
    ph = 2 * np.pi * np.cumsum(f) / SR; sig = sum(np.sin(ph * k) / k for k in range(1, 9)) + 0.25 * mx.lp(mx.rng.normal(0, 1, len(y)), 4)
    env = np.minimum(1, y / 0.04) * np.exp(-np.maximum(0, y - dur * 0.6) * 7); mx.fadd(mx.lp(sig, 3) * env, at, g)

def scratch(mx, at, g=0.35):
    y = mx.tt(0.45); f = 900 * np.exp(-y * 6) + 120 * np.sin(2 * np.pi * 7 * y)
    sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.6 + mx.lp(mx.rng.normal(0, 1, len(y)), 2) * 0.6
    mx.fadd(sig * np.exp(-y * 5), at, g)

def beep(mx, at, f=1000, dur=0.12, g=0.12):
    y = mx.tt(dur); mx.fadd(np.sin(2 * np.pi * f * y) * np.minimum(1, (dur - y) / 0.02), at, g)

def drone(mx, t0, t1, f=55, g=0.12):
    y = mx.tt(t1 - t0); s = (np.sin(2 * np.pi * f * y) + 0.6 * np.sin(2 * np.pi * f * 1.06 * y) + 0.3 * np.sin(2 * np.pi * f * 2.02 * y))
    env = np.minimum(1, y / 0.6) * np.minimum(1, (y[-1] - y) / 0.15); mx.fadd(s * env, t0, g)

def hum(mx, t0, t1, g=0.04):
    y = mx.tt(t1 - t0); s = np.sign(np.sin(2 * np.pi * 100 * y)) * 0.5 + np.sin(2 * np.pi * 200 * y) * 0.5
    mx.fadd(mx.lp(s, 8) * np.minimum(1, (y[-1] - y) / 0.05), t0, g)
