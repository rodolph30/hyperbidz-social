"""Season 3 Ep. 5 'Something you love': golden S3 grade. A paper tag names the brass coffee pot ('TETA'S DALLAH · brass,
1940s'), a light glint runs over the brass while he looks down at it, bidders gather around him on 'when people compete
for it', and on 'you walk away proud' the hammer falls: SOLD · $340 · to the 9th bidder, with a warm glow.
End card 'Sell it with pride.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
from s3_common import Look, pluck

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET = (167, 139, 250)
FR = decode()
LOOK = Look(windows=((240, 300, 120), (560, 300, 90), (880, 300, 120)), key=(540, 900))
CAPS = [(0.45, 2.95, ["Selling something you love", "shouldn't feel like [losing.]"]), (4.15, 5.65, ["When people", "[compete] for it…"]),
        (6.25, 7.85, ["you walk away [proud.]"])]
TAG_AT, GLINT, BIDS_AT, SOLD = 0.9, 3.0, 4.25, 6.4
BIDS = [(4.25, "Nadine", 90, 225, 330), (4.55, "Georges", 140, 855, 380), (4.85, "Hiba", 190, 215, 520), (5.15, "Sami", 260, 865, 560), (5.45, "+5 more", 340, 225, 700)]

def ptag(title, line, rot):
    a = R.text_layer(title, R.font(22, mono=True), (110, 84, 52), tracking=2); b = R.text_layer(line, R.font(28, 500), (62, 48, 34))
    w = max(a.width, b.width) + 44; h = a.height + b.height + 40
    im = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((18, 22, w + 14, h + 18), radius=14, fill=(40, 24, 8, 110)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(card).rounded_rectangle((0, 0, w - 1, h - 1), radius=14, fill=(250, 241, 222, 246), outline=(222, 196, 150, 255), width=2)
    card.alpha_composite(a, ((w - a.width) // 2, 16)); card.alpha_composite(b, ((w - b.width) // 2, 22 + a.height))
    im.alpha_composite(card, (15, 15)); return im.rotate(rot, resample=Image.BICUBIC, expand=True)
TAG = ptag("TETA'S DALLEH", "brass, 1940s", 3)

def bid_chip(name, amt):
    a = R.text_layer(name, R.font(30, 600), WHITE); b = R.text_layer(f"${amt}" if not name.startswith("+") else "", R.font(34, 700), WHITE)
    w = a.width + (b.width + 22 if b.width > 4 else 0) + 86; h = 66
    im = M.glass(w, h, h // 2, fill=(36, 28, 76, 236), border=(*VIOLET, 230)); d = ImageDraw.Draw(im)
    d.ellipse((12, 11, 56, 55), fill=(124, 92, 255, 255)); ini = R.text_layer(name[0], R.font(26, 700), WHITE); im.alpha_composite(ini, (34 - ini.width // 2, 33 - ini.height // 2 - 2))
    im.alpha_composite(a, (68, (h - a.height) // 2 - 2))
    if b.width > 4: im.alpha_composite(b, (68 + a.width + 22, (h - b.height) // 2 - 2))
    return im
CHIPS = [bid_chip(n, a) for _, n, a, _, _ in BIDS]

def live_pill(v):
    b = R.text_layer("LIVE BIDS", R.font(24, mono=True), (235, 238, 255), tracking=3); a = R.text_layer(f"${v}", R.font(64, 700), WHITE)
    w, h = max(a.width, b.width) + 80, a.height + b.height + 36
    im = M.glass(w, h, 30, fill=(20, 16, 44, 236), border=(*VIOLET, 230)); im.alpha_composite(b, ((w - b.width) // 2, 14)); im.alpha_composite(a, ((w - a.width) // 2, 18 + b.height)); return im
def sold_pill():
    a = R.text_layer("SOLD  ·  $340", R.font(70, 700), WHITE); b = R.text_layer("to the 9th bidder", R.font(34, 500), (235, 238, 255))
    w, h = max(a.width, b.width) + 100, a.height + b.height + 46
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=38, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(a, ((w - a.width) // 2, 18)); im.alpha_composite(b, ((w - b.width) // 2, 24 + a.height)); return im
SOLD_IM = sold_pill()

def pot_center(t):
    k = R.clamp(t / 8.0); return 530 + 10 * k, 1190 + 90 * k
def glint(im, t, t0, dur=0.9):
    k = (t - t0) / dur
    if not 0 <= k <= 1: return
    cx, cy = pot_center(t); w, h = 380, 460
    band = Image.new("L", (w, h), 0); d = ImageDraw.Draw(band); x = -w * 0.3 + k * w * 1.6
    d.polygon([(x - 50, h), (x + 50, h), (x + 50 + h * 0.5, 0), (x - 50 + h * 0.5, 0)], fill=int(255 * 0.55 * np.sin(np.pi * k)))
    band = band.filter(ImageFilter.GaussianBlur(24)); m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).ellipse((40, 30, w - 40, h - 20), fill=255); m = m.filter(ImageFilter.GaussianBlur(30))
    a = (np.asarray(band, np.float32) * np.asarray(m, np.float32) / 255).astype(np.uint8)
    lay = Image.new("RGBA", (w, h), (255, 236, 190, 0)); lay.putalpha(Image.fromarray(a)); im.alpha_composite(lay, (int(cx - w / 2), int(cy - h / 2)))

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Sell it", "with pride."], END)
    im = LOOK(FR[min(len(FR) - 1, int(t * FPS))], t)
    if t >= SOLD:                                           # a warm glow of pride behind him
        g = R.ease_out((t - SOLD) / 0.6)
        lay = Image.new("RGBA", (900, 900), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((100, 100, 800, 800), fill=(255, 210, 140, int(70 * g)))
        R.paste_center(im, lay.filter(ImageFilter.GaussianBlur(120)), 540, 760)
    if TAG_AT <= t < BIDS_AT:
        k = (t - TAG_AT) / 0.6; out = R.clamp((t - (BIDS_AT - 0.35)) / 0.35)
        lay = TAG if k >= 1 else TAG.filter(ImageFilter.GaussianBlur(8 * (1 - R.ease_out(k))))
        R.paste_center(im, lay, 215, 470 + 6 * np.sin((t - TAG_AT) * 2.2) - out * 30, R.ease_out(k) * (1 - out))
        sparkle_burst(im, t, TAG_AT + 0.15, 215, 470, ((-130, -40, 18), (130, -30, 14), (100, 40, 18)))
    glint(im, t, GLINT)
    if BIDS_AT <= t < SOLD + 0.3:
        fade = 1 - R.clamp((t - SOLD) / 0.3)
        for (at, n, a, x, y), ch in zip(BIDS, CHIPS):
            if t < at: continue
            k = (t - at) / 0.3; R.paste_center(im, ch, x, y + (1 - R.ease_out(k)) * 30, R.clamp(k * 3) * fade, 0.8 + 0.2 * R.stamp(k) if k < 1 else 1.0)
        cur = [a for at, n, a, x, y in BIDS if t >= at][-1]
        R.paste_center(im, live_pill(cur), W / 2, 160, R.clamp((t - BIDS_AT) / 0.25) * fade)
    if t >= SOLD:
        s = (t - SOLD) / 0.35; R.paste_center(im, SOLD_IM, W / 2, 170, R.clamp(s * 3), 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, SOLD, W / 2, 170, ((-330, -40, 34), (320, -60, 26), (-260, 60, 18), (300, 50, 34)))
    draw_caps(im, t, CAPS, y=1700, size=62)
    if SOLD <= t < SOLD + 0.08: im = M.flash(im, 0.25, (255, 236, 200))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, .32), (220, .22), (293.7, .16), (370, .06)))
        for i, f in enumerate([293.7, 440, 370, 392, 293.7, 440, 349.2, 293.7]): pluck(mx, 0.2 + i * 0.95, f, 0.06)
        mx.shimmer(TAG_AT, 1174.7, 0.06); mx.shimmer(GLINT + 0.1, 1568, 0.07)
        for i, (at, *_ ) in enumerate(BIDS): mx.ping(at, 1046.5 * 2 ** (i * 2 / 12), 0.11)
        mx.thud(SOLD, 0.55); mx.shimmer(SOLD + 0.02, 1318.5, 0.13)
        for i, f in enumerate([587.3, 740, 880]): pluck(mx, SOLD + 0.1 + i * 0.1, f, 0.06, 1.4)
        mx.write("s3e5_audio.wav")
    render(frame, TOTAL, "s3e5_audio.wav", OUT)
