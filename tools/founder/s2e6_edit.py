"""Season 2 Ep. 6 'First win' (season finale): a polaroid memory 'my first win · $150' floats in, stamped
LAUNCH DAY on 'You will.', a FIRST AUCTIONS · COMING SOON chip, 'Turn on notifications' on 'Be there',
a BID button tapped into a confetti burst on 'and bid.' End card 'Your first win is coming.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
FR = decode()
VIOLET = (167, 139, 250)
CAPS = [(0.05, 1.60, ["Remember your [first win?]"]), (1.75, 2.65, ["[You will.]"]),
        (2.80, 5.20, ["The first HyperBidz", "auctions are [coming.]"]), (5.40, 6.50, ["Be [there]…"]), (6.60, 7.80, ["…and [bid.]"])]
POL_AT, STAMP_AT, SOON_AT, POINT_AT, BELL_AT, BTN_AT, TAP_AT = 0.15, 1.85, 2.85, 3.0, 5.45, 6.62, 6.95
FINGER = (390, 1060)

def polaroid():
    w, h = 300, 370; im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((24, 28, w + 22, h + 26), fill=(0, 0, 0, 120)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    card = Image.new("RGBA", (w, h), (250, 248, 242, 255))
    cam = Image.open("/home/claude/ep2/camera_hq.png").convert("RGB").resize((264, 264), Image.LANCZOS); card.paste(cam, (18, 18))
    tl = R.text_layer("my first win · $150", R.font(28, 600), (40, 40, 48)); card.alpha_composite(tl, ((w - tl.width) // 2, 300))
    im.alpha_composite(card, (20, 20)); return im.rotate(-6, resample=Image.BICUBIC, expand=True)
POL = polaroid()

def date_stamp():
    tl = R.text_layer("LAUNCH DAY", R.font(36, mono=True), WHITE, tracking=4); w, h = tl.width + 44, tl.height + 26
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((2, 2, w - 3, h - 3), radius=10, fill=(124, 92, 255, 240), outline=(255, 255, 255, 230), width=3)
    im.alpha_composite(tl, (22, 12)); return im.rotate(12, resample=Image.BICUBIC, expand=True)
STAMP = date_stamp()

def soon_chip(t):
    a = R.text_layer("FIRST AUCTIONS", R.font(26, mono=True), (205, 210, 235), tracking=4); b = R.text_layer("COMING SOON", R.font(52, 700), WHITE)
    w, h = max(a.width, b.width) + 130, a.height + b.height + 50; im = M.glass(w, h, 30, fill=(16, 16, 30, 232), border=(*VIOLET, 210)); d = ImageDraw.Draw(im)
    cx, cy, r = 54, h // 2, 24; d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(60, 60, 84, 255), width=6)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * ((t * 0.6) % 1), fill=(*VIOLET, 255), width=6)
    im.alpha_composite(a, (100, 18)); im.alpha_composite(b, (100, 22 + a.height)); return im

def bell_chip():
    tl = R.text_layer("Turn on notifications", R.font(40, 700), WHITE); w, h = tl.width + 124, tl.height + 36
    im = M.glass(w, h, h // 2, fill=(20, 18, 40, 235), border=(*VIOLET, 230)); d = ImageDraw.Draw(im); cx, cy = 48, h // 2
    d.pieslice((cx - 18, cy - 20, cx + 18, cy + 16), 180, 360, fill=(255, 255, 255, 255)); d.rectangle((cx - 18, cy - 2, cx + 18, cy + 10), fill=(255, 255, 255, 255))
    d.rectangle((cx - 22, cy + 8, cx + 22, cy + 12), fill=(255, 255, 255, 255)); d.ellipse((cx - 5, cy + 12, cx + 5, cy + 20), fill=(255, 255, 255, 255))
    im.alpha_composite(tl, (84, 18)); return im
BELL = bell_chip()

def bid_btn():
    tl = R.text_layer("BID", R.font(56, 700), WHITE, tracking=4); w, h = tl.width + 150, tl.height + 44
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m); im.alpha_composite(tl, (75, 22)); return im
BTN = bid_btn()

rng = np.random.default_rng(21)
CONF = [dict(vx=rng.uniform(-900, 900), vy=rng.uniform(-1500, -500), c=[(167, 139, 250), (47, 123, 255), (255, 255, 255), (255, 214, 120), (124, 92, 255)][rng.integers(5)],
             s=rng.uniform(10, 20), spin=rng.uniform(-12, 12), ph=rng.uniform(0, 6)) for _ in range(90)]
def confetti(im, t, t0, x0, y0):
    k = t - t0
    if k <= 0 or k > 1.6: return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for p in CONF:
        x = x0 + p["vx"] * k; y = y0 + p["vy"] * k + 1700 * k * k; a = p["ph"] + p["spin"] * k; s = p["s"]
        if not (-20 < x < W + 20 and -20 < y < H + 20): continue
        dx, dy = np.cos(a) * s, np.sin(a) * s * 0.5
        d.polygon([(x - dx, y - dy), (x + dy, y - dx * 0.4), (x + dx, y + dy), (x - dy, y + dx * 0.4)], fill=(*p["c"], int(255 * min(1, (1.6 - k) / 0.4))))
    im.alpha_composite(lay)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Your first win", "is coming."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, True, 640, 150); M.scrim(im, False, 600, 140)
    if POL_AT <= t < 5.4:   # the memory: blur-in, float, stamp, then parks left
        k = (t - POL_AT) / 0.6; a = R.clamp(k * 2) * (1 - R.clamp((t - 5.1) / 0.3))
        p = R.ease_out((t - SOON_AT) / 0.45) if t >= SOON_AT else 0
        s = (0.9 + 0.1 * R.ease_out(k)) * (1 - 0.3 * p); x = W / 2 + (250 - W / 2) * p; y = 360 + 6 * np.sin(t * 2.2) + (1 - R.ease_out(k)) * 40
        pol = POL.copy()
        if t >= STAMP_AT:
            ks = (t - STAMP_AT) / 0.25; st = STAMP if ks >= 1 else STAMP.resize((int(STAMP.width * (1.8 - 0.8 * R.stamp(ks))), int(STAMP.height * (1.8 - 0.8 * R.stamp(ks)))), Image.LANCZOS)
            if R.clamp(ks * 3) > 0.02:
                stc = st.copy(); stc.putalpha(stc.getchannel("A").point(lambda v: int(v * R.clamp(ks * 3))))
                pol.alpha_composite(stc, (max(0, pol.width - stc.width - 10), max(0, 250 - stc.height // 2)))
        if k < 1: pol = pol.filter(ImageFilter.GaussianBlur(10 * (1 - R.ease_out(k))))
        R.paste_center(im, pol, x, y, a, s)
        if t >= STAMP_AT: sparkle_burst(im, t, STAMP_AT, x + 90, y + 60, ((-80, -60, 26), (90, -40, 18), (70, 60, 26)))
    if SOON_AT <= t < 5.4:
        k = (t - SOON_AT) / 0.38; a = R.clamp(k * 3) * (1 - R.clamp((t - 5.1) / 0.3))
        sc = soon_chip(t); R.paste_center(im, sc, 720 + (1 - R.stamp(k)) * 300 if k < 1 else 720, 350, a)
    if POINT_AT <= t < POINT_AT + 1.0: sparkle_burst(im, t, POINT_AT, *FINGER, ((-50, -50, 26), (60, -30, 18), (30, 60, 14)))
    if t >= BELL_AT:
        k = (t - BELL_AT) / 0.3; R.paste_center(im, BELL, W / 2, 300, R.clamp(k * 3), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0 + 0.025 * np.sin((t - BELL_AT) * 10))
    if t >= BTN_AT:
        k = (t - BTN_AT) / 0.28; press = 0.9 if TAP_AT <= t < TAP_AT + 0.1 else (1.06 if TAP_AT + 0.1 <= t < TAP_AT + 0.2 else 1.0)
        R.paste_center(im, BTN, W / 2, 460, R.clamp(k * 3), (0.8 + 0.2 * R.stamp(k) if k < 1 else 1.0) * press)
        if t >= TAP_AT:
            kk = R.clamp((t - TAP_AT) / 0.5); lay = Image.new("RGBA", (500, 500), (0, 0, 0, 0)); rr = 60 + 180 * R.ease_out(kk)
            ImageDraw.Draw(lay).ellipse((250 - rr, 250 - rr, 250 + rr, 250 + rr), outline=(*VIOLET, int(230 * (1 - kk))), width=6); R.paste_center(im, lay, W / 2, 460)
            confetti(im, t, TAP_AT, W / 2, 460)
    draw_caps(im, t, CAPS)
    if TAP_AT <= t < TAP_AT + 0.08: im = M.flash(im, 0.25)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((123.5, .35), (185, .25), (246.9, .2), (370, .08)))
        mx.shimmer(POL_AT, 1046.5, 0.08); mx.shimmer(POL_AT + 0.3, 1318.5, 0.05)                   # memory shimmer
        mx.thud(STAMP_AT, 0.4); mx.ping(STAMP_AT + 0.02, 1568, 0.1)
        mx.whoosh(SOON_AT - 0.05, 0.4, 0.2); mx.ping(SOON_AT + 0.3, 1318.5, 0.12)
        mx.ping(POINT_AT, 2093, 0.06)
        mx.ping(BELL_AT, 1760, 0.14); mx.ping(BELL_AT + 0.12, 2349, 0.1)
        mx.ping(BTN_AT, 1046.5, 0.1)
        y = mx.tt(0.05); mx.fadd(np.sin(2 * np.pi * 2200 * y) * np.exp(-y * 120), TAP_AT, 0.35)
        mx.thud(TAP_AT + 0.02, 0.55); mx.shimmer(TAP_AT + 0.03, 1318.5, 0.14)
        for i in range(10): mx.ping(TAP_AT + 0.08 + i * 0.05, 1568 + 180 * (i % 4), 0.05)          # confetti sparkle
        mx.write("s2e6_audio.wav")
    render(frame, TOTAL, "s2e6_audio.wav", OUT)
