"""Arabic (Lebanese) kit for founder clips: Readex Pro (Arabic + Latin merged from @fontsource), RTL typing, frosted
Arabic captions, people avatars with checks, the empty 'your place' seat, and the Arabic end card. Fonts load from
./fonts (run with cwd = the episode dir)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import render as R
from founder_common import W, H, WHITE
import s7_common as Q
from s7_common import ease, fade, shield, put

_AF = {}
def afont(size, w=700):
    k = (size, w)
    if k not in _AF: _AF[k] = ImageFont.truetype(f"fonts/Readex-{ {800: 700, 700: 600, 600: 500}.get(w, w) }.ttf", size, layout_engine=ImageFont.Layout.RAQM)
    return _AF[k]

def atext(s, size=60, w=700, col=WHITE):
    f = afont(size, w); asc, desc = f.getmetrics(); x0, _, x1, y1 = f.getbbox(s, direction="rtl", language="ar") if s else (0, 0, 1, 0)
    im = Image.new("RGBA", (max(1, x1 - x0) + 8, max(asc + desc, y1) + 14), (0, 0, 0, 0))
    if s: ImageDraw.Draw(im).text((4 - x0, 4), s, font=f, fill=col + (255,), direction="rtl", language="ar")
    return im

def typed_ar(lines, n, size=64, cursor=True):
    """right-aligned RTL typing; lines = [(text, highlighted)], first n characters, violet cursor at the left end"""
    rows = []; left = n; cur = None
    for i, (s, hl) in enumerate(lines):
        part = s[:max(0, left)]; left -= len(s); rows.append(atext(part, size, 800, Q.LAV if hl else WHITE))
        if left <= 0 and cur is None: cur = i
    if cur is None: cur = len(lines) - 1
    full = [atext(s, size, 800) for s, _ in lines]; w = max(r.width for r in full) + 30; lh = int(size * 1.45)
    im = Image.new("RGBA", (w, lh * len(lines)), (0, 0, 0, 0))
    for i, r in enumerate(rows):
        x = w - r.width; im.alpha_composite(r, (x, i * lh))
        if cursor and i == cur: im.alpha_composite(Image.new("RGBA", (int(size * 0.09), int(size * 0.95)), Q.VIO + (255,)), (max(0, x - 14), i * lh + int(size * 0.35)))
    return im

_CAP = {}
def ar_captions(im, t, caps, y=1730, size=60):
    for t0, t1, lines in caps:
        if not (t0 <= t < t1): continue
        a = fade(t, t0, t1, 0.35, 0.3); key = tuple(lines)
        if key not in _CAP: _CAP[key] = [atext(s, size, 700, Q.LAV if hl else WHITE) for s, hl in lines]
        ls = _CAP[key]; w = max(l.width for l in ls) + 76; h = sum(l.height for l in ls) - 14 * (len(ls) - 1) + 30
        yy = y + (1 - a) * 12; shield(im, (W / 2 - w / 2, yy - h / 2, W / 2 + w / 2, yy + h / 2), a, 28, dark=0.58)
        cy = yy - h / 2 + 12
        for l in ls: put(im, l, W / 2 - l.width / 2, cy, a); cy += l.height - 14

def person(col1, col2, s=96, check=True):
    pad = 14; im = Image.new("RGBA", (s + 2 * pad, s + 2 * pad), (0, 0, 0, 0)); m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    disc = Image.new("RGBA", (s, s), (0, 0, 0, 0)); disc.paste(Q.V.lin_grad(s, s, col1, col2), (0, 0), m)
    d = ImageDraw.Draw(disc); d.ellipse((s * 0.36, s * 0.2, s * 0.64, s * 0.48), fill=(255, 255, 255, 240)); d.pieslice((s * 0.2, s * 0.54, s * 0.8, s * 1.14), 180, 360, fill=(255, 255, 255, 240))
    ring = Image.new("RGBA", (s, s), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((1, 1, s - 2, s - 2), outline=(255, 255, 255, 210), width=3); disc.alpha_composite(ring)
    im.alpha_composite(disc, (pad, pad))
    if check:
        c = 34; b = Image.new("RGBA", (c, c), (0, 0, 0, 0)); bd = ImageDraw.Draw(b); bd.ellipse((0, 0, c - 1, c - 1), fill=Q.VIO + (255,), outline=(255, 255, 255, 255), width=2)
        bd.line([(c * 0.27, c * 0.52), (c * 0.43, c * 0.68), (c * 0.74, c * 0.34)], fill=(255, 255, 255, 255), width=4); im.alpha_composite(b, (s + pad - c + 4, s + pad - c + 4))
    return im
PEOPLE_L = [person(a, b) for a, b in (((240, 150, 60), (221, 92, 140)), ((53, 126, 221), (109, 77, 255)), ((46, 170, 140), (53, 126, 221)), ((221, 92, 140), (150, 110, 255)))]
SEAT_LABEL = atext("مطرحك", 40, 800, Q.LAV)

def seat(t, s=104):
    im = Image.new("RGBA", (s + 40, s + 40), (0, 0, 0, 0)); c = (s + 40) / 2; r = s / 2
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((c - r, c - r, c + r, c + r), fill=(124, 92, 255, int(110 + 60 * np.sin(t * 5))))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(16))); d = ImageDraw.Draw(im); d.ellipse((c - r + 4, c - r + 4, c + r - 4, c + r - 4), fill=(14, 14, 30, 235))
    for i in range(16):
        a0 = i * 22.5 + t * 60; d.arc((c - r, c - r, c + r, c + r), a0, a0 + 12, fill=(205, 194, 255, 255), width=5)
    d.line([(c - 18, c), (c + 18, c)], fill=(255, 255, 255, 255), width=6); d.line([(c, c - 18), (c, c + 18)], fill=(255, 255, 255, 255), width=6); return im

def end_card(k, END=4.4, lines=(('في مطرح إلك.', False), ('على HyperBidz.', True))):
    im = Q._bg().copy()
    Q.place(im, Q.V.glow(520, 150, (110, 90, 255), 130), W / 2, 560, ease(k / 0.6) * (0.85 + 0.15 * np.sin(k * 2.2)), 0)
    Q.place(im, Q.V.zmark(190), W / 2, 560, ease(k / 0.6), 18)
    for i, (s, hl) in enumerate(lines):
        Q.place(im, atext(s, 92, 800, Q.LAV if hl else WHITE), W / 2, 800 + i * 128, ease((k - 0.5 - i * 0.3) / 0.6), 18)
    Q.place(im, atext("مزادات مباشرة للبنان. قريباً.", 46, 600, (228, 230, 248)), W / 2, 1100, ease((k - 1.3) / 0.6))
    fa = atext("تابعنا", 46, 800, (42, 21, 128)); fh = R.text_layer("@hyperbidz", R.font(46, 700), (42, 21, 128))
    w, h = fa.width + fh.width + 16 + 100, max(fa.height, fh.height) + 24
    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(255, 255, 255, 255))
    pill.alpha_composite(fh, (50, (h - fh.height) // 2 - 2)); pill.alpha_composite(fa, (50 + fh.width + 16, (h - fa.height) // 2)); Q.place(im, pill, W / 2, 1260, ease((k - 1.7) / 0.6))
    out = im.convert("RGB")
    if k > END - 0.6: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), min(1, (k - (END - 0.6)) / 0.6))
    return out


# ---------- Season 8 (بالعربي) additions ----------
import cv2
from founder_common import SR

def track(FR, pts, size=56, search=110):
    """follow a few scene points through a slowly drifting Veo shot (template match at half size, smoothed)"""
    g = [cv2.cvtColor(np.asarray(f.convert("RGB").resize((W // 2, H // 2))), cv2.COLOR_RGB2GRAY) for f in FR]; out = {}
    for k, (x, y) in pts.items():
        cx, cy = x / 2, y / 2; s = size // 2; tpl = g[0][int(cy - s / 2):int(cy + s / 2), int(cx - s / 2):int(cx + s / 2)]; path = []
        for im in g:
            x0 = int(max(0, cx - search / 2 - s / 2)); y0 = int(max(0, cy - search / 2 - s / 2))
            win = im[y0:int(min(H // 2, cy + search / 2 + s / 2)), x0:int(min(W // 2, cx + search / 2 + s / 2))]
            if win.shape[0] > tpl.shape[0] and win.shape[1] > tpl.shape[1]:
                r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(r)
                if mx > 0.4: cx, cy = x0 + loc[0] + s / 2, y0 + loc[1] + s / 2
            path.append((cx * 2, cy * 2))
        p = np.array(path); k5 = np.ones(7) / 7
        sm = np.stack([np.convolve(np.pad(p[:, j], 3, mode="edge"), k5, "valid") for j in (0, 1)], 1); out[k] = sm
    return out

def grey(im, k, tint=(150, 155, 170)):
    """drain the colour out of the scene (k = 0..1)"""
    if k <= 0.01: return im
    a = np.asarray(im.convert("RGB"), np.float32); l = (a @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
    g = l * 0.82 + np.array(tint, np.float32) * 0.12
    return Image.fromarray(np.clip(a * (1 - k) + g * k, 0, 255).astype(np.uint8)).convert("RGBA")

def reveal(grey_im, col_im, cx, cy, r, edge=(205, 194, 255)):
    """colour floods back inside a growing circle, with a glowing violet rim"""
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    out = grey_im.copy(); out.paste(col_im, (0, 0), m.filter(ImageFilter.GaussianBlur(6)))
    rim = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0)); ImageDraw.Draw(rim).ellipse(((cx - r) / 2, (cy - r) / 2, (cx + r) / 2, (cy + r) / 2), outline=edge + (230,), width=4)
    out.alpha_composite(rim.filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)); return out

def box_icon(s=30, col=(60, 62, 72)):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(2, s // 12)
    d.polygon([(s * .5, s * .08), (s * .92, s * .28), (s * .5, s * .48), (s * .08, s * .28)], outline=col + (255,), width=w)
    d.line([(s * .08, s * .28), (s * .08, s * .72), (s * .5, s * .94), (s * .92, s * .72), (s * .92, s * .28)], fill=col + (255,), width=w, joint="curve")
    d.line([(s * .5, s * .48), (s * .5, s * .94)], fill=col + (255,), width=w); return im

def spark_icon(s=30, col=(255, 255, 255)):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); c = s / 2
    ImageDraw.Draw(im).polygon([(c, 0), (c + s * .14, c - s * .14), (s, c), (c + s * .14, c + s * .14), (c, s), (c - s * .14, c + s * .14), (0, c), (c - s * .14, c - s * .14)], fill=col + (255,)); return im

def item_tag(word, opp):
    """'بضاعة' (goods: grey paper tag with a box) or 'فرصة' (opportunity: violet gradient with a sparkle)"""
    tl = atext(word, 34, 800, WHITE if opp else (52, 54, 64)); ic = spark_icon(26) if opp else box_icon(28)
    w, h = tl.width + ic.width + 46, max(tl.height, ic.height) + 8
    im = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    if opp:
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((12, 14, w + 12, h + 14), radius=h // 2, fill=(124, 92, 255, 150)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
        body = Image.new("RGBA", (w, h), (0, 0, 0, 0)); body.paste(Q.V.lin_grad(w, h, Q.BLUE, Q.VIO), (0, 0), m)
    else:
        body = Image.new("RGBA", (w, h), (0, 0, 0, 0)); body.paste((226, 226, 230, 255), (0, 0), m)
    body.alpha_composite(tl, (w - tl.width - 18, (h - tl.height) // 2)); body.alpha_composite(ic, (18, (h - ic.height) // 2))
    im.alpha_composite(body, (12, 12)); return im

def poll_sticker(question, a, b, t, w=720):
    """an Instagram-style poll (no results shown): the question and two options, a tap ring pulsing between them"""
    q = atext(question, 50, 800, (24, 24, 36)); h = 270
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 28, w + 20, h + 28), radius=36, fill=(0, 0, 0, 120)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle((0, 0, w - 1, h - 1), radius=36, fill=(255, 255, 255, 250))
    card.alpha_composite(q, ((w - q.width) // 2, 22)); bw = (w - 3 * 26) // 2; bh = 92
    for i, (txt, opp) in enumerate(((b, True), (a, False))):                                               # RTL: first option on the right
        x = 26 + i * (bw + 26); y = h - bh - 30
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=bh // 2, fill=255)
        pill = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        if opp: pill.paste(Q.V.lin_grad(bw, bh, Q.BLUE, Q.VIO), (0, 0), m)
        else: pill.paste((236, 236, 240, 255), (0, 0), m)
        tl = atext(txt, 40, 800, WHITE if opp else (52, 54, 64)); ic = spark_icon(26) if opp else box_icon(28)
        tw = tl.width + ic.width + 14; pill.alpha_composite(tl, ((bw + tw) // 2 - tl.width, (bh - tl.height) // 2)); pill.alpha_composite(ic, ((bw - tw) // 2, (bh - ic.height) // 2))
        card.alpha_composite(pill, (x, y))
    im.alpha_composite(card, (20, 20))
    k = (t * 0.8) % 1.0; cx = 20 + w / 2 + 120 * np.sin(t * 2.2); cy = 20 + h - 76; r = 26 + 30 * k
    rl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(rl).ellipse((cx - r, cy - r, cx + r, cy + r), outline=(124, 92, 255, int(220 * (1 - k))), width=5)
    ImageDraw.Draw(rl).ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(124, 92, 255, 200)); im.alpha_composite(rl)
    return im

# a Lebanese groove: darbuka maqsum (doum-tak) + an oud-like pluck line in D Hijaz
HIJAZ = [62, 63, 66, 67, 69, 70, 72, 74]
def darbuka_groove(total, level=1.0, bpm=96, seed=4):
    rng = np.random.default_rng(seed); n = int(total * SR); out = np.zeros(n); e = 60 / bpm / 2
    def add(sig, at, g):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += sig[: j - i] * g
    y = np.arange(int(0.32 * SR)) / SR; doum = np.sin(2 * np.pi * np.cumsum(58 + 60 * np.exp(-y * 28)) / SR) * np.exp(-y * 11)
    y2 = np.arange(int(0.09 * SR)) / SR
    def tak(): return (np.convolve(rng.normal(0, 1, len(y2)), [1, -0.9], "same") * 0.6 + np.sin(2 * np.pi * 820 * y2) * 0.5) * np.exp(-y2 * 60)
    maqsum = {0: "D", 1: "T", 3: "T", 4: "D", 6: "T", 7: "k"}
    mel = [(0, 62), (2, 63), (3, 66), (4, 67), (6, 69), (8, 70), (9, 69), (10, 67), (11, 66), (12, 63), (14, 62)]   # 16 eighths
    k = 0; t = 0.0
    while t < total:
        st = k % 8; hit = maqsum.get(st)
        if hit == "D": add(doum, t, 0.55)
        elif hit == "T": add(tak(), t, 0.22)
        elif hit == "k": add(tak(), t, 0.1)
        for s16, m in mel:
            if k % 16 == s16 and (k // 16) % 2 == 1:
                p = Q.pluck(Q.note(m - 12), 0.45, 0.45, rng) * np.exp(-np.arange(int(0.45 * SR)) / SR * 5); add(p, t, 0.26)
        if k % 16 == 0: p = Q.pluck(Q.note(50 - 12), 0.6, 0.3, rng) * np.exp(-np.arange(int(0.6 * SR)) / SR * 3); add(p, t, 0.4)   # low D drone pluck
        k += 1; t = k * e
    return out * level

def muffle(sig, k_env, taps=24):
    """blend a dull, low-passed copy in where k_env → 1 (the 'goods' world sounds flat)"""
    lp = np.convolve(sig, np.ones(taps) / taps, "same") * 0.8; return sig * (1 - k_env) + lp * k_env
