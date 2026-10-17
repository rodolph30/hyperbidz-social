"""Motion kit v3 for the auction shorts (owner, 18 Oct 2026: "this is the level"; reference: a fast explainer reel built
from word-by-word kinetic captions and clean UI cards). Everything is drawn in code, in the app's colours.

What it gives a lesson script:
- bg(dark): grid-paper backgrounds, light (#F3F3F6) or dark (#0B0E14 + faint grid + a few stars). Alternate them with the mood.
- KCaps(TL): word-by-word captions at the top, timed to the narrator's real words (narration.Timeline.words). The newest word
  is strong, earlier words go grey, [emphasis] words get a lilac highlight (numbers also get selection handles).
- UI cards: card(), window(), phone(), pill(), chip(), stat(), row(), avatar() (Sami / Nour / initials), cursor(),
  select_box(), strike(), big_stamp(), counter text helpers.
- Motion: spring(), settle(), whip(a, b, k) (motion-blurred push between scenes), click ripples.
Rule of thumb: something visibly changes every 1-2 s, one idea at a time, numbers big, captions carry the words.
"""
import re
from cast import *
import narration as N

# palette (app colours)
L_BG, L_GRID, D_BG, D_GRID = (243, 243, 246), (231, 231, 238), (11, 14, 20), (21, 25, 34)
L_INK, L_MUTE, D_INK, D_MUTE = (11, 14, 20), (150, 155, 166), (255, 255, 255), (112, 118, 132)
CARD_L, CARD_D, LINE_L, LINE_D = (255, 255, 255), (21, 25, 34), (229, 230, 236), (40, 46, 60)
PILL_L, PILL_D = (233, 227, 255), (54, 42, 108)
RED_UI, GREEN_UI = (229, 56, 84), (0, 163, 100)

def spring(x):
    """0→1 with a small overshoot (cards landing)"""
    x = clamp(x); return 1 - np.exp(-6.5 * x) * np.cos(9.5 * x) if x < 1 else 1.0
def settle(t, t0, d=0.45): return spring((t - t0) / d)

_BG = {}
def bg(dark=False):
    if dark in _BG: return _BG[dark].copy()
    im = Image.new("RGBA", (W, H), (D_BG if dark else L_BG) + (255,)); d = ImageDraw.Draw(im); g = D_GRID if dark else L_GRID
    for x in range(0, W, 40): d.line([(x, 0), (x, H)], fill=g + (255,), width=1)
    for y in range(0, H, 40): d.line([(0, y), (W, y)], fill=g + (255,), width=1)
    if dark:
        r = np.random.default_rng(7)
        for _ in range(26):
            x, y, s = r.integers(0, W), r.integers(0, H), r.uniform(1.5, 3.2); d.ellipse((x - s, y - s, x + s, y + s), fill=(200, 205, 230, int(r.uniform(60, 160))))
        v = stage(top=(0, 0, 0), bot=(0, 0, 0), spot=(540, 900, 700, 900), spot_col=(70, 60, 160), spot_a=0.10)
        a = np.asarray(v.convert("RGB")).astype(np.int16); base = np.asarray(im.convert("RGB")).astype(np.int16)
        im = Image.fromarray(np.clip(base + a, 0, 255).astype(np.uint8)).convert("RGBA")
    _BG[dark] = im; return im.copy()

# ---------- text ----------
_T = {}
def T(text, size, col, w=700, mono_=False):
    k = (text, size, col, w, mono_)
    if k not in _T: _T[k] = R.text_layer(text, R.font(size, w, mono=mono_), col)
    return _T[k]

