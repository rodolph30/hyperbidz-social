"""Season 2 Ep. 4 'Just bid': 'Is it still available?' bubbles flood in and get blown away by his raised palm,
a 'typing…' bubble with the wait clock racing to 26h, then the item LIVE ('AVAILABLE NOW'), a BID button tapped
as he points. End card 'No waiting. Just bid.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
FR = decode()
VIOLET = (167, 139, 250)
CAPS = [(0.45, 2.10, ["No [“is it still available?”]"]), (2.55, 4.25, ["No waiting for [replies.]"]),
        (4.40, 6.35, ["If it's [live],", "it's [available.]"]), (6.60, 7.80, ["You just [bid.]"])]
BUBS = [(0.50, "KARIM", 290, 225), (0.78, "UNKNOWN", 790, 300), (1.03, "MAYA", 290, 405), (1.28, "TONY", 790, 480)]
PALM, SWEEP = 1.25, 2.05
PALM_XY = (175, 1090)
WAIT_IN, WAIT_OUT = 2.55, 4.25
CARD_AT, AVAIL_AT, BTN_AT, TAP_AT = 4.45, 5.55, 6.70, 7.10
CARD_Y = 350

def bubble(head, text, w_min=0):
    hd = R.text_layer(head, R.font(22, mono=True), (180, 184, 200), tracking=3); tx = R.text_layer(text, R.font(38, 600), WHITE)
    w, h = max(hd.width, tx.width, w_min) + 64, hd.height + tx.height + 48
    im = Image.new("RGBA", (w, h + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=32, fill=(52, 54, 68, 242)); d.polygon([(40, h - 2), (88, h - 2), (34, h + 22)], fill=(52, 54, 68, 242))
    im.alpha_composite(hd, (32, 18)); im.alpha_composite(tx, (32, 22 + hd.height)); return im
BUB_IMG = {name: bubble(name, "Is it still available?") for _, name, _, _ in BUBS}

def typing_bubble(t):
    w, h = 220, 92; im = Image.new("RGBA", (w, h + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=40, fill=(52, 54, 68, 242)); d.polygon([(40, h - 2), (88, h - 2), (34, h + 22)], fill=(52, 54, 68, 242))
    for i in range(3):
        b = 0.5 + 0.5 * np.sin(t * 9 - i * 0.9); r = 13; cx, cy = 62 + i * 48, h / 2 - 6 * b
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(200, 204, 220, int(120 + 135 * b)))
    return im

def wait_chip(mins):
    tl = R.text_layer(f"waiting for a reply  {mins // 60}h {mins % 60:02d}m", R.font(32, mono=True), WHITE)
    w, h = tl.width + 96, tl.height + 30; im = M.glass(w, h, h // 2, fill=(20, 20, 32, 232), border=(255, 255, 255, 50)); d = ImageDraw.Draw(im)
    cx, cy, r = 40, h // 2, 15; d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(220, 224, 240, 255), width=3)
    a = mins / 60 * 2 * np.pi; d.line([(cx, cy), (cx + 10 * np.sin(a), cy - 10 * np.cos(a))], fill=(220, 224, 240, 255), width=3)
    a2 = mins / 720 * 2 * np.pi; d.line([(cx, cy), (cx + 6 * np.sin(a2), cy - 6 * np.cos(a2))], fill=(220, 224, 240, 255), width=4)
    im.alpha_composite(tl, (72, 15)); return im

CAM = Image.open("/home/claude/ep2/camera_hq.png").convert("RGB").resize((250, 250), Image.LANCZOS)
CAM_M = Image.new("L", (250, 250), 0); ImageDraw.Draw(CAM_M).rounded_rectangle((0, 0, 249, 249), radius=26, fill=255)

def card(t):
    w, h = 880, 290; im = M.glass(w, h, 34, fill=(16, 16, 30, 236), border=(*VIOLET, 210)); d = ImageDraw.Draw(im)
    im.paste(CAM, (20, 20), CAM_M)
    secs = max(0, 45 - int((t - CARD_AT) * 1.6)); pa = int(160 + 95 * (0.5 + 0.5 * np.sin(t * 7)))
    d.ellipse((300, 34, 320, 54), fill=(*VIOLET, pa))
    im.alpha_composite(R.text_layer(f"LIVE  ·  00:{secs:02d}", R.font(26, mono=True), WHITE, tracking=3), (332, 27))
    im.alpha_composite(R.text_layer("Vintage camera", R.font(40, 600), (225, 228, 240)), (300, 70))
    won = t >= TAP_AT + 0.05
    v = R.text_layer("$150" if won else "$140", R.font(84, 700), WHITE)
    bump = 1 + 0.15 * max(0, 1 - (t - TAP_AT - 0.05) / 0.2) if won else 1.0
    if bump > 1.001: v = v.resize((int(v.width * bump), int(v.height * bump)), Image.LANCZOS)
    im.alpha_composite(v, (300, 120))
    im.alpha_composite(R.text_layer("you · highest bid" if won else "current bid", R.font(28, 600 if won else 500), (*VIOLET,) if won else (190, 195, 215)), (302, 226))
    return im

def bid_btn(press=0.0):
    tl = R.text_layer("BID  $150", R.font(44, 700), WHITE); w, h = tl.width + 80, tl.height + 36
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m); im.alpha_composite(tl, (40, 18))
    if press > 0: im = Image.blend(im, Image.new("RGBA", im.size, (255, 255, 255, 0)), 0) if False else im
    return im
BTN = bid_btn()

def avail_chip():
    tl = R.text_layer("AVAILABLE · RIGHT NOW", R.font(30, mono=True), WHITE, tracking=3); w, h = tl.width + 64, tl.height + 28
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m); im.alpha_composite(tl, (32, 14)); return im
AVAIL = avail_chip()

def ring(im, cx, cy, rad, a, width=6):
    if a <= 0.01: return
    lay = Image.new("RGBA", (int(rad * 2 + 20), int(rad * 2 + 20)), (0, 0, 0, 0)); c = lay.width / 2
    ImageDraw.Draw(lay).ellipse((c - rad, c - rad, c + rad, c + rad), outline=(*VIOLET, int(255 * a)), width=width)
    R.paste_center(im, lay, cx, cy)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["No waiting.", "Just bid."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, True, 620, 150); M.scrim(im, False, 600, 140)
    # 1. the flood, frozen by his palm, then blown away
    for i, (at, name, x, y) in enumerate(BUBS):
        if not (at <= t < SWEEP + 0.5): continue
        k = (t - at) / 0.28; a = R.clamp(k * 3)
        shake = 5 * np.sin(t * 50 + i) if PALM <= t < SWEEP else 0
        if t >= SWEEP:
            s = R.clamp((t - SWEEP - 0.04 * i) / 0.4); x += s ** 2 * 1100; a *= (1 - s)
        R.paste_center(im, BUB_IMG[name], x + shake, y, a, 0.8 + 0.2 * R.stamp(k) if k < 1 else 1.0)
    if PALM <= t < PALM + 0.7:     # stop ripple from his palm
        for j in range(2):
            k = R.clamp((t - PALM - 0.12 * j) / 0.55); ring(im, *PALM_XY, 60 + 340 * R.ease_out(k), (1 - k) * 0.9)
    # 2. waiting…
    if WAIT_IN <= t < WAIT_OUT + 0.3:
        k = (t - WAIT_IN) / 0.3; a = R.clamp(k * 3) * (1 - R.clamp((t - WAIT_OUT) / 0.25))
        R.paste_center(im, typing_bubble(t), W / 2, 270 + (1 - R.ease_out(k)) * 30, a, 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
        mins = int(1600 * R.clamp((t - 2.75) / 1.35) ** 1.6)
        wc = wait_chip(mins); R.paste_center(im, wc, W / 2, 420, R.clamp((t - 2.75) / 0.2) * a)
    # 3. live = available, then bid
    if t >= CARD_AT:
        k = (t - CARD_AT) / 0.4; x = W / 2 + ((1 - R.stamp(k)) * 700 if k < 1 else 0)
        R.paste_center(im, card(t), x, CARD_Y, R.clamp(k * 3))
        if t >= AVAIL_AT:
            s = (t - AVAIL_AT) / 0.32; R.paste_center(im, AVAIL, W / 2 + 210, CARD_Y - 168, R.clamp(s * 3), 1.5 - 0.5 * R.stamp(s) if s < 1 else 1.0)
            sparkle_burst(im, t, AVAIL_AT, W / 2 + 210, CARD_Y - 168, ((-260, -20, 26), (250, -30, 18), (230, 30, 26)))
        if t >= BTN_AT:
            s = (t - BTN_AT) / 0.3; press = 0.9 if TAP_AT <= t < TAP_AT + 0.1 else 1.0
            bx, by = W / 2 + 300, CARD_Y + 90
            R.paste_center(im, BTN, bx, by, R.clamp(s * 3) * (0.0 if t >= TAP_AT + 0.35 else 1.0) + (R.clamp(1 - (t - TAP_AT - 0.35) / 0.2) if t >= TAP_AT + 0.35 else 0),
                           (0.8 + 0.2 * R.stamp(s) if s < 1 else 1.0) * press)
            if t >= TAP_AT:
                kk = R.clamp((t - TAP_AT) / 0.45); ring(im, bx, by, 40 + 160 * R.ease_out(kk), (1 - kk) * 0.9, 5)
                sparkle_burst(im, t, TAP_AT + 0.05, W / 2 - 80, CARD_Y + 10, ((-200, -60, 34), (160, -80, 26), (-150, 70, 18), (200, 60, 34)))
    draw_caps(im, t, CAPS)
    if TAP_AT + 0.05 <= t < TAP_AT + 0.12: im = M.flash(im, 0.22)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((123.5, .35), (185, .25), (246.9, .2), (370, .08)))
        for i, (at, *_ ) in enumerate(BUBS): mx.ping(at, 880 + 60 * (i % 2), 0.1); mx.ping(at + 0.07, 1174.7 + 60 * (i % 2), 0.08)
        mx.whoosh(PALM - 0.05, 0.45, 0.25); mx.thud(PALM, 0.3)
        mx.whoosh(SWEEP, 0.4, 0.3)
        for i in range(12): y = mx.tt(0.03); mx.fadd(np.sin(2 * np.pi * 3000 * y) * np.exp(-y * 150), 2.75 + i * 0.11, 0.12)   # clock racing
        mx.whoosh(CARD_AT - 0.05, 0.35, 0.2); mx.ping(CARD_AT + 0.3, 1318.5, 0.14)
        mx.ping(AVAIL_AT, 1568, 0.14); mx.shimmer(AVAIL_AT + 0.02, 1568, 0.05)
        mx.ping(BTN_AT, 1046.5, 0.1)
        y = mx.tt(0.05); mx.fadd(np.sin(2 * np.pi * 2200 * y) * np.exp(-y * 120), TAP_AT, 0.35)          # tap
        mx.thud(TAP_AT + 0.05, 0.45); mx.shimmer(TAP_AT + 0.07, 1318.5, 0.12)
        mx.write("s2e4_audio.wav")
    render(frame, TOTAL, "s2e4_audio.wav", OUT)
