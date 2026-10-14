"""Season 8 'بالعربي' Ep. 1 'شو بتشوف؟' (What do you see?). Golden-hour office, a slow camera arc.
'في ناس بتشوف بضاعة' — the world drains to grey and plain grey tags (بضاعة, with a box) pin themselves to the mug, the
laptop, the books, the notebook and the lamp; the music goes dull. 'وفي ناس بتشوف فرصة' — colour floods back in a
violet-rimmed circle from his face, each tag flips to a glowing فرصة (with a sparkle) on a Hijaz pluck and a +$ chip
rises off each object; the music opens up. 'إنت' — a punch in, the wall Z flares. 'شو بتشوف؟' — an Instagram-style poll
pops in the ceiling: بضاعة / فرصة, a tap ring pulsing between them. Darbuka (maqsum) + oud-like plucks in D Hijaz.
Held last shot, Arabic end card. The laptop's Apple logo is found and inpainted in every frame."""
import sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
import ar_common as A
from s7_common import ease, fade, shield, put

OUT = sys.argv[1]; SHOT = 7.6; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END

def clean(fr):
    a = np.asarray(fr.convert("RGB")).copy(); x0, y0, x1, y1 = 930, 1190, 1080, 1340; reg = a[y0:y1, x0:x1]
    g = cv2.cvtColor(reg, cv2.COLOR_RGB2GRAY).astype(np.int16); med = int(np.median(g))
    m = ((g < med - 16) & (reg[..., 1].astype(np.int16) - reg[..., 0] < 12)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        if 60 < st[i, cv2.CC_STAT_AREA] < 3500:
            mm = cv2.dilate((lab == i).astype(np.uint8) * 255, np.ones((7, 7), np.uint8)); a[y0:y1, x0:x1] = cv2.inpaint(reg, mm, 7, cv2.INPAINT_TELEA)
    return Image.fromarray(a)
FR = [clean(f) for f in decode()]
ANCH = {"mug": (320, 1350), "laptop": (760, 1405), "books": (110, 1530), "note": (580, 1535), "lamp": (980, 565)}
TR = A.track(FR, ANCH)
TAGS = [("mug", (0, -150), 1.0), ("laptop", (130, -250), 1.12), ("books", (50, -160), 1.24), ("note", (10, -120), 1.36), ("lamp", (0, 92), 1.48)]
GOODS, OPP = A.item_tag("بضاعة", False), A.item_tag("فرصة", True)
FACE = (565, 740); GREY0, REV0, REV1, YOU, POLL = 0.62, 3.75, 4.45, 5.09, 6.14
HOOK = [("بضاعة… ولا فرصة؟", True)]; HOOK_N = len(HOOK[0][0]); CPS = 30
LAV = Q.LAV; MUTE = (196, 198, 210)
CAPS = [(0.62, 2.05, [("في ناس بتشوف", WHITE), ("بضاعة.", MUTE)]), (2.15, 4.98, [("وفي ناس بتشوف", WHITE), ("فرصة.", LAV)]),
        (5.0, CLIP - 0.05, [("إنت شو بتشوف؟", LAV)])]
PART = None

def part_tag():
    tl = A.atext("الموسم ٨  ·  الحلقة ١", 30, 700, LAV); w, h = tl.width + 44, tl.height + 2
    im = Q.glass_layer(w, h, h // 2, fill=(12, 14, 26, 190), edge=(255, 255, 255, 90)); im.alpha_composite(tl, (22, 0)); return im
PART = part_tag()

_CAP = {}
def caps(im, t, y=1730):
    for t0, t1, lines in CAPS:
        if not (t0 <= t < t1): continue
        a = fade(t, t0, t1, 0.35, 0.3); key = tuple(lines)
        if key not in _CAP: _CAP[key] = [A.atext(s, 60, 700, c) for s, c in lines]
        ls = _CAP[key]; w = max(l.width for l in ls) + 76; h = sum(l.height for l in ls) - 14 * (len(ls) - 1) + 30
        yy = y + (1 - a) * 12; shield(im, (W / 2 - w / 2, yy - h / 2, W / 2 + w / 2, yy + h / 2), a, 28, dark=0.58); cy = yy - h / 2 + 12
        for l in ls: put(im, l, W / 2 - l.width / 2, cy, a); cy += l.height - 14

def rev_r(t): return 1700 * ease((t - REV0) / (REV1 - REV0)) ** 1.3

def punch(im, t):
    z = 1 + 0.05 * Q.pop((t - YOU) / 0.3) if t >= YOU else 1.0
    if z <= 1.001: return im
    w, h = W / z, H / z; l = FACE[0] - w / 2; tp = min(max(FACE[1] + 200 - h / 2, 0), H - h); l = min(max(l, 0), W - w)
    return im.crop((int(l), int(tp), int(l + w), int(tp + h))).resize((W, H), Image.BICUBIC)

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = A.end_card(t - CLIP, END, (("إنت شو بتشوف؟", False), ("بضاعة… ولا فرصة؟", True))); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fi = min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS)); fr = FR[fi]
    col = Q.hq_grade(fr, 0.2)
    Q.z_glow(col, 0.15 + 0.06 * np.sin(t * 2.4) + flare(t, REV1 - 0.1, 0.7) + flare(t, YOU, 0.9), box=(130, 520, 470, 800))
    kg = ease((t - GREY0) / 0.5) * 0.92
    if kg > 0 and t < REV1:
        gi = A.grey(col, kg); im = A.reveal(gi, col, *FACE, rev_r(t)) if t >= REV0 else gi
    else: im = col
    for name, (ox, oy), t0 in TAGS:                                                                    # the tags
        if t < t0 or t > YOU + 0.4: continue
        x, y = TR[name][fi]; tx, ty = min(max(x + ox, 120), W - 120), y + oy; a = min(1, (t - t0) / 0.08) * (1 - ease((t - YOU) / 0.3))
        hit = REV0 + (REV1 - REV0) * (np.hypot(tx - FACE[0], ty - FACE[1]) / 1700) ** (1 / 1.3) * 0.9
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = (205, 194, 255) if t >= hit else (220, 222, 230)
        d.line([(x, y), (tx, ty + (24 if oy < 0 else -24))], fill=c + (int(200 * a),), width=2); d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=c + (int(255 * a),)); im.alpha_composite(L)
        kf = (t - hit) / 0.3
        if kf < 0: lay, sx = GOODS, 1.0
        elif kf < 0.5: lay, sx = GOODS, 1 - kf * 2
        else: lay, sx = OPP, min(1.0, (kf - 0.5) * 2) * (1 + 0.08 * np.sin(np.pi * min(1, (kf - 0.5) * 2)))
        if sx > 0.03:
            l2 = lay.resize((max(1, int(lay.width * sx)), lay.height), Image.BICUBIC); s = 0.8 + 0.2 * Q.pop((t - t0) / 0.3)
            R.paste_center(im, l2, tx, ty, a, s)
        if t >= hit:                                                                                   # +$ rising off the object
            kc = (t - hit) / 1.1
            if kc < 1: R.paste_center(im, CHIP[name], min(max(x + 20, 100), W - 100), y - 40 - 160 * ease(kc), (1 - ease((kc - 0.6) / 0.4)) * a, 0.85)
            Q.sparkle(im, t, hit, tx, ty) if hasattr(Q, "sparkle") else sparkle_burst(im, t, hit, tx, ty)
    im = punch(im, t)
    im = hold_zoom(im, t, SHOT, 6.8, HOLD, 1.06, (565, 900))
    a = fade(t, 0.0, POLL - 0.15, 0.3, 0.25)
    if a > 0: R.paste_center(im, PART, W / 2, 215, a)
    ah = fade(t, -0.2, 2.1, 0.2, 0.3)                                                                  # hook
    if ah > 0:
        n = HOOK_N if t > HOOK_N / CPS else max(1, int(t * CPS) + 1)
        lay = A.typed_ar(HOOK, n, 74, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 760, lay.height + 44; y = 345
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.6)
        put(im, lay, W / 2 + w / 2 - 50 - lay.width, y - h / 2 + 14, ah)
    if t >= POLL:                                                                                      # the poll
        R.paste_center(im, A.poll_sticker("إنت شو بتشوف؟", "بضاعة", "فرصة", t), W / 2, 330, min(1, (t - POLL) / 0.08) * (1 - ease((t - CLIP + 0.3) / 0.3)), 0.85 + 0.15 * Q.pop((t - POLL) / 0.35))
    Q.flash(im, flare(t, REV1 - 0.15, 0.25, 0.3), (245, 238, 255))
    caps(im, t)
    return im.convert("RGB")

