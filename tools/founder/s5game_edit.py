"""Season 5 (the Vault) Ep. 3 'Want it'. 'What's better than owning a luxury watch?': a plain retail tag swings in,
RETAIL $9,400 · Pay. Own. Done. 'Knowing you want it': the Vault's Watch heart is tapped, fills violet with a burst,
and 41 others want it too. 'HyperBidz': the retail tag is struck out, the lit edge ignites and the Vault lot card
rises, 41 watching. 'Different game': FROM THE VAULT and the live timer. Last shot held with a slow push-in.
Vault end card 'Want it? Win it.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s5_common as V

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.45; END = 3.9; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.0, 2.35, ["You know what's better than", "owning a [luxury watch?]"]), (3.15, 4.95, ["Knowing you [want it.]"]),
        (5.40, 6.55, ["[HyperBidz.]"]), (6.80, 9.20, ["Different [game.]"])]
TAG_IN, HEART, FILL, BRAND, GAME = 0.9, 3.25, 3.78, 5.5, 6.9

def tag():
    w, h = 300, 220; im = Image.new("RGBA", (w + 40, h + 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line([(w / 2 + 20, 0), (w / 2 + 20, 118)], fill=(230, 222, 205, 255), width=3)                     # string
    tg = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dt = ImageDraw.Draw(tg)
    dt.polygon([(40, 0), (w - 40, 0), (w, 40), (w, h), (0, h), (0, 40)], fill=(246, 242, 232, 250), outline=(205, 196, 176, 255))
    dt.ellipse((w / 2 - 12, 20, w / 2 + 12, 44), fill=(60, 58, 54, 255))
    a = V.mono("RETAIL", 22, (110, 104, 96), 5); tg.alpha_composite(a, ((w - a.width) // 2, 62))
    b = R.text_layer("$9,400", R.font(64, 700), (40, 38, 36)); tg.alpha_composite(b, ((w - b.width) // 2, 92))
    c = R.text_layer("Pay. Own. Done.", R.font(24, 500), (110, 104, 96)); tg.alpha_composite(c, ((w - c.width) // 2, 172))
    im.alpha_composite(tg, (20, 118)); return im
TAG = tag()

def heart_poly(cx, cy, s):
    t = np.linspace(0, 2 * np.pi, 120)
    x = 16 * np.sin(t) ** 3; y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    return [(cx + s * a, cy + s * b) for a, b in zip(x, y)]

def heart(fill_k, size=150):
    im = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0)); c = size; s = size / 34
    if fill_k > 0:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).polygon(heart_poly(c, c, s * 1.15), fill=(124, 92, 255, int(150 * fill_k))); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(22)))
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon(heart_poly(c, c, s * (0.3 + 0.7 * fill_k)), fill=255)
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); lay.paste(V.lin_grad(im.width, im.height, (92, 149, 255), (160, 120, 255)), (0, 0), m); im.alpha_composite(lay)
    ImageDraw.Draw(im).line(heart_poly(c, c, s) + [heart_poly(c, c, s)[0]], fill=(255, 255, 255, 240), width=9, joint="curve")
    return im

def watchers():
    hp = Image.new("RGBA", (40, 40), (0, 0, 0, 0)); m = Image.new("L", (40, 40), 0); ImageDraw.Draw(m).polygon(heart_poly(20, 21, 1.05), fill=255)
    hp.paste(V.lin_grad(40, 40, (92, 149, 255), (160, 120, 255)), (0, 0), m)
    tx = R.text_layer("On your watchlist  ·  41 others want it too", R.font(30, 600), WHITE)
    w, h = tx.width + 110, 76; im = M.glass(w, h, h // 2, fill=(9, 10, 15, 214), border=(*V.EDGE, 255))
    im.alpha_composite(hp, (28, (h - 40) // 2)); im.alpha_composite(tx, (80, (h - tx.height) // 2 - 3)); return im
WATCH = watchers()
CARD = V.lot_card("Swiss Chronograph · from the Vault", "$6,200", "CURRENT BID · 41 WATCHING")
PILL = V.vault_pill()

def frame(t):
    if t >= CLIP: return V.vault_end_card(t - CLIP, ["Want it?", "Win it."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = V.vault_grade(fr, warm=1.0)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 700))
    if t >= BRAND: V.lit_edge(im, R.ease_out((t - BRAND) / 0.5), t)
    if TAG_IN <= t < BRAND + 0.8:                                                                        # owning: a retail tag
        k = R.ease_out((t - TAG_IN) / 0.5); sw = 6 * np.sin((t - TAG_IN) * 3.2) * np.exp(-(t - TAG_IN) * 0.8)
        dull = R.clamp((t - 2.5) / 0.6) * 0.5; out = R.clamp((t - BRAND - 0.35) / 0.4)
        tg = TAG.rotate(sw, resample=Image.BICUBIC, center=(TAG.width / 2, 0))
        if dull > 0: tg = Image.blend(tg, tg.convert("LA").convert("RGBA"), dull)
        if t >= BRAND:                                                                                   # struck out
            d = ImageDraw.Draw(tg); kk = R.clamp((t - BRAND) / 0.25); d.line([(30, 230), (30 + 280 * kk, 300 - 50 * kk)], fill=(*V.BTN, 255), width=9)
        R.paste_center(im, tg, 210, 40 + tg.height / 2 - (1 - k) * 260, R.clamp((t - TAG_IN) / 0.2) * (1 - 0.35 * dull) * (1 - out))
    if HEART <= t < BRAND + 0.3:                                                                         # wanting: the Watch heart
        fk = R.ease_out((t - FILL) / 0.25) if t >= FILL else 0; out = R.clamp((t - BRAND) / 0.3)
        s = (t - HEART) / 0.3; sc = (0.5 + 0.5 * R.stamp(s) if s < 1 else 1.0) * (1 + 0.18 * np.sin(np.pi * R.clamp((t - FILL) / 0.3)))
        R.paste_center(im, heart(fk), 870, 1180, R.clamp(s * 3) * (1 - out), sc)
        if t >= FILL:
            for j in range(2): kk = R.clamp((t - FILL - 0.08 * j) / 0.6); V_ring(im, 870, 1180, 60 + 260 * R.ease_out(kk), (1 - kk) * 0.8)
            sparkle_burst(im, t, FILL, 870, 1180, ((-120, -80, 26), (120, -90, 18), (110, 70, 26), (-110, 80, 18)))
        if t >= FILL + 0.25:
            s2 = (t - FILL - 0.25) / 0.3; R.paste_center(im, WATCH, W / 2, 1420, R.clamp(s2 * 3) * (1 - out), 0.85 + 0.15 * R.stamp(s2) if s2 < 1 else 1.0)
    if t >= BRAND:                                                                                       # a different game: the Vault
        k = R.ease_out((t - BRAND) / 0.45); fade = 1 - R.clamp((t - (CLIP - 0.5)) / 0.3)
        R.paste_center(im, CARD, W / 2, 1560 + (1 - k) * 200, R.clamp((t - BRAND) / 0.2) * fade)
    if t >= GAME:
        s = (t - GAME) / 0.3; fade = 1 - R.clamp((t - (CLIP - 0.5)) / 0.3)
        R.paste_center(im, PILL, 290, 150, R.clamp(s * 3) * fade, 0.85 + 0.15 * R.stamp(s) if s < 1 else 1.0)
        R.paste_center(im, V.timer_chip("2:14:08" if t < GAME + 0.5 else f"2:14:0{max(0, 8 - int((t - GAME - 0.5) * 1))}"), 880, 150, R.clamp((s - 0.4) * 3) * fade)
    draw_caps(im, t, CAPS, y=1845 if t >= BRAND else 1700, size=58)
    if t > CLIP - XF: im = Image.blend(im, Image.new("RGBA", (W, H), V.STAGE + (255,)), R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

def V_ring(im, cx, cy, rad, a, col=(124, 92, 255), width=7):
    if a <= 0.01: return
    lay = Image.new("RGBA", (int(rad * 2 + 20), int(rad * 2 + 20)), (0, 0, 0, 0)); c = lay.width / 2
    ImageDraw.Draw(lay).ellipse((c - rad, c - rad, c + rad, c + rad), outline=col + (int(255 * a),), width=width); R.paste_center(im, lay, cx, cy)

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = V.VaultMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        V.pad(mx, 0.0, BRAND, ((98, .3), (146.8, .2), (174.6, .14)), 0.045, 0.8)                         # G minor, plain
        y = mx.tt(0.25); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 4) * np.exp(-y * 14), TAG_IN, 0.05)  # paper tag swish
        y = mx.tt(0.05); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 90), FILL - 0.02, 0.06)   # tap
        mx.ping(4.95, 1318.5, 0.06); mx.ping(5.05, 1760, 0.04)                                           # after 'want it'
        mx.whoosh(BRAND - 0.2, 0.5, 0.15)
        V.pad(mx, BRAND, CLIP, ((146.8, .3), (185, .22), (220, .2), (277.2, .1)), 0.05, 0.6)
        V.ticks(mx, GAME + 0.6, SHOT + 0.8, 6, 0.025)
        V.chime(mx, 7.55, 1318.5, 0.07)
        mx.write("s5game_audio.wav")
    render(frame, TOTAL, "s5game_audio.wav", OUT)
