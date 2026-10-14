"""Season 7 Ep. 1 'The envelope' (HQ office at night, fun). A typed hook on his chest, 'What will this watch sell for?'.
'I sealed a number…': a card scrambles through amounts, a black bar redacts it on 'envelope', SEALED · OPENS LAUNCH
NIGHT, and the card flies into the wax seal, which flares violet and keeps glowing. The wall Z flares on 'Okay', on
the seal and on 'guess it'. 'It's what this watch will sell for': focus brackets snap around the glass box, SELLS FOR
$ ? ? ?. 'Guess it': a comment field pops up, Your guess: $ |. Sneaky pizzicato groove with clock ticks, held last
shot with a push-in, HQ end card 'The number is sealed. / Your guess?'"""
import sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/home/claude")
from founder_common import *
import s7_common as Q
from s7_common import ease, fade, shield, put, captions

OUT = sys.argv[1]; SHOT = 7.8; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
FR = decode()
SEAL = (415, 1495); BOX = (652, 1332, 933, 1578)
CAPS = [(1.28, 3.15, ["I sealed a [number]", "in this envelope."]), (3.40, 5.30, ["It's what this watch", "[will sell for.]"]),
        (5.45, 7.05, ["I want you to…"]), (7.08, 9.15, ["[Guess it.]"])]
HOOK = [[("What will this watch", False)], [("sell for?", True)]]; HOOK_N = 29; TYPE0, CPS = 0.04, 30
NUM_IN, ROLL1, RED0, RED1, FLY0, FLY1 = 1.5, 2.55, 2.55, 2.85, 3.05, 3.38
BRK, TAG_T, GUESS = 3.75, 4.4, 7.1
AMOUNTS = ["$ 850", "$ 12,400", "$ 3,275", "$ 640", "$ 7,900", "$ 2,150", "$ 19,000", "$ 5,480", "$ 1,320", "$ 9,750", "$ 4,060", "$ 15,300", "$ 980", "$ 6,600", "$ 2,890", "$ 11,200"]
TAG = Q.mono("SELLS FOR", 22, Q.LAV, 6)
LABEL = Image.new("RGBA", (440, 42), (0, 0, 0, 0)); LABEL.alpha_composite(Q.bubble_icon(32), (0, 2)); LABEL.alpha_composite(Q.mono("COMMENTS ARE OPEN", 24, Q.LAV, 5), (46, 5))
PART = Q.part_tag(1)

def punch(im, t, t0, amt=0.035, d=0.6, focus=(540, 900)):
    k = (t - t0) / d
    if not 0 < k < 1: return im
    z = 1 + amt * np.sin(np.pi * k); w, h = W / z, H / z; l = min(max(focus[0] - w / 2, 0), W - w); tp = min(max(focus[1] - h / 2, 0), H - h)
    return im.crop((int(l), int(tp), int(l + w), int(tp + h))).resize((W, H), Image.BICUBIC)

def flare(t, at, peak, d=0.7): return peak * np.exp(-max(0, t - at) / d * 3) if t >= at else 0

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t)
    ec = Q.end_card7(t - CLIP, ["The number is sealed.", "Your guess?"], END); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01)
    return Image.blend(_LAST["f"], ec, ease(k))

