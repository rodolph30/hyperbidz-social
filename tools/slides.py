"""Render on-brand HyperBidz carousel slides (1080x1350 JPEG) from a JSON spec.

Usage: python3 tools/slides.py spec.json out_dir
spec.json = {"name": "post3", "slides": [
  {"tone": "gradient" | "dark", "kicker": "MONO LABEL", "headline": "Big line.",
   "accent": "Optional second line in violet.", "sub": "Optional smaller line.",
   "big": "00:03", "chip": "HAMMER FALLING", "cta": "Follow @hyperbidz", "footer": "SWIPE →"}, ...]}
Every slide gets the Z mark + HYPERBIDZ wordmark, an n / N counter and the countdown footer
(00:0N timer and a draining bar), matching the design system.
"""
import json, os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1080, 1350
BG = (11, 14, 20); WHITE = (255, 255, 255); MUTED = (176, 178, 181)
ACCENT = (167, 139, 250); FEED = (124, 92, 255); BLUE = (47, 123, 255); NAVY = (42, 21, 128)
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
FONTS = {"SpaceGrotesk-VF.ttf": "ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
         "SpaceMono-Bold.ttf": "ofl/spacemono/SpaceMono-Bold.ttf",
         "SpaceMono-Regular.ttf": "ofl/spacemono/SpaceMono-Regular.ttf"}

def ensure_fonts():
    os.makedirs(FONT_DIR, exist_ok=True)
    for name, src in FONTS.items():
        p = os.path.join(FONT_DIR, name)
        if not os.path.exists(p):
            urllib.request.urlretrieve("https://raw.githubusercontent.com/google/fonts/main/" + src, p)

_fc = {}
def font(size, weight=700, mono=False, regular=False):
    key = (int(size), weight, mono, regular)
    if key not in _fc:
        if mono:
            _fc[key] = ImageFont.truetype(os.path.join(FONT_DIR, "SpaceMono-Regular.ttf" if regular else "SpaceMono-Bold.ttf"), int(size))
        else:
            f = ImageFont.truetype(os.path.join(FONT_DIR, "SpaceGrotesk-VF.ttf"), int(size)); f.set_variation_by_axes([weight]); _fc[key] = f
    return _fc[key]

def mix(a, b, k): return tuple(int(round(x + (y - x) * k)) for x, y in zip(a, b))

def gradient(w, h):
    x = np.linspace(0, 1, w)[None, :]; y = np.linspace(0, 1, h)[:, None]
    k = np.clip((x * w + y * h * 0.55) / (w + h * 0.55), 0, 1)
    arr = np.array(BLUE)[None, None, :] * (1 - k[..., None]) + np.array(FEED)[None, None, :] * k[..., None]
    return Image.fromarray(arr.astype(np.uint8), "RGB")

Z_TOP = [(24.75,16),(84.75,16),(81.94,36),(59.69,54.36),(44.98,41.74),(51.94,36),(21.94,36)]
Z_BOT = [(55,58.23),(48.01,64),(78.01,64),(75.2,84),(15.2,84),(18.01,64),(40.28,45.62)]

def z_mark(size, gradient_fill):
    s = size / 100
    mask = Image.new("L", (size, size), 0); d = ImageDraw.Draw(mask)
    for poly in (Z_TOP, Z_BOT): d.polygon([(x * s, y * s) for x, y in poly], fill=255)
    fill = gradient(size, size) if gradient_fill else Image.new("RGB", (size, size), WHITE)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); im.paste(fill, (0, 0), mask); return im

