"""Season 7 Ep. 4 "The $1 start" (HQ office, crazy rocket). The hook types itself: "Why would I start / this watch at
$1?". On 'one dollar' a giant glowing $1 slams onto his chest (STARTING BID) with an impact. On 'because the price…' it
takes off: the number rockets up, bid chips shoot past, speed lines, a rumble and a riser; past $480 it turns into a
blur of digits. On 'It's where they stop.' the groove tape-stops, everything freezes, a gavel bangs, a black bar
redacts the number (WHERE THEY STOP) and it flies into the wax seal, which blasts a shockwave. Held last shot with a
push-in, HQ end card 'Start at $1. / See where they stop.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
from s7_common import ease, fade, shield, put, captions

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
FR = decode()
SEAL = (402, 1505); SEAL_BASE = 0.74
CAPS = [(3.40, 6.05, ["Because the price isn't", "where you [start.]"]), (6.55, 9.35, ["It's where they [stop.]"])]
HOOK = [[("Why would I start", False)], [("this watch at $1?", True)]]; HOOK_N = 34; CPS = 36
ONE, GO, LEGIBLE, STOP, RED, FLY0, FLY1 = 2.15, 3.45, 5.6, 6.63, 6.63, 7.05, 7.38
PART = Q.part_tag(4); KR = np.log(480) / (LEGIBLE - GO)

def value(t):
    return 1 if t < GO else int(round(np.exp(KR * (t - GO))))

def fmt(v): return f"${v:,}"

_TL = {}
def counter(txt, blur=0.0, split=0.0, size=210):
    key = (txt, size)
    if key not in _TL:
        if len(_TL) > 400: _TL.clear()
        _TL[key] = Q.big(txt, size, WHITE, (124, 92, 255))
    lay = _TL[key]
    if split > 0.5:
        a = np.asarray(lay); r = np.roll(a, int(split), 1); b = np.roll(a, -int(split), 1)
        out = a.copy(); out[..., 0] = np.maximum(a[..., 0], r[..., 0]); out[..., 2] = np.maximum(a[..., 2], b[..., 2]); out[..., 3] = np.maximum(a[..., 3], np.maximum(r[..., 3], b[..., 3]))
        lay = Image.fromarray(out)
    if blur > 0.3: lay = lay.filter(ImageFilter.GaussianBlur(blur))
    return lay

rng = np.random.default_rng(21); CHIPS = []
for i in range(46):
    u = rng.uniform(); t0 = GO + 0.15 + (STOP - GO - 0.2) * np.sqrt(u)
    x = rng.uniform(70, 1010)
    if 330 < x < 750: x = rng.choice([rng.uniform(70, 330), rng.uniform(750, 1010)])
    lay = Q.bid_chip("ABCDEGHJKLMNRSTZ"[i % 16], ["+$5", "+$10", "+$25", "+$40", "+$80", "+$150", "+$300"][min(6, int((t0 - GO) / 0.45))], Q.CROWD_COLS[i % 8], 30)
    CHIPS.append((t0, x, rng.uniform(0.55, 0.9), lay))

def stopped(t): return min(t, STOP)

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = Q.end_card7(t - CLIP, ["Start at $1.", "See where they stop."], END); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = Q.hq_grade(fr)
    run = ease((t - GO) / 2.5) if GO <= t < STOP else 0
    Q.z_glow(im, 0.18 + 0.08 * np.sin(t * 2.4) + flare(t, ONE, 0.7) + 0.6 * run * (0.6 + 0.4 * np.sin(t * 30)) + flare(t, FLY1, 0.9))
    Q.seal_glow(im, *SEAL, min(1.0, SEAL_BASE + 0.1 * np.sin(t * 2.4) + flare(t, FLY1, 0.5, 1.0)), flare(t, FLY1, 1.0, 0.6))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 1100))
    dx, dy = Q.shake_off(t, ONE, 16, 0.35); sx, sy = Q.shake_off(t, STOP, 12, 0.3, 1); fx, fy = Q.shake_off(t, FLY1, 9, 0.3, 2)
    rx, ry = (run * 6 * np.sin(t * 87), run * 6 * np.cos(t * 63)) if run else (0, 0)
    im = Q.shake(im, dx + sx + fx + rx, dy + sy + fy + ry)
    a = fade(t, 0.0, 7.4, 0.3, 0.4)
    if a > 0: R.paste_center(im, PART, W / 2, 215, a)
    ah = fade(t, -0.2, ONE + 0.05, 0.2, 0.2)                                                          # typed hook
    if ah > 0:
        n = HOOK_N if t > HOOK_N / CPS else max(1, int(t * CPS) + 1)
        lay = Q.typed_lines(HOOK, n, 70, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 810, lay.height + 64; y = 1090
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.6)
        put(im, lay, W / 2 - w / 2 + 52, y - h / 2 + 30, ah)
    Q.speed_lines(im, t, run * 0.9 if t < STOP else 0)
    for t0, x, dur, lay in CHIPS:                                                                     # bids shooting past
        tt = stopped(t)
        if tt < t0: continue
        k = (tt - t0) / dur
        if k > 1: continue
        y = 1750 - 1900 * k; al = min(1, k * 6) * (1 - ease((t - STOP) / 0.3) if t > STOP else 1)
        if al > 0.01: R.paste_center(im, lay, x + 30 * np.sin(k * 5 + x), y, al, 0.9)
    if ONE <= t < FLY1 + 0.4:                                                                         # the number
        tt = stopped(t); v = value(tt)
        if tt < LEGIBLE: txt, blur, split = fmt(v), 0, 0
        else:
            r = np.random.default_rng(int(tt * 40)); txt = "$" + f"{r.integers(1000, 9999):,}"; blur, split = (3.4, 12) if t < STOP else (7.0, 18)
        lay = counter(txt, blur, split)
        lab = Q.mono("STARTING BID" if tt < GO + 0.25 else ("WHERE THEY STOP" if t >= RED else "LIVE"), 26, Q.LAV, 7)
        s = Q.slam((t - ONE) / 0.22) * (1 + 0.04 * np.sin(tt * 40) * run)
        if t < FLY0:
            if t < STOP: R.paste_center(im, lay, W / 2, 1090, min(1, (t - ONE) / 0.06), s)
            R.paste_center(im, lab, W / 2, 935, ease((t - ONE - 0.1) / 0.2))
            if t >= RED:                                                                              # redacted
                kb = 1.0; bw = int(780 * (1 + 0.12 * Q.slam((t - RED) / 0.15) - 0.12)); bar = Image.new("RGBA", (max(2, bw), 190), (0, 0, 0, 0))
                ImageDraw.Draw(bar).rounded_rectangle((0, 0, max(2, bw) - 1, 189), radius=26, fill=(4, 4, 10, 255), outline=Q.VIO + (235,), width=4)
                R.paste_center(im, bar, W / 2 - 390 + bw / 2, 1095); R.paste_center(im, Q.lock_icon(40), W / 2 - 200, 935, kb)
        else:
            k = ease((t - FLY0) / (FLY1 - FLY0)); card = Image.new("RGBA", (800, 200), (0, 0, 0, 0))
            ImageDraw.Draw(card).rounded_rectangle((0, 0, 799, 199), radius=26, fill=(4, 4, 10, 255), outline=Q.VIO + (235,), width=4)
            x = W / 2 + (SEAL[0] - W / 2) * k; y = 1095 + (SEAL[1] - 1095) * k * k - 70 * np.sin(np.pi * k)
            R.paste_center(im, card, x, y, 1 - ease((k - 0.75) / 0.25), 1 - 0.95 * k)
    Q.shockwave(im, *SEAL, (t - FLY1) / 0.6); Q.shockwave(im, *SEAL, (t - FLY1 - 0.12) / 0.6, Q.LAV, 380, 4)
    Q.flash(im, flare(t, ONE, 0.3, 0.3) + flare(t, STOP, 0.55, 0.3) + flare(t, FLY1, 0.3, 0.3), (232, 226, 255))
    captions(im, t, CAPS, y=1730, size=58)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Q.HQMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = Q.sneaky(CLIP + 0.2, 0.0, 1.0, seed=9); x = np.arange(len(g)) / SR
        g = g * (1 + 0.35 * np.clip((x - GO) / (STOP - GO), 0, 1) * (x < STOP))                          # it builds
        D = 0.32; i0 = int((STOP - D) * SR); tau = np.arange(int(D * SR)) / SR; pos = (STOP - D) + tau - tau ** 2 / (2 * D)   # tape stop
        g[i0:i0 + len(tau)] = np.interp(pos, x, g) * (1 - tau / D) ** 0.5; g[int(STOP * SR):] = 0
        env = np.minimum(1, x / 0.5); mx.fadd(g * env, 0.0, 0.5)
        for i in range(HOOK_N): Q.key_click(mx, i / CPS, 0.028)
        Q.impact(mx, ONE, 0.28); Q.ding(mx, ONE + 0.02, 2093, 0.05)
        Q.riser(mx, GO, STOP, 0.11, 150, 2200)
        tk = GO; k = 0
        while tk < STOP: Q.coin(mx, tk, 0.017); k += 1; tk += 1 / (5 + 28 * ((tk - GO) / (STOP - GO)) ** 1.5)
        Q.gavel(mx, STOP, 0.34); Q.impact(mx, STOP, 0.2); Q.V.lock(mx, RED, 0.2)
        mx.whoosh(FLY0, 0.33, 0.2); Q.impact(mx, FLY1, 0.2); Q.V.chime(mx, FLY1 + 0.02, 1318.5, 0.05); mx.shimmer(FLY1 + 0.05, 1568, 0.03)
        mx.write("s7e4_audio.wav")
    render(frame, TOTAL, "s7e4_audio.wav", OUT)
