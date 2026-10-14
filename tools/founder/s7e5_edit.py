"""Season 7 Ep. 5 "The last three seconds" (HQ office, crazy countdown). The hook types itself: "Nobody tells you /
this about auctions.". On 'the last three seconds' the groove cuts and a ring timer slams in, 0:03 → 0:00, with a
heartbeat every second, a red pulse and a bid storm that floods the screen faster and faster. At 0:00: SOLD slams down,
gavel, flash, shake, the bids blast away. On 'what something's worth to them' it calms: SOLD stays, WHAT IT'S WORTH TO
THEM, and the wax seal blasts a shockwave on 'them'. Held last shot with a push-in, HQ end card 'The last 3 seconds /
tell the truth.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
import s6_common as K
from s7_common import ease, fade, shield, put, captions

OUT = sys.argv[1]; SHOT = 7.5; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
FR = decode()
SEAL = (396, 1498); SEAL_BASE = 0.8
CAPS = [(0.55, 2.72, ["Most auctions", "are [decided]…"]), (2.72, 4.15, ["in the last", "[three seconds.]"]), (4.15, 5.86, ["That's when people", "[finally admit]…"]),
        (5.88, 8.85, ["what something's worth", "[to them.]"])]
HOOK = [[("Nobody tells you", False)], [("this about auctions.", True)]]; HOOK_N = 36; CPS = 36
T3, SOLD, THEM = 2.8, 5.8, 7.12
PART = Q.part_tag(5)

rng = np.random.default_rng(31); STORM = []; pts = []
while len(pts) < 44:
    tx, ty = rng.uniform(80, 1000), rng.uniform(290, 1320)
    if abs(tx - 540) < 240 and ty < 900: continue
    if abs(tx - 540) < 210 and 930 < ty < 1260: continue                                                # the ring lives here
    if any((tx - a) ** 2 + ((ty - b) * 1.7) ** 2 < 100 ** 2 for a, b in pts): continue
    pts.append((tx, ty))
amts = ["+$100", "+$200", "+$50", "+$500", "+$150", "+$300", "+$1,000", "+$250", "+$400", "+$75"]
for i, (tx, ty) in enumerate(pts):
    t0 = T3 + 0.15 + (SOLD - T3 - 0.25) * (i / len(pts)) ** 0.7
    STORM.append((t0, tx, ty, Q.bid_chip("ABCDEGHJKLMNRSTZ"[i % 16], amts[i % len(amts)], Q.CROWD_COLS[(i * 3) % 8], 32), i))
def sold_card(w=600, h=300):
    im = Q.glass_layer(w, h, 30, fill=(14, 14, 30, 246), edge=Q.CORAL + (255,))
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(L).rounded_rectangle((10, 10, w - 11, h - 11), radius=24, outline=Q.CORAL + (255,), width=6); im.alpha_composite(L)
    tl = Q.big("SOLD", 150, Q.CORAL, (255, 80, 110)); im.alpha_composite(tl, ((w - tl.width) // 2, -10))
    lb = Q.mono("WHAT IT'S WORTH TO THEM", 22, Q.LAV, 5); im.alpha_composite(lb, ((w - lb.width) // 2, h - 60)); return im.rotate(-6, expand=True, resample=Image.BICUBIC)
SOLD_L = sold_card()

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = Q.end_card7(t - CLIP, ["The last 3 seconds", "tell the truth."], END); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = Q.hq_grade(fr)
    beat = sum(flare(t, T3 + i, 1.0, 0.45) for i in range(3)) if T3 <= t < SOLD else 0
    Q.z_glow(im, 0.18 + 0.08 * np.sin(t * 2.4) + 0.35 * beat + flare(t, SOLD, 0.9) + flare(t, THEM, 0.8))
    Q.seal_glow(im, *SEAL, min(1.0, SEAL_BASE + 0.1 * np.sin(t * 2.4) + flare(t, THEM, 0.4, 1.0)), flare(t, THEM, 1.0, 0.6))
    im = hold_zoom(im, t, SHOT, 6.6, HOLD, 1.07, (540, 1100))
    bx, by = (beat * 5 * np.sin(t * 90), beat * 5 * np.cos(t * 70)); sx, sy = Q.shake_off(t, SOLD, 18, 0.45); fx, fy = Q.shake_off(t, THEM, 8, 0.3, 2)
    im = Q.shake(im, bx + sx + fx, by + sy + fy)
    hot = ease((t - T3) / 3.0) if T3 <= t < SOLD else 0
    Q.vignette(im, (0.25 + 0.55 * beat) * hot * 1.4 + flare(t, SOLD, 0.6, 0.6))
    a = fade(t, 0.0, T3, 0.3, 0.25)
    if a > 0: R.paste_center(im, PART, W / 2, 215, a)
    ah = fade(t, -0.2, T3, 0.2, 0.2)                                                                  # typed hook
    if ah > 0:
        n = HOOK_N if t > HOOK_N / CPS else max(1, int(t * CPS) + 1)
        lay = Q.typed_lines(HOOK, n, 66, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 810, lay.height + 64; y = 1090
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.86)
        put(im, lay, W / 2 - w / 2 + 48, y - h / 2 + 30, ah)
    for t0, tx, ty, lay, i in STORM:                                                                  # the bid storm
        if t < t0: continue
        kb = (t - SOLD) / 0.45 if t >= SOLD else 0
        if kb >= 1: continue
        x = tx + (tx - 540) * 1.4 * kb * kb; y = ty + (ty - 1090) * 1.4 * kb * kb
        R.paste_center(im, lay, x + 3 * np.sin(t * 9 + i), y, min(1, (t - t0) / 0.06) * (1 - kb), 0.75 + 0.25 * Q.pop((t - t0) / 0.25))
    if T3 <= t < SOLD + 0.25:                                                                         # the countdown
        frac = max(0.0, 1 - (t - T3) / (SOLD - T3)); sec = max(0, 3 - int(t - T3)) if t < SOLD else 0
        ring = Q.ring_timer(frac, f"0:0{sec}", hot)
        R.paste_center(im, ring, W / 2, 1095, 1 - ease((t - SOLD) / 0.25), Q.slam((t - T3) / 0.22) * (1 + 0.07 * beat))
    if t >= SOLD:                                                                                     # SOLD
        R.paste_center(im, SOLD_L, W / 2, 1090, min(1, (t - SOLD) / 0.05), Q.slam((t - SOLD) / 0.2) * (1 - 0.1 * ease((t - SOLD - 0.6) / 0.6)))
    Q.shockwave(im, *SEAL, (t - THEM) / 0.6); Q.shockwave(im, *SEAL, (t - THEM - 0.12) / 0.6, Q.LAV, 380, 4)
    Q.flash(im, flare(t, T3, 0.25, 0.3) + flare(t, SOLD, 0.7, 0.35) + flare(t, THEM, 0.25, 0.3), (255, 238, 242))
    captions(im, t, CAPS, y=1730, size=58)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Q.HQMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = Q.sneaky(CLIP + 0.2, 0.0, 1.0, seed=10); x = np.arange(len(g)) / SR
        env = np.minimum(1, x / 0.5) * np.clip((CLIP + 0.05 - x) / 0.12, 0, 1)
        env *= np.where(x < T3 - 0.02, 1.0, np.where(x < SOLD + 0.3, 0.0, 0.55)); env = np.convolve(env, np.ones(480) / 480, "same")
        mx.fadd(g * env, 0.0, 0.5)
        for i in range(HOOK_N): Q.key_click(mx, i / CPS, 0.026)
        Q.impact(mx, T3, 0.2)
        for i in range(3): Q.heartbeat(mx, T3 + i, 0.45)
        Q.V.ticks(mx, T3, SOLD, rate=4, g=0.045); Q.riser(mx, T3, SOLD, 0.09, 120, 1800)
        for t0, *_ in STORM: Q.coin(mx, t0, 0.018)
        Q.gavel(mx, SOLD, 0.34); Q.impact(mx, SOLD, 0.24); mx.whoosh(SOLD + 0.02, 0.45, 0.14)
        Q.impact(mx, THEM, 0.18); Q.V.chime(mx, THEM + 0.02, 1318.5, 0.05); mx.shimmer(THEM + 0.05, 1568, 0.03)
        mx.write("s7e5_audio.wav")
    render(frame, TOTAL, "s7e5_audio.wav", OUT)
