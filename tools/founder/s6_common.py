"""Season 6 (bags, rooftop nights) kit. Owner: 'keep the motions classy', 'I wanna be vibing' (S1/S2 ambiance).
Warm night grade with a soft bloom on the string lights and a slow light leak; frosted-glass cards with hairline
borders, champagne mono labels and violet accents; slow eased fades and small rises (no stamps, bounces or shakes);
frosted captions; a deep-house groove (soft kick, off-beat hats, Rhodes chords in A minor, sub bass, gentle pump)
ducked under every word; an end card on the blurred last frame with drifting bokeh."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
import mhelpers as M
from founder_common import W, H, SR, WHITE, Mix

CHAMP = (236, 220, 190); VIO = (167, 139, 250); LAV = (205, 194, 255); INK = (12, 14, 26)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)

def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def fade(t, t0, t1, fin=0.55, fout=0.45):
    """0→1 over fin after t0, 1→0 over fout before t1"""
    return ease((t - t0) / fin) * (1 - ease((t - (t1 - fout)) / fout))

# ---------- grade ----------
_x = np.linspace(0, 1, 256).astype(np.float32)
_S = np.clip(0.5 + (_x - 0.5) * 1.08, 0, 1)
_LUT = [np.clip(_S * 1.03 + 0.012, 0, 1), np.clip(_S * 1.0, 0, 1), np.clip(_S * 0.95 + 0.03 * (1 - _x) ** 2, 0, 1)]
_SHADOW = (np.clip(1 - _x / 0.3, 0, 1) ** 1.6 * 0.35).astype(np.float32)
_VIG = (1 - 0.32 * np.clip((((_xx - 540) / 720) ** 2 + ((_yy - 900) / 1100) ** 2) ** 1.3, 0, 1))[..., None].astype(np.float32)
_INK01 = np.array(INK, np.float32) / 255
def night_grade(fr, bloom=0.32):
    u = np.asarray(fr.convert("RGB")); lum8 = (u.astype(np.uint16).sum(-1) // 3).astype(np.uint8)
    c = np.stack([_LUT[i][u[..., i]] for i in range(3)], -1)
    sh = _SHADOW[lum8][..., None]; c = c * (1 - sh) + _INK01 * sh
    l2 = c.mean(-1, keepdims=True); c = l2 + (c - l2) * 1.07
    out = c * _VIG
    if bloom:
        small = Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8)).resize((W // 4, H // 4), Image.BILINEAR)
        a = np.asarray(small, np.float32) / 255; hi = np.clip((a.mean(-1, keepdims=True) - 0.62) / 0.38, 0, 1) * a
        g = np.asarray(Image.fromarray((hi * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR), np.float32) / 255
        out = 1 - (1 - out) * (1 - g * bloom)                                                         # screen
    return Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8)).convert("RGBA")

_LEAK = None
def light_leak(im, t, strength=0.16, side=1):
    """a slow warm light leak drifting along one edge (computed at 1/4 size, it is soft anyway)"""
    global _LEAK
    w4, h4 = W // 4, H // 4
    if _LEAK is None:
        yy, xx = np.mgrid[0:h4 * 2, 0:w4].astype(np.float32)
        _LEAK = np.exp(-(((xx - 0) / 65) ** 2 + ((yy - h4) / 130) ** 2)).astype(np.float32)
    dy = int(55 * np.sin(t * 0.35)); a = _LEAK[h4 // 2 - dy: h4 // 2 - dy + h4]
    if side < 0: a = a[:, ::-1]
    col = np.array([255, 170, 110], np.float32) * (0.75 + 0.25 * np.sin(t * 0.5)) + np.array([0, 0, 40], np.float32) * (0.5 + 0.5 * np.sin(t * 0.3 + 1))
    lay = np.dstack([np.broadcast_to(np.clip(col, 0, 255), (h4, w4, 3)), (a * 255 * strength)[..., None]]).astype(np.uint8)
    im.alpha_composite(Image.fromarray(lay, "RGBA").resize((W, H), Image.BILINEAR)); return im

def shield(im, box, k=1.0, radius=30, tint=(10, 12, 24), dark=0.5, blur=18, border=110):
    """frosted glass behind a card: blur what's under it, tint it, hairline border"""
    if k <= 0.01: return
    x0, y0, x1, y1 = [int(v) for v in box]; x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W, x1), min(H, y1)
    if x1 - x0 < 4 or y1 - y0 < 4: return
    reg = im.crop((x0 - 0, y0, x1, y1)).convert("RGB").resize(((x1 - x0) // 3 + 1, (y1 - y0) // 3 + 1), Image.BILINEAR).filter(ImageFilter.GaussianBlur(blur / 3)).resize((x1 - x0, y1 - y0), Image.BILINEAR)
    a = np.asarray(reg, np.float32) * (1 - dark) + np.array(tint, np.float32) * dark
    glass = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", glass.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, glass.width - 1, glass.height - 1), radius=radius, fill=int(255 * k))
    im.paste(glass, (x0, y0), m)
    ln = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0)); ImageDraw.Draw(ln).rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=radius, outline=(255, 255, 255, int(border * k)), width=2)
    im.alpha_composite(ln, (x0, y0))

