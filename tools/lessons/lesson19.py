"""Auction short 19 (v3, quick, who: Sami): "Afraid it sells for nothing?". Problem: Sami fears one person bids $10 and takes his car.
Reframe (one fact): in Australia, where homes go to auction every week, the seller first sets a reserve, "the lowest price a seller is
prepared to accept"; if bids don't reach it the home doesn't sell, it's "passed in", and the top bidder only gets the first right to
negotiate (Consumer Affairs Victoria). Fix: the seller sets the floor, the buyers set the rest.
Takeaway: a reserve is a floor, not a ceiling. Loop: ends on the same $10 bid on Sami's car the video opens on.
Run: python3 tools/lessons/lesson19.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson19_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "pluck", 19
XF = 0.16
SC = [("hook", False, 0.0, S("r1") - 0.1), ("reserve", True, S("r1") - 0.1, S("r3") - 0.1), ("passed", False, S("r3") - 0.1, S("f1") - 0.1),
      ("fix", True, S("f1") - 0.1, S("tk") - 0.1), ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
BIDDER = ("K", GREEN_APP)
RES = 0.62   # where the reserve line sits on the meters (illustrative)

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def car(w=420, col=BLUE):
    """a simple side-view hatchback (same as lessons 10 and 18)"""
    S2 = 2; h = int(w * 0.5); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    d.rounded_rectangle((W2 * 0.03, H2 * 0.42, W2 * 0.97, H2 * 0.78), radius=int(H2 * 0.12), fill=col + (255,))
    d.polygon([(W2 * 0.2, H2 * 0.45), (W2 * 0.32, H2 * 0.12), (W2 * 0.68, H2 * 0.12), (W2 * 0.84, H2 * 0.45)], fill=col + (255,))
    d.polygon([(W2 * 0.27, H2 * 0.43), (W2 * 0.35, H2 * 0.2), (W2 * 0.49, H2 * 0.2), (W2 * 0.49, H2 * 0.43)], fill=(200, 220, 255, 255))
    d.polygon([(W2 * 0.53, H2 * 0.43), (W2 * 0.53, H2 * 0.2), (W2 * 0.66, H2 * 0.2), (W2 * 0.77, H2 * 0.43)], fill=(200, 220, 255, 255))
    for x in (0.25, 0.76):
        d.ellipse((W2 * x - H2 * 0.2, H2 * 0.58, W2 * x + H2 * 0.2, H2 * 0.98), fill=(24, 26, 32, 255))
        d.ellipse((W2 * x - H2 * 0.09, H2 * 0.69, W2 * x + H2 * 0.09, H2 * 0.87), fill=SILVER + (255,))
    d.rounded_rectangle((W2 * 0.9, H2 * 0.5, W2 * 0.96, H2 * 0.58), radius=6, fill=(255, 230, 140, 255))
    return im.resize((w, h), Image.LANCZOS)

def house(w=300, body=BLUE, roof=(24, 28, 44), win=(255, 255, 255)):
    """a simple generic house (same as lesson 14)"""
    S2 = 2; h = int(w * 0.92); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    d.polygon([(W2 * 0.02, H2 * 0.44), (W2 * 0.5, H2 * 0.02), (W2 * 0.98, H2 * 0.44)], fill=roof + (255,))
    d.rectangle((W2 * 0.72, H2 * 0.08, W2 * 0.82, H2 * 0.3), fill=roof + (255,))
    d.rounded_rectangle((W2 * 0.1, H2 * 0.4, W2 * 0.9, H2 * 0.99), radius=10, fill=body + (255,))
    d.rounded_rectangle((W2 * 0.42, H2 * 0.62, W2 * 0.58, H2 * 0.99), radius=10, fill=roof + (255,))
    for x0 in (0.17, 0.66):
        d.rounded_rectangle((W2 * x0, H2 * 0.54, W2 * (x0 + 0.17), H2 * 0.74), radius=8, fill=win + (235,))
    return im.resize((w, h), Image.LANCZOS)

def car_auction(t, status=None):
    """Sami's car at auction with one $10 bid; shared by the hook and the loop so the replay is seamless"""
    w, h = 880, 860; win = window(w, h, "Live auction · Sami's car", False)
    c = car(520); win.alpha_composite(c, (int(w / 2 - c.width / 2), 110))
    row = card(780, 200, False, 28, fill=(246, 246, 250))
    row.alpha_composite(head(BIDDER, 110), (30, 45))
    row.alpha_composite(T("Top bid", 30, GREY_TXT, 600), (170, 40)); row.alpha_composite(T("$10", 80, L_INK, 700), (170, 78))
    win.alpha_composite(row, (50, 420))
    st = status or pill("Ends in 00:03", 34, (236, 237, 242), RED_UI, 26, 12)
    win.alpha_composite(st, (int(w / 2 - st.width / 2), 680))
    return win

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); tc = WT("h1", "car?"); ts = WT("h2", "stops")
    put(im, lift(car_auction(t)), 540, 1060, 1, 0.97 + 0.03 * spring(t / 0.5))
    put(im, head("sami", 150), 190, 1600, 1)
    if t >= tc - 0.05:
        stamp_at(im, big_stamp("SOLD?", RED_UI, 110, -8), 690, 1560, t, tc - 0.05)
        if t >= ts - 0.05:
            strike(im, 520, 1565, 870, eout((t - ts + 0.05) / 0.3), GREEN_UI, 12)
    footnote(im, "Car, bid and names are illustrative", False, 1850)
    return im

