"""HyperBidz explainer kit: illustrated 2D explainers drawn frame by frame (no AI video tools).
Look: a dark plum stage, warm spotlights, serif headlines with italic violet emphasis, small sans captions on a dark
pill (emphasis in italic serif), flat props with soft shadows, eased camera pushes, and zoom-through transitions."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import sys
import os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.chdir(HERE)  # fonts load by relative path (fonts/...)
import render as R

W, H, FPS, SR = 1080, 1920, 30, 48000
BG0, BG1 = (19, 15, 25), (38, 30, 48)
WARM = (255, 210, 150); VIO = (124, 92, 255); LAV = (190, 172, 255); GOLD = (226, 188, 112); CREAM = (240, 231, 212)
INK = (28, 23, 34); RED = (176, 38, 48); WHITE = (255, 255, 255); MUTE = (205, 200, 214); GREEN = (64, 190, 130)

_F = {}
def serif(size, italic=False):
    k = ("s", size, italic)
    if k not in _F: _F[k] = ImageFont.truetype(f"fonts/DMSerif-{'italic' if italic else 'normal'}.ttf", size)
    return _F[k]
def sans(size, w=600): return R.font(size, w)
def mono(size): return R.font(size, mono=True)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def ein(x): x = clamp(x); return x * x * x
def pop(x):
    x = clamp(x); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def fade(t, t0, t1, fin=0.35, fout=0.3): return ease((t - t0) / fin) * (1 - ease((t - (t1 - fout)) / fout))

def tl(text, f, col): return R.text_layer(text, f, col)

def put(base, layer, cx, cy, a=1.0, s=1.0, rot=0.0):
    """paste a layer centred at (cx, cy) with alpha a, scale s and rotation rot (degrees)"""
    if a <= 0.004 or layer is None: return
    if abs(rot) > 0.05: layer = layer.rotate(rot, expand=True, resample=Image.BICUBIC)
    R.paste_center(base, layer, cx, cy, min(1.0, a), s)

def shadowed(layer, blur=18, dy=14, a=150):
    pad = blur * 2; im = Image.new("RGBA", (layer.width + 2 * pad, layer.height + 2 * pad + dy), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, a), (pad, pad + dy), layer.getchannel("A"))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur))); im.alpha_composite(layer, (pad, pad)); return im

# ---------- rich text: "plain [emphasis] plain" ----------
def _words(markup):
    out = []; emph = False; buf = ""
    for ch in markup:
        if ch in "[]":
            if buf: out += [(w, emph) for w in buf.split(" ") if w]
            buf = ""; emph = ch == "["
        else: buf += ch
    if buf: out += [(w, emph) for w in buf.split(" ") if w]
    return out

def rich(markup, size, kind="serif", col=WHITE, emph=LAV, max_w=940, align="center", line_gap=1.12):
    f_plain = serif(size) if kind == "serif" else sans(size, 600)
    f_emph = serif(int(size * (1.0 if kind == "serif" else 1.12)), italic=True)
    sp = int(size * 0.26); lines = [[]]; widths = [0]
    for w, e in _words(markup):
        lay = tl(w, f_emph if e else f_plain, emph if e else col)
        add = lay.width + (sp if lines[-1] else 0)
        if lines[-1] and widths[-1] + add > max_w: lines.append([]); widths.append(0); add = lay.width
        lines[-1].append(lay); widths[-1] += add
    lh = int(size * line_gap * 1.25); hgt = lh * len(lines) + int(size * 0.25)
    im = Image.new("RGBA", (max(widths) + 8, hgt), (0, 0, 0, 0))
    for i, (ln, wd) in enumerate(zip(lines, widths)):
        x = (im.width - wd) // 2 if align == "center" else 0
        for lay in ln:
            im.alpha_composite(lay, (x, i * lh + (lh - lay.height) // 2)); x += lay.width + sp
    return im

_RC = {}
def rich_c(*a, **k):
    key = (a, tuple(sorted(k.items())))
    if key not in _RC: _RC[key] = rich(*a, **k)
    return _RC[key]

def headline(im, t, t0, t1, markup, y=300, size=78):
    a = fade(t, t0, t1, 0.45, 0.35)
    if a > 0: put(im, rich_c(markup, size, "serif", WHITE, LAV, 960), W / 2, y + (1 - eout((t - t0) / 0.5)) * 24, a)

def caption(im, t, t0, t1, markup, y=1690, size=44):
    a = fade(t, t0, t1, 0.3, 0.25)
    if a <= 0: return
    key = ("cap", markup, size)
    if key not in _RC:
        txt = rich(markup, size, "sans", WHITE, LAV, 900); w, h = txt.width + 64, txt.height + 26
        pill = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, w - 1, h - 1), radius=min(36, h // 2), fill=(10, 8, 14, 175))
        pill.alpha_composite(txt, (32, 13)); _RC[key] = pill
    put(im, _RC[key], W / 2, y + (1 - eout((t - t0) / 0.4)) * 14, a)

# ---------- stage ----------
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
def stage(top=BG1, bot=BG0, spot=(540, 980, 520, 760), spot_col=WARM, spot_a=0.16, cone=None, floor_y=None, floor_col=(46, 36, 54), cone_col=WARM, cone_a=60):
    g = np.array(top, np.float32) * (1 - _yy[..., None] / H) + np.array(bot, np.float32) * (_yy[..., None] / H)
    if spot:
        sx, sy, rx, ry = spot; m = np.exp(-(((_xx - sx) / rx) ** 2 + ((_yy - sy) / ry) ** 2))[..., None]
        g = g + m * np.array(spot_col, np.float32) * spot_a
    if floor_y:
        fm = (_yy >= floor_y)[..., None]; fl = np.array(floor_col, np.float32) * (0.85 + 0.15 * np.clip((_yy - floor_y) / 600, 0, 1))[..., None]
        g = np.where(fm, fl, g)
    vig = (1 - 0.45 * np.clip((((_xx - 540) / 760) ** 2 + ((_yy - 960) / 1150) ** 2) ** 1.4, 0, 1))[..., None]
    im = Image.fromarray(np.clip(g * vig, 0, 255).astype(np.uint8)).convert("RGBA")
    if cone:                                                                                          # a light cone from above
        cx, top_w, bot_w, y1 = cone; c = Image.new("L", (W, H), 0)
        ImageDraw.Draw(c).polygon([(cx - top_w, 0), (cx + top_w, 0), (cx + bot_w, y1), (cx - bot_w, y1)], fill=cone_a)
        lay = Image.new("RGBA", (W, H), tuple(cone_col) + (0,)); lay.putalpha(c.filter(ImageFilter.GaussianBlur(40))); im.alpha_composite(lay)
    return im

def floor_glow(im, cx, cy, rx, ry, a=110, col=WARM):
    lay = Image.new("RGBA", (int(rx * 2 + 120), int(ry * 2 + 120)), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((60, 60, 60 + 2 * rx, 60 + 2 * ry), fill=col + (a,)); put(im, lay.filter(ImageFilter.GaussianBlur(30)), cx, cy)

def camera(im, t, t0, t1, z0=1.0, z1=1.05, focus=(540, 960)):
    k = ease((t - t0) / max(0.01, t1 - t0)); z = z0 + (z1 - z0) * k
    if abs(z - 1) < 0.002: return im
    w, h = W / z, H / z; l = clamp(focus[0] - w / 2, 0, W - w); tp = clamp(focus[1] - h / 2, 0, H - h)
    return im.crop((int(l), int(tp), int(l + w), int(tp + h))).resize((W, H), Image.BICUBIC)

def zoom_through(a_im, b_im, k):
    """transition: outgoing pushes in and fades, incoming settles from slightly small"""
    k = ease(k); za = 1 + 0.22 * k; zb = 0.9 + 0.1 * k
    def z(im, s, alpha):
        if s >= 1:
            w, h = W / s, H / s; c = im.crop((int((W - w) / 2), int((H - h) / 2), int((W + w) / 2), int((H + h) / 2))).resize((W, H), Image.BILINEAR)
        else:
            c = Image.new("RGB", (W, H), BG0); sm = im.resize((int(W * s), int(H * s)), Image.BILINEAR); c.paste(sm, ((W - sm.width) // 2, (H - sm.height) // 2))
        return c
    A = z(a_im.convert("RGB"), za, 1); B = z(b_im.convert("RGB"), zb, 1)
    return Image.blend(A, B, k)

# ---------- props ----------
def bean(col, mood="happy", s=230, look=0.0, talk=0.0, blink=False):
    """a round character: body, eyes that look sideways, a mouth for happy / sad / talk"""
    im = Image.new("RGBA", (s, int(s * 1.15)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * 0.08, s * 0.1, s * 0.92, s * 1.12), radius=int(s * 0.38), fill=col + (255,))
    hl = tuple(min(255, c + 40) for c in col); d.ellipse((s * 0.22, s * 0.2, s * 0.42, s * 0.34), fill=hl + (120,))
    ex = s * 0.07 * look
    for cx in (0.37, 0.63):
        x = s * cx; y = s * 0.5
        if blink: d.line([(x - s * 0.07, y), (x + s * 0.07, y)], fill=INK + (255,), width=max(3, s // 40))
        else:
            d.ellipse((x - s * 0.085, y - s * 0.1, x + s * 0.085, y + s * 0.1), fill=(255, 255, 255, 255))
            d.ellipse((x - s * 0.045 + ex, y - s * 0.04, x + s * 0.045 + ex, y + s * 0.06), fill=INK + (255,))
    mx, my = s * 0.5, s * 0.74; w = max(3, s // 36)
    if mood == "sad": d.arc((mx - s * 0.12, my, mx + s * 0.12, my + s * 0.16), 200, 340, fill=INK + (255,), width=w)
    elif talk > 0.05: d.ellipse((mx - s * 0.07, my - s * 0.02, mx + s * 0.07, my + s * 0.02 + s * 0.1 * talk), fill=INK + (255,))
    else: d.arc((mx - s * 0.13, my - s * 0.1, mx + s * 0.13, my + s * 0.1), 20, 160, fill=INK + (255,), width=w)
    for cx in (0.25, 0.75): d.ellipse((s * cx - s * 0.06, s * 0.66, s * cx + s * 0.06, s * 0.72), fill=(255, 120, 140, 90))
    return im

def bubble(text, size=46, fill=WHITE, tcol=INK, tail="left", font=None):
    t = tl(text, font or sans(size, 700), tcol); w, h = t.width + 56, t.height + 34
    im = Image.new("RGBA", (w, h + 26), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, w - 1, h - 1), radius=min(30, h // 2), fill=fill + (255,))
    tx = w * (0.25 if tail == "left" else 0.75); d.polygon([(tx - 16, h - 2), (tx + (10 if tail == "left" else -10) - 2, h + 24), (tx + 16, h - 2)], fill=fill + (255,))
    im.alpha_composite(t, (28, 15)); return im

def price_tag(text, w=250, h=118, fill=CREAM, tcol=INK, f=None):
    im = Image.new("RGBA", (w + 6, h + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(46, 0), (w, 0), (w, h), (46, h), (0, h / 2)], fill=fill + (255,)); d.ellipse((24, h / 2 - 11, 46, h / 2 + 11), fill=(60, 48, 60, 255))
    t = tl(text, f or serif(int(h * 0.56)), tcol); im.alpha_composite(t, (int(46 + (w - 46 - t.width) / 2), int((h - t.height) / 2 - 4))); return im

def stamp(text, col=VIO, size=74, rot=-10):
    t = tl(text, sans(size, 700), col); w, h = t.width + 60, t.height + 34
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, w - 4, h - 4), radius=14, outline=col + (255,), width=7); im.alpha_composite(t, (30, 13))
    return im.rotate(rot, expand=True, resample=Image.BICUBIC)

def paddle(n, col=VIO, s=110):
    im = Image.new("RGBA", (s, int(s * 1.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * 0.44, s * 0.85, s * 0.56, s * 1.85), radius=6, fill=(120, 86, 60, 255))
    d.ellipse((0, 0, s - 1, s - 1), fill=col + (255,)); d.ellipse((8, 8, s - 9, s - 9), outline=(255, 255, 255, 120), width=3)
    t = tl(str(n), sans(int(s * 0.38), 700), WHITE); im.alpha_composite(t, ((s - t.width) // 2, (s - t.height) // 2 - 3)); return im

def pedestal(w=380, h=330, col=(92, 86, 104)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((20, 30, w - 20, h), fill=col + (255,)); d.rectangle((0, 0, w, 40), fill=tuple(min(255, c + 30) for c in col) + (255,))
    d.rectangle((20, 40, w - 20, 52), fill=tuple(max(0, c - 25) for c in col) + (255,)); return im

def plaque(small, big, w=560):
    im = Image.new("RGBA", (w, 132), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, w - 1, 131), radius=10, fill=(226, 208, 168, 255))
    d.rounded_rectangle((6, 6, w - 7, 125), radius=8, outline=(170, 146, 100, 255), width=2)
    a = tl(small, serif(32, True), (110, 90, 60)); b = tl(big, sans(38, 700), INK)
    im.alpha_composite(a, ((w - a.width) // 2, 14)); im.alpha_composite(b, ((w - b.width) // 2, 62)); return im

def bulbs_row(w, t, n=22, seed=0):
    im = Image.new("RGBA", (w, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = np.random.default_rng(seed)
    ph = r.uniform(0, 6.28, n)
    for i in range(n):
        x = 14 + (w - 28) * i / (n - 1); a = 0.55 + 0.45 * np.sin(t * 4 + ph[i])
        d.ellipse((x - 7, 13, x + 7, 27), fill=(255, 224, 160, int(255 * a)))
    g = im.filter(ImageFilter.GaussianBlur(6)); g.alpha_composite(im); return g

def radio(s=360):
    im = Image.new("RGBA", (s, int(s * 0.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w, h = s, int(s * 0.9)
    d.arc((w * 0.22, h * 0.0, w * 0.78, h * 0.38), 180, 360, fill=(90, 60, 40, 255), width=int(s * 0.04))
    d.rounded_rectangle((0, h * 0.18, w, h), radius=int(s * 0.1), fill=(158, 98, 60, 255))
    d.rounded_rectangle((w * 0.05, h * 0.24, w * 0.95, h * 0.94), radius=int(s * 0.07), fill=(176, 116, 74, 255))
    d.ellipse((w * 0.1, h * 0.34, w * 0.5, h * 0.86), fill=(232, 214, 176, 255))
    for i in range(7):
        y = h * 0.4 + i * h * 0.064; d.line([(w * 0.15, y), (w * 0.45, y)], fill=(160, 130, 96, 255), width=4)
    d.rounded_rectangle((w * 0.56, h * 0.36, w * 0.9, h * 0.56), radius=10, fill=(240, 222, 170, 255))
    for i in range(6): x = w * 0.6 + i * w * 0.05; d.line([(x, h * 0.4), (x, h * 0.46)], fill=(120, 90, 60, 255), width=3)
    d.line([(w * 0.7, h * 0.38), (w * 0.72, h * 0.54)], fill=(200, 40, 40, 255), width=4)
    for cx in (0.64, 0.82): d.ellipse((w * cx - s * 0.06, h * 0.64, w * cx + s * 0.06, h * 0.64 + s * 0.12), fill=(80, 54, 36, 255))
    return im

def laser_pointer(s=520, beam=0.0):
    im = Image.new("RGBA", (s, int(s * 0.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); h = im.height
    d.rounded_rectangle((s * 0.08, h * 0.32, s * 0.86, h * 0.68), radius=int(h * 0.18), fill=(150, 156, 170, 255))
    d.rectangle((s * 0.08, h * 0.36, s * 0.86, h * 0.42), fill=(200, 206, 220, 255))
    d.rounded_rectangle((s * 0.82, h * 0.36, s * 0.92, h * 0.64), radius=6, fill=(70, 74, 86, 255))
    d.ellipse((s * 0.9, h * 0.44, s * 0.94, h * 0.56), fill=(220, 40, 40, 255))
    d.rounded_rectangle((s * 0.4, h * 0.24, s * 0.5, h * 0.34), radius=4, fill=(220, 50, 50, 255))
    d.line([(s * 0.58, h * 0.32), (s * 0.62, h * 0.48), (s * 0.6, h * 0.56), (s * 0.65, h * 0.68)], fill=(40, 42, 52, 255), width=5)
    return im

def crt(title, lines, w=640, h=520, t=0.0):
    im = Image.new("RGBA", (w, h + 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), radius=34, fill=(214, 204, 178, 255)); d.rounded_rectangle((34, 30, w - 34, h - 70), radius=22, fill=(26, 34, 46, 255))
    d.rectangle((w * 0.36, h, w * 0.64, h + 40), fill=(190, 180, 154, 255)); d.rounded_rectangle((w * 0.22, h + 40, w * 0.78, h + 70), radius=10, fill=(204, 194, 168, 255))
    sx, sy, sw = 60, 56, w - 120
    d.rectangle((sx, sy, sx + sw, sy + 46), fill=(190, 194, 206, 255)); im.alpha_composite(tl(title, mono(24), (24, 26, 40)), (sx + 16, sy + 10))
    for i, (txt, col) in enumerate(lines): im.alpha_composite(tl(txt, mono(24), col), (sx + 16, sy + 76 + i * 44))
    if int(t * 2.4) % 2 == 0: d.rectangle((sx + 16, sy + 76 + len(lines) * 44 + 4, sx + 30, sy + 76 + len(lines) * 44 + 30), fill=(120, 230, 150, 255))
    d.ellipse((w - 90, h - 50, w - 70, h - 30), fill=(90, 200, 120, 255)); return im

def paper(w=820, h=1020):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rectangle((0, 0, w, h), fill=CREAM + (255,))
    r = np.random.default_rng(3); a = np.asarray(im).copy(); n = r.normal(0, 5, a.shape[:2]); a[..., :3] = np.clip(a[..., :3] + n[..., None], 0, 255); im = Image.fromarray(a)
    return im

def phone_frame(screen, w=520):
    s = w / 1080; sh = screen.resize((w, int(screen.height * s)), Image.LANCZOS); pad = 18
    im = Image.new("RGBA", (w + 2 * pad, sh.height + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=70, fill=(18, 18, 22, 255), outline=(90, 92, 104, 255), width=3)
    m = Image.new("L", sh.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sh.width - 1, sh.height - 1), radius=56, fill=255)
    im.paste(sh, (pad, pad), m); return im

# ---------- sound ----------
class Snd:
    def __init__(self, total):
        self.n = int(total * SR); self.buf = np.zeros(self.n); self.rng = np.random.default_rng(5)
    def tt(self, d): return np.arange(int(d * SR)) / SR
    def lp(self, x, k): return np.convolve(x, np.ones(k) / k, "same")
    def fadd(self, sig, at, g=1.0):
        i = int(at * SR); j = min(self.n, i + len(sig))
        if 0 <= i < self.n: self.buf[i:j] += sig[: j - i] * g
    def whoosh(self, at, d=0.4, g=0.12):
        y = self.tt(d); self.fadd(self.lp(self.rng.normal(0, 1, len(y)), 6) * np.sin(np.pi * y / d) ** 2, at, g)
    def pop(self, at, g=0.1, f0=500):
        y = self.tt(0.12); self.fadd(np.sin(2 * np.pi * np.cumsum(f0 + 1400 * y / 0.12) / SR) * np.exp(-y * 30), at, g)
    def tick(self, at, g=0.05, f=2600):
        y = self.tt(0.02); self.fadd(np.sin(2 * np.pi * f * y) * np.exp(-y * 300), at, g)
    def thud(self, at, g=0.3):
        y = self.tt(0.35); self.fadd(np.sin(2 * np.pi * np.cumsum(60 + 70 * np.exp(-y * 25)) / SR) * np.exp(-y * 12) + self.lp(self.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 60) * 0.4, at, g)
    def ding(self, at, f=1568, g=0.08):
        y = self.tt(1.2); self.fadd(sum(np.sin(2 * np.pi * f * m * y) * np.exp(-y * dd) * a for m, dd, a in ((1, 3.5, 1), (2.0, 6, .35), (3.0, 9, .15))), at, g)
    def key(self, at, g=0.04):
        y = self.tt(0.03); f = 1800 + self.rng.uniform(-300, 400); self.fadd((self.rng.normal(0, 1, len(y)) * 0.5 + np.sin(2 * np.pi * f * y)) * np.exp(-y * 240), at, g)
    def write(self, path, master=0.9):
        import wave
        out = self.buf.copy(); out[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR)) ** 1.5
        out = out / (np.max(np.abs(out)) + 1e-9) * master
        with wave.open(path, "wb") as w_:
            w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

def note(m): return 440.0 * 2 ** ((m - 69) / 12)
def pluck(f, dur, bright=0.5, rng=None):
    rng = rng or np.random.default_rng(1); n = int(dur * SR); p = max(2, int(SR / f)); out = np.zeros(n + p)
    buf = rng.uniform(-1, 1, p); buf = np.convolve(buf, np.ones(3) / 3, "same") * (1 - bright) + buf * bright; out[:p] = buf
    for i in range(p, n + p, p):
        prev = out[i - p:i]; nxt = 0.5 * (prev + np.roll(prev, 1)) * 0.996; j = min(n + p, i + p); out[i:j] = nxt[: j - i]
    return out[p:p + n] * np.minimum(1, np.arange(n) / (0.002 * SR))

def music(total, bpm=92, seed=4):
    """a curious, warm explainer bed: soft kick, brushed shaker, plucked marimba-ish arpeggio in F major/D minor, sub"""
    rng = np.random.default_rng(seed); n = int(total * SR); out = np.zeros(n); e = 60 / bpm / 2
    def add(sig, at, g):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += sig[: j - i] * g
    prog = [(53, [65, 69, 72, 76]), (50, [62, 65, 69, 72]), (46, [62, 65, 70, 74]), (48, [64, 67, 72, 76])]   # F, Dm, Bb, C
    k = 0; t = 0.0
    while t < total:
        bar = (k // 8) % 4; root, ch = prog[bar]; st = k % 8
        if st in (0, 4):
            y = np.arange(int(0.3 * SR)) / SR; add(np.sin(2 * np.pi * np.cumsum(50 + 60 * np.exp(-y * 30)) / SR) * np.exp(-y * 14), t, 0.32)
        y = np.arange(int(0.05 * SR)) / SR; add(np.convolve(rng.normal(0, 1, len(y)), [1, -0.95], "same") * np.exp(-y * 80), t, 0.035 if st % 2 else 0.02)
        m = ch[[0, 2, 1, 3, 2, 1, 3, 2][st]]
        add(pluck(note(m), 0.5, 0.35, rng) * np.exp(-np.arange(int(0.5 * SR)) / SR * 7), t, 0.12)
        if st == 0: add(pluck(note(root - 12), 1.2, 0.25, rng) * np.exp(-np.arange(int(1.2 * SR)) / SR * 2.5), t, 0.35)
        k += 1; t = k * e
    x = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * note(m) * x + i) * a for i, (m, a) in enumerate(((53, .5), (60, .3), (65, .25), (69, .2))))
    return out + pad * 0.025