CHIP = {n: Q.bid_chip("ABCDE"[i], ["+$40", "+$120", "+$65", "+$30", "+$90"][i], Q.CROWD_COLS[(i * 3) % 8], 30) for i, (n, _, _) in enumerate(TAGS)}

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Q.HQMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = A.darbuka_groove(CLIP + 0.3, 1.0); x = np.arange(len(g)) / SR
        kenv = np.clip((x - GREY0) / 0.5, 0, 1) * (1 - np.clip((x - (REV1 - 0.2)) / 0.3, 0, 1))
        g = A.muffle(g, kenv) * (1 - 0.35 * kenv) * np.minimum(1, x / 0.4) * np.clip((CLIP + 0.05 - x) / 0.12, 0, 1)
        mx.fadd(g, 0.0, 0.55)
        for i in range(HOOK_N): Q.key_click(mx, i / CPS, 0.026)
        for _, _, t0 in TAGS: Q.key_click(mx, t0, 0.05)
        mx.whoosh(REV0, REV1 - REV0 + 0.2, 0.12); mx.shimmer(REV1 - 0.1, 1174.7, 0.03)
        for i, (name, (ox, oy), t0) in enumerate(TAGS):
            x0, y0 = ANCH[name]; hit = REV0 + (REV1 - REV0) * (np.hypot(x0 + ox - FACE[0], y0 + oy - FACE[1]) / 1700) ** (1 / 1.3) * 0.9
            p = Q.pluck(Q.note(A.HIJAZ[i + 2]), 0.6, 0.55) * np.exp(-np.arange(int(0.6 * SR)) / SR * 5); mx.fadd(p, hit, 0.13)
        Q.impact(mx, YOU, 0.18); Q.bubble_pop(mx, POLL, 0.09)
        mx.write("s8e1_audio.wav")
    render(frame, TOTAL, "s8e1_audio.wav", OUT)