def mono(text, size=24, col=CHAMP, tracking=None):
    return R.text_layer(text, R.font(size, mono=True), col, tracking=tracking if tracking is not None else max(3, int(size * 0.28)))

def text(t, size=40, weight=500, col=WHITE):
    return R.text_layer(t, R.font(size, weight), col)

def place(im, layer, cx, cy, a, rise=16):
    """classy entrance: fade with a small rise"""
    if a <= 0.01: return
    R.paste_center(im, layer, cx, cy + (1 - a) * rise, a)

def card(im, cx, cy, w, h, a, rows, radius=30, pad=30):
    """a frosted card at (cx, cy) with rows of (layer, align) stacked; a = 0..1 entrance"""
    if a <= 0.01: return
    y_off = (1 - a) * 16; box = (cx - w / 2, cy - h / 2 + y_off, cx + w / 2, cy + h / 2 + y_off)
    shield(im, box, a, radius)
    y = box[1] + pad
    for lay, align, gap in rows:
        if lay is None: y += gap; continue
        x = box[0] + pad if align == "l" else (box[2] - pad - lay.width if align == "r" else cx - lay.width / 2)
        if a < 0.999:
            lay = lay.copy(); al = lay.getchannel("A").point(lambda v: int(v * a)); lay.putalpha(al)
        im.alpha_composite(lay, (int(x), int(y))); y += lay.height + gap

