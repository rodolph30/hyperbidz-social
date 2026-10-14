"""Season 6 Ep. 3 'Not full price' (glossy black mini bag, blue hour). 'Why pay boutique price…': a frosted tag
settles above the bag, BOUTIQUE · $2,400, then '3,200 SOLD THIS SEASON' on 'everyone has'. 'Bid on the one nobody
else has': the tags fade, a violet hairline draws around the bag, ONE OF ONE. 'For less': a frosted card in the sky,
ONE OF ONE · WON LIVE $1,150, boutique $2,400 struck through. Classy motion, groove under the voice, held last shot,
end card 'One of one. For less.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s6_common as K

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.2; TOTAL = CLIP + END
FR = decode()
LAST = K.night_grade(FR[-1])
CAPS = [(0.30, 3.45, ["Why pay [boutique price]", "for the bag everyone has?"]), (4.10, 6.45, ["Bid on the one", "[nobody else has.]"]),
        (6.60, 9.20, ["[For less.]"])]
BAG = (855, 1320, 150, 150)
PRICE_T, EVERY_T, ONE_T, LESS_T = 1.0, 2.45, 4.35, 6.75

def frame(t):
    if t >= CLIP: return K.end_card(t - CLIP, ["One of one.", "For less."], END, LAST)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = K.night_grade(fr)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 700))
    K.light_leak(im, t, 0.09, side=-1)
    x, y, rx, ry = BAG
    a = K.fade(t, PRICE_T, ONE_T + 0.2)
    if a > 0:
        K.place(im, K.tag("BOUTIQUE · $2,400", 24), 830, 1030, a)
        K.place(im, K.tag("3,200 SOLD THIS SEASON", 20, (210, 212, 228)), 830, 1094, a * K.ease((t - EVERY_T) / 0.6))
    if t >= ONE_T:
        ar = K.fade(t, ONE_T, CLIP - 0.1)
        K.hairline_ring(im, x, y, rx + 26, ry + 26, K.ease((t - ONE_T) / 1.0), ar, K.VIO, 4)
        K.place(im, K.tag("ONE OF ONE", 24, K.LAV), x, y - ry - 70, K.fade(t, ONE_T + 0.3, CLIP - 0.1))
    al = K.fade(t, LESS_T, CLIP - 0.1, 0.7, 0.4)
    if al > 0:
        x0, y0 = K.panel(im, 790, 255, 440, 230, al)
        K.put(im, K.mono("ONE OF ONE · WON LIVE", 22, K.CHAMP, 6), x0 + 30, y0 + 28, al)
        K.put(im, K.text("$1,150", 66, 700), x0 + 28, y0 + 64, al)
        old = K.text("Boutique $2,400", 30, 500, (180, 184, 200)); ln = old.copy(); ImageDraw.Draw(ln).line([(0, ln.height // 2 + 2), (int(ln.width * K.ease((t - LESS_T - 0.3) / 0.5)), ln.height // 2 + 2)], fill=(205, 194, 255, 255), width=3)
        K.put(im, ln, x0 + 30, y0 + 160, al)
    K.captions(im, t, CAPS, y=1730, size=56)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = K.GrooveMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = K.groove(CLIP + END, 0.0, 1.0, seed=7); env = np.minimum(1, np.arange(len(g)) / SR / 1.2)
        mx.fadd(g * env, 0.0, 0.55)
        K.chime(mx, 7.35, 1318.5, 0.045)
        mx.write("s6e3_audio.wav")
    render(frame, TOTAL, "s6e3_audio.wav", OUT)
