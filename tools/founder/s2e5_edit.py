"""Season 2 Ep. 5 'Same chance': a live bid feed with the watcher count climbing, two shady chat bubbles
('psst… DM me' and 'For you habibi… special price') stamped out, then five bidders on one shared clock.
End card 'Same clock. Same chance.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
VIOLET = (167, 139, 250)

def clean(fr):
    """paint out a stray violet wedge Veo put in the top-left corner (copy plain sky from the right, feathered)."""
    m = Image.new("L", (200, 90), 0); ImageDraw.Draw(m).rectangle((0, 0, 170, 66), fill=255); m = m.filter(ImageFilter.GaussianBlur(10))
    fr.paste(fr.crop((250, 0, 450, 90)), (0, 0), m); return fr
FR = [clean(f) for f in decode()]

CAPS = [(0.30, 2.55, ["Every bid is [live],", "in front of [everyone.]"]), (2.95, 4.20, ["No [secret deals.]"]),
        (4.30, 6.20, ["No special prices", "for [friends.]"]), (6.40, 7.95, ["[Same chance] for all."])]
FEED_AT, FEED_OUT = 0.35, 2.6
FEED = [(0.55, "R", "Rami", "$210"), (1.00, "N", "Nour", "$230"), (1.45, "J", "Jad", "$250")]
B1_IN, B1_X, B1_OUT = 2.75, 3.55, 4.2
B2_IN, B2_X, B2_OUT = 4.3, 5.6, 6.25
AV_AT, ALL_AT = 6.45, 7.15
AV_COL = [(124, 92, 255), (47, 123, 255), (196, 120, 255), (64, 160, 255), (150, 110, 255)]

def avatar(ch, col, d=64):
    im = Image.new("RGBA", (d, d), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((0, 0, d - 1, d - 1), fill=(*col, 255))
    tl = R.text_layer(ch, R.font(int(d * 0.48), 700), WHITE); im.alpha_composite(tl, ((d - tl.width) // 2, (d - tl.height) // 2 - 2)); return im

def eye(sz=34):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((1, sz * 0.22, sz - 2, sz * 0.78), outline=(220, 224, 240, 255), width=3); d.ellipse((sz * 0.36, sz * 0.36, sz * 0.64, sz * 0.64), fill=(220, 224, 240, 255)); return im
EYE = eye()

def row(ini, name, amt, hot, col):
    w, h = 700, 78; im = M.glass(w, h, 22, fill=(36, 30, 70, 235) if hot else (24, 24, 36, 215), border=(*VIOLET, 220) if hot else (255, 255, 255, 30))
    im.alpha_composite(avatar(ini, col, 52), (16, 13))
    im.alpha_composite(R.text_layer(name, R.font(34, 600), WHITE if hot else (190, 194, 210)), (86, 18))
    a = R.text_layer(amt, R.font(38, 700), WHITE if hot else (190, 194, 210)); im.alpha_composite(a, (w - 24 - a.width, 15)); return im

def feed(t):
    shown = [f for f in FEED if t >= f[0]]
    e = R.ease_out((t - shown[-1][0]) / 0.25) if shown else 0
    w = 760; h = int(72 + (88 * (len(shown) - 1 + e) + 78 if shown else 0) + 18)
    im = M.glass(w, h, 30, fill=(14, 14, 24, 215), border=(*VIOLET, 140)); d = ImageDraw.Draw(im)
    pa = int(160 + 95 * (0.5 + 0.5 * np.sin(t * 7))); d.ellipse((26, 26, 46, 46), fill=(*VIOLET, pa))
    im.alpha_composite(R.text_layer("LIVE BIDS", R.font(26, mono=True), WHITE, tracking=4), (58, 20))
    k = R.clamp((t - 1.55) / 0.85); n = int(312 + (2140 - 312) * k ** 1.4)
    cnt = R.text_layer(f"{n:,} watching", R.font(28, 600), WHITE); im.alpha_composite(cnt, (w - 26 - cnt.width, 20)); im.alpha_composite(EYE, (w - 36 - cnt.width - EYE.width, 18))
    for i, (at, ini, name, amt) in enumerate(reversed(shown)):        # newest on top
        kk = R.ease_out((t - at) / 0.25); y = 72 + i * 88 - (1 - kk) * 30 if i == 0 else 72 + i * 88 - 88 * (1 - R.ease_out((t - shown[-1][0]) / 0.25))
        r = row(ini, name, amt, i == 0, AV_COL["RNJ".index(ini)])
        if i == 0 and kk < 1: a = r.getchannel("A").point(lambda v: int(v * kk)); r.putalpha(a)
        if 0 <= y <= h - r.height: im.alpha_composite(r, (30, int(y)))
    return im

def bubble(head, text, lock=False):
    hd = R.text_layer(head, R.font(24, mono=True), (180, 184, 200), tracking=3); tx = R.text_layer(text, R.font(44, 600), WHITE)
    w, h = max(hd.width + (40 if lock else 0), tx.width) + 70, hd.height + tx.height + 54
    im = Image.new("RGBA", (w, h + 26), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=(52, 54, 68, 240)); d.polygon([(46, h - 2), (96, h - 2), (40, h + 24)], fill=(52, 54, 68, 240))
    x = 35
    if lock:
        d.rounded_rectangle((x, 24, x + 22, 42), radius=4, fill=(180, 184, 200, 255)); d.arc((x + 3, 12, x + 19, 32), 180, 360, fill=(180, 184, 200, 255), width=4); x += 36
    im.alpha_composite(hd, (x, 20)); im.alpha_composite(tx, (35, 26 + hd.height)); return im
BUB1 = bubble("PRIVATE MESSAGE", "psst… DM me. Better deal.", lock=True)
BUB2 = bubble("SELLER", "For you habibi… special price.")

def x_stamp(d=150):
    im = Image.new("RGBA", (d, d), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    g.ellipse((6, 6, d - 7, d - 7), fill=(20, 14, 40, 230), outline=(*VIOLET, 255), width=10)
    p = d * 0.32; g.line([(p, p), (d - p, d - p)], fill=(*VIOLET, 255), width=14); g.line([(d - p, p), (p, d - p)], fill=(*VIOLET, 255), width=14); return im
XS = x_stamp()

def show_bubble(im, t, bub, t_in, t_x, t_out, cy=400):
    if not (t_in <= t < t_out + 0.05): return
    k = (t - t_in) / 0.3; a = R.clamp(k * 3) * (1 - R.clamp((t - (t_out - 0.25)) / 0.25))
    shake = 14 * np.sin((t - t_x) * 60) * max(0, 1 - (t - t_x) / 0.25) if t >= t_x else 0
    R.paste_center(im, bub, W / 2 + shake, cy + (1 - R.ease_out(k)) * 30, a * (0.45 if t >= t_x + 0.1 else 1.0), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    if t >= t_x:
        s = (t - t_x) / 0.3; R.paste_center(im, XS, W / 2 + bub.width / 2 - 40, cy - bub.height / 2 + 30, R.clamp(s * 3) * (1 - R.clamp((t - (t_out - 0.25)) / 0.25)), 1.7 - 0.7 * R.stamp(s) if s < 1 else 1.0)

AVS = [avatar(c, col, 120) for c, col in zip("RNJMK", AV_COL)]
def avatars(im, t):
    clock = 1 - R.clamp((t - AV_AT) / 1.5) * 0.35          # one shared clock ring, the same on every bidder
    flash = max(0, 1 - (t - ALL_AT) / 0.4) if t >= ALL_AT else 0
    for i, av in enumerate(AVS):
        k = (t - AV_AT - 0.07 * i) / 0.3
        if k <= 0: continue
        cx, cy = W / 2 + (i - 2) * 168, 420; lay = Image.new("RGBA", (156, 156), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.ellipse((4, 4, 151, 151), outline=(60, 60, 84, 255), width=8)
        d.arc((4, 4, 151, 151), -90, -90 + 360 * clock, fill=tuple(int(c + (255 - c) * flash) for c in VIOLET) + (255,), width=8)
        lay.alpha_composite(av, (18, 18)); R.paste_center(im, lay, cx, cy, R.clamp(k * 3) * (1 - R.clamp((t - 7.75) / 0.2)), 0.7 + 0.3 * R.stamp(k) if k < 1 else 1.0 + 0.06 * flash)
    if t >= ALL_AT: sparkle_burst(im, t, ALL_AT, W / 2, 420, ((-420, -90, 34), (410, -100, 26), (-330, 100, 18), (360, 95, 34), (0, -120, 26)))

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Same clock.", "Same chance."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, True, 640, 150); M.scrim(im, False, 650, 150)
    if FEED_AT <= t < FEED_OUT + 0.3:
        k = (t - FEED_AT) / 0.35; a = R.clamp(k * 3) * (1 - R.clamp((t - FEED_OUT) / 0.25))
        fd = feed(t); R.paste_center(im, fd, W / 2, 215 + fd.height / 2 + (1 - R.ease_out(k)) * -40, a)
    show_bubble(im, t, BUB1, B1_IN, B1_X, B1_OUT); show_bubble(im, t, BUB2, B2_IN, B2_X, B2_OUT)
    if t >= AV_AT: avatars(im, t)
    draw_caps(im, t, CAPS)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((123.5, .35), (185, .25), (246.9, .2), (370, .08)))
        mx.whoosh(FEED_AT - 0.05, 0.3, 0.15)
        for i, (at, *_ ) in enumerate(FEED): mx.ping(at, 1046.5 * 2 ** (i * 2 / 12), 0.13)
        for i in range(8): mx.ping(1.6 + i * 0.1, 2093 + 40 * i, 0.03)                    # watchers ticking up
        for t_in, t_x in ((B1_IN, B1_X), (B2_IN, B2_X)):
            mx.ping(t_in, 880, 0.1); mx.ping(t_in + 0.08, 1174.7, 0.1)                       # message received
            mx.thud(t_x, 0.5); y = mx.tt(0.2); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 3) * np.exp(-y * 16), t_x, 0.25)
        for i in range(5): mx.ping(AV_AT + 0.07 * i, 784 * 2 ** (i * 2 / 12), 0.09)
        mx.shimmer(ALL_AT, 1318.5, 0.12)
        mx.write("s2e5_audio.wav")
    render(frame, TOTAL, "s2e5_audio.wav", OUT)