class KCaps:
    """word-by-word captions synced to the narrator. KCaps(TL).draw(im, t, dark)"""
    def __init__(self, TL, size=62, maxw=930, y=250, max_words=7):
        self.TL, self.size, self.maxw, self.y = TL, size, maxw, y; self.chunks = []
        for key, _, _ in TL.lines:
            ws = TL.words(key); cur = []
            for i, (s, e, t) in enumerate(ws):
                cur.append((s, e, t))
                brk = re.search(r"[.?!:]$", s) or (re.search(r",$", s) and len(cur) >= 3) or len(cur) >= max_words
                if brk and i < len(ws) - 1 and len(ws) - 1 - i >= 2: self.chunks.append((key, cur)); cur = []
            if cur:
                if self.chunks and self.chunks[-1][0] == key and len(cur) <= 1: self.chunks[-1] = (key, self.chunks[-1][1] + cur)
                else: self.chunks.append((key, cur))
    def active(self, t):
        for i, (key, ws) in enumerate(self.chunks):
            t0 = ws[0][2] - 0.04; nxt = self.chunks[i + 1][1][0][2] - 0.04 if i + 1 < len(self.chunks) else 1e9
            end = min(nxt, self.TL.t(key)[1] + 0.9)
            if t0 <= t < end: return ws, end
        return None, None
    def draw(self, im, t, dark=False, y=None):
        ws, end = self.active(t)
        if not ws: return
        y = self.y if y is None else y; ink, mute = (D_INK, D_MUTE) if dark else (L_INK, L_MUTE)
        size = self.size; sp = int(size * 0.28); lines, cur, wsum = [], [], 0
        lays = []
        for s, e, wt in ws:
            lays.append((s, e, wt, T(s, size, (0, 0, 0))))
        for item in lays:
            w = item[3].width
            if cur and wsum + sp + w > self.maxw: lines.append(cur); cur, wsum = [], 0
            cur.append(item); wsum += (sp if cur[:-1] else 0) + w
        if cur: lines.append(cur)
        shown = [x for x in ws if x[2] <= t + 0.02]; newest = shown[-1][2] if shown else None
        fade_out = 1 - ease((t - (end - 0.12)) / 0.12) if end < 1e8 else 1
        lh = int(size * 1.18)
        for li, line in enumerate(lines):
            tw = sum(x[3].width for x in line) + sp * (len(line) - 1); x = 540 - tw / 2; yy = y + li * lh
            for s, e, wt, lay in line:
                k = (t - wt) / 0.14
                if k < 0: x += lay.width + sp; continue
                a = ease(k) * fade_out; dy = (1 - eout(k)) * 18
                strong = e or wt == newest
                col = (VIOLET if not dark else (255, 255, 255)) if e else (ink if strong else mute)
                layer = T(s, size, col)
                if e:                                                                   # highlight behind emphasis words
                    pad = 10; hl = Image.new("RGBA", (layer.width + 2 * pad, int(size * 1.1)), (0, 0, 0, 0))
                    ImageDraw.Draw(hl).rounded_rectangle((0, 0, hl.width - 1, hl.height - 1), radius=12, fill=(PILL_D if dark else PILL_L) + (255,))
                    wk = eout((t - wt) / 0.25); hl = hl.crop((0, 0, max(1, int(hl.width * wk)), hl.height))
                    put(im, hl, x - pad + hl.width / 2, yy + size * 0.55 + dy, a)
                    if any(ch.isdigit() for ch in s): select_box(im, (x - pad, yy + 2 + dy, x + layer.width + pad, yy + size * 1.1 + dy), wk, a)
                put(im, layer, x + layer.width / 2, yy + layer.height / 2 + dy, a)
                x += lay.width + sp

def select_box(im, box, k=1.0, a=1.0, col=VIOLET):
    """design-tool selection: violet outline with 4 corner handles"""
    if k <= 0 or a <= 0: return
    x0, y0, x1, y1 = box; lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    xx = x0 + (x1 - x0) * clamp(k); al = int(255 * a)
    d.rectangle((x0, y0, xx, y1), outline=col + (al,), width=3)
    for (hx, hy) in ((x0, y0), (xx, y0), (x0, y1), (xx, y1)): d.rectangle((hx - 7, hy - 7, hx + 7, hy + 7), fill=(255, 255, 255, al), outline=col + (al,), width=3)
    im.alpha_composite(lay)

def strike(im, x0, y, x1, k, col=RED_UI, w=8):
    if k <= 0: return
    ImageDraw.Draw(im).line([(x0, y), (x0 + (x1 - x0) * clamp(k), y)], fill=col + (255,), width=w)

# ---------- cards ----------
def card(w, h, dark=False, r=30, fill=None, border=True):
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=(fill or (CARD_D if dark else CARD_L)) + (255,), outline=((LINE_D if dark else LINE_L) + (255,)) if border else None, width=2)
    return im
def lift(layer, dark=False): return shadowed(layer, 26, 18, 120 if dark else 70)

def window(w, h, title="", dark=False):
    im = card(w, h, dark, 26); d = ImageDraw.Draw(im)
    d.line([(0, 70), (w, 70)], fill=(LINE_D if dark else LINE_L) + (255,), width=2)
    for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))): d.ellipse((24 + i * 30, 26, 42 + i * 30, 44), fill=c + (255,))
    if title: tt = T(title, 28, D_MUTE if dark else (90, 96, 110), 600); im.alpha_composite(tt, (int(w / 2 - tt.width / 2), 18))
    return im

def phone(w=520, h=1040, dark=False):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=74, fill=(24, 26, 32, 255))
    d.rounded_rectangle((14, 14, w - 15, h - 15), radius=62, fill=(CARD_D if dark else CARD_L) + (255,))
    d.rounded_rectangle((w / 2 - 70, 30, w / 2 + 70, 66), radius=18, fill=(10, 10, 14, 255))
    tt = T("9:41", 26, D_INK if dark else L_INK, 600); im.alpha_composite(tt, (54, 34)); return im

