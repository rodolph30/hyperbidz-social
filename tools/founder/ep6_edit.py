"""Founder Ep. 6 'Don't hear about it later': HyperBidz notification, reminder set near his phone,
YOU'RE #1 IN LINE, missed-auction ghosts, Turn on notifications. End card 'Be first in.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *

OUT = sys.argv[1]; CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.30, 2.40, ["The first HyperBidz", "auction is [coming.]"]), (3.25, 6.20, ["[First in] always gets", "the best deals."]),
        (6.55, 7.80, ["Don't hear about it [later.]"])]
NOTIF_AT, REMIND_AT, FIRST_AT, GHOST_AT, BELL_AT = 0.5, 2.6, 4.3, 6.6, 7.05

def app_icon(size):
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.24), fill=255)
    ic = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ic.paste(M.grad(size, size), (0, 0), m)
    z = R.z_mark(int(size * 0.78)); ic.alpha_composite(z, ((size - z.width) // 2, (size - z.height) // 2)); return ic
ICON = app_icon(84)

def notif(title, body, dim=False):
    w, h = 960, 150; im = M.glass(w, h, 38, fill=(20, 22, 32, 235 if not dim else 170), border=(255, 255, 255, 50 if not dim else 25))
    ic = ICON.copy()
    if dim: ic = Image.blend(Image.new("RGBA", ic.size, (0, 0, 0, 0)), ic.convert("LA").convert("RGBA"), 0.6)
    im.alpha_composite(ic, (30, (h - 84) // 2))
    im.alpha_composite(R.text_layer("HYPERBIDZ", R.font(24, mono=True), (200, 205, 225), tracking=3), (136, 22))
    when = "now" if not dim else body[1]; tl = R.text_layer(when, R.font(26, 500), (176, 178, 181)); im.alpha_composite(tl, (w - 36 - tl.width, 20))
    im.alpha_composite(R.text_layer(title, R.font(40, 700), WHITE if not dim else (150, 152, 160)), (136, 54))
    im.alpha_composite(R.text_layer(body[0] if dim else body, R.font(30, 500), (205, 208, 220) if not dim else (120, 122, 130)), (136, 102))
    return im
N1 = notif("The first live auction is almost here", "Be there when it opens.")
GHOSTS = [notif("Auction ended", ("Vintage watch · sold $640", "launch day"), dim=True), notif("Auction ended", ("Classic scooter · sold $2,900", "launch day"), dim=True)]

def pill_grad(text, size=44, pad=(34, 16)):
    tl = R.text_layer(text, R.font(size, 700), WHITE); w, h = tl.width + pad[0] * 2, tl.height + pad[1] * 2
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m); im.alpha_composite(tl, pad); return im
REMIND = R.pill("Reminder set", R.font(38, 700), NAVY, WHITE, pad=(30, 14))
FIRST = pill_grad("FIRST IN · BEST DEALS", 50)
def bell_chip():
    tl = R.text_layer("Turn on notifications", R.font(38, 700), WHITE); w, h = tl.width + 120, tl.height + 34
    im = M.glass(w, h, h // 2, fill=(20, 18, 40, 235), border=(167, 139, 250, 230)); d = ImageDraw.Draw(im); cx, cy = 46, h // 2
    d.pieslice((cx - 18, cy - 20, cx + 18, cy + 16), 180, 360, fill=(255, 255, 255, 255)); d.rectangle((cx - 18, cy - 2, cx + 18, cy + 10), fill=(255, 255, 255, 255))
    d.rectangle((cx - 22, cy + 8, cx + 22, cy + 12), fill=(255, 255, 255, 255)); d.ellipse((cx - 5, cy + 12, cx + 5, cy + 20), fill=(255, 255, 255, 255))
    im.alpha_composite(tl, (82, 17)); return im
BELL = bell_chip()

def slide(t, at, dur=0.38):
    k = (t - at) / dur
    return 1.0 if k <= 0 else (1 - R.stamp(k) if k < 1 else 0.0)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Be first in."], END)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA"); M.scrim(im, True, 560, 150); M.scrim(im, False, 360, 100)
    if NOTIF_AT <= t < 3.2:
        y = 330 - slide(t, NOTIF_AT) * 330; a = 1 - R.clamp((t - 2.95) / 0.25)
        R.paste_center(im, N1, W / 2, y, a)
    if REMIND_AT <= t < 4.4:  # near the phone in his hand
        k = (t - REMIND_AT) / 0.3; a = R.clamp(k * 3) * (1 - R.clamp((t - 4.15) / 0.25))
        R.paste_center(im, REMIND, 560, 1330, a, 0.8 + 0.2 * R.stamp(k) if k < 1 else 1.0)
        sparkle_burst(im, t, REMIND_AT, 560, 1330, ((-160, -40, 26), (160, -30, 18), (120, 40, 26)))
    if FIRST_AT <= t < 6.45:
        k = (t - FIRST_AT) / 0.32; a = R.clamp(k * 3) * (1 - R.clamp((t - 6.2) / 0.25))
        R.paste_center(im, FIRST, W / 2, 330, a, 1.5 - 0.5 * R.stamp(k) if k < 1 else 1.0)
        sparkle_burst(im, t, FIRST_AT, W / 2, 330, ((-300, -30, 34), (300, -40, 26), (-250, 50, 18), (270, 45, 34)))
    if t >= GHOST_AT:  # what you'd have missed
        for i, g in enumerate(GHOSTS):
            k = (t - GHOST_AT - 0.15 * i) / 0.35
            if k > 0: R.paste_center(im, g, W / 2, 300 + i * 165 + (1 - R.ease_out(min(1, k))) * -40, R.clamp(k * 2) * 0.9)
    if t >= BELL_AT:
        k = (t - BELL_AT) / 0.3; R.paste_center(im, BELL, W / 2, 1420, R.clamp(k * 3), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0 + 0.03 * np.sin((t - BELL_AT) * 10))
    draw_caps(im, t, CAPS, y=150, size=62)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((110, .35), (164.8, .25), (220, .2), (329.6, .08)))
        for f0, dd in ((1318.5, 0), (1975.5, 0.11)):
            y = mx.tt(0.5); mx.fadd((np.sin(2 * np.pi * f0 * y) + 0.3 * np.sin(4 * np.pi * f0 * y)) * np.exp(-y * 9), NOTIF_AT + dd, 0.22)
        mx.ping(REMIND_AT, 1568, 0.16); mx.shimmer(REMIND_AT + 0.02, 2093, 0.04)
        mx.thud(FIRST_AT, 0.45); mx.shimmer(FIRST_AT + 0.02, 1318.5, 0.11)
        y = mx.tt(1.0); mx.fadd(np.sin(2 * np.pi * np.cumsum(520 - 200 * y) / SR) * np.exp(-y * 3) * 0.5, GHOST_AT, 0.12)   # missed
        mx.ping(BELL_AT, 1760, 0.16); mx.ping(BELL_AT + 0.12, 2349, 0.12)
        mx.write("ep6_audio.wav")
    render(frame, TOTAL, "ep6_audio.wav", OUT)
