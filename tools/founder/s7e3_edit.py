"""Season 7 Ep. 3 "Who decides?" (HQ office, crazy game show). The hook types itself: "Who decides what / something's
worth?". Then three contestants slam onto his chest with a game-show ding each: YOU? · A DEALER? · YOUR COUSIN (who
'knows a guy', with a "trust me habibi" bubble). On "No." the groove cuts, a buzzer, three coral X stamps, a shake and a
red flash, and the cards fly off. On "The buyers do." an impact and a burst: a crowd of bidder avatars and +$ bid chips
explodes out around him. On "All at once." they all rush into the wax seal, which flares; the wall Z flares with it.
Held last shot with a push-in, HQ end card 'The buyers decide. / All at once.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
import s6_common as K
from s7_common import ease, fade, shield, put, captions

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
FR = decode()
SEAL = (400, 1530); SEAL_BASE = 0.68
CAPS = [(1.85, 2.45, ["[You?]"]), (2.45, 3.32, ["A [dealer?]"]), (3.36, 4.98, ["Your cousin", "who [knows a guy?]"]), (5.02, 5.78, ["[No.]"]),
        (5.82, 6.98, ["The [buyers] do."]), (7.0, 9.35, ["[All at once.]"])]
HOOK = [[("Who decides what", False)], [("something's worth?", True)]]; HOOK_N = 34; CPS = 36
C1, C2, C3, NO, BUY, ALL = 1.9, 2.53, 3.41, 5.07, 5.85, 7.05
PART = Q.part_tag(3)

def podium(icon, title, sub=None, w=300, h=250):
    im = Q.glass_layer(w, h, 30, fill=(14, 14, 30, 244), edge=(205, 194, 255, 150))
    bar = Image.new("RGBA", (w - 60, 6), (0, 0, 0, 0)); bar.paste(Q.V.lin_grad(w - 60, 6, Q.BLUE, Q.VIO), (0, 0)); im.alpha_composite(bar, (30, 0))
    im.alpha_composite(icon, ((w - icon.width) // 2, 26))
    tl = R.text_layer(title, R.font(40, 700), WHITE); im.alpha_composite(tl, ((w - tl.width) // 2, 138))
    if sub: sl = Q.mono(sub, 18, Q.LAV, 3); im.alpha_composite(sl, ((w - sl.width) // 2, 196))
    return im

def dollar_icon(s=96):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    im.paste(Q.V.lin_grad(s, s, (240, 150, 60), (221, 92, 140)), (0, 0), m); tl = R.text_layer("$", R.font(64, 700), WHITE)
    im.alpha_composite(tl, ((s - tl.width) // 2, (s - tl.height) // 2 - 6)); return im

def phone_icon(s=96):
    im = Image.new("RGBA", (s + 90, s), (0, 0, 0, 0)); m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    disc = Image.new("RGBA", (s, s), (0, 0, 0, 0)); disc.paste(Q.V.lin_grad(s, s, (46, 170, 140), (53, 126, 221)), (0, 0), m); im.alpha_composite(disc, (45, 0))
    d = ImageDraw.Draw(im); d.rounded_rectangle((45 + s * 0.32, s * 0.2, 45 + s * 0.68, s * 0.8), radius=8, outline=(255, 255, 255, 255), width=5)
    d.line([(45 + s * 0.44, s * 0.7), (45 + s * 0.56, s * 0.7)], fill=(255, 255, 255, 255), width=4); return im

def habibi():
    tl = R.text_layer("trust me habibi", R.font(26, 600), (20, 20, 30)); w, h = tl.width + 34, tl.height + 22
    im = Image.new("RGBA", (w, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(255, 255, 255, 250)); d.polygon([(w * 0.22, h - 2), (w * 0.18, h + 13), (w * 0.36, h - 2)], fill=(255, 255, 255, 250))
    im.alpha_composite(tl, (17, 9)); return im

CARDS = [(C1, 200, podium(Q.you_avatar(96), "You?")), (C2, 540, podium(dollar_icon(), "A dealer?")),
         (C3, 880, podium(phone_icon(), "Your cousin", "WHO KNOWS A GUY"))]
HAB = habibi(); XM = Q.xmark(150)

rng = np.random.default_rng(11); CROWD = []
letters = "ABCDEGHJKLMNRSTZ"; amounts = ["+$50", "+$120", "+$75", "+$300", "+$40", "+$200", "+$90", "+$150", "+$60", "+$250", "+$110", "+$80"]
pts = []
while len(pts) < 58:
    tx, ty = rng.uniform(70, 1010), rng.uniform(280, 1300)
    if abs(tx - 540) < 240 and ty < 930: continue                                                        # keep his face clear
    if any((tx - a) ** 2 + ((ty - b) * 1.6) ** 2 < 95 ** 2 for a, b in pts): continue
    pts.append((tx, ty))
for i, (tx, ty) in enumerate(pts):
    chip = i % 3 == 0
    lay = Q.bid_chip(letters[i % len(letters)], amounts[(i // 3) % len(amounts)], Q.CROWD_COLS[i % 8]) if chip else K.avatar(letters[(i * 5) % len(letters)], Q.CROWD_COLS[(i * 3) % 8], int(rng.uniform(50, 76)))
    CROWD.append((tx, ty, rng.uniform(0, 0.35), rng.uniform(0, 0.25), lay, i))

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = Q.end_card7(t - CLIP, ["The buyers decide.", "All at once."], END); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = Q.hq_grade(fr)
    Q.z_glow(im, 0.18 + 0.08 * np.sin(t * 2.4) + flare(t, 0.15, 0.6) + flare(t, BUY, 0.8) + flare(t, ALL + 0.45, 0.9))
    Q.seal_glow(im, *SEAL, min(1.0, SEAL_BASE + 0.1 * np.sin(t * 2.4) + flare(t, ALL + 0.45, 0.5, 1.0)), flare(t, ALL + 0.45, 1.0, 0.6))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 1100))
    dx, dy = Q.shake_off(t, NO, 16, 0.4); ex, ey = Q.shake_off(t, BUY, 10, 0.3, 1); fx, fy = Q.shake_off(t, ALL + 0.45, 9, 0.3, 2)
    im = Q.shake(im, dx + ex + fx, dy + ey + fy)
    Q.vignette(im, flare(t, NO, 0.85, 0.9))
    a = fade(t, 0.0, BUY + 0.1, 0.3, 0.25)
    if a > 0: R.paste_center(im, PART, W / 2, 215, a)
    ah = fade(t, -0.2, 1.85, 0.2, 0.25)                                                               # typed hook
    if ah > 0:
        n = HOOK_N if t > HOOK_N / CPS else max(1, int(t * CPS) + 1)
        lay = Q.typed_lines(HOOK, n, 70, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 810, lay.height + 64; y = 1090
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.86)
        put(im, lay, W / 2 - w / 2 + 52, y - h / 2 + 30, ah)
    for j, (t0, cx, card) in enumerate(CARDS):                                                        # the contestants
        if not t0 <= t < 5.95: continue
        kf = max(0, (t - 5.42 - 0.05 * j) / 0.4); s = Q.slam((t - t0) / 0.22) * (1 - 0.3 * kf)
        x = cx + (-1, 0, 1)[j] * 700 * kf ** 2; y = 1095 + (0.2 if j != 1 else 1) * 900 * kf ** 2; rot = (-1, 0.4, 1)[j] * 40 * kf
        lay = card.rotate(rot, expand=True, resample=Image.BICUBIC) if rot else card
        R.paste_center(im, lay, x, y, min(1, (t - t0) / 0.08) * (1 - min(1, kf)), s)
        if j == 2 and t < NO: R.paste_center(im, HAB, cx - 30, 940 - 6 * Q.pop((t - t0 - 0.25) / 0.3), ease((t - t0 - 0.25) / 0.15), 0.9 + 0.1 * Q.pop((t - t0 - 0.25) / 0.3))
        tx_ = NO + 0.06 * j
        if t >= tx_: R.paste_center(im, XM, x, y - 20, min(1, (t - tx_) / 0.06) * (1 - min(1, kf)), Q.slam((t - tx_) / 0.18) * (1 - 0.3 * kf))
    if BUY <= t < ALL + 0.5:                                                                          # the buyers, all at once
        for tx, ty, d0, d1, lay, i in CROWD:
            kb = Q.pop((t - BUY - d0 * 0.5) / 0.55); kc = Q.ease_in((t - ALL - d1) / 0.42)
            if t < BUY + d0 * 0.5: continue
            bx = 540 + (tx - 540) * kb + 7 * np.sin(t * 3 + i); by = 1090 + (ty - 1090) * kb + 7 * np.cos(t * 2.6 + i)
            x = bx + (SEAL[0] - bx) * kc; y = by + (SEAL[1] - by) * kc
            R.paste_center(im, lay, x, y, min(1, (t - BUY - d0 * 0.5) / 0.08) * (1 - ease((kc - 0.75) / 0.25)), max(0.15, (0.4 + 0.6 * min(1, kb)) * (1 - 0.8 * kc)))
    Q.shockwave(im, *SEAL, (t - ALL - 0.45) / 0.6); Q.shockwave(im, *SEAL, (t - ALL - 0.58) / 0.6, Q.LAV, 380, 4)
    Q.flash(im, flare(t, BUY, 0.45, 0.35) + flare(t, ALL + 0.45, 0.35, 0.3), (230, 222, 255))
    captions(im, t, CAPS, y=1730, size=58)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Q.HQMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = Q.sneaky(CLIP + 0.2, 0.0, 1.0, seed=7); x = np.arange(len(g)) / SR
        env = np.minimum(1, x / 0.5) * np.clip((CLIP + 0.05 - x) / 0.12, 0, 1)
        env *= np.where((x > NO - 0.02) & (x < BUY), 0.0, 1.0); env = np.convolve(env, np.ones(480) / 480, "same")   # the groove cuts on "No."
        g2 = Q.sneaky(CLIP + 0.2, 0.0, 1.0, seed=8) * np.clip((x - BUY) / 0.05, 0, 1) * 0.35             # and comes back doubled
        mx.fadd(g * env + g2 * env, 0.0, 0.5)
        for i in range(HOOK_N): Q.key_click(mx, i / CPS, 0.028)
        for t0, f in ((C1, 1318.5), (C2, 1568), (C3, 1760)): Q.ding(mx, t0, f, 0.08)
        Q.bubble_pop(mx, C3 + 0.25, 0.06)
        Q.buzzer(mx, NO, 0.2); [mx.thud(NO + 0.06 * j, 0.3) for j in range(3)]; mx.whoosh(5.42, 0.4, 0.15)
        Q.impact(mx, BUY, 0.45); mx.whoosh(BUY, 0.5, 0.18); [Q.coin(mx, BUY + 0.05 + 0.04 * i, 0.03) for i in range(14)]
        Q.riser(mx, ALL - 0.1, ALL + 0.45, 0.1); Q.impact(mx, ALL + 0.45, 0.35); Q.V.chime(mx, ALL + 0.47, 1318.5, 0.05); mx.shimmer(ALL + 0.5, 1568, 0.03)
        mx.write("s7e3_audio.wav")
    render(frame, TOTAL, "s7e3_audio.wav", OUT)
