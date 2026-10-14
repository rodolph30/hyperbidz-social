"""Season 5 (watches) = the HyperBidz Vault. Overlay kit taken from the Vault design canvas (owner, 14 Oct 2026):
black stage #06070B, lit gradient edge (#2F7BFF → #7C5CFF, border #6D4DFF with a blue-violet glow), the Z mark as a
members' seal (black disc, #6D4DFF ring, Z in #5C95FF → #A08BFF), Space Grotesk + Space Mono labels in #B9A8FF,
lot card (rgba(9,10,15,.82), lit border), TOP BID chip, YOU-lead chip (green), timer chip, Won panel
(165° #5B3BE8 → #3A22B8 → #160C46), Vault end card. Plus the season's sounds: watch ticks, vault lock, chimes."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
import mhelpers as M
from founder_common import W, H, SR, WHITE, Mix

STAGE = (6, 7, 11); EDGE = (109, 77, 255); BTN = (124, 92, 255); BLUE = (47, 123, 255); LAV = (185, 168, 255); ICON = (157, 176, 255)
LIVE_RED = (255, 77, 106); GREEN = (78, 217, 138)
S = 2.3                                                                                       # design px → video px
Z_POLYS = [[(24.75, 16), (84.75, 16), (81.94, 36), (59.69, 54.36), (44.98, 41.74), (51.94, 36), (21.94, 36)],
           [(55, 58.23), (48.01, 64), (78.01, 64), (75.2, 84), (15.2, 84), (18.01, 64), (40.28, 45.62)]]
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)

def lin_grad(w, h, c1, c2, angle=135):
    a = np.radians(angle); x = np.linspace(0, 1, w)[None, :]; y = np.linspace(0, 1, h)[:, None]
    k = np.clip((x * np.sin(a) * w - y * np.cos(a) * h - min(0, -np.cos(a) * h) - min(0, np.sin(a) * w)) / (abs(np.sin(a)) * w + abs(np.cos(a)) * h), 0, 1)
    arr = np.array(c1, np.float32) * (1 - k[..., None]) + np.array(c2, np.float32) * k[..., None]
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")

def zmark(size, c1=(92, 149, 255), c2=(160, 139, 255)):
    """the Z in the seal's blue → violet gradient (viewBox 12..88)"""
    m = Image.new("L", (size, size), 0); d = ImageDraw.Draw(m); s = size / 76
    for p in Z_POLYS: d.polygon([((x - 12) * s, (y - 12) * s) for x, y in p], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0)); out.paste(lin_grad(size, size, c1, c2), (0, 0), m); return out

def zflat(size, col=ICON):
    m = Image.new("L", (size, size), 0); d = ImageDraw.Draw(m); s = size / 76
    for p in Z_POLYS: d.polygon([((x - 12) * s, (y - 12) * s) for x, y in p], fill=255)
    out = Image.new("RGBA", (size, size), col + (0,)); out.putalpha(m); return out

def glow(size, rad, col=(94, 108, 255), a=165, blur=None):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); c = size / 2
    ImageDraw.Draw(im).ellipse((c - rad, c - rad, c + rad, c + rad), fill=col + (a,)); return im.filter(ImageFilter.GaussianBlur(blur or rad * 0.5))

def seal(d=170):
    """the members' seal: a black disc, a lit #6D4DFF ring and the gradient Z"""
    pad = int(d * 0.45); s = d + 2 * pad; im = glow(s, d * 0.55, a=170, blur=d * 0.28)
    dr = ImageDraw.Draw(im); c = s / 2; r = d / 2
    dr.ellipse((c - r, c - r, c + r, c + r), fill=(7, 8, 12, 255), outline=EDGE + (255,), width=max(3, int(d * 2 / 62)))
    z = zmark(int(d * 0.45)); im.alpha_composite(z, (int(c - z.width / 2), int(c - z.height / 2))); return im

def mono(text, size=26, col=LAV, tracking=None):
    return R.text_layer(text, R.font(size, mono=True), col, tracking=tracking if tracking is not None else max(2, int(size * 0.2)))

