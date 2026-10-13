"""Season 3 look: warm golden-afternoon grade (curves, warm highlights, rolled-off windows), vignette, a soft key glow,
light shafts from the windows and dust drifting in the sun. Shared by every S3 edit so the season looks like one show."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from founder_common import W, H

_x = np.linspace(0, 1, 256)
def _curve(v):
    v = v ** 1.10
    v = 0.5 + (v - 0.5) * 1.14
    v = np.where(v > 0.78, 0.78 + (v - 0.78) * 0.62, v)
    return np.clip(v, 0, 1)
_c = _curve(_x)
LUT_R = np.clip((_c * 1.07 + 0.012) * 255, 0, 255).astype(np.uint8)
LUT_G = np.clip((_c * 0.985 + 0.004) * 255, 0, 255).astype(np.uint8)
LUT_B = np.clip((_c * 0.84 + 0.035 * (1 - _x)) * 255, 0, 255).astype(np.uint8)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)

class Look:
    def __init__(self, windows=((310, 330, 120), (570, 330, 90), (830, 330, 120)), key=(540, 760), vig_center=(540, 900), motes=46, seed=5):
        self.vig = (1 - 0.34 * np.clip((((_xx - vig_center[0]) / 760) ** 2 + ((_yy - vig_center[1]) / 1150) ** 2) ** 1.3, 0, 1))[..., None]
        self.glow = (np.exp(-(((_xx - key[0]) / 420) ** 2 + ((_yy - key[1]) / 560) ** 2)) * 0.10)[..., None] * np.array([255, 214, 160], np.float32)
        lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay)
        for wx, wy, a in windows: d.polygon([(wx - 60, wy), (wx + 60, wy), (wx + 420, 1950), (wx + 40, 1950)], fill=a)
        self.shaft = (np.asarray(lay.filter(ImageFilter.GaussianBlur(46)), np.float32) / 255.0)[..., None] * np.array([255, 210, 150], np.float32)
        rng = np.random.default_rng(seed)
        self.motes = [(rng.uniform(80, 1000), rng.uniform(300, 1700), rng.uniform(8, 26), rng.uniform(1.5, 3.4), rng.uniform(0, 6.3)) for _ in range(motes)]

    def __call__(self, fr, t, shafts=True, dust=True):
        a = np.asarray(fr)
        g = np.stack([LUT_R[a[..., 0]], LUT_G[a[..., 1]], LUT_B[a[..., 2]]], -1).astype(np.float32)
        g = g * self.vig + self.glow
        if shafts: g = g + self.shaft * (0.13 + 0.025 * np.sin(t * 1.3))
        lum = g.mean(-1, keepdims=True); g = lum + (g - lum) * 1.08
        im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA")
        if dust:
            d = ImageDraw.Draw(im, "RGBA")
            for mx, my, sp, r, ph in self.motes:
                yv = (my - sp * t) % 1500 + 250; xv = mx + 14 * np.sin(t * 0.7 + ph)
                al = int(120 * (0.35 + 0.65 * np.sin(t * 1.8 + ph) ** 2))
                d.ellipse((xv - r, yv - r, xv + r, yv + r), fill=(255, 232, 190, al))
        return im

def memory(im, amount=0.5, grain_seed=0):
    """faded-photo look for flashbacks: warm sepia mix, lifted blacks, grain, heavy vignette."""
    a = np.asarray(im.convert("RGB"), np.float32)
    lum = a.mean(-1, keepdims=True); sep = lum * np.array([1.08, 0.94, 0.74], np.float32) + np.array([18, 10, 0], np.float32)
    a = a * (1 - amount) + sep * amount
    a = a * 0.9 + 18
    rng = np.random.default_rng(grain_seed); a = a + rng.normal(0, 7, a.shape[:2])[..., None]
    v = (1 - 0.55 * np.clip((((_xx - 540) / 640) ** 2 + ((_yy - 960) / 1050) ** 2) ** 1.5, 0, 1))[..., None]
    return Image.fromarray(np.clip(a * v, 0, 255).astype(np.uint8)).convert("RGBA")

def pluck(mx, at, f0, g=0.08, dur=1.6, sr=48000):
    n = int(dur * sr); p = int(sr / f0); buf = mx.rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    mx.fadd(out * np.exp(-np.arange(n) / sr * 1.6), at, g)
