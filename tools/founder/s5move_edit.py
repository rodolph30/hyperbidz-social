"""Season 5 (the Vault) Ep. 2 'Your move'. 'Luxury used to decide who gets in': frosted glass doors stand half-closed
around him with a lock badge, BY INVITATION ONLY. 'Now?': the lock clicks open, the doors slide apart and the lit
gradient edge ignites. 'You make the move': a Vault lot card rises and Place Bid is pressed; the card turns green,
'You're leading', YOU lead at $2,065. 'HyperBidz': the members' seal stamps in, HYPERBIDZ VAULT. 'Your game.'
Last shot held with a slow push-in. Vault end card 'Your move. Your game.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s5_common as V

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.45; END = 3.9; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.0, 2.00, ["Luxury used to decide", "[who gets in.]"]), (2.60, 3.50, ["[Now?]"]), (4.00, 5.30, ["You make [the move.]"]),
        (5.50, 6.55, ["[HyperBidz.]"]), (6.75, 9.20, ["[Your game.]"])]
UNLOCK, OPEN, CARD_IN, PRESS, BRAND = 2.88, 3.0, 3.6, 4.62, 5.62
DL, DR = 330, 750

def lock_icon(size, open_k=0.0, col=V.LAV):
    im = Image.new("RGBA", (size, int(size * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(3, size // 10)
    by = int(size * 0.55); d.rounded_rectangle((w, by, size - w, im.height - w), radius=size // 6, outline=col + (255,), width=w)
    lift = int(size * 0.28 * open_k); x0, x1 = int(size * 0.25), int(size * 0.75)
    d.arc((x0, by - size * 0.42 - lift, x1, by + size * 0.12 - lift), 180, 360, fill=col + (255,), width=w)
    d.line([(x0, by - size * 0.15 - lift), (x0, by - lift + (0 if open_k > 0.5 else w))], fill=col + (255,), width=w)
    d.line([(x1, by - size * 0.15 - lift), (x1, by)], fill=col + (255,), width=w)
    return im

def badge(open_k):
    green = open_k >= 1
    lb = V.mono("OPEN TO YOU" if green else "BY INVITATION ONLY", 28, V.GREEN if green else V.LAV, 6)
    ic = lock_icon(34, open_k, V.GREEN if green else V.LAV); w, h = 40 + ic.width + 20 + lb.width + 40, 92
    im = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((30, 30, w + 30, h + 30), radius=h // 2, fill=(94, 108, 255, 100)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(16)))
    p = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(p).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(6, 7, 11, 225), outline=((52, 199, 123) if green else V.EDGE) + (255,), width=3)
    p.alpha_composite(ic, (40, (h - ic.height) // 2)); p.alpha_composite(lb, (40 + ic.width + 20, (h - lb.height) // 2)); im.alpha_composite(p, (30, 30)); return im
BADGE = [badge(0), badge(1)]

def frosted(im):
    small = im.convert("RGB").resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(7)).resize((W, H), Image.BILINEAR)
    a = np.asarray(small, np.float32) * 0.42 + np.array([14, 12, 30], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
SHEEN = V.lin_grad(DL, H, (60, 60, 120), (6, 7, 11), 120)

def doors(im, k):
    """two frosted glass doors; k = 0 closed (half-open, framing him), 1 slid out of frame"""
    if k >= 1: return im
    fz = frosted(im); off = int(DL * R.ease_out(k) ** 1.3 * 1.05)
    for side in (0, 1):
        x0, x1 = (0, DL) if side == 0 else (DR, W)
        panel = fz.crop((x0, 0, x1, H)); panel = Image.blend(panel, SHEEN.resize(panel.size) if side == 0 else SHEEN.resize(panel.size).transpose(Image.FLIP_LEFT_RIGHT), 0.18)
        d = ImageDraw.Draw(panel); ex = panel.width - 3 if side == 0 else 0
        d.line([(ex, 0), (ex, H)], fill=(214, 186, 120, 230), width=5)                                   # brass edge
        hx = panel.width - 46 if side == 0 else 34; d.rounded_rectangle((hx, 820, hx + 12, 1140), radius=6, fill=(214, 186, 120, 255))   # handle
        im.alpha_composite(panel, (x0 - off if side == 0 else x0 + off, 0))
    return im

def frame(t):
    if t >= CLIP: return V.vault_end_card(t - CLIP, ["Your move.", "Your game."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = V.vault_grade(fr)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 720))
    ok = R.clamp((t - OPEN) / 0.6)
    im = doors(im, ok)
    if t >= OPEN + 0.2: V.lit_edge(im, R.ease_out((t - OPEN - 0.2) / 0.5), t)
    if t < OPEN + 0.5:                                                                                   # the lock
        op = R.ease_out((t - UNLOCK) / 0.12) if t >= UNLOCK else 0
        b = BADGE[1] if op >= 1 else BADGE[0]
        R.paste_center(im, b, W / 2, 1480, R.clamp(t / 0.3) * (1 - R.clamp((t - OPEN - 0.15) / 0.35)), 1 + 0.08 * np.sin(np.pi * R.clamp((t - UNLOCK) / 0.3)))
    if t >= CARD_IN:                                                                                     # you make the move
        k = R.ease_out((t - CARD_IN) / 0.45); lead = t >= PRESS + 0.2
        if lead: c = V.lot_card("Dive Chronograph", "$2,065", "YOUR BID · 8 BIDS", ("You're leading", "YOUR BID", "$2,065", "green"), border=(52, 199, 123), label_col=V.GREEN)
        else: c = V.lot_card("Dive Chronograph", "$2,015", "CURRENT BID · 7 BIDS", ("Place Bid", "NEXT", "$2,065"))
        sc = 1 - 0.03 * np.sin(np.pi * R.clamp((t - PRESS) / 0.2)) if PRESS <= t < PRESS + 0.2 else (1 + 0.03 * (1 - R.clamp((t - PRESS - 0.2) / 0.25)) if lead else 1.0)
        R.paste_center(im, c, W / 2, 1500 + (1 - k) * 220, R.clamp((t - CARD_IN) / 0.2) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), sc)
        if PRESS <= t < PRESS + 0.7:
            kk = R.clamp((t - PRESS) / 0.6)
            lay = Image.new("RGBA", (700, 700), (0, 0, 0, 0)); rr = 40 + 300 * R.ease_out(kk)
            ImageDraw.Draw(lay).ellipse((350 - rr, 350 - rr, 350 + rr, 350 + rr), outline=(124, 92, 255, int(220 * (1 - kk))), width=8); R.paste_center(im, lay, 300, 1632)
        if lead:
            s = (t - PRESS - 0.2) / 0.3; ch = V.bid_chip("R", "You lead at $2,065", "you", (109, 77, 255))
            R.paste_center(im, ch, 40 + ch.width / 2, 1215, R.clamp(s * 3) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), 0.85 + 0.15 * R.stamp(s) if s < 1 else 1.0)
    if t >= BRAND:                                                                                       # HyperBidz: the seal
        s = (t - BRAND) / 0.34; a = R.clamp(s * 3) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3))
        R.paste_center(im, V.seal(130), W / 2, 205, a, 1.5 - 0.5 * R.stamp(s) if s < 1 else 1.0)
        R.paste_center(im, V.mono_pill("HYPERBIDZ VAULT", 26), W / 2, 345, R.clamp((t - BRAND - 0.2) / 0.3) * a)
        sparkle_burst(im, t, BRAND, W / 2, 205, ((-110, -40, 26), (110, -50, 18), (90, 50, 26)))
    draw_caps(im, t, CAPS, y=1845 if t >= CARD_IN else 1700, size=58)
    if t > CLIP - XF: im = Image.blend(im, Image.new("RGBA", (W, H), V.STAGE + (255,)), R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = V.VaultMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        V.pad(mx, 0.0, OPEN + 0.3, ((73.4, .35), (110, .2), (130.8, .15)), 0.05, 0.8)                   # closed: D minor
        V.ticks(mx, 0.0, OPEN, 6, 0.025)
        V.lock(mx, UNLOCK, 0.32)                                                                          # in the gap after 'Now?'
        y = mx.tt(0.7); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 9) * np.sin(np.pi * y / 0.7) ** 2, OPEN + 0.05, 0.12)   # doors glide
        V.pad(mx, OPEN + 0.2, CLIP, ((146.8, .3), (185, .22), (220, .2), (277.2, .1)), 0.05, 0.6)
        V.chime(mx, OPEN + 0.3, 1567.98, 0.05)
        y = mx.tt(0.05); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 90), PRESS, 0.06)    # tap
        mx.ping(PRESS + 0.35, 1318.5, 0.05)
        V.chime(mx, 6.4, 1318.5, 0.06)                                                                    # after 'HyperBidz'
        mx.thud(7.45, 0.3)
        mx.write("s5move_audio.wav")
    render(frame, TOTAL, "s5move_audio.wav", OUT)