def hairline_ring(im, cx, cy, rx, ry, k, a=1.0, col=CHAMP, width=3):
    """a thin ellipse drawing itself around something (k = 0..1 of the stroke)"""
    if k <= 0 or a <= 0.01: return
    lay = Image.new("RGBA", (int(rx * 2 + 20), int(ry * 2 + 20)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.arc((10, 10, 10 + 2 * rx, 10 + 2 * ry), -90, -90 + 360 * k, fill=col + (int(235 * a),), width=width)
    R.paste_center(im, lay.filter(ImageFilter.GaussianBlur(0.6)), cx, cy)

def caption_layer(lines, size=56):
    f = R.font(size, 600); out = []
    for ln in lines:
        parts = []
        for chunk in ln.replace("[", "|[").replace("]", "]|").split("|"):
            if chunk: parts.append((chunk[1:-1], True) if chunk.startswith("[") else (chunk, False))
        layers = [R.text_layer(p, f, LAV if h else WHITE) for p, h in parts]
        w = sum(l.width for l in layers) - 4 * (len(layers) - 1); im = Image.new("RGBA", (w, max(l.height for l in layers)), (0, 0, 0, 0)); x = 0
        for l in layers: im.alpha_composite(l, (x, 0)); x += l.width - 4
        out.append(im)
    return out
_CAPS = {}
def captions(im, t, caps, y=1700, size=56):
    for t0, t1, lines in caps:
        if not (t0 <= t < t1): continue
        a = fade(t, t0, t1, 0.4, 0.3); key = (tuple(lines), size)
        if key not in _CAPS: _CAPS[key] = caption_layer(lines, size)
        ls = _CAPS[key]; w = max(l.width for l in ls) + 76; h = sum(l.height for l in ls) - 6 * (len(ls) - 1) + 40
        yy = y + (1 - a) * 12; shield(im, (W / 2 - w / 2, yy - h / 2, W / 2 + w / 2, yy + h / 2), a, 28, dark=0.55)
        cy = yy - h / 2 + 20
        for l in ls:
            if a < 0.999: l = l.copy(); l.putalpha(l.getchannel("A").point(lambda v: int(v * a)))
            im.alpha_composite(l, (int(W / 2 - l.width / 2), int(cy))); cy += l.height - 6

def blur_mark(fr, cx, cy, r=26, keep=None):
    """smooth away a small embossed mark on a bag (feathered round patch of blurred leather)"""
    box = (int(cx - r * 1.6), int(cy - r * 1.6), int(cx + r * 1.6), int(cy + r * 1.6))
    reg = fr.crop(box).filter(ImageFilter.GaussianBlur(r * 0.35))
    m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).ellipse((r * 0.3, r * 0.3, reg.width - r * 0.3, reg.height - r * 0.3), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(r * 0.25))
    if keep is not None:
        k = keep(np.asarray(fr.crop(box).convert("RGB"), np.int32))
        m = Image.fromarray((np.asarray(m, np.float32) * (1 - k)).astype(np.uint8))
    fr.paste(reg, box[:2], m); return fr

SKIN = lambda a: ((a[..., 0] - a[..., 2] > 40) & (a[..., 0] - a[..., 1] > 22) & (a[..., 1] > 70) & (a[..., 0] > 150)).astype(np.float32)

# ---------- end card ----------
_EC = {}
_rb = np.random.default_rng(42)
_BOKEH = [(_rb.uniform(0, W), _rb.uniform(0, H), _rb.uniform(16, 52), i) for i in range(24)]
def end_card(k, lines, END, last):
    """the blurred last frame, deepened, with drifting bokeh; Z mark, the lines, follow"""
    key = id(last)
    if _EC.get("key") != key:
        bg = last.convert("RGB").resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BILINEAR)
        a = np.asarray(bg, np.float32) * 0.42 + np.array([10, 10, 26], np.float32) * 0.58
        _EC.update(key=key, bg=Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA"))
    im = _EC["bg"].copy()
    bok = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0)); d = ImageDraw.Draw(bok)
    for x, y, r, i in _BOKEH:
        yy = (y - k * (14 + i % 5 * 6)) % H; xx = x + 20 * np.sin(k * 0.6 + i)
        col = (255, 196, 140) if i % 3 else (190, 170, 255)
        d.ellipse(((xx - r) / 2, (yy - r) / 2, (xx + r) / 2, (yy + r) / 2), fill=col + (int(30 + 16 * np.sin(k * 1.3 + i)),))
    im.alpha_composite(bok.filter(ImageFilter.GaussianBlur(1.5)).resize((W, H), Image.BILINEAR))
    z = R.z_mark(150); place(im, z, W / 2, 520, ease(k / 0.6), 20)
    place(im, mono("ROOFTOP NIGHTS  ·  SEASON 6", 24, CHAMP, 7), W / 2, 660, ease((k - 0.3) / 0.6))
    for i, line in enumerate(lines):
        place(im, text(line, 92, 700), W / 2, 790 + i * 112, ease((k - 0.55 - i * 0.3) / 0.6), 18)
    y0 = 790 + len(lines) * 112 + 30
    place(im, text("Live auctions for Lebanon. Coming soon.", 42, 500, (225, 226, 240)), W / 2, y0, ease((k - 1.4) / 0.6))
    fl = text("Follow @hyperbidz", 46, 700); w, h = fl.width + 110, fl.height + 50
    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(255, 255, 255, 236))
    pill.alpha_composite(text("Follow @hyperbidz", 46, 700, (42, 21, 128)), (55, 22))
    place(im, pill, W / 2, y0 + 150, ease((k - 1.8) / 0.6))
    out = im.convert("RGB")
    if k > END - 0.6: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), min(1, (k - (END - 0.6)) / 0.6))
    return out

# ---------- the groove ----------
BPM = 112
def note(n): return 440.0 * 2 ** ((n - 69) / 12)
CHORDS = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 52, 55, 59, 62], [55, 59, 62, 64, 67]]   # Am9, Fmaj9, Cmaj9, G6
ROOTS = [45, 41, 36, 43]

