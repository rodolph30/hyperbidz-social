"""Season 2 Ep. 1 'You decide': SELLER'S PRICE $500 struck out, your max-bid slider to $320 (locked),
then YOU WON $290. End card 'You decide what it's worth.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.10, 2.60, ["On other apps, the", "[seller] decides the price."]), (2.85, 4.40, ["Here… [you do.]"]),
        (4.80, 6.30, ["Bid what it's", "[worth to you.]"]), (6.55, 7.80, ["Not a dollar more."])]
TAG_AT, STRIKE, SLIDER_AT, SLIDE0, SLIDE1, LOCK, WON = 0.6, 3.0, 3.7, 4.85, 6.1, 6.65, 7.15

def seller_tag(strike_k=0.0):
    a = R.text_layer("SELLER'S PRICE", R.font(26, mono=True), (205, 210, 225), tracking=4); b = R.text_layer("$500", R.font(76, 700), WHITE)
    c = R.text_layer("fixed. take it or leave it.", R.font(28, 500), (170, 175, 190))
    w = max(a.width, b.width, c.width) + 80; h = a.height + b.height + c.height + 52
    im = M.glass(w, h, 28, fill=(34, 36, 46, 230), border=(255, 255, 255, 60))
    im.alpha_composite(a, ((w - a.width) // 2, 18)); im.alpha_composite(b, ((w - b.width) // 2, 22 + a.height)); im.alpha_composite(c, ((w - c.width) // 2, 28 + a.height + b.height))
    if strike_k > 0:
        d = ImageDraw.Draw(im); y = 22 + a.height + b.height // 2 + 4; d.line([(24, y), (24 + (w - 48) * strike_k, y - 10 * strike_k)], fill=(167, 139, 250, 255), width=10)
    return im

def slider(v, locked=False, a=1.0):
    w, h = 860, 170; im = M.glass(w, h, 34, fill=(16, 16, 30, 225), border=(167, 139, 250, 200))
    lab = R.text_layer("YOUR MAX BID", R.font(26, mono=True), (215, 220, 245), tracking=4); im.alpha_composite(lab, (36, 22))
    val = R.text_layer(f"${int(v)}", R.font(54, 700), WHITE); im.alpha_composite(val, (w - 36 - val.width - (56 if locked else 0), 12))
    if locked:  # padlock
        d = ImageDraw.Draw(im); x0, y0 = w - 76, 22; d.rounded_rectangle((x0, y0 + 18, x0 + 34, y0 + 46), radius=6, fill=(167, 139, 250, 255)); d.arc((x0 + 5, y0, x0 + 29, y0 + 30), 180, 360, fill=(167, 139, 250, 255), width=5)
    d = ImageDraw.Draw(im); y = 118; x0, x1 = 40, w - 40
    d.rounded_rectangle((x0, y - 6, x1, y + 6), radius=6, fill=(60, 62, 80, 255))
    frac = min(1, v / 500); xf = x0 + (x1 - x0) * frac
    bar = M.grad(int(max(2, xf - x0)), 12); m = Image.new("L", bar.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bar.width - 1, 11), radius=6, fill=255); im.paste(bar, (x0, y - 6), m)
    d.ellipse((xf - 20, y - 20, xf + 20, y + 20), fill=(255, 255, 255, 255), outline=(124, 92, 255, 255), width=4)
    return im

def won_pill():
    a = R.text_layer("YOU WON  ·  $290", R.font(64, 700), WHITE); b = R.text_layer("$30 under your max", R.font(34, 500), (235, 238, 255))
    w, h = max(a.width, b.width) + 90, a.height + b.height + 44
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=36, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(a, ((w - a.width) // 2, 18)); im.alpha_composite(b, ((w - b.width) // 2, 22 + a.height)); return im
WON_P = won_pill()

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["You decide", "what it's worth."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, False, 650, 150); M.scrim(im, True, 360, 100)
    if TAG_AT <= t < WON:
        k = (t - TAG_AT) / 0.3; sk = R.clamp((t - STRIKE) / 0.3) if t >= STRIKE else 0
        a = R.clamp(k * 3) * (0.5 if t >= STRIKE + 0.4 else 1.0) * (1 - R.clamp((t - (WON - 0.2)) / 0.2))
        wob = 6 * np.sin(t * 30) * max(0, 1 - abs(t - 2.1) / 0.3)          # little shake on "decides the price"
        R.paste_center(im, seller_tag(sk), W / 2 + wob, 230, a, 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    if SLIDER_AT <= t < WON + 0.2:
        k = (t - SLIDER_AT) / 0.3; v = 0 if t < SLIDE0 else 320 * R.ease_out((t - SLIDE0) / (SLIDE1 - SLIDE0))
        a = R.clamp(k * 3) * (1 - R.clamp((t - WON) / 0.2))
        R.paste_center(im, slider(v, locked=t >= LOCK), W / 2, 420, a, 0.85 + 0.15 * R.stamp(k) if k < 1 else (1.04 if LOCK <= t < LOCK + 0.12 else 1.0))
    if t >= WON:
        s = (t - WON) / 0.35; R.paste_center(im, WON_P, W / 2, 300, R.clamp(s * 3), 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, WON, W / 2, 300, ((-330, -40, 34), (320, -60, 26), (-260, 60, 18), (300, 50, 34)))
    draw_caps(im, t, CAPS)
    if WON <= t < WON + 0.08: im = M.flash(im, 0.3)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((123.5, .35), (185, .25), (246.9, .2), (370, .08)))
        mx.ping(TAG_AT, 660, 0.12)
        y = mx.tt(0.25); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 3) * np.exp(-y * 14), STRIKE, 0.3)
        mx.ping(SLIDER_AT, 1318.5, 0.14); mx.shimmer(SLIDER_AT + 0.02, 1568, 0.04)
        y = mx.tt(SLIDE1 - SLIDE0); mx.fadd(np.sin(2 * np.pi * np.cumsum(500 + 500 * (y / y[-1])) / SR) * 0.25 * np.minimum(1, y / 0.05) * np.minimum(1, (y[-1] - y) / 0.05), SLIDE0, 0.25)   # rising slide
        y = mx.tt(0.06); mx.fadd(np.sin(2 * np.pi * 1800 * y) * np.exp(-y * 90), LOCK, 0.35)   # lock click
        mx.thud(WON, 0.5); mx.shimmer(WON + 0.02, 1318.5, 0.12)
        mx.write("s2e1_audio.wav")
    render(frame, TOTAL, "s2e1_audio.wav", OUT)
