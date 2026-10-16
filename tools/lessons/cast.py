"""The recurring cast and set for the auction lessons, in the app's colours. Reuse these in every lesson so viewers
recognise them (owner, 16 Oct 2026: keep the same characters every time).

    SAMI  - the seller. Electric-blue bean with a small moustache.
    NOUR  - the buyer. Lilac bean with a hair bun.
    BIDDERS - three smaller beans (violet, green, silver) who raise numbered paddles.
Set: app_stage() (near-black #0B0E14 with a violet-blue spotlight), table(), radio() in slate, tag() white price tag."""
from ex_kit import *

STAGE = (11, 14, 20); BLUE = (47, 123, 255); VIOLET = (124, 92, 255); LILAC = (167, 139, 250); GREEN_APP = (0, 163, 100)
SILVER = (201, 204, 211); SLATE = (34, 40, 58); MUTED_APP = (154, 161, 174); NAVY = (20, 24, 38)
BIDDER_COLS = [VIOLET, GREEN_APP, SILVER]

def app_stage(spot=(540, 980, 560, 760), spot_a=0.22, cone=None, floor_y=None):
    return stage(top=(20, 24, 38), bot=STAGE, spot=spot, spot_col=(96, 92, 255), spot_a=spot_a, cone=cone, floor_y=floor_y,
                 floor_col=(18, 21, 32), cone_col=(150, 150, 255), cone_a=46)

def _pad_top(im, k):
    out = Image.new("RGBA", (im.width, im.height + k), (0, 0, 0, 0)); out.alpha_composite(im, (0, k)); return out

def sami(mood="happy", s=230, look=0.0, talk=0.0, blink=False):
    im = bean(BLUE, mood, s, look, talk, blink); d = ImageDraw.Draw(im); c = (24, 28, 44, 255)
    y = s * 0.655; d.ellipse((s * 0.37, y - s * 0.025, s * 0.5, y + s * 0.04), fill=c); d.ellipse((s * 0.5, y - s * 0.025, s * 0.63, y + s * 0.04), fill=c)
    return _pad_top(im, int(s * 0.14))

def nour(mood="happy", s=230, look=0.0, talk=0.0, blink=False):
    im = _pad_top(bean(LILAC, mood, s, look, talk, blink), int(s * 0.14)); d = ImageDraw.Draw(im); k = s * 0.14
    d.ellipse((s * 0.38, k - s * 0.1, s * 0.62, k + s * 0.14), fill=(108, 84, 196, 255)); d.rounded_rectangle((s * 0.4, k + s * 0.08, s * 0.6, k + s * 0.13), radius=4, fill=(124, 92, 255, 255))
    return im

def bidder(i=0, s=150, mood="happy", talk=0.0):
    return _pad_top(bean(BIDDER_COLS[i % 3], mood, s, 0, talk), int(s * 0.14))

def bidder_with_paddle(i, n, s=150, raise_k=1.0, t=0.0):
    """a bidder holding a numbered paddle up (raise_k 0..1)"""
    b = bidder(i, s); p = paddle(n, [BLUE, VIOLET, GREEN_APP][i % 3], int(s * 0.62))
    out = Image.new("RGBA", (int(s * 1.7), int(s * 2.3)), (0, 0, 0, 0))
    out.alpha_composite(b, (int(s * 0.1), out.height - b.height))
    py = int(out.height - b.height - p.height * 0.55 * raise_k + p.height * 0.35)
    out.alpha_composite(p, (int(s * 0.95), max(0, py))); return out

def table(im, y=1240, x0=110, x1=970):
    d = ImageDraw.Draw(im); d.rectangle((x0, y, x1, y + 44), fill=(52, 60, 84, 255)); d.rectangle((x0, y + 44, x1, y + 58), fill=(36, 42, 60, 255))
    for x in (x0 + 50, x1 - 76): d.rectangle((x, y + 58, x + 26, y + 360), fill=(30, 35, 50, 255))

def radio(s=340):
    im = Image.new("RGBA", (s, int(s * 0.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w, h = s, int(s * 0.9)
    d.arc((w * 0.22, 0, w * 0.78, h * 0.38), 180, 360, fill=(120, 128, 150, 255), width=int(s * 0.04))
    d.rounded_rectangle((0, h * 0.18, w, h), radius=int(s * 0.1), fill=(70, 78, 104, 255))
    d.rounded_rectangle((w * 0.05, h * 0.24, w * 0.95, h * 0.94), radius=int(s * 0.07), fill=(88, 98, 128, 255))
    d.ellipse((w * 0.1, h * 0.33, w * 0.5, h * 0.86), fill=(201, 204, 211, 255))
    for i in range(7): yy = h * 0.4 + i * h * 0.065; d.line([(w * 0.14, yy), (w * 0.46, yy)], fill=(140, 146, 166, 255), width=max(2, s // 90))
    d.rounded_rectangle((w * 0.56, h * 0.34, w * 0.9, h * 0.52), radius=8, fill=(232, 228, 255, 255))
    for i in range(6): xx = w * 0.6 + i * w * 0.05; d.line([(xx, h * 0.37), (xx, h * 0.42)], fill=(80, 70, 140, 255), width=2)
    d.line([(w * 0.7, h * 0.36), (w * 0.72, h * 0.5)], fill=(124, 92, 255, 255), width=3)
    for xx in (0.64, 0.82): d.ellipse((w * xx - w * 0.05, h * 0.62, w * xx + w * 0.05, h * 0.74), fill=(36, 42, 60, 255))
    return im

def tag(text, w=240, h=112):
    return price_tag(text, w, h, fill=(255, 255, 255), tcol=STAGE, f=sans(int(h * 0.48), 700))

def chip_label(text, col=SILVER):
    t = tl(text, mono(24), col); w, h = t.width + 32, t.height + 16
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(11, 14, 20, 200), outline=col + (130,), width=2)
    im.alpha_composite(t, (16, 7)); return im

def subtitle(im, t, TL, y=1600, size=46):
    """the narrator's words, a few at a time, in a dark pill near the bottom ([word] = lilac italic emphasis)"""
    s = TL.subtitle_at(t)
    if not s: return
    c0, c1, text = s; a = ease((t - c0 + 0.05) / 0.12) * (1 - ease((t - (c1 + 0.2)) / 0.15))
    if a <= 0: return
    lay = rich_c(text, size, "sans", WHITE, LILAC, 900)
    w, h = lay.width + 64, lay.height + 34
    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=(11, 14, 20, 215))
    pill.alpha_composite(lay, (32, 15)); put(im, pill, 540, y, a)
