"""Season 6 (bags, rooftop nights) Ep. 1 'The one that got away'. Sunset rooftop, warm night grade, soft bloom on the
lanterns, a slow light leak and a deep-house groove under the voice. On 'that one bag' a thin champagne line draws
itself around the caramel bag (THE ONE). On 'the one that got away' a ghost of the bag drifts off and fades while the
real one dims. On 'On HyperBidz' a frosted card rises in the sky: BACK IN AUCTION · Caramel shoulder bag · Live tonight
22:00; on 'it comes back' the ghost glides home and the line redraws in violet. Classy motion only: slow fades, small
rises. Last shot held with a slow push-in. End card on the blurred last frame."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s6_common as K

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.5; END = 4.2; TOTAL = CLIP + END
FR = decode()
for fr in FR: K.blur_mark(fr, 910, 1430, 24, K.SKIN)                                                   # embossed mark on the bag
LAST = K.night_grade(FR[-1])
CAPS = [(0.10, 2.70, ["Everyone has that one bag", "they still [think about.]"]), (3.15, 4.50, ["The one that [got away.]"]),
        (5.15, 9.20, ["On HyperBidz…", "it [comes back.]"])]
BAG = (900, 1410, 175, 125)                                                                            # centre and half-size of the caramel bag
RING, AWAY, BACK_CARD, BACK = 0.75, 3.3, 5.25, 6.4

def bag_ghost(im_src):
    """the bag's body only (a tight rounded mask), for the ghost that drifts away"""
    box = (755, 1298, 1022, 1494); g = im_src.crop(box)
    m = Image.new("L", g.size, 0); ImageDraw.Draw(m).rounded_rectangle((3, 3, g.width - 4, g.height - 4), radius=34, fill=255)
    g.putalpha(m.filter(ImageFilter.GaussianBlur(2.5))); return g
BODY = ((755 + 1022) / 2, (1298 + 1494) / 2)
GHOST = None

def frame(t):
    global GHOST
    if t >= CLIP: return K.end_card(t - CLIP, ["The one", "that got away", "comes back."], END, LAST)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = K.night_grade(fr)
    if GHOST is None: GHOST = bag_ghost(K.night_grade(FR[int(3.0 * FPS)]))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 700))
    K.light_leak(im, t, 0.13, side=1)
    x, y, rx, ry = BAG
    away = K.ease((t - AWAY) / 0.9) * (1 - K.ease((t - BACK) / 0.9))                                  # 0 → 1 → 0
    if away > 0.01:                                                                                    # the real bag dims; its ghost drifts off
        dim = Image.new("RGBA", GHOST.size, (8, 10, 22, 0)); dim.putalpha(GHOST.getchannel("A").point(lambda v: int(v * 0.5 * away)))
        R.paste_center(im, dim, *BODY)
        drift = away; R.paste_center(im, GHOST, BODY[0] + 30 * drift, BODY[1] - 200 * drift, (0.85 * np.sin(np.pi * min(1, drift)) if t < BACK else 0.85 * away), 1 + 0.05 * drift)
    ring_a = K.fade(t, RING, AWAY + 0.4) if t < BACK else K.fade(t, BACK + 0.3, CLIP - 0.1)
    if t < BACK: K.hairline_ring(im, x, y, rx + 34, ry + 34, K.ease((t - RING) / 0.8), ring_a, K.CHAMP, 3)
    else: K.hairline_ring(im, x, y, rx + 34, ry + 34, K.ease((t - BACK - 0.3) / 0.9), ring_a, K.VIO, 4)
    if RING + 0.3 <= t < AWAY + 0.4:
        K.place(im, K.tag("THE ONE", 24), x, y - ry - 78, K.fade(t, RING + 0.3, AWAY + 0.4))
    a = K.fade(t, BACK_CARD, CLIP - 0.1, 0.7, 0.4)                                                    # back in auction
    if a > 0:
        live = K.mono("LIVE TONIGHT  ·  22:00", 22, (200, 204, 220), 4)
        dot = Image.new("RGBA", (live.width + 34, live.height), (0, 0, 0, 0)); ImageDraw.Draw(dot).ellipse((2, live.height / 2 - 7, 16, live.height / 2 + 7), fill=(255, 77, 106, 255)); dot.alpha_composite(live, (34, 0))
        K.card(im, 790, 330, 500, 214, a, [(K.mono("BACK IN AUCTION", 22, K.CHAMP, 7), "l", 14), (K.text("Caramel shoulder bag", 40, 600), "l", 16), (dot, "l", 0)])
    K.captions(im, t, CAPS, y=1730, size=56)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = K.GrooveMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = K.groove(CLIP + END, 0.0, 1.0); env = np.minimum(1, np.arange(len(g)) / SR / 1.2)
        mx.fadd(g * env, 0.0, 0.55)
        K.chime(mx, 7.3, 1318.5, 0.045)                                                                # after 'back'
        mx.write("s6e1_audio.wav")
    render(frame, TOTAL, "s6e1_audio.wav", OUT)