def edge_layer(inset=16, radius=118, width=6):
    """the lit gradient edge around the whole frame (C4 'Leading' look), with its inner glow"""
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((inset, inset, W - inset, H - inset), radius=radius, outline=255, width=width)
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).rounded_rectangle((inset, inset, W - inset, H - inset), radius=radius, outline=255, width=width * 7)
    g = g.filter(ImageFilter.GaussianBlur(38))
    col = np.asarray(lin_grad(W, H, BLUE, BTN, 160).convert("RGB"), np.float32)
    a = np.clip(np.asarray(m, np.float32) * 0.95 + np.asarray(g, np.float32) * 0.55, 0, 255)
    return np.dstack([col, a])
EDGE_ARR = None
EDGE_IDX = None
def lit_edge(im, k, t=0.0):
    """alpha-composite the edge at strength k, with a slow breathing and a light running along it (computed only
    on the pixels the edge touches)"""
    global EDGE_ARR, EDGE_IDX
    if k <= 0.01: return im
    if EDGE_ARR is None:
        EDGE_ARR = edge_layer(); ys, xs = np.nonzero(EDGE_ARR[..., 3] > 1)
        ang = np.arctan2(ys - H / 2, (xs - W / 2) * 1.78).astype(np.float32)
        EDGE_IDX = (ys, xs, ang, EDGE_ARR[ys, xs, :3].astype(np.float32), EDGE_ARR[ys, xs, 3].astype(np.float32))
    ys, xs, ang, rgb, a0 = EDGE_IDX
    d = (ang - t * 1.3 + np.pi) % (2 * np.pi) - np.pi; run = np.exp(-(d / 0.35) ** 2)
    a = np.clip(a0 * k * (0.88 + 0.12 * np.sin(t * 2.4)) * (1 + 0.8 * run), 0, 255)
    lay = np.zeros((H, W, 4), np.uint8)
    lay[ys, xs, :3] = np.clip(rgb + run[:, None] * 60, 0, 255).astype(np.uint8); lay[ys, xs, 3] = a.astype(np.uint8)
    im.alpha_composite(Image.fromarray(lay, "RGBA")); return im

_x = np.linspace(0, 1, 256).astype(np.float32)
_CURVE = (np.clip(0.5 + (_x - 0.5) * 1.16, 0, 1) ** 1.12).astype(np.float32)
_SHADOW = (np.clip(1 - _x / 0.35, 0, 1) ** 1.5 * 0.55).astype(np.float32)
_HI = np.clip((_x - 0.55) / 0.45, 0, 1).astype(np.float32)
_VIG = (1 - 0.55 * np.clip((((_xx - 540) / 680) ** 2 + ((_yy - 820) / 1050) ** 2) ** 1.2, 0, 1))[..., None].astype(np.float32)
_STAGE01 = np.array(STAGE, np.float32) / 255; _WARM = np.array([0.05, 0.01, -0.06], np.float32)
def vault_grade(fr, k=1.0, warm=1.0):
    """black stage: crush the shadows into #06070B, keep the boutique's gold warm, deep vignette"""
    u = np.asarray(fr.convert("RGB")); lum8 = (u.astype(np.uint16).sum(-1) // 3).astype(np.uint8)
    c = _CURVE[u]; sh = _SHADOW[lum8][..., None]
    c = c * (1 - sh) + _STAGE01 * sh
    c = c * (1 + _HI[lum8][..., None] * _WARM * warm)
    l2 = c.mean(-1, keepdims=True); c = l2 + (c - l2) * 1.06
    out = c * _VIG
    if k < 1: out = u.astype(np.float32) / 255 * (1 - k) + out * k
    return Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8)).convert("RGBA")

