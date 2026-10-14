"""Season 6 finale 'Bid like you mean it' (pistachio mini bag, dusk). One frosted card grows with his lines:
HYPERBIDZ · BAGS · First auctions · coming soon; 'Set your reminder' → a bell and a toggle that slides on (violet);
'call your girls' → three friends' avatars, invited. 'and bid like you mean it': a Place bid pill rises above the bag
and is pressed softly → Bid placed. Classy motion, groove under the voice, held last shot, end card 'Bid like you
mean it.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s6_common as K
import s5_common as V

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; END = 4.4; TOTAL = CLIP + END
FR = decode()
for fr in FR: K.blur_mark(fr, 940, 1467, 22, K.SKIN)                                                   # embossed mark on the bag
LAST = K.night_grade(FR[-1])
CAPS = [(0.25, 2.20, ["The first bags", "go [live soon.]"]), (2.45, 4.75, ["Set your reminder,", "[call your girls…]"]),
        (4.85, 9.20, ["and bid like", "you [mean it.]"])]
CARD_T, REM_T, ON_T, GIRLS_T, BID_T, PRESS_T = 0.3, 2.55, 3.0, 3.65, 5.0, 6.3

def bell(s=34, col=WHITE):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(2, s // 12)
    d.arc((s * 0.18, s * 0.12, s * 0.82, s * 0.86), 180, 360, fill=col + (255,), width=w)
    d.line([(s * 0.18, s * 0.49), (s * 0.18, s * 0.7), (s * 0.1, s * 0.78), (s * 0.9, s * 0.78), (s * 0.82, s * 0.7), (s * 0.82, s * 0.49)], fill=col + (255,), width=w)
    d.ellipse((s * 0.42, s * 0.82, s * 0.58, s * 0.96), fill=col + (255,)); return im

def toggle(k):
    w, h = 76, 42; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    off, on = np.array([70, 74, 92]), np.array([124, 92, 255]); c = tuple(int(v) for v in off + (on - off) * k)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=c + (255,)); x = 4 + (w - h) * k
    d.ellipse((x, 4, x + h - 8, h - 4), fill=(255, 255, 255, 255)); return im

def bid_pill(placed, glow):
    txt = "Bid placed" if placed else "Place bid"; t = K.text(txt, 40, 700); w, h = t.width + 120, 92
    im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((40, 46, w + 40, h + 46), radius=h // 2, fill=(124, 92, 255, int(110 + 90 * glow))); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(20)))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    b = Image.new("RGBA", (w, h), (0, 0, 0, 0)); b.paste(V.lin_grad(w, h, (47, 123, 255), (124, 92, 255), 90), (0, 0), m)
    if placed: ImageDraw.Draw(b).line([(34, h // 2 + 2), (46, h // 2 + 14), (66, h // 2 - 10)], fill=(255, 255, 255, 255), width=6)
    b.alpha_composite(t, ((w - t.width) // 2 + (16 if placed else 0), (h - t.height) // 2 - 4)); im.alpha_composite(b, (40, 40)); return im
PILL = [bid_pill(False, 0), bid_pill(True, 1)]

def frame(t):
    if t >= CLIP: return K.end_card(t - CLIP, ["Bid like", "you mean it."], END, LAST)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = K.night_grade(fr)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (600, 700))
    K.light_leak(im, t, 0.12, side=1)
    a = K.fade(t, CARD_T, CLIP - 0.1, 0.7, 0.4)
    if a > 0:
        hh = 124 + 66 * K.ease((t - REM_T) / 0.5) + 72 * K.ease((t - GIRLS_T) / 0.5)          # the card grows with each line
        x0, y0 = K.panel(im, 790, 109 + hh / 2, 500, hh, a)
        K.put(im, K.mono("HYPERBIDZ · BAGS", 22, K.CHAMP, 7), x0 + 30, y0 + 26, a)
        K.put(im, K.text("First auctions", 40, 700), x0 + 30, y0 + 60, a)
        K.put(im, K.dot(), x0 + 342, y0 + 80, a * (0.6 + 0.4 * np.sin(t * 5))); K.put(im, K.mono("SOON", 22, (255, 190, 200), 5), x0 + 368, y0 + 72, a)
        b = a * K.ease((t - REM_T) / 0.5)                                                            # set your reminder
        if b > 0.01:
            K.put(im, bell(36), x0 + 30, y0 + 128, b); K.put(im, K.text("Reminder", 32, 500), x0 + 82, y0 + 126, b)
            K.put(im, toggle(K.ease((t - ON_T) / 0.35)), x0 + 394, y0 + 124, b)
        c = a * K.ease((t - GIRLS_T) / 0.5)                                                          # call your girls
        if c > 0.01:
            for i, (ini, col) in enumerate((("L", (221, 92, 140)), ("M", (109, 77, 255)), ("N", (53, 126, 221)))):
                ci = c * K.ease((t - GIRLS_T - 0.15 * i) / 0.45); K.put(im, K.avatar(ini, col, 50), x0 + 28 + i * 36, y0 + 190, ci)
            K.put(im, K.mono("3 FRIENDS INVITED", 20, (210, 212, 228), 4), x0 + 160, y0 + 204, c)
    if t >= BID_T:                                                                                    # bid like you mean it
        ab = K.fade(t, BID_T, CLIP - 0.1, 0.6, 0.4); placed = t >= PRESS_T + 0.12
        press = np.exp(-((t - PRESS_T) / 0.1) ** 2) if abs(t - PRESS_T) < 0.4 else 0
        R.paste_center(im, PILL[1 if placed else 0], 850, 1130 + (1 - ab) * 16, ab, 1 - 0.035 * press)
    K.captions(im, t, CAPS, y=1730, size=56)
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = K.GrooveMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = K.groove(CLIP + END, 0.0, 1.0, seed=13); env = np.minimum(1, np.arange(len(g)) / SR / 1.2)
        mx.fadd(g * env, 0.0, 0.55)
        y = mx.tt(0.04); mx.fadd(np.sin(2 * np.pi * 2200 * y) * np.exp(-y * 120), ON_T + 0.05, 0.03)        # toggle click
        y = mx.tt(0.05); mx.fadd(np.convolve(mx.rng.normal(0, 1, len(y)), np.ones(3) / 3, "same") * np.exp(-y * 90), PRESS_T, 0.05)   # soft tap
        K.chime(mx, 6.45, 1318.5, 0.045)                                                              # after 'mean it'
        mx.write("s6e6_audio.wav")
    render(frame, TOTAL, "s6e6_audio.wav", OUT)