def scene(t):
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = Q.hq_grade(fr)
    Q.z_glow(im, 0.18 + 0.08 * np.sin(t * 2.4) + flare(t, 0.2, 0.75) + flare(t, FLY1, 0.6) + flare(t, 7.13, 0.75))
    if t >= FLY1 - 0.05:                                                                              # the seal keeps the number
        Q.seal_glow(im, *SEAL, min(1.0, 0.55 + 0.1 * np.sin(t * 2.4) + flare(t, FLY1, 0.7, 0.9)) * ease((t - FLY1 + 0.05) / 0.12), flare(t, FLY1, 0.9, 0.5))
    im = punch(im, t, 0.15)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 1150))
    a = fade(t, 0.1, 7.4, 0.4, 0.4)
    if a > 0: R.paste_center(im, PART, W / 2, 215, a)
    ah = fade(t, -0.2, 1.72, 0.2, 0.3)                                                                # typed hook
    if ah > 0:
        n = HOOK_N if t > TYPE0 + HOOK_N / CPS else max(1, int((t - TYPE0) * CPS) + 1)
        lay = Q.typed_lines(HOOK, n, 70, cursor=(n < HOOK_N or int(t * 3.4) % 2 == 0))
        w, h = 810, lay.height + 64; y = 1100 - (1 - ah) * 14 * (t > 1) 
        shield(im, (W / 2 - w / 2, y - h / 2, W / 2 + w / 2, y + h / 2), ah, 34, dark=0.55)
        put(im, lay, W / 2 - w / 2 + 52, y - h / 2 + 30, ah)
    if NUM_IN <= t < FLY1:                                                                            # the number
        i = int((min(t, RED1) - NUM_IN) / (0.07 + 0.05 * max(0, t - 2.1)))
        cardl = Q.number_card(AMOUNTS[i % len(AMOUNTS)], ease((t - RED0) / (RED1 - RED0)), t >= RED1 - 0.05)
        if t < FLY0:
            s = 0.86 + 0.14 * Q.pop((t - NUM_IN) / 0.35); R.paste_center(im, cardl, W / 2, 1110, min(1, (t - NUM_IN) / 0.12), s)
        else:
            k = ease((t - FLY0) / (FLY1 - FLY0)); x = W / 2 + (SEAL[0] - W / 2) * k; y = 1110 + (SEAL[1] - 1110) * k * k - 60 * np.sin(np.pi * k)
            R.paste_center(im, cardl, x, y, 1 - ease((k - 0.7) / 0.3), 1 - 0.94 * k)
    ab = fade(t, BRK, 6.95, 0.2, 0.35)                                                                # this watch
    if ab > 0:
        Q.brackets(im, BOX, Q.pop((t - BRK) / 0.3), ab)
    at = fade(t, TAG_T, 6.95, 0.15, 0.35)
    if at > 0:
        qm = Q.qmarks(t, 50); w = TAG.width + qm.width + 70; tg = Q.glass_layer(w, 84, 42); tg.alpha_composite(TAG, (30, (84 - TAG.height) // 2))
        tg.alpha_composite(qm, (TAG.width + 50, (84 - qm.height) // 2 - 2)); R.paste_center(im, tg, 792, 1262, at, 0.9 + 0.1 * Q.pop((t - TAG_T) / 0.3))
    ag = fade(t, GUESS, CLIP + 0.3, 0.15, 0.4)                                                        # guess it
    if ag > 0:
        s = 0.88 + 0.12 * Q.pop((t - GUESS) / 0.35)
        R.paste_center(im, Q.composer(int((t - GUESS) * 3.2) % 2 == 0), W / 2, 1120, ag, s)
        R.paste_center(im, LABEL, W / 2 + 22, 1022, ag * ease((t - GUESS - 0.15) / 0.3))
    captions(im, t, CAPS, y=1730, size=56)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Q.HQMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = Q.sneaky(CLIP + 0.2, 0.0, 1.0); x = np.arange(len(g)) / SR
        env = np.minimum(1, x / 0.5) * np.clip((CLIP + 0.05 - x) / 0.12, 0, 1); mx.fadd(g * env, 0.0, 0.5)
        for i in range(HOOK_N): Q.key_click(mx, TYPE0 + i / CPS, 0.03)
        Q.bubble_pop(mx, NUM_IN, 0.07); V_t = Q.V; V_t.ticks(mx, NUM_IN + 0.05, RED0, rate=14, g=0.03)
        mx.whoosh(RED0, 0.3, 0.12); V_t.lock(mx, RED1 - 0.05, 0.2)
        mx.whoosh(FLY0, 0.33, 0.2); V_t.chime(mx, FLY1, 1318.5, 0.05); mx.shimmer(FLY1 + 0.02, 1568, 0.03)
        Q.bips(mx, BRK + 0.03, 0.045); Q.bubble_pop(mx, TAG_T, 0.06)
        Q.bubble_pop(mx, GUESS, 0.11); Q.key_click(mx, GUESS + 0.3, 0.04)
        mx.write("s7e1_audio.wav")
    render(frame, TOTAL, "s7e1_audio.wav", OUT)