def lot_card(title, price, label, button=None, w=1034, border=EDGE, label_col=(255, 255, 255)):
    """the Vault lot card: title, big price + label, and optionally the Place Bid button with its NEXT pill"""
    p = int(12 * S); hrow = int(44 * S); prow = int(58 * S); brow = int(56 * S) + int(10 * S) if button else 0
    h = p * 2 + hrow + prow + brow
    im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((40, 40, w + 40, h + 40), radius=int(22 * S), fill=(94, 108, 255, 90))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26)))
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(22 * S), fill=(9, 10, 15, 214), outline=border + (255,), width=3)
    tl = R.text_layer(title, R.font(int(16 * S), 600), WHITE); card.alpha_composite(tl, (p + 4, p + (hrow - tl.height) // 2 - 4))
    d.line([(p, p + hrow), (w - p, p + hrow)], fill=(255, 255, 255, 30), width=2)
    pr = R.text_layer(price, R.font(int(30 * S), 700), WHITE); card.alpha_composite(pr, (p + 4, p + hrow + (prow - pr.height) // 2 - 2))
    lb = R.text_layer(label, R.font(int(9.5 * S), 600), label_col, tracking=2); card.alpha_composite(lb, (p + 4 + pr.width + int(10 * S), p + hrow + (prow - lb.height) // 2 + 6))
    if button:
        d.line([(p, p + hrow + prow), (w - p, p + hrow + prow)], fill=(255, 255, 255, 30), width=2)
        txt, small, big = button[:3]; green = len(button) > 3 and button[3] == "green"; by = p + hrow + prow + int(10 * S); bh = int(56 * S)
        b = Image.new("RGBA", (w - 2 * p, bh), (0, 0, 0, 0)); db = ImageDraw.Draw(b)
        if green:
            m = Image.new("L", b.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, b.width - 1, bh - 1), radius=bh // 2, fill=255)
            b.paste(lin_grad(b.width, bh, (47, 191, 113), (22, 143, 78), 90), (0, 0), m); tx0 = int(18 * S)
        else:
            db.rounded_rectangle((0, 0, b.width - 1, bh - 1), radius=bh // 2, fill=(10, 12, 20, 255), outline=BTN + (255,), width=4)
            gav(b, int(16 * S), bh // 2); tx0 = int(16 * S) + int(30 * S)
        bt = R.text_layer(txt, R.font(int(17 * S), 700), WHITE); b.alpha_composite(bt, (tx0, (bh - bt.height) // 2 - 3))
        if small:
            pw, ph = int(68 * S), int(44 * S); pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=ph // 2, fill=(0, 0, 0, 56) if green else (124, 92, 255, 56))
            s1 = R.text_layer(small, R.font(int(9.5 * S), 600), (255, 255, 255), tracking=1); s2 = R.text_layer(big, R.font(int(15 * S), 700), WHITE)
            pill.alpha_composite(s1, ((pw - s1.width) // 2, 8)); pill.alpha_composite(s2, ((pw - s2.width) // 2, 8 + s1.height - 6))
            b.alpha_composite(pill, (b.width - pw - int(6 * S), (bh - ph) // 2))
        card.alpha_composite(b, (p, by))
    im.alpha_composite(card, (40, 40)); return im

def gav(im, x, cy):
    """the gavel icon from the Place Bid button"""
    d = ImageDraw.Draw(im); s = 2.1
    d.line([(x + 2 * s, cy + 9 * s), (x + 11 * s, cy)], fill=ICON + (255,), width=int(2.2 * s))
    d.polygon([(x + 8 * s, cy - 6 * s), (x + 14 * s, cy - 12 * s), (x + 20 * s, cy - 6 * s), (x + 14 * s, cy)], outline=ICON + (255,), width=int(2 * s))

def bid_chip(initial, text, kind="top", av_col=(53, 126, 221)):
    """TOP BID chip (violet glass) or YOU chip (green) next to a round avatar"""
    ah = int(26 * S); ph = int(30 * S)
    lab = mono("TOP BID" if kind == "top" else "YOU", int(10 * S), WHITE, tracking=2)
    tx = R.text_layer(text, R.font(int(13 * S), 600), WHITE)
    pw = int(6 * S) + lab.width + int(14 * S) + int(8 * S) + tx.width + int(12 * S)
    im = Image.new("RGBA", (ah + int(6 * S) + pw, max(ah, ph)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cy = im.height / 2
    d.ellipse((0, cy - ah / 2, ah, cy + ah / 2), fill=av_col + (255,))
    ini = R.text_layer(initial, R.font(int(11 * S), 700), WHITE); im.alpha_composite(ini, (int(ah / 2 - ini.width / 2), int(cy - ini.height / 2 - 2)))
    x0 = ah + int(6 * S)
    if kind == "top": g = lin_grad(pw, ph, (98, 84, 170), (40, 30, 90), 180); bc = (165, 148, 255)
    else: g = lin_grad(pw, ph, (78, 217, 138), (31, 164, 91), 180); bc = (143, 240, 184)
    m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=ph // 2, fill=235)
    pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); pill.paste(g, (0, 0), m); dp = ImageDraw.Draw(pill)
    dp.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=ph // 2, outline=bc + (255,), width=3)
    lw, lh = lab.width + int(14 * S), int(20 * S); dp.rounded_rectangle((int(6 * S), (ph - lh) // 2, int(6 * S) + lw, (ph + lh) // 2), radius=lh // 2, fill=(255, 255, 255, 40))
    pill.alpha_composite(lab, (int(6 * S) + int(7 * S), (ph - lab.height) // 2))
    pill.alpha_composite(tx, (int(6 * S) + lw + int(8 * S), (ph - tx.height) // 2 - 3))
    im.alpha_composite(pill, (x0, int(cy - ph / 2))); return im

def clock_icon(size, col):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(2, size // 9)
    d.ellipse((w, w, size - w, size - w), outline=col + (255,), width=w); c = size / 2
    d.line([(c, c - size * 0.25), (c, c), (c + size * 0.16, c + size * 0.11)], fill=col + (255,), width=w); return im

def timer_chip(text, hot=False):
    h = int(34 * S); col = (217, 207, 255) if hot else WHITE
    tx = R.text_layer(text, R.font(int(13 * S), 700), col); ic = clock_icon(int(15 * S), col)
    w = int(12 * S) * 2 + ic.width + int(6 * S) + tx.width
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(124, 92, 255, 82) if hot else (11, 14, 20, 140), outline=(167, 139, 250, 255) if hot else (255, 255, 255, 52), width=3)
    im.alpha_composite(ic, (int(12 * S), (h - ic.height) // 2)); im.alpha_composite(tx, (int(12 * S) + ic.width + int(6 * S), (h - tx.height) // 2 - 3)); return im

def vault_pill(text="FROM THE VAULT"):
    h = int(34 * S); lb = mono(text, int(10.5 * S), LAV, tracking=3); zs = int(24 * S)
    w = int(5 * S) + zs + int(7 * S) + lb.width + int(12 * S)
    im = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((30, 30, w + 30, h + 30), radius=h // 2, fill=(94, 108, 255, 110)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    p = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(p); d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(6, 7, 11, 200), outline=EDGE + (255,), width=3)
    zc = Image.new("RGBA", (zs, zs), (0, 0, 0, 0)); m = Image.new("L", (zs, zs), 0); ImageDraw.Draw(m).ellipse((0, 0, zs - 1, zs - 1), fill=255); zc.paste(lin_grad(zs, zs, BLUE, BTN), (0, 0), m)
    z = zflat(int(zs * 0.5), WHITE); zc.alpha_composite(z, ((zs - z.width) // 2, (zs - z.height) // 2))
    p.alpha_composite(zc, (int(5 * S), (h - zs) // 2)); p.alpha_composite(lb, (int(5 * S) + zs + int(7 * S), (h - lb.height) // 2))
    im.alpha_composite(p, (30, 30)); return im

def live_line(text="5 VAULT LOTS LIVE NOW", t=0.0):
    lb = mono(text, int(10.5 * S), LAV, tracking=3); r = int(3.5 * S)
    im = Image.new("RGBA", (lb.width + 4 * r + 20, max(lb.height, 4 * r) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cy = im.height / 2
    a = int(160 + 95 * (0.5 + 0.5 * np.sin(t * 6)))
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((10 - r, cy - 2 * r, 10 + 3 * r, cy + 2 * r), fill=LIVE_RED + (a,)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(5)))
    d.ellipse((10, cy - r, 10 + 2 * r, cy + r), fill=LIVE_RED + (255,)); im.alpha_composite(lb, (10 + 2 * r + 14, int(cy - lb.height / 2))); return im

def won_panel(when, lot, price, w=900):
    h = 470; g = lin_grad(w, h, (91, 59, 232), (22, 12, 70), 165)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=56, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(g, (0, 0), m)
    z = zflat(30, WHITE); im.alpha_composite(z, (54, 52)); im.alpha_composite(mono(f"VAULT · HAMMER FELL {when}", 24, (255, 255, 255), 3), (98, 50))
    a = R.text_layer("You won it", R.font(120, 700), WHITE); im.alpha_composite(a, (50, 110))
    im.alpha_composite(mono(lot.upper(), 22, (215, 215, 235), 3), (54, 296))
    p = R.text_layer(price, R.font(84, 700), WHITE); im.alpha_composite(p, (50, 330)); return im

def join_button(text="Join the Vault", w=820, pressed=0.0):
    h = 136; m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((40, 50, w + 40, h + 50), radius=h // 2, fill=(94, 108, 255, int(150 * (1 + pressed)))); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(24)))
    b = Image.new("RGBA", (w, h), (0, 0, 0, 0)); b.paste(lin_grad(w, h, BLUE, BTN, 90), (0, 0), m)
    t = R.text_layer(text, R.font(46, 700), WHITE); b.alpha_composite(t, ((w - t.width) // 2, (h - t.height) // 2 - 4))
    im.alpha_composite(b, (40, 40)); return im

END_GLOW = None
def vault_end_card(k, lines, END, tag="Where luxury is auctioned."):
    """the Vault end card: black stage, blue-violet glow, the seal, HYPERBIDZ VAULT, the lines, follow"""
    global END_GLOW
    if END_GLOW is None:
        g = np.exp(-(((_xx - 260) / 560) ** 2 + ((_yy - 240) / 560) ** 2)) * 0.5 + np.exp(-(((_xx - 880) / 520) ** 2 + ((_yy - 1750) / 520) ** 2)) * 0.12
        base = np.array(STAGE, np.float32)[None, None] + g[..., None] * np.array([94, 108, 255], np.float32)
        END_GLOW = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    im = END_GLOW.copy(); s = k / 0.42; sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, seal(190), W / 2, 470, R.clamp(s * 3), sc)
    a0 = R.ease_out((k - 0.25) / 0.3); R.paste_center(im, mono("HYPERBIDZ VAULT", 30, LAV, 7), W / 2, 650, a0)
    for i, line in enumerate(lines):
        a = R.ease_out((k - 0.4 - i * 0.3) / 0.3); R.paste_center(im, R.text_layer(line, R.font(96, 700), WHITE), W / 2, 780 + i * 114 + (1 - a) * 20, a)
    b = R.ease_out((k - 1.3) / 0.35); y0 = 780 + len(lines) * 114 + 40
    R.paste_center(im, R.text_layer(tag, R.font(46, 500), (225, 228, 245)), W / 2, y0, b)
    R.paste_center(im, mono("LIVE AUCTIONS FOR LEBANON · COMING SOON", 24, (170, 175, 200), 3), W / 2, y0 + 70, b)
    c = R.ease_out((k - 1.7) / 0.35); R.paste_center(im, join_button("Follow @hyperbidz", 700), W / 2, y0 + 230, c, 0.94 + 0.06 * c)
    out = im.convert("RGB")
    if k > END - 0.5: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), R.clamp((k - (END - 0.5)) / 0.5))
    return out

# ---------- sound ----------
class VaultMix(Mix):
    """same voice/duck/fx bus; the end card opens like a vault (heavy lock + metal ring) on a dark D major 9"""
    def write(self, path):
        import wave
        fx = self.fx.copy(); fx[:len(self.duck)] *= (0.4 + 0.6 * self.duck)
        out = self.main + fx; out[:len(self.voice)] += self.voice
        i = int((self.clip + 0.02) * SR); x = self.tt(0.6)
        door = np.sin(2 * np.pi * np.cumsum(48 + 40 * np.exp(-x * 25)) / SR) * np.exp(-x * 7) * 0.7
        door += sum(np.sin(2 * np.pi * f * x) * np.exp(-x * d) * a for f, d, a in ((523, 6, .10), (797, 8, .07), (1180, 10, .05)))
        out[i:i + len(x)] += door[: self.n - i]
        x = self.tt(self.end); env2 = np.minimum(1, x / 0.4) * np.exp(-np.maximum(0, x - 1.8) * 0.8); i = int((self.clip + 0.1) * SR)
        chord = sum(np.sin(2 * np.pi * f * x) * a for f, a in ((73.4, .4), (146.8, .45), (185, .3), (220, .3), (277.2, .2), (329.6, .14))) * env2 * 0.28
        out[i:i + len(chord)] += chord[: self.n - i]
        out[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR)) ** 1.5
        out = out / (np.max(np.abs(out)) + 1e-9) * 0.92
        with wave.open(path, "wb") as w_:
            w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

def ticks(mx, t0, t1, rate=6, g=0.03, skip=()):
    """a mechanical watch: tick-tock"""
    k = 0; t = t0
    while t < t1:
        if not any(a <= t < b for a, b in skip):
            y = mx.tt(0.012); click = np.sin(2 * np.pi * (3200 if k % 2 else 2600) * y) * np.exp(-y * 600)
            mx.fadd(click, t, g)
        k += 1; t = t0 + k / rate

def lock(mx, at, g=0.35):
    y = mx.tt(0.35); s = np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-y * 30)) / SR) * np.exp(-y * 14)
    s += mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 60) * 0.6; mx.fadd(s, at, g)
    y = mx.tt(0.05); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 1) * np.exp(-y * 120), at + 0.11, g * 0.6)

def chime(mx, at, f=1318.5, g=0.07):
    y = mx.tt(1.6); s = sum(np.sin(2 * np.pi * f * m * y) * np.exp(-y * d) * a for m, d, a in ((1, 2.5, 1), (2.76, 4, .35), (5.4, 6, .15)))
    mx.fadd(s, at, g)

def pad(mx, t0, t1, freqs, g, fade=0.6):
    y = mx.tt(t1 - t0); s = sum(np.sin(2 * np.pi * f * y + i) * a for i, (f, a) in enumerate(freqs)) * (0.9 + 0.1 * np.sin(2 * np.pi * 0.25 * y))
    env = np.minimum(1, y / fade) * np.minimum(1, (y[-1] - y) / 0.2); mx.fadd(s * env, t0, g)

def won_strip(when, price, w=1000, h=290):
    """a compact Won card for the bottom of the frame"""
    g = lin_grad(w, h, (91, 59, 232), (22, 12, 70), 165)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=50, fill=255)
    im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((40, 40, w + 40, h + 40), radius=50, fill=(124, 92, 255, 140)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26)))
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0)); c.paste(g, (0, 0), m)
    z = zflat(28, WHITE); c.alpha_composite(z, (46, 40)); c.alpha_composite(mono(f"VAULT · HAMMER FELL {when}", 23, (255, 255, 255), 3), (88, 38))
    a = R.text_layer("You won it", R.font(104, 700), WHITE); c.alpha_composite(a, (40, 92))
    p = R.text_layer(price, R.font(72, 700), WHITE); c.alpha_composite(p, (w - 46 - p.width, 120))
    im.alpha_composite(c, (40, 40)); return im

def mono_pill(text, size=28, col=LAV, tracking=6):
    lb = mono(text, size, col, tracking); w, h = lb.width + 60, lb.height + 28
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(6, 7, 11, 190), outline=(124, 92, 255, 120), width=2)
    im.alpha_composite(lb, (30, (h - lb.height) // 2)); return im
