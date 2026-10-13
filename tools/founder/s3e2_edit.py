"""Season 3 Ep. 2 'Forty years': golden S3 grade. The 3.45-5.15 s gap where Veo fumbled the watch between his hands is
covered by a memory close-up of the watch in his palm (faded photo look, ticking, 1985 -> 2026 year counter), then back
to him holding it to his chest. A '$50. Final offer.' lowball gets stamped out on 'ending', the bids answer: 14 bidders,
$1,240. End card 'Write a better ending.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
from s3_common import Look, memory, pluck

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, AMBER = (167, 139, 250), (255, 184, 92)
FR = decode()
LOOK = Look(windows=((220, 300, 120), (560, 300, 80), (880, 300, 120)), key=(560, 800))
CAPS = [(0.15, 1.55, ["This watch has a [story.]"]), (1.62, 3.50, ["[Forty years]", "on one wrist."]),
        (5.20, 7.70, ["Don't let a lowball offer", "write the [ending.]"])]
CUT_IN, CUT_OUT, SRC0 = 3.45, 5.15, 0.7
WATCH = (480, 1440)
BUB_AT, XST, PILL = 5.45, 7.02, 7.18
FIST = (440, 1215)

def crop_zoom(img, z, cx, cy):
    w, h = W / z, H / z; l = min(max(cx - w / 2, 0), W - w); t = min(max(cy - h / 2, 0), H - h)
    return img.crop((int(l), int(t), int(l + w), int(t + h))).resize((W, H), Image.BICUBIC)

def year_layer(t):
    k = R.clamp((t - (CUT_IN + 0.15)) / 1.3); yr = int(round(1985 + (2026 - 1985) * (1 - (1 - k) ** 2)))
    a = R.text_layer(str(yr), R.font(150, mono=True), (255, 240, 214)); b = R.text_layer("40 YEARS  ·  EVERY SINGLE DAY", R.font(26, mono=True), (255, 230, 196), tracking=4)
    im = Image.new("RGBA", (max(a.width, b.width) + 20, a.height + b.height + 20), (0, 0, 0, 0))
    im.alpha_composite(a, ((im.width - a.width) // 2, 0)); im.alpha_composite(b, ((im.width - b.width) // 2, a.height + 12)); return im

def bubble(head, text):
    hd = R.text_layer(head, R.font(22, mono=True), (180, 184, 200), tracking=3); tx = R.text_layer(text, R.font(40, 600), WHITE)
    w, h = max(hd.width, tx.width) + 60, hd.height + tx.height + 48
    im = Image.new("RGBA", (w, h + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=(52, 54, 68, 242)); d.polygon([(40, h - 2), (88, h - 2), (34, h + 22)], fill=(52, 54, 68, 242))
    im.alpha_composite(hd, (30, 18)); im.alpha_composite(tx, (30, 22 + hd.height)); return im
LOWBALL = bubble("BUYER", "$50. Final offer.")

def x_stamp(d=120):
    im = Image.new("RGBA", (d, d), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    g.ellipse((6, 6, d - 7, d - 7), fill=(20, 14, 40, 230), outline=(*VIOLET, 255), width=9)
    p = d * 0.32; g.line([(p, p), (d - p, d - p)], fill=(*VIOLET, 255), width=12); g.line([(d - p, p), (p, d - p)], fill=(*VIOLET, 255), width=12); return im
XS = x_stamp()

def bid_pill():
    b = R.text_layer("LIVE  ·  14 BIDDERS", R.font(22, mono=True), (235, 238, 255), tracking=3); a = R.text_layer("$1,240", R.font(72, 700), WHITE)
    w, h = max(a.width, b.width) + 70, a.height + b.height + 40
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=32, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(b, ((w - b.width) // 2, 16)); im.alpha_composite(a, ((w - a.width) // 2, 20 + b.height)); return im
PILL_IM = bid_pill()

def leak(im, k):
    """warm light-leak flash for the cuts in and out of the memory."""
    if k <= 0: return im
    lay = Image.new("RGBA", (W, H), (255, 214, 150, int(220 * k))); return Image.alpha_composite(im, lay)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Write a", "better ending."], END)
    if CUT_IN <= t < CUT_OUT:                                # the memory close-up
        src = FR[min(len(FR) - 1, int((SRC0 + (t - CUT_IN)) * FPS))]
        z = 2.0 + 0.3 * (t - CUT_IN) / (CUT_OUT - CUT_IN)
        im = memory(LOOK(crop_zoom(src, z, *WATCH), t, shafts=False, dust=False), 0.5, int(t * FPS))
        M.scrim(im, True, 620, 120); yl = year_layer(t); R.paste_center(im, yl, W / 2, 330, R.clamp((t - CUT_IN - 0.1) / 0.3))
        sparkle_burst(im, t, CUT_IN + 0.2, W / 2, 1000, ((-180, -60, 26), (190, -20, 18), (120, 90, 26)))
    else:
        im = LOOK(FR[min(len(FR) - 1, int(t * FPS))], t)
        if t >= CUT_OUT:                                     # the watch held to his heart: a warm glow at the fist
            g = 0.5 + 0.5 * np.sin((t - CUT_OUT) * 3)
            lay = Image.new("RGBA", (360, 360), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((40, 40, 320, 320), fill=(255, 214, 150, int(60 + 40 * g)))
            R.paste_center(im, lay.filter(ImageFilter.GaussianBlur(50)), *FIST)
        if BUB_AT <= t < XST + 0.6:
            k = (t - BUB_AT) / 0.3; fall = R.clamp((t - XST - 0.2) / 0.4)
            shake = 10 * np.sin((t - XST) * 60) * max(0, 1 - (t - XST) / 0.25) if t >= XST else 0
            R.paste_center(im, LOWBALL, 235 + shake, 640 + fall ** 2 * 260, R.clamp(k * 3) * (0.55 if t >= XST + 0.1 else 1) * (1 - fall), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
            if t >= XST:
                s = (t - XST) / 0.25; R.paste_center(im, XS, 235 + LOWBALL.width / 2 - 30, 640 - 50 + fall ** 2 * 260, R.clamp(s * 3) * (1 - fall), 1.7 - 0.7 * R.stamp(s) if s < 1 else 1.0)
        if t >= PILL:
            s = (t - PILL) / 0.32; R.paste_center(im, PILL_IM, 860, 620, R.clamp(s * 3), 1.4 - 0.4 * R.stamp(s) if s < 1 else 1.0)
            sparkle_burst(im, t, PILL, 860, 620, ((-180, -40, 26), (170, -60, 18), (150, 60, 26)))
        draw_caps(im, t, CAPS, y=1640, size=62)
    if CUT_IN <= t < CUT_IN + 0.22: im = leak(im, 1 - (t - CUT_IN) / 0.22)
    if CUT_OUT <= t < CUT_OUT + 0.22: im = leak(im, 1 - (t - CUT_OUT) / 0.22)
    if CUT_IN - 0.12 <= t < CUT_IN: im = leak(im, (t - (CUT_IN - 0.12)) / 0.12 * 0.8)
    if CUT_OUT - 0.12 <= t < CUT_OUT: im = leak(im, (t - (CUT_OUT - 0.12)) / 0.12 * 0.8)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, .32), (220, .22), (293.7, .16), (370, .06)))
        for i, f in enumerate([293.7, 440, 370, 392, 293.7, 440, 349.2, 293.7]): pluck(mx, 0.2 + i * 0.95, f, 0.06)
        mx.shimmer(CUT_IN - 0.05, 1174.7, 0.08)
        for i in range(7):                                                   # the watch ticking in the memory
            y = mx.tt(0.03); mx.fadd(np.sin(2 * np.pi * (3400 if i % 2 else 2900) * y) * np.exp(-y * 160), CUT_IN + 0.15 + i * 0.22, 0.4)
        mx.shimmer(CUT_OUT - 0.05, 880, 0.06)
        mx.ping(BUB_AT, 659.3, 0.08); mx.ping(BUB_AT + 0.08, 523.3, 0.08)
        mx.thud(XST, 0.45); y = mx.tt(0.2); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 3) * np.exp(-y * 16), XST, 0.22)
        mx.ping(PILL, 1318.5, 0.12); mx.shimmer(PILL + 0.03, 1568, 0.08)
        mx.write("s3e2_audio.wav")
    render(frame, TOTAL, "s3e2_audio.wav", OUT)