def pill(text, size=30, fill=VIOLET, col=(255, 255, 255), padx=22, pady=10, w=700, r=None):
    tt = T(text, size, col, w); pw, ph = tt.width + 2 * padx, tt.height + 2 * pady
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=r or ph // 2, fill=fill + (255,))
    im.alpha_composite(tt, (padx, pady)); return im

def chip(text, dark=False, size=24):
    return pill(text.upper(), size, (40, 46, 60) if dark else (236, 237, 242), D_MUTE if dark else (96, 102, 116), 18, 8, 700)

def stat(label, value, sub="", w=860, dark=False, vsize=150, vcol=None):
    lab = T(label.upper(), 26, D_MUTE if dark else (110, 116, 130), 700, True); v = T(value, vsize, vcol or (D_INK if dark else L_INK), 700)
    sb = T(sub, 30, D_MUTE if dark else (110, 116, 130), 500) if sub else None
    h = 40 + lab.height + 26 + v.height + (20 + sb.height if sb else 0) + 44; im = card(w, h, dark, 30); x = 44; y = 40
    im.alpha_composite(lab, (x, y)); y += lab.height + 26; im.alpha_composite(v, (x, y)); y += v.height + 20
    if sb: im.alpha_composite(sb, (x, y))
    return im

def head(who, s=90):
    """round avatar: 'sami', 'nour', or (initial, colour)"""
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    if who in ("sami", "nour"):
        col = BLUE if who == "sami" else LILAC; bgc = Image.new("RGBA", (s, s), tuple(min(255, c + 40) for c in col) + (255,))
        bs = int(s * 1.1); b = (sami if who == "sami" else nour)("happy", bs); bgc.alpha_composite(b, (int(s / 2 - b.width / 2), int(s * 0.47 - 0.64 * bs)))
        im.paste(bgc, (0, 0), m)
    else:
        ch, col = who; c = Image.new("RGBA", (s, s), col + (255,)); tt = T(ch, int(s * 0.45), (255, 255, 255)); c.alpha_composite(tt, (int(s / 2 - tt.width / 2), int(s / 2 - tt.height / 2)))
        im.paste(c, (0, 0), m)
    return im

def cursor(s=54):
    im = Image.new("RGBA", (s, int(s * 1.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(4, 4), (4, s * 1.15), (s * 0.3, s * 0.9), (s * 0.52, s * 1.32), (s * 0.68, s * 1.24), (s * 0.47, s * 0.84), (s * 0.85, s * 0.82)]
    d.polygon(pts, fill=(255, 255, 255, 255)); d.line(pts + [pts[0]], fill=(20, 20, 24, 255), width=4); return im
def ripple(im, x, y, k, col=VIOLET):
    if 0 < k < 1:
        r = 20 + 60 * eout(k); a = int(200 * (1 - k)); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse((x - r, y - r, x + r, y + r), outline=col + (a,), width=6); im.alpha_composite(lay)

def big_stamp(text, col=RED_UI, size=110, rot=-8):
    tt = T(text, size, col, 700); w, h = tt.width + 70, tt.height + 44
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((4, 4, w - 5, h - 5), radius=18, outline=col + (255,), width=10)
    im.alpha_composite(tt, (35, 18)); return im.rotate(rot, expand=True, resample=Image.BICUBIC)
def stamp_at(im, layer, x, y, t, t0):
    if t >= t0: put(im, layer, x, y, min(1, (t - t0) / 0.06), 1 + 0.6 * (1 - eout((t - t0) / 0.22)))

def money(v, dec=0): return f"${v:,.{dec}f}"
def roll(t, t0, d, a, b): return a + (b - a) * eout((t - t0) / d) if t >= t0 else a

def footnote(im, text, dark=False, y=1830):
    tt = T(text, 22, D_MUTE if dark else (140, 146, 158), 500); put(im, tt, 540, y)

# ---------- transitions ----------
def whip(a_im, b_im, k, direction=1):
    """push to the next scene with motion blur (k 0..1)"""
    k = ease(k); a = a_im.convert("RGB"); b = b_im.convert("RGB")
    off = int(W * k) * direction; frame = Image.new("RGB", (W, H)); frame.paste(a, (-off, 0)); frame.paste(b, (W * direction - off, 0))
    blur = int(80 * np.sin(np.pi * k))
    if blur > 2:
        arr = np.asarray(frame).astype(np.float32); acc = np.zeros_like(arr); n = 6
        for i in range(n): acc += np.roll(arr, int((i - n / 2) * blur / n), axis=1)
        frame = Image.fromarray((acc / n).astype(np.uint8))
    return frame
