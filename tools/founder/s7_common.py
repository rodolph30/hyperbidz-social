"""Season 7 'The Envelope' kit (HyperBidz HQ office at night). A fun mystery season: a cool violet grade that keeps
the warm shelf LEDs, the wall Z that pulses on the big beats, a glowing wax seal on the envelope (brighter each
episode), typed hooks, a rolling number that gets redacted and flies into the envelope, focus brackets, a comment
composer, frosted captions, a playful 'sneaky' pizzicato groove with clock ticks, and a crisp HQ end card."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
from founder_common import W, H, SR, WHITE, Mix
import s6_common as K
import s5_common as V

VIO = (124, 92, 255); BLUE = (47, 123, 255); LAV = (205, 194, 255); INK = (9, 9, 20); MUTE = (190, 192, 210)
ease, fade, shield, mono, text, place, put, captions = K.ease, K.fade, K.shield, K.mono, K.text, K.place, K.put, K.captions

def pop(x):
    """a playful entrance with a small overshoot (this season is fun)"""
    x = min(1.0, max(0.0, x)); c = 1.9; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------- grade ----------
_x = np.linspace(0, 1, 256).astype(np.float32)
_S = np.clip(0.5 + (_x - 0.5) * 1.07, 0, 1)
_LUT = [np.clip(_S * 1.0 + 0.004, 0, 1), np.clip(_S * 0.985, 0, 1), np.clip(_S * 1.0 + 0.035 * (1 - _x) ** 2, 0, 1)]
_SHADOW = (np.clip(1 - _x / 0.28, 0, 1) ** 1.6 * 0.3).astype(np.float32)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_VIG = (1 - 0.26 * np.clip((((_xx - 540) / 740) ** 2 + ((_yy - 980) / 1100) ** 2) ** 1.3, 0, 1))[..., None].astype(np.float32)
_INK01 = np.array(INK, np.float32) / 255
def hq_grade(fr, bloom=0.24):
    u = np.asarray(fr.convert("RGB")); lum8 = (u.astype(np.uint16).sum(-1) // 3).astype(np.uint8)
    c = np.stack([_LUT[i][u[..., i]] for i in range(3)], -1)
    sh = _SHADOW[lum8][..., None]; c = c * (1 - sh) + _INK01 * sh
    l2 = c.mean(-1, keepdims=True); c = l2 + (c - l2) * 1.05
    out = c * _VIG
    if bloom:
        small = Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8)).resize((W // 4, H // 4), Image.BILINEAR)
        a = np.asarray(small, np.float32) / 255; hi = np.clip((a.mean(-1, keepdims=True) - 0.55) / 0.45, 0, 1) * a
        g = np.asarray(Image.fromarray((hi * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR), np.float32) / 255
        out = 1 - (1 - out) * (1 - g * bloom)
    return Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8)).convert("RGBA")

# ---------- the room reacts ----------
def z_glow(im, k, box=(110, 160, 530, 560)):
    """the wall Z flares (screen-blend a blurred copy of its own blue-violet pixels)"""
    if k <= 0.01: return im
    x0, y0, x1, y1 = box; reg = np.asarray(im.crop(box).convert("RGB"), np.float32)
    m = ((reg[..., 2] > 150) & (reg[..., 2] - reg[..., 0] > 30)).astype(np.uint8) * 255
    g = np.asarray(Image.fromarray(m).resize(((x1 - x0) // 2, (y1 - y0) // 2)).filter(ImageFilter.GaussianBlur(11)).resize((x1 - x0, y1 - y0), Image.BILINEAR), np.float32)[..., None] / 255
    g = g * (1 - np.clip(np.abs(np.mgrid[0:y1 - y0, 0:x1 - x0][1][..., None] - (x1 - x0) / 2) / ((x1 - x0) / 2) - 0.8, 0, 1) * 5)   # no hard edge at the box sides
    col = np.array([150, 130, 255], np.float32) / 255
    out = 255 - (255 - reg) * (1 - np.clip(g * k * 1.6, 0, 1) * col)
    im.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA"), (x0, y0)); return im

_GL = {}
def seal_glow(im, cx, cy, k, core=0.0):
    """violet light around the wax seal; k = halo strength, core = flash on the seal itself"""
    if k <= 0.01 and core <= 0.01: return
    if "h" not in _GL:
        h = Image.new("RGBA", (420, 300), (0, 0, 0, 0)); ImageDraw.Draw(h).ellipse((130, 105, 290, 195), fill=(140, 110, 255, 255)); _GL["h"] = h.filter(ImageFilter.GaussianBlur(38))
        c = Image.new("RGBA", (200, 140), (0, 0, 0, 0)); ImageDraw.Draw(c).ellipse((62, 48, 138, 92), fill=(215, 205, 255, 255)); _GL["c"] = c.filter(ImageFilter.GaussianBlur(9))
    if k > 0.01: R.paste_center(im, _GL["h"], cx, cy, min(1, k))
    if core > 0.01: R.paste_center(im, _GL["c"], cx, cy, min(1, core))

# ---------- type ----------
def typed_lines(lines, n, size=70, cursor=True):
    """lines = [[(text, highlighted), …], …]; shows the first n characters, a violet cursor after the last one"""
    f = R.font(size, 700); out = []; left = n; cur_at = None
    for li, parts in enumerate(lines):
        row = []
        for txt, hl in parts:
            s = txt[:max(0, left)]; left -= len(txt)
            if s: row.append(R.text_layer(s, f, LAV if hl else WHITE))
        out.append(row)
        if left <= 0 and cur_at is None: cur_at = li
    if cur_at is None: cur_at = len(lines) - 1
    full = [[R.text_layer(t, f, WHITE) for t, _ in parts] for parts in lines]
    w = max(sum(l.width - 4 for l in r) for r in full) + 30; lh = int(size * 1.18)
    im = Image.new("RGBA", (w, lh * len(lines)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for li, row in enumerate(out):
        x = 0
        for l in row: im.alpha_composite(l, (x, li * lh)); x += l.width - 4
        if cursor and li == cur_at:
            cur = Image.new("RGBA", (int(size * 0.09), int(size * 0.9)), VIO + (255,)); im.alpha_composite(cur, (x + 8, li * lh + int(size * 0.2)))
    return im

def lock_icon(s=30, col=LAV):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(2, s // 10)
    d.arc((s * 0.24, s * 0.04, s * 0.76, s * 0.62), 180, 360, fill=col + (255,), width=w)
    d.line([(s * 0.24, s * 0.33), (s * 0.24, s * 0.46)], fill=col + (255,), width=w); d.line([(s * 0.76, s * 0.33), (s * 0.76, s * 0.46)], fill=col + (255,), width=w)
    d.rounded_rectangle((s * 0.12, s * 0.44, s * 0.88, s * 0.98), radius=s // 8, fill=col + (255,))
    d.ellipse((s * 0.44, s * 0.6, s * 0.56, s * 0.74), fill=INK + (255,)); return im

def glass_layer(w, h, radius=34, fill=(14, 14, 30, 214), edge=(255, 255, 255, 70)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=fill)
    ln = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(ln).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, outline=edge, width=2)
    im.alpha_composite(ln); return im

def number_card(amount, redact, sealed, w=600, h=230):
    """THE NUMBER: a scrambling amount; redact 0..1 slides a bar over it; sealed swaps the label for a lock"""
    im = glass_layer(w, h)
    lab = mono("SEALED · OPENS LAUNCH NIGHT", 21, LAV, 4) if sealed else mono("THE NUMBER", 22, LAV, 6)
    if sealed: li = lock_icon(26); im.alpha_composite(li, ((w - lab.width - 36) // 2, 34)); im.alpha_composite(lab, ((w - lab.width - 36) // 2 + 36, 36))
    else: im.alpha_composite(lab, ((w - lab.width) // 2, 36))
    num = R.text_layer(amount, R.font(104, 700), WHITE); im.alpha_composite(num, ((w - num.width) // 2, 74))
    if redact > 0:
        bw = int((w - 90) * redact); bar = Image.new("RGBA", (max(1, bw), 122), (0, 0, 0, 0)); bd = ImageDraw.Draw(bar)
        bd.rounded_rectangle((0, 0, max(1, bw) - 1, 121), radius=18, fill=(4, 4, 10, 255))
        if bw > 30: bd.rounded_rectangle((0, 0, bw - 1, 121), radius=18, outline=VIO + (230,), width=3)
        im.alpha_composite(bar, (45, 84))
    return im

def brackets(im, box, k, a, col=WHITE, L=38, width=5):
    """camera focus corners snapping in around something (k = 0..1 travel)"""
    if a <= 0.01: return
    x0, y0, x1, y1 = box; o = (1 - k) * 46; lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = col + (int(255 * a),)
    for sx, sy, x, y in ((1, 1, x0 - o, y0 - o), (-1, 1, x1 + o, y0 - o), (1, -1, x0 - o, y1 + o), (-1, -1, x1 + o, y1 + o)):
        d.line([(x, y + sy * L), (x, y), (x + sx * L, y)], fill=c, width=width, joint="curve")
    im.alpha_composite(lay)

def qmarks(t, size=54):
    """'$ ? ? ?' with the question marks bobbing out of phase"""
    f = R.font(size, 700); parts = [R.text_layer("$", f, WHITE)] + [R.text_layer("?", f, LAV) for _ in range(3)]
    w = sum(p.width for p in parts) + 18 * 3; im = Image.new("RGBA", (w, size + 30), (0, 0, 0, 0)); x = 0
    for i, p in enumerate(parts):
        dy = 0 if i == 0 else -7 * max(0, np.sin(t * 7 - i * 0.9)); im.alpha_composite(p, (x, int(10 + dy))); x += p.width + 18
    return im

def bubble_icon(s=34, col=LAV):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(2, s // 11)
    d.rounded_rectangle((s * 0.06, s * 0.08, s * 0.94, s * 0.72), radius=s // 4, outline=col + (255,), width=w)
    d.polygon([(s * 0.26, s * 0.68), (s * 0.24, s * 0.94), (s * 0.48, s * 0.70)], fill=col + (255,)); return im

def you_avatar(s=74):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    im.paste(V.lin_grad(s, s, BLUE, VIO), (0, 0), m); d = ImageDraw.Draw(im)
    d.ellipse((s * 0.36, s * 0.2, s * 0.64, s * 0.48), fill=(255, 255, 255, 235)); d.pieslice((s * 0.2, s * 0.54, s * 0.8, s * 1.14), 180, 360, fill=(255, 255, 255, 235))
    return im

def composer(cursor_on, typed="", w=820, h=112):
    """an Instagram-style comment field: you · 'Your guess:' · $ … cursor · send"""
    im = glass_layer(w, h, radius=h // 2, fill=(16, 16, 34, 226), edge=(205, 194, 255, 120))
    im.alpha_composite(you_avatar(76), (18, (h - 76) // 2))
    a = R.text_layer("Your guess:", R.font(42, 600), MUTE); im.alpha_composite(a, (116, (h - a.height) // 2 - 4))
    d = R.text_layer("$" + typed, R.font(46, 700), WHITE); x = 116 + a.width + 16; im.alpha_composite(d, (x, (h - d.height) // 2 - 4))
    if cursor_on: im.alpha_composite(Image.new("RGBA", (5, 50), VIO + (255,)), (x + d.width + 6, (h - 50) // 2))
    b = Image.new("RGBA", (84, 84), (0, 0, 0, 0)); m = Image.new("L", (84, 84), 0); ImageDraw.Draw(m).ellipse((0, 0, 83, 83), fill=255)
    b.paste(V.lin_grad(84, 84, BLUE, VIO), (0, 0), m); bd = ImageDraw.Draw(b)
    bd.line([(42, 62), (42, 24)], fill=(255, 255, 255, 255), width=7); bd.line([(27, 38), (42, 23), (57, 38)], fill=(255, 255, 255, 255), width=7, joint="curve")
    im.alpha_composite(b, (w - 84 - 14, (h - 84) // 2)); return im

def part_tag(ep, total=7):
    return K.tag(f"THE ENVELOPE  ·  PART {ep}/{total}", 22, LAV)

# ---------- end card ----------
_EC = {}
def _bg():
    if "bg" in _EC: return _EC["bg"]
    top, bot = np.array([7, 7, 18], np.float32), np.array([16, 13, 36], np.float32)
    g = top + (bot - top) * (_yy / H)[..., None]
    g += np.exp(-(((_xx - 540) / 430) ** 2 + ((_yy - 600) / 380) ** 2))[..., None] * np.array([96, 78, 230], np.float32) * 0.55   # the Z's light on the wall
    for sx in (70, 1010):                                                                               # violet strips like the HQ wall
        g += np.exp(-((_xx - sx) / 7) ** 2)[..., None] * np.array([150, 120, 255], np.float32) * 0.75
        g += np.exp(-((_xx - sx) / 60) ** 2)[..., None] * np.array([90, 60, 230], np.float32) * 0.22
    g += np.exp(-(((_xx - 540) / 760) ** 2 + ((_yy - 2080) / 380) ** 2))[..., None] * np.array([255, 170, 90], np.float32) * 0.22   # shelf warmth
    _EC["bg"] = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA"); return _EC["bg"]

def envelope_icon(s=150, glow=1.0):
    w, h = s, int(s * 0.64); pad = 40; im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((pad + w * 0.32, pad + h * 0.3, pad + w * 0.68, pad + h * 0.78), fill=(140, 110, 255, int(200 * glow)))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(22)))
    d = ImageDraw.Draw(im); d.rounded_rectangle((pad, pad, pad + w, pad + h), radius=8, fill=(242, 232, 214, 255))
    ln = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(ln).line([(pad + 6, pad + 6), (pad + w / 2, pad + h * 0.55), (pad + w - 6, pad + 6)], fill=(196, 182, 160, 255), width=3); im.alpha_composite(ln)
    d = ImageDraw.Draw(im); r = s * 0.12; cx, cy = pad + w / 2, pad + h * 0.55
    d.ellipse((cx - r, cy - r * 0.92, cx + r, cy + r * 0.92), fill=(92, 62, 210, 255)); d.ellipse((cx - r * 0.62, cy - r * 0.56, cx + r * 0.62, cy + r * 0.56), outline=(150, 125, 255, 255), width=2)
    return im

def end_card7(k, lines, END, season_tag="THE ENVELOPE  ·  SEASON 7"):
    im = _bg().copy()
    place(im, V.glow(520, 150, (110, 90, 255), 120), W / 2, 560, ease(k / 0.6) * (0.85 + 0.15 * np.sin(k * 2.2)), 0)
    place(im, envelope_icon(230, 0.7 + 0.3 * np.sin(k * 2.5)), W / 2, 560, ease(k / 0.6), 18)
    place(im, mono(season_tag, 24, (225, 222, 255), 7), W / 2, 760, ease((k - 0.3) / 0.6))
    for i, line in enumerate(lines):
        place(im, text(line, 80, 700, LAV if i == len(lines) - 1 else WHITE), W / 2, 900 + i * 100, ease((k - 0.55 - i * 0.3) / 0.6), 18)
    y0 = 900 + len(lines) * 100 + 60
    zm = V.zmark(60); hy, bz = R.text_layer("HYPER", R.font(50, 500), (215, 225, 255), tracking=6), R.text_layer("BIDZ", R.font(50, 700), WHITE, tracking=6)
    wm = Image.new("RGBA", (zm.width + 18 + hy.width + bz.width, max(zm.height, hy.height)), (0, 0, 0, 0)); wm.alpha_composite(zm, (0, (wm.height - zm.height) // 2))
    wm.alpha_composite(hy, (zm.width + 18, (wm.height - hy.height) // 2)); wm.alpha_composite(bz, (zm.width + 18 + hy.width, (wm.height - bz.height) // 2))
    place(im, wm, W / 2, y0, ease((k - 1.25) / 0.6))
    place(im, text("Live auctions for Lebanon. Coming soon.", 42, 500, (228, 230, 248)), W / 2, y0 + 84, ease((k - 1.45) / 0.6))
    fl = text("Follow @hyperbidz", 46, 700, (42, 21, 128)); w, h = fl.width + 110, fl.height + 50
    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(255, 255, 255, 255))
    pill.alpha_composite(fl, (55, 22)); place(im, pill, W / 2, y0 + 230, ease((k - 1.8) / 0.6))
    out = im.convert("RGB")
    if k > END - 0.6: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), min(1, (k - (END - 0.6)) / 0.6))
    return out

# ---------- sound: a sneaky pizzicato groove with clock ticks ----------
def note(m): return 440.0 * 2 ** ((m - 69) / 12)

def pluck(f, dur, bright=0.5, rng=None):
    """Karplus-Strong string, computed one period at a time"""
    rng = rng or np.random.default_rng(1); n = int(dur * SR); p = max(2, int(SR / f)); out = np.zeros(n + p)
    buf = rng.uniform(-1, 1, p); buf = np.convolve(buf, np.ones(3) / 3, "same") * (1 - bright) + buf * bright; out[:p] = buf
    for i in range(p, n + p, p):
        prev = out[i - p:i]; nxt = 0.5 * (prev + np.roll(prev, 1)) * 0.996; j = min(n + p, i + p); out[i:j] = nxt[: j - i]
    s = out[p:p + n]; env = np.minimum(1, np.arange(n) / (0.002 * SR)); return s * env

def sneaky(total, start=0.0, level=1.0, bpm=100, seed=5):
    rng = np.random.default_rng(seed); n = int(total * SR); out = np.zeros(n); e = 60 / bpm / 2       # eighth note
    def add(sig, at, g):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += sig[: j - i] * g
    bass = [50, None, 50, 53, 57, None, 56, 57, 50, None, 50, 53, 60, 58, 57, 55]                       # D minor with a sneaky G#
    top = {3: 69, 7: 68, 11: 69, 14: 72}
    k = 0; t = start
    while t < total:
        st = k % 16
        m = bass[st]
        if m: add(pluck(note(m - 12), 0.32, 0.35, rng) * np.exp(-np.arange(int(0.32 * SR)) / SR * 9), t, 0.55)
        if st in top and (k // 16) % 2 == 1: add(pluck(note(top[st]), 0.28, 0.6, rng) * np.exp(-np.arange(int(0.28 * SR)) / SR * 11), t, 0.16)
        y = np.arange(int(0.012 * SR)) / SR; add(np.sin(2 * np.pi * (3300 if k % 2 else 2500) * y) * np.exp(-y * 600), t, 0.05)   # clock tick-tock
        if st % 8 == 0:
            y = np.arange(int(0.3 * SR)) / SR; add(np.sin(2 * np.pi * np.cumsum(52 + 70 * np.exp(-y * 30)) / SR) * np.exp(-y * 13), t, 0.42)   # soft kick
        if st % 8 == 4:
            y = np.arange(int(0.09 * SR)) / SR; sn = np.convolve(rng.normal(0, 1, len(y)), [1, -1], "same") * np.exp(-y * 55); add(sn, t, 0.09)   # finger snap
        k += 1; t = start + k * e
    return out * level

class HQMix(Mix):
    """voice + ducked groove/fx; the end card lands on a pizzicato D major arpeggio and a soft chord"""
    def write(self, path):
        import wave
        fx = self.fx.copy(); fx[:len(self.duck)] *= (0.4 + 0.6 * self.duck)
        out = self.main + fx; out[:len(self.voice)] += self.voice
        rng = np.random.default_rng(3)
        for i, m in enumerate((50, 54, 57, 62, 66)):
            s = pluck(note(m), 1.2, 0.5, rng) * np.exp(-np.arange(int(1.2 * SR)) / SR * 3.5); j = int((self.clip + 0.06 + i * 0.09) * SR)
            out[j:j + len(s)] += s[: self.n - j] * 0.3
        x = self.tt(self.end); env2 = np.minimum(1, x / 0.5) * np.exp(-np.maximum(0, x - 1.8) * 0.9); i = int((self.clip + 0.1) * SR)
        chord = sum(np.sin(2 * np.pi * note(m) * x) * a for m, a in ((38, .35), (50, .3), (54, .22), (57, .22), (61, .14), (64, .12))) * env2 * 0.22
        out[i:i + len(chord)] += chord[: self.n - i]
        out[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR)) ** 1.5
        out = out / (np.max(np.abs(out)) + 1e-9) * 0.92
        with wave.open(path, "wb") as w_:
            w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

def key_click(mx, at, g=0.05):
    y = mx.tt(0.025); f = 1800 + mx.rng.uniform(-300, 400)
    mx.fadd((mx.rng.normal(0, 1, len(y)) * 0.5 + np.sin(2 * np.pi * f * y)) * np.exp(-y * 260), at, g)

def bubble_pop(mx, at, g=0.12):
    y = mx.tt(0.12); mx.fadd(np.sin(2 * np.pi * np.cumsum(500 + 1400 * y / 0.12) / SR) * np.exp(-y * 30), at, g)

def bips(mx, at, g=0.05):
    for d in (0, 0.09):
        y = mx.tt(0.05); mx.fadd(np.sin(2 * np.pi * 2093 * y) * np.exp(-y * 40), at + d, g)

# ---------- the crazy kit (owner, E3–E6: "I want something crazy") ----------
CORAL = (255, 92, 120)
CROWD_COLS = [(221, 92, 140), (109, 77, 255), (53, 126, 221), (46, 170, 140), (240, 150, 60), (150, 110, 255), (255, 110, 110), (70, 190, 220)]

def ease_in(x):
    x = min(1.0, max(0.0, x)); return x * x * x

def slam(x):
    """scale for a stamp slam: 2.2 → 1 with a tiny settle"""
    x = min(1.0, max(0.0, x)); return 1 + 1.2 * (1 - x) ** 3 - 0.05 * np.sin(np.pi * x) * (x > 0.6)

def shake_off(t, t0, amp=14, d=0.35, seed=0):
    k = (t - t0) / d
    if not 0 <= k < 1: return 0.0, 0.0
    a = amp * (1 - k) ** 2; return a * np.sin(t * 93 + seed), a * np.cos(t * 71 + seed * 2)

def shake(im, dx, dy, z=1.03):
    if abs(dx) < 0.3 and abs(dy) < 0.3: return im
    w, h = W / z, H / z; l = (W - w) / 2 + dx; tp = (H - h) / 2 + dy
    return im.crop((int(l), int(tp), int(l + w), int(tp + h))).resize((W, H), Image.BILINEAR)

def flash(im, a, col=(255, 255, 255)):
    if a > 0.01: im.alpha_composite(Image.new("RGBA", (W, H), col + (int(255 * min(1, a)),)))

_VG = {}
def vignette(im, a, col=CORAL):
    if a <= 0.01: return
    if "m" not in _VG:
        small = np.clip((((_xx[::4, ::4] - 540) / 600) ** 2 + ((_yy[::4, ::4] - 960) / 980) ** 2) - 0.3, 0, 1) ** 1.1
        _VG["m"] = Image.fromarray((small * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    lay = Image.new("RGBA", (W, H), col + (0,)); lay.putalpha(_VG["m"].point(lambda v: int(v * min(1, a)))); im.alpha_composite(lay)

def xmark(s=150, col=CORAL, w=24):
    im = Image.new("RGBA", (s + 30, s + 30), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for c, o, ww in (((0, 0, 0, 150), 6, w + 6), (col + (255,), 0, w)):
        L = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        dl.line([(15 + w, 15 + w + o), (15 + s - w, 15 + s - w + o)], fill=c, width=ww); dl.line([(15 + s - w, 15 + w + o), (15 + w, 15 + s - w + o)], fill=c, width=ww)
        im.alpha_composite(L.filter(ImageFilter.GaussianBlur(5)) if o else L)
    return im

def bid_chip(ini, amount, col, size=34):
    av = K.avatar(ini, col, 52); tx = R.text_layer(amount, R.font(size, 700), WHITE)
    h = 68; w = 8 + 52 + 14 + tx.width + 26
    im = glass_layer(w, h, h // 2, fill=(16, 16, 34, 238), edge=(205, 194, 255, 120))
    im.alpha_composite(av, (8, 8)); im.alpha_composite(tx, (74, (h - tx.height) // 2 - 3)); return im

def speed_lines(im, t, a, cx=540, cy=1090, n=46, seed=3):
    if a <= 0.01: return
    rng = np.random.default_rng(seed); lay = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(n):
        ang = rng.uniform(0, 2 * np.pi); sp = rng.uniform(900, 1700); ph = rng.uniform(0, 1); L = rng.uniform(80, 260)
        r0 = 160 + ((t * sp / 1000 + ph) % 1.0) * 1100
        x0, y0 = cx + np.cos(ang) * r0, cy + np.sin(ang) * r0; x1, y1 = cx + np.cos(ang) * (r0 + L), cy + np.sin(ang) * (r0 + L)
        d.line([(x0 / 2, y0 / 2), (x1 / 2, y1 / 2)], fill=(215, 205, 255, int(150 * a)), width=2)
    im.alpha_composite(lay.resize((W, H), Image.BILINEAR))

def ring_timer(frac, label, hot=0.0, s=300):
    im = Image.new("RGBA", (s + 60, s + 60), (0, 0, 0, 0)); c = (s + 60) / 2; r = s / 2
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((c - r, c - r, c + r, c + r), fill=(255, 70, 100, int(110 * hot)))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26)))
    d = ImageDraw.Draw(im); d.ellipse((c - r + 10, c - r + 10, c + r - 10, c + r - 10), fill=(14, 14, 30, 242))
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    dl.arc((c - r + 4, c - r + 4, c + r - 4, c + r - 4), 0, 360, fill=(255, 255, 255, 40), width=12)
    col = tuple(int(a + (b - a) * hot) for a, b in zip(VIO, (255, 80, 110)))
    if frac > 0: dl.arc((c - r + 4, c - r + 4, c + r - 4, c + r - 4), -90, -90 + 360 * frac, fill=col + (255,), width=12)
    im.alpha_composite(L); tl = R.text_layer(label, R.font(104, 700), WHITE); im.alpha_composite(tl, (int(c - tl.width / 2), int(c - tl.height / 2 - 8)))
    return im

def big(text_, size=220, col=WHITE, glow=None):
    tl = R.text_layer(text_, R.font(size, 700), col)
    if not glow: return tl
    im = Image.new("RGBA", (tl.width + 120, tl.height + 120), (0, 0, 0, 0)); g = Image.new("RGBA", im.size, (0, 0, 0, 0))
    g.paste(glow + (210,), (60, 60), tl.getchannel("A")); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(26))); im.alpha_composite(tl, (60, 60)); return im

# sounds
def buzzer(mx, at, g=0.22, d=0.55):
    y = mx.tt(d); s = sum(np.sign(np.sin(2 * np.pi * f * y)) for f in (110, 116.5, 221)) / 3
    mx.fadd(mx.lp(s, 6) * np.minimum(1, y / 0.01) * np.clip((d - y) / 0.06, 0, 1), at, g)

def ding(mx, at, f=1568, g=0.08):
    y = mx.tt(1.0); mx.fadd(sum(np.sin(2 * np.pi * f * m * y) * np.exp(-y * dd) * a for m, dd, a in ((1, 4, 1), (2.0, 6, .4), (3.01, 9, .2))), at, g)

def impact(mx, at, g=0.45):
    y = mx.tt(1.0); boom = np.sin(2 * np.pi * np.cumsum(38 + 90 * np.exp(-y * 18)) / SR) * np.exp(-y * 4.5)
    mx.fadd(boom + mx.lp(mx.rng.normal(0, 1, len(y)), 3) * np.exp(-y * 14) * 0.5, at, g)

def riser(mx, t0, t1, g=0.12, f0=200, f1=1600):
    D = t1 - t0; y = mx.tt(D); k = y / D; f = f0 + (f1 - f0) * k ** 2
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + mx.lp(mx.rng.normal(0, 1, len(y)), 4) * 0.5; mx.fadd(s * k ** 1.5, t0, g)

def heartbeat(mx, at, g=0.55):
    for d, a in ((0, 1), (0.17, 0.7)):
        y = mx.tt(0.28); mx.fadd(np.sin(2 * np.pi * np.cumsum(42 + 34 * np.exp(-y * 25)) / SR) * np.exp(-y * 15) * a, at + d, g)

def coin(mx, at, g=0.04):
    y = mx.tt(0.18); f = 2600 + mx.rng.uniform(-200, 500); mx.fadd((np.sin(2 * np.pi * f * y) + 0.5 * np.sin(2 * np.pi * f * 1.5 * y)) * np.exp(-y * 28), at, g)

def gavel(mx, at, g=0.5):
    y = mx.tt(0.5); s = np.sin(2 * np.pi * np.cumsum(90 + 120 * np.exp(-y * 40)) / SR) * np.exp(-y * 18)
    s += mx.lp(mx.rng.normal(0, 1, len(y)), 1) * np.exp(-y * 70) * 0.8; mx.fadd(s, at, g)

def shockwave(im, cx, cy, k, col=(205, 194, 255), rmax=520, width=7):
    """a ring blasting out of a point (k = 0..1)"""
    if not 0 < k < 1: return
    r = 20 + rmax * (1 - (1 - k) ** 2); a = (1 - k) ** 1.5
    lay = Image.new("RGBA", (int(2 * r + 40), int(1.2 * r + 40)), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((20, 20, 20 + 2 * r, 20 + 1.2 * r), outline=col + (int(255 * a),), width=max(2, int(width * (1 - k) + 2)))
    R.paste_center(im, lay.filter(ImageFilter.GaussianBlur(1.5)), cx, cy)
