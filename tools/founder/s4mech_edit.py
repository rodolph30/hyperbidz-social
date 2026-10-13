"""Season 4 'Forty bidders disagree' (mechanic). Played like a doctor breaking bad news: tight on his face in a cold
clinic grade, an ECG monitor beeping under him. 'I'm sorry.' A diagnosis card: 'Your mechanic says it's only worth
$3,000' stamps in red. Then the line flatlines with a long tone in the silence. A defibrillator jolt (flash, thud), the
camera pulls back to the full workshop in warm light, and the flat line comes back to life as a climbing bid line while
40 bidders pop in above the car: $3,000 → $7,400 on '40 bidders disagree'. Last shot held with a slow push-in.
End card 'Second opinion? Get forty.' Plate and grille badge blurred."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s4_common as S

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, RED = S.VIOLET, S.RED
GREEN = (90, 255, 160)
FR = decode()
SKIN = lambda a: (a[..., 0] - a[..., 1] > 24) | (a[..., 0] > 238)
for fr in FR:
    S.blur_unless(fr, (430, 352, 740, 516), 18, SKIN, edge=24)                                         # licence plate behind his head
    S.blur_unless(fr, (540, 258, 622, 338), 9, lambda a: np.zeros(a.shape[:2], bool), edge=14)  # grille badge

CAPS = [(0.55, 1.45, ["I'm [sorry.]"]), (2.00, 3.30, ["Your mechanic says…"]), (3.30, 4.75, ["it's only worth [$3,000.]"]),
        (5.65, 9.20, ["[40 bidders] disagree."])]
ZOOM, FOCUS = 1.42, (560, 700)
CARD_IN, PRICE_AT, FLAT, SHOCK, DIS = 2.10, 3.85, 4.70, 5.60, 6.70
PANEL = (60, 1110, 1020, 1470)
PERIOD, SPEED = 0.85, 560.0
rng = np.random.default_rng(5)
NAMES = "KRMJNTLSHAGDBWFYZEOPQCVIUXRMJNKALSTHGDBW"
AV_AT = sorted(SHOCK + 0.15 + rng.uniform(0, 1.0, 40) ** 1.4)                                 # 40 bidders arrive, fast then faster
AV_POS = [(108 + (i % 10) * 96, 150 + (i // 10) * 92) for i in range(40)]
AV_POS = [AV_POS[j] for j in rng.permutation(40)]
PRICES = np.linspace(3000, 7400, 41)

def avatar(ch, k):
    s = 74; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hue = [(124, 92, 255), (47, 123, 255), (167, 139, 250), (98, 70, 230)][k % 4]
    d.ellipse((2, 2, s - 3, s - 3), fill=hue + (255,), outline=(255, 255, 255, 230), width=3)
    tl = R.text_layer(ch, R.font(32, 700), WHITE); im.alpha_composite(tl, ((s - tl.width) // 2, (s - tl.height) // 2 - 2)); return im
AV_IM = [avatar(NAMES[i], i) for i in range(40)]

def diag_card(stamp_k):
    w, h = 700, 250; im = M.glass(w, h, 30, fill=(240, 246, 250, 236), border=(255, 255, 255, 255)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 10), fill=(90, 150, 200, 255))
    hd = R.text_layer("DIAGNOSIS", R.font(26, mono=True), (60, 90, 120), tracking=6); im.alpha_composite(hd, (34, 30))
    pt = R.text_layer("Patient: your car", R.font(28, 500), (40, 48, 60)); im.alpha_composite(pt, (34, 78))
    lb = R.text_layer("Mechanic's estimate", R.font(28, 500), (40, 48, 60)); im.alpha_composite(lb, (34, 124))
    d.line([(34, 178), (w - 34, 178)], fill=(200, 210, 220, 255), width=2)
    if stamp_k > 0:
        pr = R.text_layer("$3,000", R.font(76, 700), (220, 50, 70)); lay = Image.new("RGBA", (pr.width + 40, pr.height + 20), (0, 0, 0, 0)); lay.alpha_composite(pr, (20, 10))
        sc = 1.8 - 0.8 * R.stamp(stamp_k) if stamp_k < 1 else 1.0
        R.paste_center(im, lay, w - 30 - pr.width / 2, 112, R.clamp(stamp_k * 3), sc)
        lo = R.text_layer("LOW", R.font(24, mono=True), WHITE, tracking=4); lw = lo.width + 26
        tag = Image.new("RGBA", (lw, 40), (0, 0, 0, 0)); ImageDraw.Draw(tag).rounded_rectangle((0, 0, lw - 1, 39), radius=12, fill=(220, 50, 70, 255)); tag.alpha_composite(lo, (13, 4))
        im.alpha_composite(tag, (34, 196)) if stamp_k >= 1 else None
    return im

def ecg(tau):
    """one PQRST beat per PERIOD; flat after FLAT"""
    if tau >= FLAT or tau < 0: return 0.0
    p = (tau % PERIOD) / PERIOD
    return (0.12 * np.exp(-((p - 0.18) / 0.03) ** 2) - 0.15 * np.exp(-((p - 0.30) / 0.008) ** 2) + 1.0 * np.exp(-((p - 0.33) / 0.012) ** 2)
            - 0.25 * np.exp(-((p - 0.36) / 0.01) ** 2) + 0.22 * np.exp(-((p - 0.55) / 0.045) ** 2))

def monitor(im, t, a):
    x0, y0, x1, y1 = PANEL; w, h = x1 - x0, y1 - y0
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, fill=(6, 12, 14, 170), outline=(255, 255, 255, 40), width=2)
    for gx in range(40, w, 60): d.line([(gx, 20), (gx, h - 20)], fill=(90, 255, 160, 18))
    for gy in range(20, h, 60): d.line([(20, gy), (w - 20, gy)], fill=(90, 255, 160, 18))
    base = h * 0.62; amp = h * 0.42
    if t < SHOCK:
        head = (t * SPEED) % (w - 80) + 40; pts = []
        for x in range(40, w - 40, 3):
            back = head - x if x <= head else head + (w - 80) - x
            if back < 30: pts.append(None); continue
            tau = t - back / SPEED; pts.append((x, base - amp * ecg(tau), max(0.15, 1 - back / (w - 80))))
        for p, q in zip(pts, pts[1:]):
            if p and q: d.line([(p[0], p[1]), (q[0], q[1])], fill=GREEN + (int(255 * p[2]),), width=5)
        hy = base - amp * ecg(t); d.ellipse((head - 9, hy - 9, head + 9, hy + 9), fill=(220, 255, 235, 255))
        bpm = "72" if t < 3.6 else ("41" if t < FLAT else "0")
        col = GREEN if t < FLAT else RED
        lab = R.text_layer("HR", R.font(24, mono=True), col, tracking=3); lay.alpha_composite(lab, (34, 22))
        v = R.text_layer(bpm, R.font(52, 700), col); lay.alpha_composite(v, (34, 52))
        if t >= FLAT and (t * 3) % 1 < 0.6:
            fl = R.text_layer("NO VALUE", R.font(26, mono=True), RED, tracking=5); lay.alpha_composite(fl, (w - fl.width - 34, 26))
    else:                                                                                       # back to life: the bid line
        n = sum(t >= at for at in AV_AT); k = R.ease_out((t - SHOCK) / 0.3)
        lo, hi = 3000, 7600; yv = lambda v: h * 0.74 - (v - lo) / (hi - lo) * (h * 0.44)
        pts = [(40, yv(3000))] + [(40 + (w - 120) * (at - SHOCK - 0.15) / 1.05, yv(PRICES[i + 1])) for i, at in enumerate(AV_AT[:n])]
        if n: pts.append((pts[-1][0] + 8, pts[-1][1]))
        steps = [pts[0]]
        for p in pts[1:]: steps += [(p[0], steps[-1][1]), p]
        glow = Image.new("RGBA", lay.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).line(steps, fill=VIOLET + (200,), width=14); lay.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))
        d.line(steps, fill=(225, 215, 255, 255), width=5)
        d.line([(40, yv(3000)), (w - 40, yv(3000))], fill=RED + (150,), width=2)
        m = R.text_layer("Mechanic: $3,000", R.font(24, mono=True), (255, 150, 160), tracking=1); lay.alpha_composite(m, (w - 40 - m.width, int(yv(3000)) + 10))
        lab = R.text_layer("BIDDERS", R.font(24, mono=True), (200, 190, 255), tracking=3); lay.alpha_composite(lab, (34, 22))
        v = R.text_layer(str(n), R.font(52, 700), WHITE); lay.alpha_composite(v, (34, 52))
        price = int(PRICES[n]) // 100 * 100
        pv = R.text_layer(f"${price:,}", R.font(52, 700), WHITE); lay.alpha_composite(pv, (w - 34 - pv.width, 34))
        if n: ex = steps[-1]; d.ellipse((ex[0] - 10, ex[1] - 10, ex[0] + 10, ex[1] + 10), fill=(255, 255, 255, 255))
        a *= 1 - R.clamp((t - (CLIP - 0.5)) / 0.3)
    R.paste_center(im, lay, (x0 + x1) / 2, (y0 + y1) / 2, a)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Second opinion?", "Get forty."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    w = R.ease_out((t - SHOCK) / 0.4) if t >= SHOCK else 0.0
    if w <= 0:
        im = S.look(fr, "clinic")
        if t >= FLAT: im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.25 * R.clamp((t - FLAT) / 0.5))   # the room dims
    elif w >= 1: im = S.look(fr, "dusk")
    else: im = Image.blend(S.look(fr, "clinic"), S.look(fr, "dusk"), w)
    im = S.zcrop(im, ZOOM + (1 - ZOOM) * w, FOCUS)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (560, 640))
    if CARD_IN <= t < SHOCK + 0.4:
        k = R.ease_out((t - CARD_IN) / 0.35); fly = R.clamp((t - SHOCK) / 0.35)
        R.paste_center(im, diag_card((t - PRICE_AT) / 0.3 if t >= PRICE_AT else 0), W / 2, 250 + (1 - k) * -40 - fly ** 2 * 600, R.clamp((t - CARD_IN) / 0.2) * (1 - fly))
    monitor(im, t, R.clamp(t / 0.4))
    for i, at in enumerate(AV_AT):                                                              # 40 bidders pop in over the car
        if t < at: continue
        s = (t - at) / 0.25; x, y = AV_POS[i]
        R.paste_center(im, AV_IM[i], x, y, R.clamp(s * 3) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), 0.5 + 0.5 * R.stamp(s) if s < 1 else 1.0)
    if t >= DIS: sparkle_burst(im, t, DIS, 900, 1180, ((-60, -40, 26), (60, -50, 18), (40, 40, 26)))
    draw_caps(im, t, CAPS, y=1700, size=62)
    if SHOCK <= t < SHOCK + 0.1: im = M.flash(im, 0.6 * (1 - (t - SHOCK) / 0.1), (230, 240, 255))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, 0.0),))
        S.tone(mx, 0.0, SHOCK, ((110, .3), (130.8, .2), (164.8, .14)), 0.045, 1.0)                 # A minor, cold
        S.hum(mx, 0.0, SHOCK, 0.02)
        b = 0.0
        while b < FLAT:                                                                            # monitor beep on every R peak
            at = b + 0.33 * PERIOD
            if not (0.9 < at < 1.35 or 3.7 < at < 4.7): S.beep(mx, at, 988, 0.09, 0.05)
            b += PERIOD
        S.beep(mx, FLAT, 988, SHOCK - FLAT - 0.05, 0.075)                                          # flatline, in the silence
        mx.thud(SHOCK, 0.6); y = mx.tt(0.25); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 18), SHOCK, 0.35)   # the jolt
        mx.whoosh(SHOCK + 0.02, 0.4, 0.25)
        S.tone(mx, SHOCK, CLIP, ((146.8, .3), (185, .22), (220, .2), (293.7, .1)), 0.05, 0.5)     # D major, alive
        for i, at in enumerate(AV_AT):
            if 6.55 < at < 7.15: continue                                                          # keep 'disagree' clean
            y = mx.tt(0.05); mx.fadd(np.sin(2 * np.pi * (1400 + 18 * i) * y) * np.exp(-y * 70), at, 0.018)
        mx.thud(7.2, 0.35); mx.shimmer(7.22, 1318.5, 0.09)
        mx.write("s4mech_audio.wav")
    render(frame, TOTAL, "s4mech_audio.wav", OUT)
