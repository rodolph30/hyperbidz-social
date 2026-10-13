"""Season 4 'Auction it once' (rooftop at dusk, green classic). 'Listing a car means 100 calls': a missed-calls counter
races to 100 while call notifications stack in the sky. '...and 1,000 lowballs': lowball messages flood in from every
side ('Would you take $2,000?', 'Swap for my scooter?', 'Bro, $1,500 cash, khalas?'), a lowball counter spins to
1,000 and the frame starts to shake. 'Auction it once.': a single violet wave wipes it all away, silence, and one clean
pill: ONE LIVE AUCTION. 'Let the market decide.': bids climb $24,000 → $38,000 and SOLD stamps after 'decide'.
Last shot held with a slow push-in. End card 'One auction. No lowballs.' Plate and grille badge blurred."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s4_common as S

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, RED = S.VIOLET, S.RED
FR = decode()
for fr in FR:
    S.blur_region(fr, (130, 1866, 580, 1920), 10); S.blur_region(fr, (254, 1612, 294, 1682), 6)

CAPS = [(0.45, 2.45, ["Listing a car means", "[100 calls]…"]), (2.45, 4.10, ["and [1,000 lowballs.]"]),
        (4.65, 5.80, ["[Auction it once.]"]), (6.15, 9.20, ["Let the [market] decide."])]
CALLS0, CALLS1, LOW0, LOW1, WIPE, PILL, BIDS0, SOLD = 0.55, 2.4, 2.5, 4.55, 4.68, 4.95, 6.2, 7.28
FACE = (540, 440)
rng = np.random.default_rng(21)
LOWS = ["Would you take $2,000?", "Swap for my scooter?", "Bro, $1,500 cash, khalas?", "I'll give you half.", "$800 and I pick it up today",
        "Is it still available? $1k", "Can you do $3k with the rims?", "My cousin offers $2,500", "Trade for an iPhone?", "Cash, no papers, $1,200",
        "Half now, half next year?", "I come see it, $900?", "Final: $1,800", "$1,000, yalla?"]
LOW_IM = [S.msg_bubble(None, s, fill=(46, 48, 60, 240), size=32) for s in LOWS]
LOW_AT = [LOW0 + (LOW1 - LOW0) * (i / len(LOWS)) ** 0.8 for i in range(len(LOWS))]
KEEP_CLEAR = [(330, 280, 750, 640), (30, 400, 270, 545), (810, 400, 1050, 545), (290, 60, 790, 330)]   # face, both counters, the calls
def place():
    """spread the bubbles over the frame, never on his face or the captions, overlapping each other as little as possible"""
    rects, out = [], []
    for b in LOW_IM:
        w, h = b.width, b.height; best = None
        for _ in range(600):
            x, y = rng.uniform(w / 2 + 18, W - w / 2 - 18), rng.uniform(140, 1520)
            r = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
            if any(r[2] > a and r[0] < c and r[3] > b and r[1] < d for a, b, c, d in KEEP_CLEAR): continue
            ov = sum(max(0, min(r[2], q[2]) - max(r[0], q[0])) * max(0, min(r[3], q[3]) - max(r[1], q[1])) for q in rects)
            if best is None or ov < best[0]: best = (ov, x, y, r)
            if ov == 0: break
        rects.append(best[3]); out.append((best[1], best[2]))
    return out
LOW_POS = place()
CALL_AT = [CALLS0 + i * 0.32 for i in range(6)]

def call_note(name, n):
    w, h = 470, 92; im = M.glass(w, h, 26, fill=(24, 26, 36, 236), border=(255, 255, 255, 50)); d = ImageDraw.Draw(im)
    d.ellipse((20, 18, 76, 74), fill=(255, 76, 96, 255)); ph = R.text_layer("✆", R.font(30, 700), WHITE)
    tl = R.text_layer("Missed call", R.font(28, 700), WHITE); im.alpha_composite(tl, (96, 14))
    sl = R.text_layer(name, R.font(24, 500), (190, 194, 210)); im.alpha_composite(sl, (96, 50))
    d.line([(36, 34), (60, 58)], fill=WHITE + (255,), width=5); d.line([(60, 34), (36, 58)], fill=WHITE + (255,), width=5)
    return im
CALL_IM = [call_note(n, i) for i, n in enumerate(["Unknown number", "+961 3 ••• •••", "Unknown number", "+961 71 ••• •••", "Unknown number", "+961 76 ••• •••"])]

def counter(label, val, col):
    a = R.text_layer(label, R.font(22, mono=True), (225, 228, 240), tracking=3); b = R.text_layer(f"{val:,}", R.font(54, 700), WHITE)
    w, h = max(a.width, b.width) + 60, a.height + b.height + 34
    im = M.glass(w, h, 24, fill=(20, 20, 30, 225), border=col + (220,)); im.alpha_composite(a, ((w - a.width) // 2, 14)); im.alpha_composite(b, ((w - b.width) // 2, 16 + a.height))
    return im

def one_pill():
    return S.grad_pill("1 LISTING  ·  1 NIGHT  ·  0 LOWBALLS", "ONE LIVE AUCTION", 64, 22)
PILL_IM = one_pill()
BIDS = [(6.30, "Karim", 24000), (6.55, "Maya", 29500), (6.80, "Nadim", 33000), (7.05, "Rita", 38000)]
CHIPS = [S.bid_chip(n, f"${v:,}", hot=(i == 3)) for i, (_, n, v) in enumerate(BIDS)]

def sold():
    a = R.text_layer("SOLD", R.font(30, mono=True), WHITE, tracking=8); b = R.text_layer("$38,000", R.font(72, 700), WHITE)
    w, h = max(a.width, b.width) + 100, a.height + b.height + 40
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(a, ((w - a.width) // 2, 16)); im.alpha_composite(b, ((w - b.width) // 2, 18 + a.height)); return im.rotate(-4, resample=Image.BICUBIC, expand=True)
SOLD_IM = sold()

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["One auction.", "No lowballs."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = S.look(fr, "dusk")
    chaos = R.clamp((t - LOW0) / (WIPE - LOW0)) if t < WIPE else max(0.0, 1 - (t - WIPE) / 0.15)
    if chaos > 0:                                                                            # the phone won't stop
        z = 1 + 0.025 * chaos; sx, sy = 9 * chaos * np.sin(t * 53), 7 * chaos * np.sin(t * 41 + 1)
        im = S.zcrop(im, z, (540 + sx * 4, 860 + sy * 4))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 560))
    wipe = R.clamp((t - WIPE) / 0.45) if t >= WIPE else 0
    for i, at in enumerate(CALL_AT):                                                         # missed calls stack in the sky
        if t < at or wipe >= 1: continue
        k = (t - at) / 0.25; slot = sum(1 for a2 in CALL_AT if at < a2 <= t)
        if slot > 1: continue
        R.paste_center(im, CALL_IM[i], W / 2 + (-1 if i % 2 else 1) * wipe ** 2 * 900, 120 + slot * 104, R.clamp(k * 3) * (1 - 0.3 * slot) * (1 - wipe), 0.9 + 0.1 * R.stamp(k) if k < 1 else 1.0)
    if CALLS0 <= t < WIPE + 0.45:
        n = int(100 * R.clamp((t - CALLS0) / (CALLS1 - CALLS0)) ** 1.6)
        R.paste_center(im, counter("MISSED CALLS", n, RED), 150, 470, R.clamp((t - CALLS0) / 0.2) * (1 - wipe), 1.0 + (0.08 if n == 100 and t < CALLS1 + 0.15 else 0))
    if LOW0 <= t < WIPE + 0.45:
        n = int(1000 * R.clamp((t - LOW0) / (LOW1 - LOW0)) ** 1.5)
        R.paste_center(im, counter("LOWBALLS", n, (255, 184, 92)), 930, 470, R.clamp((t - LOW0) / 0.2) * (1 - wipe))
    for i, at in enumerate(LOW_AT):                                                          # the lowballs flood in
        if t < at or wipe >= 1: continue
        k = (t - at) / 0.22; x, y = LOW_POS[i]; dx, dy = x - FACE[0], y - FACE[1]; dn = np.hypot(dx, dy) + 1e-6
        R.paste_center(im, LOW_IM[i], x + dx / dn * wipe ** 2 * 900 + 2 * chaos * np.sin(t * 37 + i), y + dy / dn * wipe ** 2 * 900, R.clamp(k * 3) * (1 - wipe), 0.8 + 0.2 * R.stamp(k) if k < 1 else 1.0)
    if WIPE <= t < WIPE + 0.8:
        for j in range(3): kk = R.clamp((t - WIPE - 0.08 * j) / 0.7); S.ring(im, FACE[0], FACE[1] + 200, 60 + 1100 * R.ease_out(kk), (1 - kk) * 0.85, VIOLET, 10)
    if t >= PILL:
        s = (t - PILL) / 0.32
        R.paste_center(im, PILL_IM, W / 2, 190, R.clamp(s * 3) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), 1.5 - 0.5 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, PILL, W / 2, 190, ((-300, -30, 26), (290, -40, 18), (250, 40, 26)))
    shown = [(at, ch) for (at, *_), ch in zip(BIDS, CHIPS) if t >= at][-3:]
    for j, (at, ch) in enumerate(reversed(shown)):                                           # the market decides
        kk = R.ease_out((t - at) / 0.25)
        R.paste_center(im, ch, 860, 820 + j * 70 + (1 - kk) * 30, R.clamp((t - at) / 0.15) * (1 - 0.3 * j) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)))
    if t >= SOLD:
        s = (t - SOLD) / 0.3; R.paste_center(im, SOLD_IM, 240, 860, R.clamp(s * 3) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), 1.8 - 0.8 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, SOLD, 240, 860, ((-150, -70, 34), (150, -60, 26), (130, 70, 18)))
    draw_caps(im, t, CAPS, y=1690, size=62)
    if WIPE <= t < WIPE + 0.08: im = M.flash(im, 0.3)
    if SOLD <= t < SOLD + 0.07: im = M.flash(im, 0.2, (255, 236, 220))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, 0.0),))
        S.tone(mx, 0.0, WIPE, ((110, .25), (164.8, .18), (220, .12)), 0.04, 0.6)
        for i, at in enumerate(CALL_AT): S.beep(mx, at, 880 if i % 2 else 740, 0.08, 0.03)    # quiet ringtone blips
        for i, at in enumerate(LOW_AT):
            if at > 3.6: continue
            y = mx.tt(0.1); mx.fadd(np.sin(2 * np.pi * (1500 + 60 * (i % 5)) * y) * np.exp(-y * 40), at, 0.02 + 0.015 * i / len(LOWS))
        y = mx.tt(1.2); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 6) * (y / y[-1]) ** 2, LOW0, 0.05)              # rising noise, gone before 'lowballs'
        mx.whoosh(WIPE - 0.5, 0.48, 0.4); mx.thud(WIPE - 0.04, 0.3)      # done before "Auction"
        S.tone(mx, 5.7, CLIP, ((146.8, .3), (185, .22), (220, .2), (293.7, .1)), 0.05, 0.4)                 # after 'once'
        mx.shimmer(5.72, 1174.7, 0.06)
        for i, (at, *_ ) in enumerate(BIDS): mx.ping(at + 0.02, 880 * 2 ** (i * 3 / 12), 0.035)
        mx.thud(SOLD, 0.55); mx.shimmer(SOLD + 0.03, 1318.5, 0.1)
        mx.write("s4roof_audio.wav")
    render(frame, TOTAL, "s4roof_audio.wav", OUT)