def meter(w, h, dark, fill_k=0.0, fill_col=VIOLET, res_k=1.0, shade_k=0.0, label=None):
    """a tall price bar with the reserve line; heights are illustrative"""
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, x1, top, base = w / 2 - 90, w / 2 + 90, 20, h - 20
    d.rounded_rectangle((x0, top, x1, base), radius=24, fill=((30, 36, 52) if dark else (236, 237, 242)) + (255,))
    if shade_k > 0:
        yr = base - (base - top) * RES
        d.rounded_rectangle((x0, yr, x1, base), radius=24, fill=(RED_UI + (int(70 * clamp(shade_k)),)))
    if fill_k > 0:
        yf = base - (base - top) * fill_k
        d.rounded_rectangle((x0, yf, x1, base), radius=24, fill=fill_col + (255,))
    if res_k > 0:
        yr = base - (base - top) * RES; xe = x0 - 60 + (x1 - x0 + 120) * eout(res_k)
        for xx in range(int(x0 - 60), int(xe), 34): d.line([(xx, yr), (min(xx + 20, xe), yr)], fill=GREEN_UI + (255,), width=8)
        if res_k > 0.6:
            p = pill("RESERVE", 30, GREEN_UI, padx=18, pady=8); lay.alpha_composite(fade_in(p, (res_k - 0.6) / 0.4), (int(x1 + 70), int(yr - p.height / 2)))
    if label is not None and fill_k > 0:
        yf = base - (base - top) * fill_k; lay.alpha_composite(label, (int(x0 - 50 - label.width), int(yf - label.height / 2)))
    return lay

