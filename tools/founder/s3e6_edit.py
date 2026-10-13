"""Season 3 Ep. 6 'The very first' (finale): golden S3 grade on the sunset loggia. Three empty lots for the first
auctions wait at the top ('need great items'); on 'Yours could open the very first one' LOT 01 lights up: YOUR ITEM,
opening auction. On 'Send us a message' a DM types SELLER and sends. End card 'DM us "SELLER" to go first.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
from s3_common import Look, pluck

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET = (167, 139, 250)
FR = decode()
LOOK = Look(windows=((160, 120, 70),), key=(520, 820), vig_center=(540, 960), motes=34)
CAPS = [(0.45, 3.35, ["The first HyperBidz auctions", "need [great items.]"]), (3.70, 6.10, ["Yours could open", "the [very first one.]"]),
        (6.40, 7.85, ["[Send us a message.]"])]
LOTS_AT, LIGHT, DM_AT, SEND = 0.9, 3.85, 6.45, 7.2
LOT_X = (220, 540, 860)

def lot(n, lit=False):
    w, h = 270, 190
    if lit:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=24, fill=255)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
        a = R.text_layer(f"LOT {n:02d}", R.font(24, mono=True), (235, 238, 255), tracking=3); b = R.text_layer("YOUR ITEM", R.font(44, 700), WHITE)
        c = R.text_layer("opening auction", R.font(26, 500), (235, 238, 255))
        im.alpha_composite(a, ((w - a.width) // 2, 22)); im.alpha_composite(b, ((w - b.width) // 2, 58)); im.alpha_composite(c, ((w - c.width) // 2, 122)); return im
    im = M.glass(w, h, 24, fill=(16, 14, 28, 200), border=(255, 255, 255, 90)); d = ImageDraw.Draw(im)
    for x in range(18, w - 18, 22): d.line([(x, 14), (x + 10, 14)], fill=(255, 255, 255, 110), width=2); d.line([(x, h - 14), (x + 10, h - 14)], fill=(255, 255, 255, 110), width=2)
    a = R.text_layer(f"LOT {n:02d}", R.font(24, mono=True), (220, 224, 240), tracking=3); q = R.text_layer("?", R.font(64, 700), (220, 224, 240))
    im.alpha_composite(a, ((w - a.width) // 2, 26)); im.alpha_composite(q, ((w - q.width) // 2, 66)); return im
LOTS = [lot(i + 1) for i in range(3)]; LOT1 = lot(1, True)

def dm(text, sent):
    hd = R.text_layer("MESSAGE  @hyperbidz", R.font(22, mono=True), (180, 184, 200), tracking=2)
    tx = R.text_layer(text + ("" if sent else "|"), R.font(44, 700), WHITE)
    w, h = 360, hd.height + 90 + 36; im = M.glass(w, h, 28, fill=(22, 22, 34, 238), border=(*VIOLET, 210)); d = ImageDraw.Draw(im)
    im.alpha_composite(hd, (24, 18))
    d.rounded_rectangle((20, 26 + hd.height, w - 20, h - 22), radius=24, fill=(44, 46, 60, 255))
    im.alpha_composite(tx, (40, 26 + hd.height + (h - 48 - hd.height - tx.height) // 2))
    cx, cy = w - 52, 26 + hd.height + (h - 48 - hd.height) // 2
    d.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=(124, 92, 255, 255) if not sent else (47, 200, 140, 255))
    if sent: d.line([(cx - 11, cy + 1), (cx - 3, cy + 9), (cx + 12, cy - 8)], fill=(255, 255, 255, 255), width=5)
    else: d.polygon([(cx - 9, cy - 11), (cx + 12, cy), (cx - 9, cy + 11), (cx - 5, cy)], fill=(255, 255, 255, 255))
    return im

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["DM us “SELLER”", "to go first."], END)
    im = LOOK(FR[min(len(FR) - 1, int(t * FPS))], t)
    for i, x in enumerate(LOT_X):                               # the first lots wait to be filled
        at = LOTS_AT + 0.18 * i
        if t < at: continue
        k = (t - at) / 0.35; a = R.clamp(k * 3) * (1 - R.clamp((t - (CLIP - 0.6)) / 0.3))
        if i == 0 and t >= LIGHT:
            s = (t - LIGHT) / 0.35; R.paste_center(im, LOT1, x, 230, a, 1.35 - 0.35 * R.stamp(s) if s < 1 else 1.0 + 0.02 * np.sin((t - LIGHT) * 4))
            sparkle_burst(im, t, LIGHT, x, 230, ((-150, -70, 26), (150, -80, 18), (140, 80, 26), (-120, 90, 18)))
        else:
            R.paste_center(im, LOTS[i], x, 230 + 4 * np.sin(t * 2 + i), a * (0.6 if t >= LIGHT else 1.0), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    if t >= DM_AT:
        k = (t - DM_AT) / 0.3; n = int(R.clamp((t - DM_AT - 0.2) / 0.45) * 6)
        R.paste_center(im, dm("SELLER"[:n], t >= SEND), 860, 640, R.clamp(k * 3), (0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0) * (0.94 if SEND <= t < SEND + 0.08 else 1.0))
        if t >= SEND: sparkle_burst(im, t, SEND, 860, 640, ((-170, -60, 18), (170, -70, 26), (150, 60, 18)))
    draw_caps(im, t, CAPS, y=1700, size=60)
    if LIGHT <= t < LIGHT + 0.08: im = M.flash(im, 0.2, (255, 236, 200))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, .32), (220, .22), (293.7, .16), (370, .06)))
        for i, f in enumerate([293.7, 440, 370, 392, 293.7, 440, 587.3, 440]): pluck(mx, 0.2 + i * 0.95, f, 0.06)
        for i in range(3): mx.ping(LOTS_AT + 0.18 * i, 784 + 120 * i, 0.07)
        mx.thud(LIGHT, 0.45); mx.shimmer(LIGHT + 0.02, 1318.5, 0.12)
        for i in range(6): y = mx.tt(0.03); mx.fadd(np.sin(2 * np.pi * 2600 * y) * np.exp(-y * 150), DM_AT + 0.2 + i * 0.075, 0.18)   # typing
        y = mx.tt(0.3); mx.fadd(np.sin(2 * np.pi * np.cumsum(600 + 900 * y / 0.3) / SR) * np.exp(-y * 8), SEND, 0.14)          # sent
        mx.shimmer(SEND + 0.05, 1568, 0.08)
        mx.write("s3e6_audio.wav")
    render(frame, TOTAL, "s3e6_audio.wav", OUT)
