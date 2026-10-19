"""Auction short 05 (v3, quick): "The auction where the price goes down". The Dutch flower clock (Royal FloraHolland) and
Lebanon's slow-motion version (Code of Civil Procedure Art. 931: no bidders -> price cut, sale again 15-30 days later, until a buyer).
Run: python3 tools/lessons/lesson05.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson05_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "lofi", 5
XF = 0.16
SC = [("hook", True, 0.0, S("d1") - 0.1), ("clock", False, S("d1") - 0.1, S("n1") - 0.1), ("number", True, S("n1") - 0.1, S("l1") - 0.1),
      ("lebanon", False, S("l1") - 0.1, S("p1") - 0.1), ("payoff", True, S("p1") - 0.1, S("e2") - 0.15), ("outro", True, S("e2") - 0.15, TOTAL)]
T_PRESS = WT("d2", "press")

# ---------- drawings ----------
def clock_face(price, dark=True, s=640, frozen=False):
    """the flower clock: 100 dots round the rim, the lit dot is the price (in cents), a trail shows where it came from"""
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s / 2; r = s * 0.44
    d.ellipse((c - s * 0.49, c - s * 0.49, c + s * 0.49, c + s * 0.49), fill=((21, 25, 34) if dark else (255, 255, 255)) + (255,),
              outline=((40, 46, 60) if dark else (229, 230, 236)) + (255,), width=4)
    p = int(round(price * 100))
    for i in range(100):                                                         # 0 at the top, values run clockwise
        a = -np.pi / 2 + 2 * np.pi * i / 100; x, y = c + r * np.cos(a), c + r * np.sin(a)
        on = i == p; trail = p < i <= p + 12
        col = (RED_UI if frozen else VIOLET) if on else (LILAC if trail else ((60, 66, 86) if dark else (214, 216, 226)))
        al = 255 if on else (int(255 * (1 - (i - p) / 13)) if trail else 255); rr = s * (0.022 if on else 0.011)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col + (al,))
    lab = T("PRICE PER STEM", int(s * 0.04), D_MUTE if dark else (110, 116, 130), 700, True); im.alpha_composite(lab, (int(c - lab.width / 2), int(c - s * 0.2)))
    v = T(f"€0.{p:02d}", int(s * 0.2), (RED_UI if frozen else (D_INK if dark else L_INK)), 700); im.alpha_composite(v, (int(c - v.width / 2), int(c - s * 0.11)))
    return im

def flower(s=160, col=(236, 72, 153)):
    im = Image.new("RGBA", (s, int(s * 1.5)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s / 2
    d.line([(c, s * 0.5), (c, s * 1.45)], fill=(60, 150, 90, 255), width=int(s * 0.07))
    d.ellipse((c - s * 0.05, s * 0.85, c + s * 0.3, s * 1.0), fill=(70, 170, 100, 255))
    for i in range(6):
        a = 2 * np.pi * i / 6; x, y = c + s * 0.2 * np.cos(a), s * 0.4 + s * 0.2 * np.sin(a)
        d.ellipse((x - s * 0.17, y - s * 0.17, x + s * 0.17, y + s * 0.17), fill=col + (255,))
    d.ellipse((c - s * 0.12, s * 0.28, c + s * 0.12, s * 0.52), fill=(255, 214, 102, 255)); return im

def arrow_down(h=220, col=VIOLET, w=150):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((w * 0.34, 0, w * 0.66, h * 0.6), fill=col + (255,)); d.polygon([(0, h * 0.55), (w, h * 0.55), (w / 2, h)], fill=col + (255,)); return im

def price_at(t, t0, p0=0.95, rate=0.16, stop=None, floor=0.20):
    tt = (min(t, stop) if stop is not None else t) - t0
    return max(floor, p0 - rate * max(0, tt))

# ---------- scenes ----------
def sc_hook(t):
    im = bg(True); p = price_at(t, 0, 0.98, 0.12)
    put(im, lift(clock_face(p, True, 700), True), 540, 1000, 1, 0.97 + 0.03 * spring(t / 0.5))
    ta = WT("h1", "down,")
    if t >= ta - 0.1: put(im, arrow_down(200, VIOLET, 140), 900, 640 + 40 * eout((t - ta) / 0.4), ease((t - ta + 0.1) / 0.2))
    tu = WT("h1", "up.")
    if t >= tu - 0.05 and t < S("h2"):
        u = pill("up?", 40, (60, 66, 86), D_MUTE); put(im, u, 180, 640, ease((t - tu + 0.05) / 0.2)); strike(im, 140, 642, 225, eout((t - tu - 0.1) / 0.25), RED_UI, 8)
    tl_ = WT("h2", "Lebanon")
    if t >= tl_ - 0.1:                                                           # the open loop: Lebanon's version, revealed later
        k = spring((t - tl_ + 0.1) / 0.45); c = card(560, 150, True, 28); c.alpha_composite(chip("LEBANON", True, 26), (36, 52))
        tt = T("slow motion", 46, LILAC, 700) if t >= WT("h2", "slow-motion") - 0.05 else T("?", 46, D_MUTE, 700); c.alpha_composite(tt, (250, 44))
        put(im, lift(c, True), 540, 1560 + (1 - k) * 80, min(1, k * 1.5))
    return im

def sc_clock(t):
    im = bg(False); t0 = S("d1"); frozen = t >= T_PRESS
    p = price_at(t, t0, 0.95, 0.072, T_PRESS)
    w, h = 900, 1100; win = window(w, h, "Flower auction · Clock 4", False)
    win.alpha_composite(flower(110), (60, 110)); win.alpha_composite(T("Roses · lot of 400", 34, L_INK, 700), (200, 140)); win.alpha_composite(T("grower: Sami", 28, (110, 116, 130), 500), (200, 190))
    win.alpha_composite(head("sami", 60), (w - 110, 130))
    cf = clock_face(p, False, 560, frozen); win.alpha_composite(cf, (int(w / 2 - 280), 270))
    for i, who in enumerate(("nour", ("B", VIOLET), ("C", GREEN_APP))):           # buyers' keypads under the clock
        x = 90 + i * 260; hl = who == "nour" and frozen
        row = card(220, 190, False, 22, fill=(240, 235, 255) if hl else None); row.alpha_composite(head(who, 80), (70, 20))
        row.alpha_composite(pill("BUY" if not hl else "BOUGHT", 26, VIOLET if hl else (236, 237, 242), (255, 255, 255) if hl else (96, 102, 116)), (40 if not hl else 22, 118))
        win.alpha_composite(row, (x, 870))
    put(im, lift(win), 540, 1110, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    bx, by = 540 - 450 + 90 + 110, 1110 - 550 + 870 + 136                           # Nour's BUY button on screen
    if T_PRESS - 0.6 <= t < T_PRESS + 0.6:
        k = eout((t - (T_PRESS - 0.6)) / 0.6); put(im, cursor(), bx + 160 * (1 - k) + 20, by + 140 * (1 - k) + 30)
    ripple(im, bx, by, (t - T_PRESS) / 0.5)
    if frozen and t < WT("d2", "Too") - 0.05: stamp_at(im, big_stamp("SOLD", RED_UI, 90, -8), 540, 1290, t, T_PRESS + 0.05)
    ts, tl_ = WT("d2", "soon,"), WT("d2", "late,")
    if ts - 0.1 <= t < tl_ - 0.1: put(im, pill("too soon  →  you overpay", 40, RED_UI), 540, 520, ease((t - ts + 0.1) / 0.2), 0.85 + 0.15 * spring((t - ts + 0.1) / 0.4))
    if t >= tl_ - 0.1: put(im, pill("too late  →  gone", 40, (60, 66, 86)), 540, 520, ease((t - tl_ + 0.1) / 0.2), 0.85 + 0.15 * spring((t - tl_ + 0.1) / 0.4))
    footnote(im, "Prices are illustrative · how the clock works: Royal FloraHolland")
    return im

def sc_number(t):
    im = bg(True); t0 = S("n1")
    if t < S("n2") - 0.1:
        tb = WT("n1", "5 billion"); v = roll(t, tb - 0.35, 0.8, 0, 5)
        c = stat("Sold on the clock in 2025", f"{v:.1f} billion" if v < 4.95 else "5 billion", "almost · flowers and plants", 900, True, 150)
        put(im, lift(c, True), 540, 1000, ease((t - t0 + 0.12) / 0.25), 0.95 + 0.05 * spring((t - t0 + 0.12) / 0.5))
        for i in range(5):
            k = spring((t - WT("n1", "flowers") - i * 0.09) / 0.4)
            if k > 0: put(im, flower(110, [(236, 72, 153), LILAC, (255, 255, 255), VIOLET, (236, 72, 153)][i]), 540 + (i - 2) * 160, 1420 + (1 - k) * 60, min(1, k * 1.5))
        footnote(im, "Royal FloraHolland, Auction developments 2025/2026 (Jan 2026)", True)
    else:
        tn = S("n2"); wilt = clamp((t - WT("n2", "wait,")) / 0.8)
        f = flower(260).rotate(-28 * eout(wilt), expand=True, resample=Image.BICUBIC)
        put(im, f, 540, 1000, ease((t - tn + 0.1) / 0.25))
        if t >= WT("n2", "falling") - 0.1: put(im, arrow_down(200, VIOLET, 140), 800, 900 + 40 * eout((t - WT("n2", "falling")) / 0.5), ease((t - WT("n2", "falling") + 0.1) / 0.2))
        stamp_at(im, big_stamp("SOLD FAST", LILAC, 90, -7), 540, 1470, t, WT("n2", "fast."))
        footnote(im, "Known worldwide as a Dutch auction · Royal FloraHolland", True)
    return im

def sc_lebanon(t):
    im = bg(False); t0 = S("l1")
    tcut, tback, tbid = WT("l1", "cut,"), WT("l2", "back"), WT("l2", "bids.")
    steps = [1.0, 0.8, 0.64]                                                    # illustrative levels
    lvl = 0 if t < tcut else (1 if t < WT("l2", "until") else 2)
    w, h = 900, 1060; c = card(w, h, False, 30); d = ImageDraw.Draw(c)
    c.alpha_composite(T("COURT SALE · SEIZED GOODS", 26, (110, 116, 130), 700, True), (50, 46))
    c.alpha_composite(radio(220), (50, 110))
    c.alpha_composite(T("The price", 30, (110, 116, 130), 500), (320, 140))
    word = ["Opening", "Cut", "Cut again"][lvl]; tl0 = [t0, tcut, WT("l2", "until")][lvl]
    put(c, T(word, 96, VIOLET, 700), 320 + T(word, 96, VIOLET, 700).width / 2, 240, ease((t - tl0 + 0.05) / 0.2), 0.85 + 0.15 * spring((t - tl0 + 0.05) / 0.4))
    for i in range(3):                                                          # sessions: a staircase going down
        if i > lvl: break
        x = 60 + i * 270; top = 420 + (1 - steps[i]) * 600; bh = 960 - top
        k = eout((t - (t0 if i == 0 else (tcut if i == 1 else WT("l2", "until")))) / 0.35)
        d.rounded_rectangle((x, 960 - bh * k, x + 230, 960), radius=18, fill=((236, 237, 242) if i < 2 or t < tbid else (240, 235, 255)) + (255,))
        lab = T(f"Session {i + 1}", 28, L_INK, 700); c.alpha_composite(lab, (x + 115 - lab.width // 2, int(960 - bh * k) + 24))
        if i < 2 and (i < lvl or (i == 0 and t >= WT("l1", "bids"))):
            nb = T("no bids", 26, RED_UI, 700); c.alpha_composite(nb, (x + 115 - nb.width // 2, int(960 - bh * k) + 70))
    if t >= tback - 0.1 and lvl >= 1: c.alpha_composite(chip("+15 to 30 days", False, 30), (300, 980))
    put(im, lift(c), 540, 1090, ease((t - t0 + 0.12) / 0.25), 0.95 + 0.05 * spring((t - t0 + 0.12) / 0.5))
    if t >= tbid - 0.1:
        k = spring((t - tbid + 0.1) / 0.45); put(im, head("nour", 120), 540 - 450 + 60 + 540 + 115, 1100 + (1 - k) * 40, min(1, k * 1.5))
        stamp_at(im, big_stamp("SOLD", VIOLET, 70, -8), 540 - 450 + 60 + 540 + 115, 1460, t, tbid + 0.15)
    footnote(im, "Code of Civil Procedure, Art. 931 · bar heights are illustrative")
    return im

def sc_payoff(t):
    im = bg(True); t0 = S("p1")
    for i, (lab, sub, x) in enumerate((("FAST", "Holland's clock", 300), ("SLOW", "Lebanon's courts", 780))):
        k = spring((t - t0 - i * 0.15 + 0.1) / 0.45)
        if k <= 0: continue
        c = card(380, 200, True, 26); c.alpha_composite(T(lab, 64, LILAC if i == 0 else D_INK, 700), (34, 30)); c.alpha_composite(T(sub, 28, D_MUTE, 500), (34, 120))
        put(im, lift(c, True), x, 700 + (1 - k) * 60, min(1, k * 1.5))
    td = WT("p1", "down"); y = 960 + 420 * eout((t - td + 0.2) / 0.7)
    tg = pill("€ price", 44, VIOLET); put(im, tg, 540, y, ease((t - t0) / 0.25))
    put(im, head("nour", 150), 540, 1520, ease((t - WT("p1", "meet")) / 0.2) if t >= WT("p1", "meet") - 0.05 else 0)
    ripple(im, 540, 1440, (t - WT("p1", "buyer.")) / 0.5)
    stamp_at(im, big_stamp("SOLD", VIOLET, 80, -8), 540, 1720, t, WT("p1", "buyer.") + 0.1)
    return im

def sc_outro(t):
    im = bg(True); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 14, BLUE), (540, 27, VIOLET), (750, 8, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "clock": sc_clock, "number": sc_number, "lebanon": sc_lebanon, "payoff": sc_payoff, "outro": sc_outro}

def scene_at(i, t):
    name, dark, t0, t1 = SC[i]; im = FN[name](t)
    im = camera(im, t, t0, t1, 1.0, 1.03, (540, 980)); CAP.draw(im, t, dark)
    return im

def frame(t):
    for i, (name, dark, t0, t1) in enumerate(SC):
        if t0 <= t < t1 or i == len(SC) - 1:
            if i > 0 and t < t0 + XF: return whip(scene_at(i - 1, t), scene_at(i, t), (t - (t0 - XF)) / (2 * XF))
            if i < len(SC) - 1 and t > t1 - XF: return whip(scene_at(i, t), scene_at(i + 1, t), (t - (t1 - XF)) / (2 * XF))
            return scene_at(i, t).convert("RGB")
    return Image.new("RGB", (W, H))

def audio(path):
    s = Snd(TOTAL)
    for _, _, t0, _ in SC[1:]: s.whoosh(t0 - 0.18, 0.36, 0.06)
    for i in range(int(S("d1") / 0.25)): s.tick(0.1 + i * 0.25, 0.008, 2200)           # the clock ticking down
    s.pop(WT("h1", "down,"), 0.04, 600); s.pop(WT("h2", "Lebanon"), 0.04, 700)
    for i in range(int((T_PRESS - S("d1")) / 0.25)): s.tick(S("d1") + i * 0.25, 0.008, 2200)
    s.thud(T_PRESS + 0.05, 0.08); s.pop(WT("d2", "soon,"), 0.04, 500); s.pop(WT("d2", "late,"), 0.04, 450)
    for i in range(10): s.tick(WT("n1", "5 billion") - 0.35 + i * 0.08, 0.012, 2400)
    s.ding(WT("n1", "5 billion") + 0.45, 1318, 0.03); s.thud(WT("n2", "fast."), 0.07)
    s.pop(WT("l1", "cut,"), 0.05, 500); s.pop(WT("l2", "until"), 0.05, 450); s.ding(WT("l2", "bids."), 1568, 0.03); s.thud(WT("l2", "bids.") + 0.15, 0.07)
    s.pop(S("p1"), 0.04, 650); s.ding(WT("p1", "buyer."), 1175, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson05_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
