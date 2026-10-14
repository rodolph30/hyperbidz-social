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
