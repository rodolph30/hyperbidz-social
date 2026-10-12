import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
W, H = 1080, 1920
WHITE, BG, BLUE, FEED, NAVY = R.WHITE, R.BG, R.BLUE, R.FEED, R.NAVY
# ---------- helpers ----------
def grad(w, h): return R.diag_gradient(w, h, BLUE, FEED).convert("RGBA")

def glass(w, h, r, fill=(20, 22, 32, 222), border=(255, 255, 255, 34)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=fill, outline=border, width=2)
    return im

def bid_row(name, amount, mine):
    hl = R.text_layer(name, R.font(36, 500), WHITE if mine else (205, 208, 222))
    am = R.text_layer(amount, R.font(42, 700), WHITE)
    w, h = 24 + 64 + 22 + hl.width + 26 + am.width + 40, 100
    if mine:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=50, fill=255)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(grad(w, h), (0, 0), m)
    else:
        im = glass(w, h, 50, fill=(11, 14, 20, 185))
    d = ImageDraw.Draw(im); d.ellipse((24, 18, 88, 82), fill=(255, 255, 255, 255) if mine else (124, 92, 255, 255))
    ini = R.text_layer(name[0], R.font(34, 700), NAVY if mine else WHITE)
    im.alpha_composite(ini, (56 - ini.width // 2, 50 - ini.height // 2 - 2))
    im.alpha_composite(hl, (110, (h - hl.height) // 2)); im.alpha_composite(am, (110 + hl.width + 26, (h - am.height) // 2 - 1))
    return im

def chip(text, fill, border=None, size=38, tracking=5):
    tl = R.text_layer(text, R.font(size, mono=True), WHITE, tracking=tracking)
    w, h = tl.width + 76, tl.height + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=fill, outline=border, width=3 if border else 0)
    im.alpha_composite(tl, (38, 20)); return im

def live_chip(t):
    tl = R.text_layer("LIVE  ·  LAST MANOUCHE", R.font(28, mono=True), WHITE, tracking=2)
    w, h = tl.width + 86, tl.height + 30
    im = glass(w, h, h // 2, fill=(11, 14, 20, 175)); a = int(160 + 95 * (0.5 + 0.5 * np.sin(t * 6)))
    ImageDraw.Draw(im).ellipse((26, h // 2 - 10, 46, h // 2 + 10), fill=(167, 139, 250, a)); im.alpha_composite(tl, (60, 15)); return im

def stamp_text(text, size):
    layer = R.text_layer(text, R.font(size, 700), WHITE)
    a = layer.getchannel("A").point(lambda v: int(v * 0.6))
    sh = Image.merge("RGBA", (*[Image.new("L", layer.size, 0)] * 3, a)).filter(ImageFilter.GaussianBlur(8))
    out = Image.new("RGBA", (layer.width + 30, layer.height + 30), (0, 0, 0, 0)); out.alpha_composite(sh, (15, 20)); out.alpha_composite(layer, (15, 15)); return out

def scrim(im, top=True, hgt=520, a0=140):
    s = Image.new("RGBA", (W, hgt), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    for y in range(hgt): d.line([(0, y), (W, y)], fill=(11, 14, 20, int(a0 * (1 - y / hgt) ** 1.6)))
    im.alpha_composite(s if top else s.transpose(Image.FLIP_TOP_BOTTOM), (0, 0 if top else H - hgt))

def cover(img):
    s = max(W / img.width, H / img.height); im = img.resize((int(img.width * s + 0.5), int(img.height * s + 0.5)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2; return im.crop((l, t, l + W, t + H))

def zoom(img, z, fx, fy, dx=0, dy=0):
    """z>=1 zoom keeping normalized focus point (fx,fy) fixed; dx,dy = shake in px."""
    cx, cy = fx * W, fy * H; w, h = W / z, H / z
    l = min(max(cx - cx / z - dx / z, 0), W - w); t = min(max(cy - cy / z - dy / z, 0), H - h)
    return img.crop((int(l), int(t), int(l + w), int(t + h))).resize((W, H), Image.BICUBIC)

def blur_box(im, x0, y0, x1, y1, r=18):
    bx = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)); reg = im.crop(bx).filter(ImageFilter.GaussianBlur(r)); im.paste(reg, bx[:2]); return im

def flash(im, k, color=(235, 238, 255)):
    return im if k <= 0 else Image.blend(im, Image.new(im.mode, im.size, color + ((255,) if im.mode == "RGBA" else ())), min(1, k))

