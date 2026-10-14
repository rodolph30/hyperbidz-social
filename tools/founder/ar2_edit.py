"""Arabic test 2 (Lebanese), office with the big HyperBidz sign. Same line as test 1, new staging: the question types
itself (RTL) on the desk; 'الناس الصحّ' — four people pop in on the left wall, checked and linked; 'ومع HyperBidz' — the
ceiling sign flares with a shockwave; 'في مطرح إلك' — as he gestures to the right, an empty dashed seat spins in right
above his hand, 'مطرحك', with a shockwave on 'إلك'. Arabic captions, warm groove, held last shot, Arabic end card.
The laptop's Apple logo is inpainted away; the clip's blurred last 0.4 s is cut."""
import sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
import s6_common as K
import ar_common as A
from s7_common import ease, fade, shield, put

OUT = sys.argv[1]; SHOT = 7.6; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
def clean(fr):
    a = np.asarray(fr.convert("RGB")).copy(); x0, y0, x1, y1 = 880, 1130, 1000, 1255; reg = a[y0:y1, x0:x1]
    m = np.zeros(reg.shape[:2], np.uint8); cv2.ellipse(m, (62, 63), (30, 36), 0, 0, 360, 255, -1); a[y0:y1, x0:x1] = cv2.inpaint(reg, m, 9, cv2.INPAINT_TELEA)
    return Image.fromarray(a)
FR = [clean(f) for f in decode()]
SIGN = (150, 130, 730, 410); SIGN_C = (430, 275); SEAT = (920, 640)
Q1, PEOPLE, HB, PLACE, YOU = 0.0, 2.22, 4.26, 4.98, 5.68
CAPS = [(2.16, 3.5, [("الناس الصحّ.", True)]), (3.6, 4.95, [("ومع HyperBidz،", False)]), (4.95, CLIP - 0.05, [("في مطرح إلك.", True)])]
HOOK = [("تعرف شو اللي بيخلّي", False), ("الشغل يكبر؟", True)]; HOOK_N = sum(len(s) for s, _ in HOOK); CPS = 30
CLUSTER = [(95, 565), (232, 600), (112, 735), (245, 778)]

def sign_glow(im, k):
    if k <= 0.01: return
    x0, y0, x1, y1 = SIGN; reg = np.asarray(im.crop(SIGN).convert("RGB"), np.float32)
    m = (reg.mean(-1) > 185).astype(np.uint8) * 255
    g = np.asarray(Image.fromarray(m).resize(((x1 - x0) // 2, (y1 - y0) // 2)).filter(ImageFilter.GaussianBlur(10)).resize((x1 - x0, y1 - y0), Image.BILINEAR), np.float32)[..., None] / 255
    col = np.array([170, 150, 255], np.float32) / 255; out = 255 - (255 - reg) * (1 - np.clip(g * k * 1.5, 0, 1) * col)
    im.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA"), (x0, y0))

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = A.end_card(t - CLIP, END); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = Q.hq_grade(fr, 0.2)
    sign_glow(im, 0.12 + 0.05 * np.sin(t * 2.4) + flare(t, HB, 1.0, 1.0))
    im = hold_zoom(im, t, SHOT, 6.8, HOLD, 1.06, (600, 820))
    sx, sy = Q.shake_off(t, HB, 9, 0.3); im = Q.shake(im, sx, sy)
    ah = fade(t, -0.2, PEOPLE - 0.06, 0.2, 0.3)                                                          # the question
    if ah > 0:
        n = HOOK_N if t > Q1 + HOOK_N / CPS else max(1, int((t - Q1) * CPS) + 1)
        lay = A.typed_ar(HOOK, n, 64, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 820, lay.height + 50; y = 1620
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.62)
        put(im, lay, W / 2 + w / 2 - 50 - lay.width, y - h / 2 + 18, ah)
    if t >= PEOPLE:                                                                                    # the right people
        a_all = 1 - ease((t - CLIP + 0.35) / 0.3); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for i, (p, q) in enumerate(((0, 1), (0, 2), (1, 3), (2, 3), (1, 2))):
            kl = ease((t - PEOPLE - 0.4 - 0.08 * i) / 0.3)
            if kl > 0: (x0, y0), (x1, y1) = CLUSTER[p], CLUSTER[q]; d.line([(x0, y0), (x0 + (x1 - x0) * kl, y0 + (y1 - y0) * kl)], fill=(205, 194, 255, int(170 * a_all)), width=3)
        im.alpha_composite(L)
        for i, ((x, y), lay) in enumerate(zip(CLUSTER, A.PEOPLE_L)):
            t0 = PEOPLE + 0.12 * i
            if t >= t0: R.paste_center(im, lay, x, y + 4 * np.sin(t * 2 + i), min(1, (t - t0) / 0.06) * a_all, Q.slam((t - t0) / 0.22) * 0.85)
        if t >= PLACE:                                                                                 # your place
            R.paste_center(im, A.seat(t, 132), *SEAT, min(1, (t - PLACE) / 0.08) * a_all, 0.6 + 0.4 * Q.pop((t - PLACE) / 0.4))
            R.paste_center(im, A.SEAT_LABEL, SEAT[0], SEAT[1] - 120, ease((t - PLACE - 0.25) / 0.3) * a_all)
    Q.shockwave(im, *SIGN_C, (t - HB) / 0.6, (170, 150, 255), 460); Q.shockwave(im, *SIGN_C, (t - HB - 0.12) / 0.6, Q.LAV, 320, 4)
    Q.shockwave(im, *SEAT, (t - YOU) / 0.55, Q.LAV, 330, 5)
    Q.flash(im, flare(t, HB, 0.22, 0.3), (240, 232, 255))
    A.ar_captions(im, t, CAPS)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = K.GrooveMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = K.groove(CLIP + END, 0.0, 1.0, seed=23); x = np.arange(len(g)) / SR; mx.fadd(g * np.minimum(1, x / 0.8), 0.0, 0.5)
        for i in range(HOOK_N): Q.key_click(mx, Q1 + i / CPS, 0.024)
        for i in range(4): Q.ding(mx, PEOPLE + 0.12 * i, (1046.5, 1318.5, 1568, 2093)[i], 0.05)
        Q.impact(mx, HB, 0.22); Q.V.chime(mx, HB + 0.02, 1318.5, 0.045); mx.shimmer(HB + 0.05, 1568, 0.025)
        mx.whoosh(PLACE, 0.4, 0.1); Q.bubble_pop(mx, PLACE + 0.05, 0.07); Q.V.chime(mx, YOU, 1568, 0.05)
        mx.write("ar2_audio.wav")
    render(frame, TOTAL, "ar2_audio.wav", OUT)
