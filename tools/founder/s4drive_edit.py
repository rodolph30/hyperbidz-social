"""Season 4 'Drove it home' (red convertible on the Corniche at blue hour). '23 people wanted this car': 23 bidders
pop in across the sky, counter climbing to 23. 'Only one drove it home tonight': 22 of them turn grey and fall away; one
glows, grows and takes the centre: 'Drove it home · $41,500'. 'Next time?': a pill 'NEXT CAR AUCTION · SOON' with a
pulsing dot. 'Make it you': a YOU avatar pops in and a gold crown drops onto it. Speed streaks at the edges throughout.
Last shot held with a slow push-in. End card 'Next time, make it you.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s4_common as S

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, RED, GOLD = S.VIOLET, S.RED, (255, 206, 92)
FR = decode()
CAPS = [(0.15, 2.20, ["[23 people] wanted", "this car."]), (2.80, 4.60, ["Only [one] drove it", "home tonight."]),
        (5.35, 6.35, ["[Next time?]"]), (6.60, 9.20, ["Make it [you.]"])]
FILL0, FILL1, ONE, WIN, NEXT, YOU, CROWN = 0.25, 1.85, 3.0, 3.25, 5.35, 6.65, 7.0
rng = np.random.default_rng(9)
POS = [(78 + i * 84, 118) for i in range(12)] + [(120 + i * 84, 204) for i in range(11)]
ORDER = rng.permutation(23); AT = {int(j): FILL0 + (FILL1 - FILL0) * (k / 22) ** 0.85 for k, j in enumerate(ORDER)}
WINNER = 6
NAMES = "RKMJNTLSHAGDBWFYZEOPQCV"

def avatar(ch, k, s=68, grey=False):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hue = (110, 110, 120) if grey else [(124, 92, 255), (47, 123, 255), (167, 139, 250), (98, 70, 230)][k % 4]
    d.ellipse((2, 2, s - 3, s - 3), fill=hue + (255,), outline=(255, 255, 255, 150 if grey else 230), width=3)
    tl = R.text_layer(ch, R.font(int(s * 0.44), 700), (200, 200, 205) if grey else WHITE); im.alpha_composite(tl, ((s - tl.width) // 2, (s - tl.height) // 2 - 2)); return im
AV = [avatar(NAMES[i], i) for i in range(23)]; AVG = [avatar(NAMES[i], i, grey=True) for i in range(23)]
WIN_BIG = avatar(NAMES[WINNER], WINNER, 110)

def counter(n):
    a = R.text_layer("BIDDERS", R.font(22, mono=True), (225, 228, 240), tracking=3); b = R.text_layer(str(n), R.font(46, 700), WHITE)
    w, h = a.width + b.width + 70, 70; im = M.glass(w, h, h // 2, fill=(14, 16, 28, 220), border=(*VIOLET, 200))
    im.alpha_composite(a, (26, (h - a.height) // 2)); im.alpha_composite(b, (w - 26 - b.width, (h - b.height) // 2 - 3)); return im

def label(top, big):
    a = R.text_layer(top, R.font(22, mono=True), (230, 226, 255), tracking=3); b = R.text_layer(big, R.font(40, 700), WHITE)
    w, h = max(a.width, b.width) + 60, a.height + b.height + 30; im = M.glass(w, h, 26, fill=(26, 20, 60, 236), border=(*VIOLET, 230))
    im.alpha_composite(a, ((w - a.width) // 2, 12)); im.alpha_composite(b, ((w - b.width) // 2, 12 + a.height)); return im
WIN_LAB = label("DROVE IT HOME", "$41,500")

def next_pill(t):
    tl = R.text_layer("NEXT CAR AUCTION  ·  SOON", R.font(28, mono=True), WHITE, tracking=3); w, h = tl.width + 110, tl.height + 34
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    a = int(150 + 105 * (0.5 + 0.5 * np.sin(t * 8))); ImageDraw.Draw(im).ellipse((34, h // 2 - 12, 58, h // 2 + 12), fill=(255, 255, 255, a))
    im.alpha_composite(tl, (76, 17)); return im

def you_avatar():
    s = 120; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((3, 3, s - 4, s - 4), fill=(255, 255, 255, 255), outline=(*VIOLET, 255), width=6)
    tl = R.text_layer("YOU", R.font(36, 700), (60, 40, 150)); im.alpha_composite(tl, ((s - tl.width) // 2, (s - tl.height) // 2 - 2)); return im
YOU_IM = you_avatar()

def crown():
    w, h = 110, 70; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(6, 62), (12, 16), (34, 40), (55, 6), (76, 40), (98, 16), (104, 62)], fill=GOLD + (255,), outline=(200, 140, 30, 255))
    d.rectangle((6, 54, 104, 66), fill=(235, 176, 60, 255))
    for x, y in ((12, 14), (55, 5), (98, 14)): d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 240, 200, 255))
    return im
CROWN_IM = crown()

STREAKS = [(rng.choice([-1, 1]), rng.uniform(-0.9, 0.9), rng.uniform(0, 1), rng.uniform(0.7, 1.3)) for _ in range(26)]
VP = (540, 560)
def streaks(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    for side, ang, ph, sp in STREAKS:
        k = (ph + t * 0.9 * sp) % 1; r0, r1 = 420 + 700 * k, 420 + 700 * k + 140 + 160 * k
        a = np.radians(ang * 40) + (0 if side > 0 else np.pi)
        x0, y0 = VP[0] + r0 * np.cos(a), VP[1] + r0 * np.sin(a) * 0.9; x1, y1 = VP[0] + r1 * np.cos(a), VP[1] + r1 * np.sin(a) * 0.9
        if 230 < x0 < 850 and 230 < x1 < 850: continue
        d.line([(x0, y0), (x1, y1)], fill=(220, 230, 255, int(70 * np.sin(np.pi * k))), width=3)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Next time,", "make it you."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = S.look(fr, "night")
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 560))
    if t < SHOT: streaks(im, t)
    fade = 1 - R.clamp((t - (CLIP - 0.5)) / 0.3)
    for i in range(23):                                                                        # 23 people wanted it
        at = AT[i]
        if t < at or (i != WINNER and t >= ONE + 1.0) or (i == WINNER and t >= WIN): continue
        s = (t - at) / 0.25; x, y = POS[i]
        if t >= ONE and i != WINNER:                                                          # ...they fall away
            k = t - ONE - 0.02 * (i % 7); k = max(0.0, k)
            R.paste_center(im, AVG[i] if k > 0.05 else AV[i], x, y + 900 * k * k, max(0, 1 - k / 0.9))
        else: R.paste_center(im, AV[i], x, y, R.clamp(s * 3), 0.5 + 0.5 * R.stamp(s) if s < 1 else 1.0)
    if FILL0 <= t < ONE + 0.5:
        n = sum(t >= AT[i] for i in range(23)) if t < ONE else 1
        R.paste_center(im, counter(n), 175, 300, R.clamp((t - FILL0) / 0.2) * (1 - R.clamp((t - ONE - 0.2) / 0.3)))
    if WIN <= t < NEXT + 0.3:                                                                 # only one drove it home
        k = R.ease_out((t - WIN) / 0.45); x0, y0 = POS[WINNER]; out = R.clamp((t - NEXT) / 0.3)
        x, y = x0 + (W / 2 - x0) * k, y0 + (150 - y0) * k
        glow = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((30, 30, 170, 170), fill=(*VIOLET, 170)); glow = glow.filter(ImageFilter.GaussianBlur(18))
        R.paste_center(im, glow, x, y, (0.6 + 0.4 * np.sin(t * 5)) * (1 - out))
        R.paste_center(im, WIN_BIG, x, y, 1 - out, (68 + (110 - 68) * k) / 110 * (1 - 0.3 * out))
        if t >= WIN + 0.35: s = (t - WIN - 0.35) / 0.3; R.paste_center(im, WIN_LAB, W / 2, 262, R.clamp(s * 3) * (1 - out), 0.85 + 0.15 * R.stamp(s) if s < 1 else 1.0)
        if t >= 4.45: sparkle_burst(im, t, 4.45, W / 2, 150, ((-80, -40, 26), (85, -30, 18), (70, 50, 26)))
    if t >= NEXT:                                                                            # next time?
        s = (t - NEXT) / 0.3; up = R.ease_out((t - YOU) / 0.35) if t >= YOU else 0
        R.paste_center(im, next_pill(t), W / 2, 150 - 60 * up, R.clamp(s * 3) * fade, 0.85 + 0.15 * R.stamp(s) if s < 1 else 1.0)
    if t >= YOU:                                                                             # make it you
        s = (t - YOU) / 0.32
        R.paste_center(im, YOU_IM, W / 2, 228, R.clamp(s * 3) * fade, 0.4 + 0.6 * R.stamp(s) if s < 1 else 1.0)
        for j in range(2): kk = R.clamp((t - YOU - 0.1 * j) / 0.6); S.ring(im, W / 2, 228, 60 + 260 * R.ease_out(kk), (1 - kk) * 0.8, VIOLET, 6)
    if t >= CROWN:
        k = R.clamp((t - CROWN) / 0.3); y = 160 - 260 * (1 - R.ease_out(k)) + (8 * np.sin((t - CROWN - 0.3) * 18) * np.exp(-(t - CROWN - 0.3) * 6) if k >= 1 else 0)
        R.paste_center(im, CROWN_IM.rotate(-8, resample=Image.BICUBIC, expand=True), W / 2 + 12, y, R.clamp(k * 4) * fade)
        if t >= CROWN + 0.3: sparkle_burst(im, t, CROWN + 0.3, W / 2 + 12, 160, ((-70, -30, 26), (75, -20, 18), (60, 40, 26)))
    draw_caps(im, t, CAPS, y=1700, size=62)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, 0.0),))
        y = mx.tt(SHOT); eng = (np.sin(2 * np.pi * 46 * y) + 0.5 * np.sin(2 * np.pi * 92 * y + 1)) * (0.8 + 0.2 * np.sin(2 * np.pi * 3.1 * y))
        mx.fadd(mx.lp(eng, 6) * np.minimum(1, y / 0.3) * np.minimum(1, (y[-1] - y) / 0.4), 0, 0.06)                         # engine purr
        y = mx.tt(SHOT); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 30) * np.minimum(1, y / 0.5) * np.minimum(1, (y[-1] - y) / 0.4), 0, 0.12)   # wind
        S.tone(mx, 0.0, CLIP, ((146.8, .28), (185, .2), (220, .18), (293.7, .08)), 0.04, 1.0)
        for i in range(23):
            at = AT[i]
            if i % 2: continue
            y = mx.tt(0.05); mx.fadd(np.sin(2 * np.pi * (1300 + 25 * i) * y) * np.exp(-y * 70), at, 0.02)
        y = mx.tt(0.7); mx.fadd(np.sin(2 * np.pi * np.cumsum(600 * np.exp(-y * 2)) / SR) * np.exp(-y * 3), ONE + 0.05, 0.03)   # they fall away
        mx.ping(4.47, 1318.5, 0.08); mx.shimmer(4.5, 1567.98, 0.05)                                                          # after 'tonight'
        mx.ping(NEXT - 0.08, 1046.5, 0.05)
        mx.thud(7.35, 0.4); mx.shimmer(7.37, 1318.5, 0.1)                                                                     # after 'you'
        mx.write("s4drive_audio.wav")
    render(frame, TOTAL, "s4drive_audio.wav", OUT)
