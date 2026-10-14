"""Season 6 Ep. 4 'Girls' night' (red clutch, sunset). 'Girls' night. Dinner at nine, auction at eleven': a frosted
itinerary in the sky, GIRLS' NIGHT · 21:00 Dinner · Mar Mikhael · 23:00 Auction · HyperBidz (live dot). 'Ten seconds
left…': a quiet countdown pill by the clutch, 0:10 → 0:07, while a hairline around it closes. 'and your best friend
bids against you': a frosted note drops in, Lea · YOUR BEST FRIEND · outbid you · $340. Classy motion, groove under
the voice, held last shot, end card 'Best friends. Fierce bidders.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s6_common as K

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.2; TOTAL = CLIP + END
FR = decode()
for fr in FR: K.blur_mark(fr, 862, 1422, 22, K.SKIN)                                                   # embossed mark on the clutch
LAST = K.night_grade(FR[-1])
CAPS = [(0.00, 1.00, ["[Girls' night.]"]), (1.30, 3.85, ["Dinner at nine,", "[auction at eleven.]"]), (4.15, 5.25, ["[Ten seconds left…]"]),
        (5.25, 9.20, ["and your best friend", "[bids against you.]"])]
CLUTCH = (865, 1400, 165, 110)
PLAN_T, ROW1, ROW2, TEN, OUTBID = 0.2, 1.45, 2.55, 4.3, 5.5

def frame(t):
    if t >= CLIP: return K.end_card(t - CLIP, ["Best friends.", "Fierce bidders."], END, LAST)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = K.night_grade(fr)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 700))
    K.light_leak(im, t, 0.12, side=1)
    a = K.fade(t, PLAN_T, TEN + 0.2, 0.7, 0.5)                                                        # the plan
    if a > 0:
        x0, y0 = K.panel(im, 790, 255, 540, 230, a)
        K.put(im, K.mono("GIRLS' NIGHT", 22, K.CHAMP, 7), x0 + 30, y0 + 28, a)
        for i, (at, tm, what, live) in enumerate(((ROW1, "21:00", "Dinner · Mar Mikhael", False), (ROW2, "23:00", "Auction · HyperBidz", True))):
            b = a * K.ease((t - at) / 0.5); yy = y0 + 76 + i * 64
            K.put(im, K.mono(tm, 26, K.LAV, 2), x0 + 30, yy + 6, b); K.put(im, K.text(what, 34, 600 if live else 500), x0 + 150, yy, b)
            if live: K.put(im, K.dot(), x0 + 500, yy + 16, b * (0.6 + 0.4 * np.sin(t * 5)))
    x, y, rx, ry = CLUTCH
    if TEN <= t < CLIP:                                                                               # ten seconds left
        ac = K.fade(t, TEN, CLIP - 0.1)
        left = max(7, 10 - int((t - TEN) / 0.45)) if t < OUTBID + 0.4 else 7
        K.place(im, K.tag(f"0:{left:02d}  LEFT", 24, (255, 196, 190)), x, y - ry - 70, ac)
        frac = 1 - min(1.0, (t - TEN) / 3.0) * 0.3
        K.hairline_ring(im, x, y, rx + 26, ry + 26, frac, ac * K.ease((t - TEN) / 0.4), (255, 150, 160), 3)
    ao = K.fade(t, OUTBID, CLIP - 0.1, 0.7, 0.4)                                                       # your best friend
    if ao > 0:
        x0, y0 = K.panel(im, 790, 255, 500, 200, ao)
        K.put(im, K.avatar("L", (221, 92, 140), 64), x0 + 28, y0 + 30, ao)
        K.put(im, K.mono("YOUR BEST FRIEND", 20, K.CHAMP, 5), x0 + 112, y0 + 30, ao)
        K.put(im, K.text("Lea outbid you", 38, 700), x0 + 110, y0 + 62, ao)
        K.put(im, K.text("$340", 34, 600, K.LAV), x0 + 112, y0 + 122, ao * K.ease((t - OUTBID - 0.3) / 0.5))
    K.captions(im, t, CAPS, y=1730, size=56)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = K.GrooveMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = K.groove(CLIP + END, 0.0, 1.0, seed=9); env = np.minimum(1, np.arange(len(g)) / SR / 1.2)
        mx.fadd(g * env, 0.0, 0.55)
        K.chime(mx, 7.55, 1174.7, 0.045)
        mx.write("s6e4_audio.wav")
    render(frame, TOTAL, "s6e4_audio.wav", OUT)
