"""Season 7 Ep. 2 "What's it worth?" (HQ office at night, fun). The hook types itself on his chest: "What's your /
car worth?". 'Not what you paid': a paper receipt pops up, PAID $24,000, and gets struck through. 'Not what you
want': a tag, WHAT YOU WANT $28,000 with two sparkles, struck through too. 'What someone would actually pay': both
fall away and a LIVE card scrambles through amounts; on 'You don't know' it lands on $ ? ? ? with a playful
'nope' pluck. The wall Z flares on the question and the punchline; the wax seal glows a step brighter than in E1.
Held last shot with a push-in, HQ end card 'You don't know. / Not yet.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
from s7_common import ease, fade, shield, put, captions

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
FR = decode()
SEAL = (402, 1515); SEAL_BASE = 0.62
CAPS = [(2.00, 3.30, ["Not what you [paid.]"]), (3.40, 4.70, ["Not what you [want.]"]),
        (4.75, 6.85, ["What someone would", "[actually pay.]"]), (6.92, 9.35, ["[You don't know.]"])]
HOOK = [[("What's your", False)], [("car worth?", True)]]; HOOK_N = 21; TYPE0, CPS = 0.0, 24
PAID, PAID_X, WANT, WANT_X, DROP, LIVE, NOPE = 2.05, 2.62, 3.45, 4.02, 4.72, 4.95, 6.98
CORAL = (255, 92, 120)
AMOUNTS = ["$ 14,200", "$ 9,800", "$ 17,500", "$ 12,900", "$ 21,000", "$ 11,300", "$ 16,400", "$ 8,700", "$ 19,200", "$ 13,600", "$ 15,100", "$ 10,400"]
PART = Q.part_tag(2)

def shadowed(lay, r=14, a=130):
    pad = 30; im = Image.new("RGBA", (lay.width + 2 * pad, lay.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, a), (pad, pad + 8), lay.getchannel("A"))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(r))); im.alpha_composite(lay, (pad, pad)); return im

def receipt(w=380, h=226):
    im = Image.new("RGBA", (w, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im); n = 12; st = w / n
    pts = [(0, 0), (w, 0), (w, h)] + [p for i in range(n, 0, -1) for p in ((i * st - st / 2, h + 13), ((i - 1) * st, h))]
    d.polygon(pts, fill=(246, 242, 234, 255))
    ink = (40, 40, 52); grey = (120, 118, 128)
    im.alpha_composite(Q.mono("RECEIPT  ·  2019", 20, grey, 4), (28, 24))
    for x in range(28, w - 28, 14): d.line([(x, 62), (x + 7, 62)], fill=grey + (255,), width=2)
    im.alpha_composite(Q.mono("PAID", 22, ink, 5), (28, 82))
    im.alpha_composite(R.text_layer("$24,000", R.font(76, 700), ink), (24, 112)); return im

def want_tag(w=400, h=226):
    im = Q.glass_layer(w, h, 30, fill=(16, 16, 34, 236), edge=(205, 194, 255, 140))
    im.alpha_composite(Q.mono("WHAT YOU WANT", 22, Q.LAV, 5), (30, 30))
    im.alpha_composite(R.text_layer("$28,000", R.font(76, 700), WHITE), (26, 74))
    for (x, y, s) in ((w - 70, 30, 26), (w - 44, 66, 18)): R.paste_center(im, STARS[s], x, y, 0.9)
    return im

def strike(lay, k, y, x0=22, x1=None):
    if k <= 0: return lay
    lay = lay.copy(); x1 = x1 or lay.width - 22; L = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    ImageDraw.Draw(L).line([(x0, y + 8), (x0 + (x1 - x0) * k, y - 8)], fill=CORAL + (255,), width=9)
    lay.alpha_composite(L); return lay

RECEIPT, WANT_TAG = receipt(), want_tag()

def live_card(t, w=640, h=236):
    im = Q.glass_layer(w, h, 34, fill=(14, 14, 30, 242))
    lab = Q.mono("WHAT SOMEONE WOULD PAY", 21, Q.LAV, 4); x = (w - lab.width - 30) // 2
    im.alpha_composite(K_dot(t), (x, 36)); im.alpha_composite(lab, (x + 30, 34))
    if t < NOPE:
        i = int((t - LIVE) / 0.075); num = R.text_layer(AMOUNTS[i % len(AMOUNTS)], R.font(100, 700), WHITE)
        im.alpha_composite(num, ((w - num.width) // 2, 80))
    else:
        qm = Q.qmarks(t, 96); s = 0.8 + 0.2 * Q.pop((t - NOPE) / 0.35)
        qm = qm.resize((int(qm.width * s), int(qm.height * s)), Image.LANCZOS); im.alpha_composite(qm, ((w - qm.width) // 2, 70 + int((1 - s) * 60)))
    return im

def K_dot(t):
    import s6_common as K
    d = K.dot((255, 77, 106), 8); d.putalpha(d.getchannel("A").point(lambda v: int(v * (0.55 + 0.45 * np.sin(t * 6))))); return d

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = Q.end_card7(t - CLIP, ["You don't know.", "Not yet."], END); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = Q.hq_grade(fr)
    Q.z_glow(im, 0.18 + 0.08 * np.sin(t * 2.4) + flare(t, 0.4, 0.75) + flare(t, NOPE, 0.8))
    Q.seal_glow(im, *SEAL, min(1.0, SEAL_BASE + 0.1 * np.sin(t * 2.4) + flare(t, NOPE, 0.35, 0.9)))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 1100))
    a = fade(t, 0.0, 7.4, 0.3, 0.4)
    if a > 0: R.paste_center(im, PART, W / 2, 215, a)
    ah = fade(t, -0.2, 1.95, 0.2, 0.3)                                                                # typed hook
    if ah > 0:
        n = HOOK_N if t > TYPE0 + HOOK_N / CPS else max(1, int((t - TYPE0) * CPS) + 1)
        lay = Q.typed_lines(HOOK, n, 74, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 640, lay.height + 64; y = 1090
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.86)
        put(im, lay, W / 2 - w / 2 + 52, y - h / 2 + 30, ah)
    for t0, tx, lay, cx, rot, sy in ((PAID, PAID_X, RECEIPT, 292, 4, 154), (WANT, WANT_X, WANT_TAG, 790, -3, 118)):   # paid / want
        if not t0 <= t < DROP + 0.45: continue
        l = strike(lay, ease((t - tx) / 0.25), sy); kd = max(0, (t - DROP - (0.06 if cx > 540 else 0)) / 0.34)
        s = 0.8 + 0.2 * Q.pop((t - t0) / 0.35); r = rot + 28 * kd * kd * (1 if cx > 540 else -1)
        l = shadowed(l).rotate(r, expand=True, resample=Image.BICUBIC)
        R.paste_center(im, l, cx, 1095 + 700 * kd * kd, min(1, (t - t0) / 0.1) * (1 - min(1, kd)), s)
    al = fade(t, LIVE, CLIP + 0.3, 0.15, 0.4)                                                         # what someone would pay
    if al > 0: R.paste_center(im, live_card(t), W / 2, 1095, al, 0.86 + 0.14 * Q.pop((t - LIVE) / 0.35))
    captions(im, t, CAPS, y=1730, size=56)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Q.HQMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = Q.sneaky(CLIP + 0.2, 0.0, 1.0, seed=6); x = np.arange(len(g)) / SR
        env = np.minimum(1, x / 0.5) * np.clip((CLIP + 0.05 - x) / 0.12, 0, 1); mx.fadd(g * env, 0.0, 0.5)
        for i in range(HOOK_N): Q.key_click(mx, TYPE0 + i / CPS, 0.03)
        Q.V.ticks(mx, PAID, PAID + 0.25, rate=40, g=0.02)                                            # receipt printing
        mx.whoosh(PAID_X, 0.18, 0.12); Q.bubble_pop(mx, WANT, 0.06); mx.whoosh(WANT_X, 0.18, 0.12)
        mx.whoosh(DROP, 0.4, 0.14); Q.bubble_pop(mx, LIVE, 0.07); Q.V.ticks(mx, LIVE + 0.05, NOPE, rate=13, g=0.028)
        for i, m in enumerate((69, 65, 62)):                                                          # 'nope'
            s = Q.pluck(Q.note(m), 0.5, 0.5) * np.exp(-np.arange(int(0.5 * SR)) / SR * 6); mx.fadd(s, NOPE + 0.62 + i * 0.1, 0.13)
        mx.write("s7e2_audio.wav")
    render(frame, TOTAL, "s7e2_audio.wav", OUT)
