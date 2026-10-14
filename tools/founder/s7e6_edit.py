"""Season 7 Ep. 6 "Same watch" (HQ office, crazy guess storm). The hook types itself: "Notice something?". On 'you all
guessed a different price' guesses flood the screen, comment bubbles with a different amount each, popping faster and
faster; on 'for the same watch' focus brackets snap on the glass box (SAME WATCH) and every guess draws a thin line to
it. On 'That's why a fixed price' the guesses dim and a white FIXED PRICE $2,500 tag slams in; on 'always wrong' it
glitches and shatters, the guesses light back up and the wax seal blasts a shockwave. Held last shot, HQ end card
'A fixed price / is always wrong.'

GUESSES are placeholders: swap in the real guesses from Part 1's comments before this goes live."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
import s6_common as K
from s7_common import ease, fade, shield, put, captions

GUESSES = ["$1,200", "$350", "$4,800", "$900", "$15,000", "$2,300", "$600", "$8,500", "$1,750", "$3,000", "$450", "$12,000", "$2,000", "$5,500",
           "$800", "$7,200", "$1,000", "$25,000", "$3,600", "$1,500", "$700", "$9,900", "$2,750", "$6,000", "$1,100", "$4,000", "$500", "$18,000"]

OUT = sys.argv[1]; SHOT = 7.8; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
FR = decode()
SEAL = (402, 1521); SEAL_BASE = 0.86; BOX = (655, 1345, 945, 1600)
CAPS = [(1.45, 4.45, ["You all guessed a different", "price for the [same watch.]"]), (4.85, 6.66, ["That's why a", "[fixed price]"]), (6.66, 9.15, ["is always [wrong.]"])]
HOOK = [[("Notice something?", True)]]; HOOK_N = 17; CPS = 28
GUESS0, SAME, FIXED, WRONG, BOOM = 1.55, 3.45, 5.2, 6.74, 6.95
PART = Q.part_tag(6)

def guess_bubble(ini, amt, col):
    av = K.avatar(ini, col, 50); tx = R.text_layer(amt, R.font(36, 700), WHITE); h = 70; w = 8 + 50 + 16 + tx.width + 30
    im = Q.glass_layer(w, h + 12, 22, fill=(16, 16, 34, 238), edge=(205, 194, 255, 120))
    im.alpha_composite(av, (10, 10 + 6)); im.alpha_composite(tx, (74, (h + 12 - tx.height) // 2 - 3))
    d = ImageDraw.Draw(im); d.polygon([(26, h + 10), (22, h + 22), (40, h + 10)], fill=(16, 16, 34, 238)); return im

rng = np.random.default_rng(41); BUBS = []; pts = []
while len(pts) < len(GUESSES):
    tx, ty = rng.uniform(110, 970), rng.uniform(290, 1290)
    if abs(tx - 540) < 250 and ty < 900: continue
    if any(((tx - a) / 2.1) ** 2 + (ty - b) ** 2 < 84 ** 2 for a, b in pts): continue
    pts.append((tx, ty))
for i, ((tx, ty), g) in enumerate(zip(pts, GUESSES)):
    t0 = GUESS0 + (SAME - GUESS0 - 0.1) * (i / len(GUESSES)) ** 0.75
    BUBS.append((t0, tx, ty, guess_bubble("ABCDEGHJKLMNRSTZ"[(i * 7) % 16], g, Q.CROWD_COLS[(i * 3) % 8]), i))

def price_tag():
    w, h = 470, 250; im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(20 + 60, 30), (20 + w, 30), (20 + w, 30 + h), (20 + 60, 30 + h), (20, 30 + h / 2)], fill=(0, 0, 0, 140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im); d.polygon([(20 + 60, 20), (20 + w, 20), (20 + w, 20 + h), (20 + 60, 20 + h), (20, 20 + h / 2)], fill=(250, 248, 244, 255))
    d.ellipse((20 + 44, 20 + h / 2 - 14, 20 + 72, 20 + h / 2 + 14), fill=(14, 14, 30, 255))
    im.alpha_composite(Q.mono("FIXED PRICE", 26, (110, 108, 120), 6), (120, 58))
    im.alpha_composite(R.text_layer("$2,500", R.font(110, 700), (24, 24, 36)), (112, 96)); return im
TAG = price_tag()
SHARDS = []
_r = np.random.default_rng(5)
for j in range(7):
    y0, y1 = int(TAG.height * j / 7), int(TAG.height * (j + 1) / 7); piece = Image.new("RGBA", TAG.size, (0, 0, 0, 0)); piece.paste(TAG.crop((0, y0, TAG.width, y1)), (0, y0))
    SHARDS.append((piece, _r.uniform(-700, 700), _r.uniform(-900, 300), _r.uniform(-90, 90)))

def glitch(lay, k, seed):
    r = np.random.default_rng(seed); a = np.asarray(lay).copy(); h = a.shape[0]
    for _ in range(6):
        y0 = r.integers(0, h - 10); y1 = min(h, y0 + r.integers(6, 40)); a[y0:y1] = np.roll(a[y0:y1], int(r.integers(-40, 40) * k), 1)
    out = a.copy(); out[..., 0] = np.roll(a[..., 0], int(12 * k), 1); out[..., 2] = np.roll(a[..., 2], -int(12 * k), 1); return Image.fromarray(out)

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = Q.end_card7(t - CLIP, ["A fixed price", "is always wrong."], END); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = Q.hq_grade(fr)
    Q.z_glow(im, 0.18 + 0.08 * np.sin(t * 2.4) + flare(t, 0.1, 0.6) + flare(t, SAME, 0.6) + flare(t, BOOM, 0.95))
    Q.seal_glow(im, *SEAL, min(1.0, SEAL_BASE + 0.08 * np.sin(t * 2.4) + flare(t, BOOM, 0.4, 1.0)), flare(t, BOOM, 1.0, 0.6))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 1100))
    sx, sy = Q.shake_off(t, FIXED, 12, 0.3); bx, by = Q.shake_off(t, BOOM, 18, 0.45, 1)
    im = Q.shake(im, sx + bx, sy + by)
    a = fade(t, 0.0, GUESS0 + 0.6, 0.3, 0.3)
    if a > 0: R.paste_center(im, PART, W / 2, 215, a)
    ah = fade(t, -0.2, GUESS0 + 0.05, 0.2, 0.2)                                                       # typed hook
    if ah > 0:
        n = HOOK_N if t > HOOK_N / CPS else max(1, int(t * CPS) + 1)
        lay = Q.typed_lines(HOOK, n, 78, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 760, lay.height + 64; y = 1090
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.6)
        put(im, lay, W / 2 - w / 2 + 56, y - h / 2 + 30, ah)
    dim = 1 - 0.6 * ease((t - FIXED) / 0.3) + 0.6 * ease((t - BOOM) / 0.25)
    al = ease((t - SAME - 0.1) / 0.5) * dim                                                           # every guess → the watch
    if al > 0.01:
        L = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0)); d = ImageDraw.Draw(L); tgt = ((BOX[0] + BOX[2]) / 4, BOX[1] / 2)
        for t0, tx, ty, lay, i in BUBS:
            k = ease((t - SAME - 0.1 - 0.012 * i) / 0.35)
            if k > 0: d.line([(tx / 2, ty / 2), (tx / 2 + (tgt[0] - tx / 2) * k, ty / 2 + (tgt[1] - ty / 2) * k)], fill=(185, 168, 255, int(120 * al)), width=1)
        im.alpha_composite(L.resize((W, H), Image.BILINEAR))
    ab = fade(t, SAME, CLIP - 0.1, 0.2, 0.3)
    if ab > 0:
        Q.brackets(im, BOX, Q.pop((t - SAME) / 0.3), ab * (0.4 + 0.6 * dim))
        R.paste_center(im, K.tag("SAME WATCH", 22, Q.LAV), (BOX[0] + BOX[2]) / 2, BOX[1] - 44, ab * ease((t - SAME - 0.1) / 0.25) * (0.4 + 0.6 * dim))
    for t0, tx, ty, lay, i in BUBS:                                                                   # the guesses
        if t < t0: continue
        R.paste_center(im, lay, tx + 4 * np.sin(t * 2.5 + i), ty + 4 * np.cos(t * 2.1 + i), min(1, (t - t0) / 0.06) * dim, 0.7 + 0.3 * Q.pop((t - t0) / 0.28))
    if FIXED <= t < BOOM:                                                                             # the fixed price
        lay = TAG.rotate(-5, expand=True, resample=Image.BICUBIC)
        if t >= WRONG: lay = glitch(lay, 0.5 + 0.5 * np.sin(t * 80), int(t * 60))
        R.paste_center(im, lay, W / 2, 1090, min(1, (t - FIXED) / 0.05), Q.slam((t - FIXED) / 0.22))
    elif BOOM <= t < BOOM + 0.8:
        k = (t - BOOM) / 0.8
        for piece, vx, vy, vr in SHARDS:
            p = piece.rotate(-5 + vr * k, expand=True, resample=Image.BICUBIC)
            R.paste_center(im, p, W / 2 + vx * k, 1090 + vy * k + 1400 * k * k, 1 - ease((k - 0.5) / 0.5))
    Q.shockwave(im, *SEAL, (t - BOOM) / 0.6); Q.shockwave(im, *SEAL, (t - BOOM - 0.12) / 0.6, Q.LAV, 380, 4)
    Q.flash(im, flare(t, FIXED, 0.25, 0.3) + flare(t, BOOM, 0.6, 0.35), (240, 236, 255))
    captions(im, t, CAPS, y=1730, size=58)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Q.HQMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = Q.sneaky(CLIP + 0.2, 0.0, 1.0, seed=12); x = np.arange(len(g)) / SR
        env = np.minimum(1, x / 0.5) * np.clip((CLIP + 0.05 - x) / 0.12, 0, 1) * np.where((x > FIXED - 0.02) & (x < BOOM), 0.35, 1.0)
        env = np.convolve(env, np.ones(480) / 480, "same"); mx.fadd(g * env, 0.0, 0.5)
        for i in range(HOOK_N): Q.key_click(mx, i / CPS, 0.028)
        for t0, *_ in BUBS: Q.bubble_pop(mx, t0, 0.035)
        Q.bips(mx, SAME + 0.03, 0.05); mx.whoosh(SAME + 0.1, 0.45, 0.1)
        Q.impact(mx, FIXED, 0.35); Q.ding(mx, FIXED + 0.02, 1046.5, 0.05)
        y = mx.tt(0.22); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 1) * (np.sin(2 * np.pi * 37 * y) > 0) * 0.6, WRONG, 0.12)   # glitch crackle
        Q.buzzer(mx, WRONG + 0.02, 0.1, 0.25)
        Q.impact(mx, BOOM, 0.45); mx.whoosh(BOOM, 0.5, 0.2); Q.V.chime(mx, BOOM + 0.05, 1318.5, 0.05); mx.shimmer(BOOM + 0.08, 1568, 0.03)
        mx.write("s7e6_audio.wav")
    render(frame, TOTAL, "s7e6_audio.wav", OUT)
