"""Season 2 Ep. 3 'The rush': a live card counting down from 00:10, 'You're winning', OUTBID by Karim (shake + amber),
heartbeat rings on his hand on his heart, BID $520 tapped, 00:00 -> YOU WON. End card 'Ten seconds. Your move.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
VIOLET, AMBER = (167, 139, 250), (255, 184, 92)

def clean(fr):
    m = Image.new("L", (200, 90), 0); ImageDraw.Draw(m).rectangle((0, 0, 160, 62), fill=255); m = m.filter(ImageFilter.GaussianBlur(10))
    fr.paste(fr.crop((250, 0, 450, 90)), (0, 0), m); return fr
FR = [clean(f) for f in decode()]

CAPS = [(0.05, 1.95, ["[Ten seconds] left.", "You're winning."]), (2.30, 4.45, ["Someone bids.", "Your [heart jumps]…"]),
        (4.50, 5.95, ["…and you [bid again.]"]), (6.20, 7.80, ["Nothing else", "[feels like that.]"])]
CARD_AT, WIN_AT, OUTBID, BTN_AT, TAP_AT, WON = 0.1, 1.25, 2.4, 4.7, 4.98, 6.9
BEATS = [3.45, 3.68, 4.12, 4.35]
HEART = (500, 1430)
CARD_Y = 395

def secs_left(t):
    return max(0, 10 - int(max(0, t - CARD_AT) / 0.68))

def card(t):
    w, h = 820, 250; out = t >= OUTBID and t < TAP_AT
    im = M.glass(w, h, 34, fill=(16, 16, 30, 236), border=(*AMBER, 230) if out else (*VIOLET, 210)); d = ImageDraw.Draw(im)
    pa = int(160 + 95 * (0.5 + 0.5 * np.sin(t * 7))); d.ellipse((30, 30, 50, 50), fill=(*VIOLET, pa))
    im.alpha_composite(R.text_layer("LIVE  ·  VINTAGE WATCH", R.font(26, mono=True), WHITE, tracking=3), (62, 24))
    s = secs_left(t); hot = s <= 3
    tl = R.text_layer(f"00:{s:02d}", R.font(104, 700, mono=True), AMBER if hot else WHITE)
    tick = max(0, 1 - ((t - CARD_AT) % 0.68) / 0.15) if t < WON else 0
    if tick > 0.01: tl = tl.resize((int(tl.width * (1 + 0.06 * tick)), int(tl.height * (1 + 0.06 * tick))), Image.LANCZOS)
    im.alpha_composite(tl, (34, 62))
    price = "$520" if t >= TAP_AT + 0.05 else ("$500" if t >= OUTBID else "$480")
    p = R.text_layer(price, R.font(76, 700), WHITE); im.alpha_composite(p, (w - 36 - p.width, 74))
    lab = R.text_layer("current bid", R.font(26, 500), (190, 195, 215)); im.alpha_composite(lab, (w - 36 - lab.width, 64 + p.height + 6))
    if t >= WIN_AT and not out and t < WON:
        st = R.text_layer("You're winning" + ("  ·  your bid" if t >= TAP_AT else ""), R.font(32, 700), VIOLET)
    elif out:
        st = R.text_layer("Outbid  ·  Karim bid $500", R.font(32, 700), AMBER)
    else:
        st = None
    if st is not None: im.alpha_composite(st, (36, h - 30 - st.height))
    return im

def bid_btn():
    tl = R.text_layer("BID  $520", R.font(40, 700), WHITE); w, h = tl.width + 70, tl.height + 30
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m); im.alpha_composite(tl, (35, 15)); return im
BTN = bid_btn()

def won_pill():
    a = R.text_layer("YOU WON  ·  $520", R.font(68, 700), WHITE); b = R.text_layer("with 0 seconds left", R.font(34, 500), (235, 238, 255))
    w, h = max(a.width, b.width) + 100, a.height + b.height + 46
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=38, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(a, ((w - a.width) // 2, 18)); im.alpha_composite(b, ((w - b.width) // 2, 24 + a.height)); return im
WON_P = won_pill()

def ring(im, cx, cy, rad, a, col, width=6):
    if a <= 0.01: return
    lay = Image.new("RGBA", (int(rad * 2 + 20), int(rad * 2 + 20)), (0, 0, 0, 0)); c = lay.width / 2
    ImageDraw.Draw(lay).ellipse((c - rad, c - rad, c + rad, c + rad), outline=(*col, int(255 * a)), width=width); R.paste_center(im, lay, cx, cy)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Ten seconds.", "Your move."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, True, 660, 170); M.scrim(im, False, 420, 100)
    if CARD_AT <= t < WON + 0.25:
        k = (t - CARD_AT) / 0.35; a = R.clamp(k * 3) * (1 - R.clamp((t - WON) / 0.2))
        shake = 16 * np.sin((t - OUTBID) * 70) * max(0, 1 - (t - OUTBID) / 0.35) if t >= OUTBID else 0
        R.paste_center(im, card(t), W / 2 + shake, CARD_Y + (1 - R.ease_out(k)) * -40, a)
        if OUTBID <= t < OUTBID + 0.5: ring(im, W / 2, CARD_Y, 300 + 200 * R.ease_out((t - OUTBID) / 0.5), (1 - (t - OUTBID) / 0.5) * 0.7, AMBER, 5)
        if BTN_AT <= t < TAP_AT + 0.4:
            s = (t - BTN_AT) / 0.25; press = 0.9 if TAP_AT <= t < TAP_AT + 0.1 else 1.0
            R.paste_center(im, BTN, W / 2 + 240, CARD_Y + 88, R.clamp(s * 3) * (1 - R.clamp((t - TAP_AT - 0.2) / 0.2)), (0.8 + 0.2 * R.stamp(s) if s < 1 else 1.0) * press)
            if t >= TAP_AT: ring(im, W / 2 + 240, CARD_Y + 88, 40 + 150 * R.ease_out((t - TAP_AT) / 0.4), 1 - R.clamp((t - TAP_AT) / 0.4), VIOLET, 5)
        if t >= TAP_AT: sparkle_burst(im, t, TAP_AT + 0.05, W / 2 + 200, CARD_Y - 10, ((-150, -80, 26), (130, -90, 18), (160, 60, 26)))
    for b in BEATS:                      # heartbeat at his hand on his heart
        k = (t - b) / 0.45
        if 0 <= k < 1: ring(im, *HEART, 50 + 230 * R.ease_out(k), (1 - k) * 0.85, (232, 120, 200), 7)
    if t >= WON:
        s = (t - WON) / 0.35; R.paste_center(im, WON_P, W / 2, CARD_Y, R.clamp(s * 3), 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, WON, W / 2, CARD_Y, ((-380, -50, 34), (370, -70, 26), (-320, 60, 18), (350, 55, 34)))
    draw_caps(im, t, CAPS, y=170, size=62)
    if WON <= t < WON + 0.08: im = M.flash(im, 0.3)
    if OUTBID <= t < OUTBID + 0.06: im = M.flash(im, 0.15, (255, 214, 160))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((123.5, .35), (185, .25), (246.9, .2), (370, .08)))
        for k in range(11):                                                       # countdown ticks, higher at the end
            at = CARD_AT + k * 0.68
            if at < WON: y = mx.tt(0.04); mx.fadd(np.sin(2 * np.pi * (2400 if k < 7 else 3200) * y) * np.exp(-y * 120), at, 0.22 if k < 7 else 0.32)
        mx.ping(WIN_AT, 1318.5, 0.12)
        y = mx.tt(0.5); mx.fadd(np.sign(np.sin(2 * np.pi * 440 * y)) * np.exp(-y * 9) * 0.5, OUTBID, 0.14); mx.thud(OUTBID, 0.4)   # outbid alarm
        for b in BEATS: mx.thud(b, 0.55)                                          # heartbeat
        mx.ping(BTN_AT, 1046.5, 0.1); y = mx.tt(0.05); mx.fadd(np.sin(2 * np.pi * 2200 * y) * np.exp(-y * 120), TAP_AT, 0.35)
        mx.ping(TAP_AT + 0.05, 1568, 0.12)
        mx.thud(WON, 0.6); mx.shimmer(WON + 0.02, 1318.5, 0.13)
        mx.write("s2e3_audio.wav")
    render(frame, TOTAL, "s2e3_audio.wav", OUT)
