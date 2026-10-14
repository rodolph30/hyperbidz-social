"""Season 6 Ep. 5 'Its next story' (vintage tan bucket bag, dusk). As he names its life, small frosted tags settle in
the sky one by one: WEDDING · BYBLOS, FARAYA · SKI WEEKEND, FIRST DATES · ×3. On 'Now it's ready for its next story'
the tags fade away in turn and a frosted card takes their place, NEXT STORY · Vintage tan bucket bag · Starts at $90
· Live soon, while a violet hairline draws around the bag. Classy motion, groove under the voice, held last shot,
end card 'Every bag has a next story.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s6_common as K

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.2; TOTAL = CLIP + END
FR = decode()
LAST = K.night_grade(FR[-1])
CAPS = [(0.20, 2.00, ["This bag has been", "to [weddings,]"]), (2.00, 3.25, ["[Faraya weekends,]"]), (3.25, 4.75, ["and [three first dates.]"]),
        (5.15, 9.20, ["Now it's ready", "for its [next story.]"])]
TAGS = [(1.35, "WEDDING · BYBLOS"), (2.2, "FARAYA · SKI WEEKEND"), (3.4, "FIRST DATES · ×3")]
TAG_IM = [K.tag(s, 26) for _, s in TAGS]
NEXT = 5.35; BAG = (315, 1470, 225, 320)

def frame(t):
    if t >= CLIP: return K.end_card(t - CLIP, ["Every bag", "has a next story."], END, LAST)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = K.night_grade(fr)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (560, 700))
    K.light_leak(im, t, 0.12, side=-1)
    for i, ((at, _), tg) in enumerate(zip(TAGS, TAG_IM)):                                            # the bag's life so far
        a = K.fade(t, at, NEXT + 0.35 + 0.15 * i, 0.6, 0.4)
        if a > 0: K.place(im, tg, 1040 - tg.width / 2, 205 + i * 84, a, 14)
    an = K.fade(t, NEXT + 0.4, CLIP - 0.1, 0.7, 0.4)                                                  # its next story
    if an > 0:
        x0, y0 = K.panel(im, 790, 285, 500, 210, an)
        K.put(im, K.mono("NEXT STORY", 22, K.CHAMP, 7), x0 + 30, y0 + 28, an)
        K.put(im, K.text("Vintage tan bucket bag", 38, 600), x0 + 30, y0 + 66, an)
        K.put(im, K.dot(), x0 + 32, y0 + 140, an * (0.6 + 0.4 * np.sin(t * 5)))
        K.put(im, K.text("Starts at $90 · live soon", 30, 500, (210, 212, 228)), x0 + 58, y0 + 128, an)
    if t >= NEXT:
        x, y, rx, ry = BAG
        K.hairline_ring(im, x, y, rx + 20, ry + 20, K.ease((t - NEXT) / 1.1), K.fade(t, NEXT, CLIP - 0.1), K.VIO, 4)
    K.captions(im, t, CAPS, y=1730, size=56)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = K.GrooveMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = K.groove(CLIP + END, 0.0, 1.0, seed=11); env = np.minimum(1, np.arange(len(g)) / SR / 1.2)
        mx.fadd(g * env, 0.0, 0.55)
        K.chime(mx, 7.35, 1318.5, 0.045)
        mx.write("s6e5_audio.wav")
    render(frame, TOTAL, "s6e5_audio.wav", OUT)