def tracked(d, xy, text, f, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += f.getlength(ch) + tracking
    return x

def wrap(text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if f.getlength(t) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def fit_headline(text, max_w, max_lines=4, start=150, floor=96):
    size = start
    while size > floor:
        if len(wrap(text, font(size), max_w)) <= max_lines: return size
        size -= 6
    return floor

def slide(s, i, n):
    grad = s.get("tone", "dark") == "gradient"
    im = (gradient(W, H) if grad else Image.new("RGB", (W, H), BG)).convert("RGBA")
    d = ImageDraw.Draw(im)
    L, R = 80, W - 80
    muted = (230, 233, 255) if grad else MUTED
    timer_col = WHITE if grad else ACCENT
    # header: mark + wordmark + counter
    im.alpha_composite(z_mark(52, not grad), (L, 66))
    x = tracked(d, (L + 66, 72), "HYPER", font(30, 500), (215, 225, 255) if grad else (200, 205, 220), 3)
    tracked(d, (x, 72), "BIDZ", font(30, 700), WHITE, 3)
    cnt = f"{i:02d} / {n:02d}"; f_m = font(24, mono=True, regular=True)
    d.text((R, 92), cnt, font=f_m, fill=muted, anchor="rm")
    # content block, vertically centred
    blocks = []
    if s.get("kicker"): blocks.append(("kicker", s["kicker"]))
    if s.get("chip"): blocks.append(("chip", s["chip"]))
    if s.get("big"): blocks.append(("big", s["big"]))
    if s.get("headline"): blocks.append(("headline", s["headline"]))
    if s.get("accent"): blocks.append(("accent", s["accent"]))
    if s.get("sub"): blocks.append(("sub", s["sub"]))
    if s.get("cta"): blocks.append(("cta", s["cta"]))
    hsize = fit_headline(s.get("headline", "") + " " + s.get("accent", ""), R - L, 5)
    rendered, total = [], 0
    for kind, txt in blocks:
        if kind == "kicker": h = 40
        elif kind == "chip": h = 96
        elif kind == "big": h = 240
        elif kind in ("headline", "accent"): h = int(len(wrap(txt, font(hsize), R - L)) * hsize * 0.98)
        elif kind == "sub": h = int(len(wrap(txt, font(50, 500), R - L)) * 50 * 1.18)
        else: h = 116
        rendered.append((kind, txt, h)); total += h + 36
    y = int((H - total) / 2) + 10
    for kind, txt, h in rendered:
        if kind == "kicker":
            tracked(d, (L, y), txt.upper(), font(26, mono=True), (235, 238, 255) if grad else ACCENT, 3.5)
        elif kind == "chip":
            f = font(34, mono=True); tw = sum(f.getlength(c) + 5 for c in txt) + 64
            d.rounded_rectangle((L, y, L + tw, y + 84), radius=42, fill=(49, 38, 98) if not grad else WHITE, outline=ACCENT if not grad else None, width=3)
            tracked(d, (L + 32, y + 20), txt.upper(), f, WHITE if not grad else NAVY, 5)
        elif kind == "big":
            d.text((L - 6, y - 20), txt, font=font(250), fill=ACCENT if not grad else WHITE, features=["tnum"])
        elif kind in ("headline", "accent"):
            col = WHITE if (kind == "headline" or grad) else ACCENT
            for j, ln in enumerate(wrap(txt, font(hsize), R - L)):
                d.text((L, y + j * hsize * 0.98), ln, font=font(hsize), fill=col)
        elif kind == "sub":
            for j, ln in enumerate(wrap(txt, font(50, 500), R - L)):
                d.text((L, y + j * 59), ln, font=font(50, 500), fill=muted)
        elif kind == "cta":
            f = font(44); tw = f.getlength(txt) + 96
            d.rounded_rectangle((L, y, L + tw, y + 104), radius=52, fill=WHITE if grad else None, outline=None if grad else ACCENT, width=0 if grad else 3)
            d.text((L + 48, y + 52), txt, font=f, fill=NAVY if grad else WHITE, anchor="lm")
        y += h + 36
    # footer: countdown timer + draining bar
    secs = max(1, n - i + 1)
    d.text((L, H - 118), f"00:{secs:02d}", font=font(26, mono=True), fill=timer_col)
    d.text((R, H - 118), s.get("footer", "SWIPE →" if i < n else "LIVE AUCTIONS · COMING SOON"), font=f_m, fill=muted, anchor="ra")
    d.rounded_rectangle((L, H - 70, R, H - 64), radius=3, fill=(255, 255, 255, 72) if grad else (35, 38, 47))
    fw = int((R - L) * secs / n)
    if grad: d.rounded_rectangle((L, H - 70, L + fw, H - 64), radius=3, fill=WHITE)
    else:
        bar = Image.fromarray(np.array([[mix(BLUE, FEED, k / max(1, fw - 1)) for k in range(fw)]] * 6, dtype=np.uint8), "RGB")
        im.paste(bar, (L, H - 70))
    return im.convert("RGB")

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    ensure_fonts()
    slides = spec["slides"]
    for i, s in enumerate(slides, 1):
        p = os.path.join(out, f"hyperbidz-{spec.get('name', 'post')}-slide{i}.jpg")
        slide(s, i, len(slides)).save(p, "JPEG", quality=92, optimize=True)
        print(p)