def sc_reserve(t):
    im = bg(True); t0 = S("r1"); tr = WT("r1", "reserve."); ta = WT("r2", "lowest")
    w, h = 880, 1080; win = window(w, h, "Home auction · Australia", True)
    hs = house(230, BLUE, (24, 28, 44)); win.alpha_composite(hs, (int(w / 2 - hs.width / 2), 100))
    m = meter(w, 700, True, 0, VIOLET, (t - tr + 0.15) / 0.5, (t - ta) / 0.5)
    win.alpha_composite(m, (0, 350))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win, True), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= ta - 0.05:
        kp = spring((t - ta + 0.05) / 0.4)
        put(im, pill("Below it: no sale", 40, RED_UI, padx=30, pady=14), 540, 1740 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    footnote(im, "Source: Consumer Affairs Victoria (Australia)", True, 1850)
    return im

def sc_passed(t):
    im = bg(False); t0 = S("r3"); tb = WT("r3", "bids"); tn = WT("r3", "doesn't"); tp = WT("r3", "passed"); tf = WT("r4", "first")
    w, h = 880, 1000; win = window(w, h, "Home auction · Australia", False)
    fk = roll(t, tb - 0.1, tn - tb + 0.2, 0, RES * 0.78)
    col = VIOLET if t < tn else (RED_UI if t < tp - 0.05 else (196, 199, 208))
    lab = T("Top bid", 34, GREY_TXT, 700)
    m = meter(w, 820, False, fk, col, 1.0, 0, lab if fk > 0.05 else None); win.alpha_composite(m, (0, 120))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    stamp_at(im, big_stamp("PASSED IN", RED_UI, 100, -8), 540, 1360, t, tp - 0.05)
    if t >= tf - 0.15:
        kp = spring((t - tf + 0.15) / 0.4); r = pill("Top bidder: first chance to negotiate", 36, VIOLET, padx=28, pady=14)
        put(im, r, 540, 1720 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    footnote(im, "Source: Consumer Affairs Victoria · bar heights illustrative", False, 1850)
    return im

def sc_fix(t):
    im = bg(True); t0 = S("f1"); tf = WT("f1", "floor."); tb = WT("f1", "buyers"); tr = WT("f1", "rest.")
    w, h = 880, 1080; win = window(w, h, "Who sets the price?", True)
    d = ImageDraw.Draw(win); x0, x1, top, base = w / 2 - 110, w / 2 + 110, 120, h - 60
    d.rounded_rectangle((x0, top, x1, base), radius=24, fill=(30, 36, 52, 255))
    yr = base - (base - top) * RES
    kf = eout((t - tf + 0.35) / 0.4)
    if kf > 0:
        yy = base - (base - yr) * kf; d.rounded_rectangle((x0, yy, x1, base), radius=24, fill=BLUE + (255,))
        win.alpha_composite(fade_in(head("sami", 120), kf), (int(x0 - 170), int((yr + base) / 2 - 60)))
        lb = T("Floor", 44, D_INK, 700); win.alpha_composite(fade_in(lb, kf), (int(x1 + 40), int((yr + base) / 2 - lb.height / 2)))
    cols = (VIOLET, GREEN_APP, LILAC); seg = (yr - top) / 3
    for i in range(3):
        ki = eout((t - tb + 0.1 - i * 0.22) / 0.3)
        if ki <= 0: continue
        y1 = yr - seg * i; y0 = y1 - seg * ki
        d.rectangle((x0, y0 + 4, x1, y1 - 4), fill=cols[i] + (255,))
        p = paddle([17, 1, 7][i], cols[i], 70); win.alpha_composite(fade_in(p, ki), (int(x0 - 150 + (i % 2) * 40), int(y1 - seg / 2 - p.height / 2)))
    if t >= tr - 0.1:
        lb = T("The rest", 44, D_INK, 700); win.alpha_composite(fade_in(lb, (t - tr + 0.1) / 0.3), (int(x1 + 40), int((top + yr) / 2 - lb.height / 2)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win, True), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Bar heights are illustrative", True, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tn = WT("tk", "never"); tfl = WT("tk", "floor,")
    st = pill("Reserve not met", 34, (236, 237, 242), GREEN_UI, 26, 12) if t >= tn else None
    put(im, lift(car_auction(t, st)), 540, 1060, ease((t - t0) / 0.2))
    put(im, head("sami", 150), 190, 1600, 1)
    stamp_at(im, big_stamp("NOT SOLD", GREEN_UI, 96, -8), 690, 1560, t, tn - 0.05)
    footnote(im, "Car, bid and names are illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 17, BLUE), (540, 1, VIOLET), (750, 7, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "reserve": sc_reserve, "passed": sc_passed, "fix": sc_fix, "loop": sc_loop, "outro": sc_outro}

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
    s.thud(WT("h1", "car?") - 0.05, 0.08); s.ding(WT("h2", "stops") - 0.05, 1568, 0.03)
    s.pop(WT("r1", "reserve.") - 0.15, 0.04, 600); s.pop(WT("r2", "lowest") - 0.05, 0.035, 520)
    for i in range(6): s.tick(WT("r3", "bids") + i * 0.1, 0.018)
    s.thud(WT("r3", "passed") - 0.05, 0.08); s.pop(WT("r4", "first") - 0.15, 0.035, 640)
    s.pop(WT("f1", "floor.") - 0.3, 0.04, 520)
    for j in range(3): s.pop(WT("f1", "buyers") - 0.1 + j * 0.22, 0.03, 560 + j * 50)
    s.ding(WT("f1", "rest.") - 0.1, 1318, 0.03)
    s.thud(WT("tk", "never") - 0.05, 0.06); s.ding(WT("tk", "floor,") - 0.05, 1568, 0.025)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson19_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
