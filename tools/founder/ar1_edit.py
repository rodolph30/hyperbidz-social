"""Arabic test (Lebanese), golden-hour office. 'تعرف شو اللي بيخلّي الشغل يكبر؟ الناس الصحّ. ومع HyperBidz، في مطرح إلك.'
The question types itself (right to left) in a glass panel in the ceiling. 'الناس الصحّ': four people pop in along an arc,
each with a violet check, linked into a network. 'ومع HyperBidz': the wall Z flares and blasts a shockwave. 'في مطرح إلك':
the row opens and an empty dashed seat spins in the middle, '+' and 'مطرحك' (your place), with a shockwave on 'إلك'.
Arabic captions (Cairo), warm groove, held last shot, Arabic end card. The floating ceiling watermark and the laptop's
Apple logo are inpainted away."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
import s6_common as K
from s7_common import ease, fade, shield, put
sys.path.insert(0, "/home/claude/ar1"); from clean import clean

OUT = sys.argv[1]; SHOT = 7.2; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
FR = [clean(f) for f in decode()]
LOGO = (350, 668); Q1, PEOPLE, HB, PLACE, YOU = 0.0, 2.44, 4.24, 5.04, 5.94

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

CAPS = [(2.38, 3.55, [("الناس الصحّ.", True)]), (3.58, 5.0, [("ومع HyperBidz،", False)]), (5.0, CLIP - 0.05, [("في مطرح إلك.", True)])]
HOOK = [("تعرف شو اللي بيخلّي", False), ("الشغل يكبر؟", True)]; HOOK_N = sum(len(s) for s, _ in HOOK); CPS = 30

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

def slots(t):
    """x positions of the 4 people (+ the opening seat in the middle once 'في مطرح إلك' starts)"""
    k = ease((t - PLACE) / 0.45); base = [240, 420, 660, 840]; opened = [190, 345, 735, 890]
    return [b + (o - b) * k for b, o in zip(base, opened)], k
ROW_Y = [345, 300, 300, 345]

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = end_card(t - CLIP); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = Q.hq_grade(fr, 0.2)
    Q.z_glow(im, 0.15 + 0.06 * np.sin(t * 2.4) + flare(t, HB, 1.0, 0.9) + flare(t, YOU, 0.5), box=(200, 560, 500, 800))
    im = hold_zoom(im, t, SHOT, 6.4, HOLD, 1.06, (560, 820))
    sx, sy = Q.shake_off(t, HB + 0.1, 8, 0.3); im = Q.shake(im, sx, sy)
    ah = fade(t, -0.2, PEOPLE - 0.05, 0.2, 0.3)                                                          # the question
    if ah > 0:
        n = HOOK_N if t > Q1 + HOOK_N / CPS else max(1, int((t - Q1) * CPS) + 1)
        lay = typed_ar(HOOK, n, 64, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 820, lay.height + 50; y = 330
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.6)
        put(im, lay, W / 2 + w / 2 - 50 - lay.width, y - h / 2 + 18, ah)
    if PEOPLE <= t:                                                                                    # the right people
        xs, ko = slots(t); a_all = 1 - ease((t - CLIP + 0.35) / 0.3)
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        pts = [(x, y) for x, y in zip(xs, ROW_Y)]
        if ko > 0: pts = pts[:2] + [(W / 2, 270)] + pts[2:]
        for i in range(len(pts) - 1):
            kl = ease((t - PEOPLE - 0.35 - 0.12 * i) / 0.3)
            if kl > 0: (x0, y0), (x1, y1) = pts[i], pts[i + 1]; d.line([(x0, y0), (x0 + (x1 - x0) * kl, y0 + (y1 - y0) * kl)], fill=(205, 194, 255, int(170 * a_all)), width=3)
        im.alpha_composite(L)
        for i, (x, y, lay) in enumerate(zip(xs, ROW_Y, PEOPLE_L)):
            t0 = PEOPLE + 0.12 * i; R.paste_center(im, lay, x, y + 4 * np.sin(t * 2 + i), min(1, (t - t0) / 0.06) * a_all if t >= t0 else 0, Q.slam((t - t0) / 0.22) * 0.95)
        if ko > 0:
            R.paste_center(im, seat(t), W / 2, 270, ko * a_all, 0.6 + 0.4 * Q.pop((t - PLACE) / 0.4))
            R.paste_center(im, SEAT_LABEL, W / 2, 380, ease((t - PLACE - 0.25) / 0.3) * a_all)
    Q.shockwave(im, *LOGO, (t - HB - 0.1) / 0.6, (150, 130, 255), 420); Q.shockwave(im, *LOGO, (t - HB - 0.22) / 0.6, Q.LAV, 300, 4)
    Q.shockwave(im, W / 2, 270, (t - YOU) / 0.55, Q.LAV, 360, 5)
    Q.flash(im, flare(t, HB + 0.1, 0.22, 0.3), (240, 232, 255))
    ar_captions(im, t, CAPS)
    return im.convert("RGB")

def end_card(k):
    im = Q._bg().copy()
    Q.place(im, Q.V.glow(520, 150, (110, 90, 255), 130), W / 2, 560, ease(k / 0.6) * (0.85 + 0.15 * np.sin(k * 2.2)), 0)
    Q.place(im, Q.V.zmark(190), W / 2, 560, ease(k / 0.6), 18)
    for i, (s, hl) in enumerate((("في مطرح إلك.", False), ("على HyperBidz.", True))):
        Q.place(im, atext(s, 92, 800, Q.LAV if hl else WHITE), W / 2, 800 + i * 128, ease((k - 0.5 - i * 0.3) / 0.6), 18)
    Q.place(im, atext("مزادات مباشرة للبنان. قريباً.", 46, 600, (228, 230, 248)), W / 2, 1100, ease((k - 1.3) / 0.6))
    fa = atext("تابعنا", 46, 800, (42, 21, 128)); fh = R.text_layer("@hyperbidz", R.font(46, 700), (42, 21, 128))
    w, h = fa.width + fh.width + 16 + 100, max(fa.height, fh.height) + 24
    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(255, 255, 255, 255))
    pill.alpha_composite(fh, (50, (h - fh.height) // 2 - 2)); pill.alpha_composite(fa, (50 + fh.width + 16, (h - fa.height) // 2)); Q.place(im, pill, W / 2, 1260, ease((k - 1.7) / 0.6))
    out = im.convert("RGB")
    if k > END - 0.6: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), min(1, (k - (END - 0.6)) / 0.6))
    return out

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = K.GrooveMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = K.groove(CLIP + END, 0.0, 1.0, seed=21); x = np.arange(len(g)) / SR; mx.fadd(g * np.minimum(1, x / 0.8), 0.0, 0.5)
        for i in range(HOOK_N): Q.key_click(mx, Q1 + i / CPS, 0.024)
        for i in range(4): Q.ding(mx, PEOPLE + 0.12 * i, (1046.5, 1318.5, 1568, 2093)[i], 0.05)
        Q.impact(mx, HB + 0.1, 0.22); Q.V.chime(mx, HB + 0.12, 1318.5, 0.045); mx.shimmer(HB + 0.15, 1568, 0.025)
        mx.whoosh(PLACE, 0.4, 0.1); Q.bubble_pop(mx, PLACE + 0.05, 0.07); Q.V.chime(mx, YOU, 1568, 0.05)
        mx.write("ar1_audio.wav")
    render(frame, TOTAL, "ar1_audio.wav", OUT)
