"""Season 3 Ep. 4 'They come to you': golden S3 grade. While he says 'For years, you chased buyers. Answered every
message. Dropped your price.' his own messages pile up unanswered ('Seen') and his price tag drops $300 -> $250 -> $200.
On 'Now?' a violet ripple sweeps it all away, and on 'They come to you' bids fly in from every side: 12 bidders, $480.
End card 'Now they come to you.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
from s3_common import Look, pluck

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, AMBER = (167, 139, 250), (255, 184, 92)
FR = decode()
LOOK = Look(windows=((324, 300, 120), (670, 300, 90), (994, 300, 120)), key=(540, 760))
CAPS = [(0.45, 2.40, ["For years, you", "[chased] buyers."]), (2.50, 3.95, ["Answered", "every message."]),
        (4.00, 5.35, ["Dropped your [price.]"]), (5.60, 6.40, ["Now…"]), (6.45, 7.85, ["[they come to you.]"])]
MSGS = [(0.75, "Hi! Still available :)", "Seen · 2h", 245, 235), (1.65, "I can do $20 less", "Seen · 5h", 835, 335),
        (2.65, "Hello? Still interested?", "Seen · yesterday", 250, 445), (3.55, "OK, final: $200", "Delivered", 830, 545)]
PRICES = [(4.05, "$300"), (4.45, "$250"), (4.85, "$200")]
NOW, COME = 5.72, 6.45
BIDS = [(6.50, "Karim", "$320", -1, 250, 330), (6.68, "Maya", "$350", 1, 830, 420), (6.86, "Rami", "$380", -1, 240, 520), (7.04, "+9 bidders", "", 1, 840, 600)]
TOP = 7.15

def out_msg(text, rcpt):
    tx = R.text_layer(text, R.font(34, 600), WHITE); w, h = tx.width + 52, tx.height + 34
    im = Image.new("RGBA", (w, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=(58, 92, 160, 238)); d.polygon([(w - 70, h - 2), (w - 26, h - 2), (w - 18, h + 16)], fill=(58, 92, 160, 238))
    im.alpha_composite(tx, (26, 15)); r = R.text_layer(rcpt, R.font(22, mono=True), (225, 228, 238), tracking=1); im.alpha_composite(r, (w - r.width - 8, h + 14)); return im
MSG_IM = [out_msg(t, r) for _, t, r, _, _ in MSGS]

def price_tag(p, strike):
    tl = R.text_layer(p, R.font(48, 700), (60, 40, 10)); w, h = tl.width + 50, tl.height + 26
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=14, fill=(250, 241, 222, 245), outline=(222, 196, 150, 255), width=2)
    im.alpha_composite(tl, (25, 13))
    if strike > 0: ImageDraw.Draw(im).line([(10, h // 2 + 3), (10 + (w - 20) * strike, h // 2 - 3)], fill=(200, 60, 60, 255), width=6)
    return im

def bid_chip(name, amt):
    a = R.text_layer(name, R.font(30, 600), WHITE); b = R.text_layer(amt, R.font(34, 700), WHITE) if amt else None
    w = a.width + (b.width + 22 if b else 0) + 86; h = 66
    im = M.glass(w, h, h // 2, fill=(36, 28, 76, 236), border=(*VIOLET, 230)); d = ImageDraw.Draw(im)
    d.ellipse((12, 11, 56, 55), fill=(124, 92, 255, 255)); ini = R.text_layer(name[0] if name[0] != "+" else "+", R.font(26, 700), WHITE); im.alpha_composite(ini, (34 - ini.width // 2, 33 - ini.height // 2 - 2))
    im.alpha_composite(a, (68, (h - a.height) // 2 - 2))
    if b: im.alpha_composite(b, (68 + a.width + 22, (h - b.height) // 2 - 2))
    return im
BID_IM = [bid_chip(n, a) for _, n, a, _, _, _ in BIDS]

def top_pill():
    b = R.text_layer("LIVE  ·  12 BIDDERS", R.font(24, mono=True), (235, 238, 255), tracking=3); a = R.text_layer("$480", R.font(70, 700), WHITE)
    w, h = max(a.width, b.width) + 90, a.height + b.height + 40
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=32, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(b, ((w - b.width) // 2, 16)); im.alpha_composite(a, ((w - a.width) // 2, 20 + b.height)); return im
TOP_IM = top_pill()

def ring(im, cx, cy, rad, a, width=6):
    if a <= 0.01: return
    lay = Image.new("RGBA", (int(rad * 2 + 20), int(rad * 2 + 20)), (0, 0, 0, 0)); c = lay.width / 2
    ImageDraw.Draw(lay).ellipse((c - rad, c - rad, c + rad, c + rad), outline=(*VIOLET, int(255 * a)), width=width); R.paste_center(im, lay, cx, cy)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Now they", "come to you."], END)
    im = LOOK(FR[min(len(FR) - 1, int(t * FPS))], t)
    sweep = R.clamp((t - NOW) / 0.45) if t >= NOW else 0
    for (at, *_r, x, y), mi in zip(MSGS, MSG_IM):          # his unanswered messages pile up
        if t < at or sweep >= 1: continue
        k = (t - at) / 0.3; side = -1 if x < 540 else 1
        R.paste_center(im, mi, x + side * sweep ** 2 * 700, y - sweep * 60, R.clamp(k * 3) * (1 - sweep) * (0.75 if t >= at + 1.6 else 1.0), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    shown = [p for p in PRICES if t >= p[0]]
    if shown and t < NOW + 0.3:                               # the price keeps dropping
        at, p = shown[-1]; nxt = [q for q in PRICES if q[0] > at]; k = (t - at) / 0.25
        sk = R.clamp((t - (nxt[0][0] - 0.18)) / 0.15) if nxt else 0
        R.paste_center(im, price_tag(p, sk), W / 2, 150 + (1 - R.ease_out(k)) * -20, R.clamp(k * 3) * (1 - sweep), 0.9 + 0.1 * R.stamp(k) if k < 1 else 1.0)
    if NOW <= t < NOW + 0.7:
        for j in range(2): kk = R.clamp((t - NOW - 0.1 * j) / 0.6); ring(im, 540, 900, 80 + 700 * R.ease_out(kk), (1 - kk) * 0.8, 7)
    for (at, n, a, side, x, y), bi in zip(BIDS, BID_IM):   # the bids come to him
        if t < at: continue
        k = R.ease_out((t - at) / 0.45); sx = x + side * (1 - k) * 700
        R.paste_center(im, bi, sx, y, R.clamp((t - at) / 0.2), 1.0 + 0.08 * (1 - R.clamp((t - at - 0.4) / 0.15)) if t > at + 0.4 else 1.0)
    if t >= TOP:
        s = (t - TOP) / 0.32; R.paste_center(im, TOP_IM, W / 2, 150, R.clamp(s * 3), 1.4 - 0.4 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, TOP, W / 2, 150, ((-250, -30, 26), (240, -40, 18), (200, 40, 26)))
    draw_caps(im, t, CAPS, y=1660, size=62)
    if TOP <= t < TOP + 0.07: im = M.flash(im, 0.18, (255, 236, 200))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, .32), (220, .22), (293.7, .16), (370, .06)))
        for i, f in enumerate([293.7, 349.2, 293.7, 261.6, 293.7]): pluck(mx, 0.3 + i * 1.05, f, 0.055)       # lonely, falling
        for at, *_ in MSGS: y = mx.tt(0.12); mx.fadd(np.sin(2 * np.pi * 1200 * y) * np.exp(-y * 40), at, 0.12)   # message sent
        for at, _ in PRICES[1:]: y = mx.tt(0.25); mx.fadd(np.sin(2 * np.pi * np.cumsum(700 - 400 * y / 0.25) / 48000) * np.exp(-y * 9), at - 0.15, 0.12)  # dropping
        mx.whoosh(NOW - 0.05, 0.5, 0.3); mx.thud(NOW, 0.4)
        for i, (at, *_ ) in enumerate(BIDS[:2]): mx.ping(at + 0.35, 1046.5 * 2 ** (i * 3 / 12), 0.1)   # keep 'you' clear
        for i, f in enumerate([440, 554.4, 659.3, 880]): pluck(mx, 7.5 + i * 0.12, f, 0.06, 1.4)                   # rising, warm
        mx.thud(7.5, 0.45); mx.shimmer(7.52, 1318.5, 0.12)
        mx.write("s3e4_audio.wav")
    render(frame, TOTAL, "s3e4_audio.wav", OUT)
