"""Season 6 Ep. 2 'That bag' (cream tote, dusk). 'That bag you never carry anymore?': a small frosted tag hangs from the
tote on a hairline thread, LAST CARRIED · SUMMER 2023. 'Someone in Beirut is waiting for exactly that one': a frosted
note settles in the sky, Maya · Achrafieh saved it to her wishlist, then '+ 11 others waiting'. 'Let them bid': the note
turns into LIVE BIDS, $180 → $210 → $240, and a violet hairline draws around the tote. Classy motion, groove under the
voice, last shot held with a slow push-in, end card 'Your closet. Their wishlist.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s6_common as K

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.2; TOTAL = CLIP + END
FR = decode()
for fr in FR: K.blur_mark(fr, 874, 1412, 18, K.SKIN)                                                   # small plaque on the tote
LAST = K.night_grade(FR[-1])
CAPS = [(0.30, 2.30, ["That bag you never", "[carry anymore?]"]), (2.75, 6.20, ["Someone in Beirut is waiting", "for [exactly that one.]"]),
        (6.20, 9.20, ["[Let them bid.]"])]
TOTE = (870, 1210, 190, 250)
TAG_T, NOTE_T, MORE_T, BIDS_T = 0.6, 3.0, 4.6, 6.25
BIDS = [(6.35, "M", "Maya", "$180", (221, 92, 140)), (6.75, "N", "Nour", "$210", (109, 77, 255)), (7.15, "L", "Lea", "$240", (53, 126, 221))]

def frame(t):
    if t >= CLIP: return K.end_card(t - CLIP, ["Your closet.", "Their wishlist."], END, LAST)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = K.night_grade(fr)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (560, 700))
    K.light_leak(im, t, 0.12, side=1)
    x, y, rx, ry = TOTE
    a = K.fade(t, TAG_T, NOTE_T + 0.5)                                                                # last carried
    if a > 0:
        d = Image.new("RGBA", (6, 130), (0, 0, 0, 0)); ImageDraw.Draw(d).line([(3, 0), (3, 130)], fill=K.CHAMP + (200,), width=2)
        K.put(im, d, 935 - 3, 870 - 4, a)
        tg = K.tag("LAST CARRIED · SUMMER 2023", 22); K.place(im, tg, 790, 850, a)
    an = K.fade(t, NOTE_T, CLIP - 0.1, 0.7, 0.4)                                                       # someone is waiting
    if an > 0:
        x0, y0 = K.panel(im, 790, 255, 520, 190, an)
        bids = t >= BIDS_T
        a1 = an * (1 - K.ease((t - BIDS_T) / 0.4)); a2 = an * K.ease((t - BIDS_T - 0.1) / 0.4)
        if a1 > 0.01:
            K.put(im, K.avatar("M", (221, 92, 140), 56), x0 + 28, y0 + 30, a1)
            K.put(im, K.text("Maya · Achrafieh", 34, 600), x0 + 100, y0 + 28, a1)
            K.put(im, K.text("saved it to her wishlist", 28, 500, (210, 212, 228)), x0 + 100, y0 + 72, a1)
            K.put(im, K.mono("+ 11 OTHERS WAITING", 20, K.CHAMP, 5), x0 + 28, y0 + 138, a1 * K.ease((t - MORE_T) / 0.6))
        if a2 > 0.01:
            K.put(im, K.dot(), x0 + 30, y0 + 34, a2); K.put(im, K.mono("LIVE BIDS", 22, K.CHAMP, 7), x0 + 56, y0 + 26, a2)
            for i, (at, ini, nm, amt, col) in enumerate(BIDS):
                if t < at: continue
                b = a2 * K.ease((t - at) / 0.5); xx = x0 + 28 + i * 160
                K.put(im, K.avatar(ini, col, 44), xx, y0 + 80, b); K.put(im, K.text(amt, 30, 700 if i == len([q for q in BIDS if t >= q[0]]) - 1 else 500), xx + 52, y0 + 86, b)
    if t >= BIDS_T:
        K.hairline_ring(im, x, y, rx + 20, ry + 20, K.ease((t - BIDS_T) / 1.0), K.fade(t, BIDS_T, CLIP - 0.1), K.VIO, 4)
    K.captions(im, t, CAPS, y=1730, size=56)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = K.GrooveMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = K.groove(CLIP + END, 0.0, 1.0, seed=5); env = np.minimum(1, np.arange(len(g)) / SR / 1.2)
        mx.fadd(g * env, 0.0, 0.55)
        K.chime(mx, 7.45, 1318.5, 0.045)
        mx.write("s6e2_audio.wav")
    render(frame, TOTAL, "s6e2_audio.wav", OUT)