def groove(total, start=0.0, level=1.0, seed=3):
    """a deep-house loop rendered to a buffer (mono, SR): soft kick, off-beat hats, a clap on 2 and 4, Rhodes stabs, sub"""
    rng = np.random.default_rng(seed); n = int(total * SR); out = np.zeros(n); beat = 60 / BPM
    t = np.arange(n) / SR + start; ph = (t % beat) / beat
    pump = 1 - 0.45 * np.exp(-((t % beat)) / 0.11)
    def add(sig, at, g):
        i = int((at - start) * SR)
        if i >= n or i + len(sig) <= 0: return
        a = max(0, -i); i = max(0, i); j = min(n, i + len(sig) - a); out[i:j] += sig[a:a + j - i] * g
    nb = int(total / beat) + 2
    for b in range(nb):
        at = start + b * beat - (start % beat)
        y = np.arange(int(0.32 * SR)) / SR
        add(np.sin(2 * np.pi * np.cumsum(46 + 70 * np.exp(-y * 28)) / SR) * np.exp(-y * 9), at, 0.55)               # kick
        y = np.arange(int(0.05 * SR)) / SR; hz = np.diff(rng.normal(0, 1, len(y) + 1))
        add(hz * np.exp(-y * 90), at + beat / 2, 0.06)                                                         # off-beat hat
        if b % 4 in (1, 3):
            y = np.arange(int(0.18 * SR)) / SR; cl = np.convolve(rng.normal(0, 1, len(y)), np.ones(6) / 6, "same")
            add(cl * np.exp(-y * 22) * (1 + 0.5 * (y < 0.012)), at, 0.08)                                    # soft clap
    bar = beat * 4; nbar = int(total / bar) + 2
    for k in range(nbar):
        at = start + k * bar - (start % bar); ch = CHORDS[k % 4]; root = ROOTS[k % 4]
        for off, dur in ((0, beat * 1.4), (beat * 1.5, beat * 0.9), (beat * 2.5, beat * 1.4)):
            y = np.arange(int(dur * SR)) / SR; env = np.minimum(1, y / 0.01) * np.exp(-y * 2.6) * np.minimum(1, (y[-1] - y) / 0.05)
            s = sum((np.sin(2 * np.pi * note(m) * y) + 0.28 * np.sin(4 * np.pi * note(m) * y) + 0.08 * np.sin(6 * np.pi * note(m) * y)) for m in ch) / len(ch)
            add(s * env * (1 + 0.15 * np.sin(2 * np.pi * 5.2 * y)), at + off, 0.16)                         # Rhodes stab
        for off in (0, beat * 1.5, beat * 2, beat * 3.5):
            y = np.arange(int(beat * 0.45 * SR)) / SR; env = np.minimum(1, y / 0.01) * np.exp(-y * 5)
            add(np.sin(2 * np.pi * note(root - 12 + 12) * y) * env, at + off, 0.22)                           # sub
    out *= pump * level
    return out

class GrooveMix(Mix):
    """voice + ducked groove; the end card rides the groove out on a soft Am9 swell (no thud)"""
    def write(self, path):
        import wave
        fx = self.fx.copy(); fx[:len(self.duck)] *= (0.4 + 0.6 * self.duck)
        out = self.main + fx; out[:len(self.voice)] += self.voice
        x = self.tt(self.end); env2 = np.minimum(1, x / 0.6) * np.exp(-np.maximum(0, x - 2.0) * 0.9); i = int((self.clip + 0.05) * SR)
        chord = sum(np.sin(2 * np.pi * note(m) * x) * a for m, a in ((45, .35), (57, .3), (60, .22), (64, .22), (67, .16), (71, .12))) * env2 * 0.22
        out[i:i + len(chord)] += chord[: self.n - i]
        out[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR)) ** 1.5
        out = out / (np.max(np.abs(out)) + 1e-9) * 0.92
        with wave.open(path, "wb") as w_:
            w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

def chime(mx, at, f=1318.5, g=0.05):
    y = mx.tt(1.4); s = sum(np.sin(2 * np.pi * f * m * y) * np.exp(-y * d) * a for m, d, a in ((1, 2.5, 1), (2.0, 4, .3), (3.0, 6, .12)))
    mx.fadd(s, at, g)

def tag(text_, size=22, col=CHAMP):
    """a tiny frosted label (drawn standalone, not over the frame)"""
    lb = mono(text_, size, col, max(4, int(size * 0.3))); w, h = lb.width + 40, lb.height + 22
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(12, 14, 26, 170), outline=(255, 255, 255, 90), width=2)
    im.alpha_composite(lb, (20, (h - lb.height) // 2)); return im

def color_cutout(src, box, keep):
    """cut an object out of a frame by its colour (keep(arr) → 0..1 mask), feathered"""
    reg = src.crop(box).convert("RGB"); a = np.asarray(reg, np.int32)
    m = Image.fromarray((np.clip(keep(a), 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(2.5))
    out = reg.convert("RGBA"); out.putalpha(m); return out
