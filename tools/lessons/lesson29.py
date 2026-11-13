"""Auction short 29 (v3, standard, who: Sami): "How to sell like a pro". Sami's five rules, one per beat, each carried by one
sourced fact or rule: 1 start low (179 rugs / 87 cameras: lower starts drew more bidders and ended higher, Ku, Galinsky &
Murnighan 2006); 2 set a reserve, the floor, below it the item is passed in (Consumer Affairs Victoria); 3 one more buyer beats
the best negotiation (Bulow & Klemperer 1996); 4 a deadline: 41% of deals in the last 30 seconds (Roth, Murnighan & Schoumaker
1988); 5 buyers from anywhere: 81% of Christie's bids placed online in 2024. Takeaway: don't guess the price; set the rules and
let them bid. Opens and ends on the same phone (Sami's camera listing, illustrative and labelled) so the replay loops.
Run: python3 tools/lessons/lesson29.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson29_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
import math
STYLE, SEED = "pluck", 29
XF = 0.16
SC = [("hook", False, 0.0, S("r1") - 0.1), ("r1", True, S("r1") - 0.1, S("r2") - 0.1), ("r2", False, S("r2") - 0.1, S("r3") - 0.1),
      ("r3", True, S("r3") - 0.1, S("r4") - 0.1), ("r4", False, S("r4") - 0.1, S("r5") - 0.1), ("r5", True, S("r5") - 0.1, S("tk") - 0.1),
      ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
BIDDERS = (("K", VIOLET), ("M", GREEN_APP), ("R", (150, 156, 170)), ("J", BLUE), ("T", LILAC))

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def dim(layer, a):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * a))); return layer

# ---------- drawings ----------
def camera_icon(w=170, col=BLUE, ink=(24, 28, 44)):
    S2 = 2; W2 = w * S2; im = Image.new("RGBA", (W2, W2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((W2 * 0.3, W2 * 0.2, W2 * 0.55, W2 * 0.32), radius=int(W2 * 0.03), fill=col + (255,))
    d.rounded_rectangle((W2 * 0.06, W2 * 0.28, W2 * 0.94, W2 * 0.8), radius=int(W2 * 0.08), fill=col + (255,))
    c = (W2 * 0.5, W2 * 0.54); r = W2 * 0.2
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=(255, 255, 255, 255), outline=ink + (255,), width=int(W2 * 0.03))
    r2 = r * 0.55; d.ellipse((c[0] - r2, c[1] - r2, c[0] + r2, c[1] + r2), fill=ink + (255,))
    d.ellipse((W2 * 0.76, W2 * 0.36, W2 * 0.84, W2 * 0.44), fill=(255, 255, 255, 255))
    return im.resize((w, w), Image.LANCZOS)

def tick(s=60, col=GREEN_UI):
    S2 = 3; im = Image.new("RGBA", (s * S2, s * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); z = s * S2
    d.ellipse((0, 0, z - 1, z - 1), fill=col + (255,))
    d.line([(z * 0.27, z * 0.53), (z * 0.44, z * 0.7), (z * 0.75, z * 0.33)], fill=(255, 255, 255, 255), width=int(z * 0.1), joint="curve")
    return im.resize((s, s), Image.LANCZOS)

def numeral(n, text, dark):
    s = 120; c = Image.new("RGBA", (s, s), (0, 0, 0, 0)); ImageDraw.Draw(c).ellipse((0, 0, s - 1, s - 1), fill=BLUE + (255,))
    nt = T(str(n), 76, (255, 255, 255), 700); c.alpha_composite(nt, (int(s / 2 - nt.width / 2), int(s / 2 - nt.height / 2 - 4)))
    tt = T(text, 64, D_INK if dark else L_INK, 700); w = s + 30 + tt.width
    im = Image.new("RGBA", (w, s), (0, 0, 0, 0)); im.alpha_composite(c, (0, 0)); im.alpha_composite(tt, (s + 30, int(s / 2 - tt.height / 2 - 4)))
    return im

def put_numeral(im, n, text, dark, t, t0):
    k = spring((t - t0 + 0.05) / 0.4)
    if k > 0: put(im, numeral(n, text, dark), 540, 600 + (1 - k) * 30, min(1, k * 1.5), 0.9 + 0.1 * k)

def sell_phone(t, struck=0.0, by_bidders=0.0, ticks_k=None):
    """Sami's phone: his camera listing. Shared by the hook and the loop so the replay is seamless."""
    pw, ph = 640, 900; p = phone(pw, ph, False)
    lc = card(560, 250, False, 26, fill=(246, 247, 251)); lc.alpha_composite(camera_icon(170), (30, 40))
    lc.alpha_composite(T("Camera · vintage", 34, L_INK, 600), (230, 40))
    lc.alpha_composite(T("MY PRICE", 22, GREY_TXT, 700, True), (230, 96))
    pt = T("$???", 84, L_INK if struck <= 0 else GREY_TXT, 700); lc.alpha_composite(pt, (230, 122))
    if struck > 0: ImageDraw.Draw(lc).line([(226, 176), (226 + (pt.width + 8) * struck, 176)], fill=RED_UI + (255,), width=8)
    p.alpha_composite(lc, (40, 100))
    p.alpha_composite(T("PRICE SET BY", 22, GREY_TXT, 700, True), (60, 390))
    if by_bidders > 0:
        bp = fade_in(pill("the bidders", 44, GREEN_UI, padx=24, pady=12), by_bidders); p.alpha_composite(bp, (60, 430))
    p.alpha_composite(head("sami", 120), (pw - 60 - 120, 400))
    p.alpha_composite(T("MY RULES", 22, GREY_TXT, 700, True), (60, 590))
    for i in range(5):
        x = 60 + i * 108; y = 640
        ImageDraw.Draw(p).ellipse((x, y, x + 80, y + 80), outline=(214, 216, 224, 255), width=4)
        nt = T(str(i + 1), 36, GREY_TXT, 700); p.alpha_composite(nt, (int(x + 40 - nt.width / 2), int(y + 40 - nt.height / 2 - 2)))
        if ticks_k is not None:
            kk = ticks_k(i)
            if kk > 0: p.alpha_composite(fade_in(tick(84), kk), (x - 2, y - 2))
    return p

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); tp = WT("h1", "pick"); tb = WT("h1", "buyers"); t2 = S("h2") - 0.05; tf = WT("h2", "five"); tw = WT("h2", "backwards")
    kout = ease((t - t2) / 0.3)
    if kout < 1:
        p = sell_phone(t, eout((t - tp) / 0.35) if t >= tp else 0, spring((t - tb + 0.05) / 0.35) if t >= tb - 0.05 else 0)
        put(im, lift(p), 540, 1150 - 40 * kout, 1 - kout, 0.97 + 0.03 * spring(t / 0.5))
        stamp_at(im, big_stamp("LET THEM BID", BLUE, 88, -8), 560, 1650, t, WT("h1", "do.") - 0.02)
    if t >= t2:
        for i in range(5):
            k = spring((t - tf + 0.1 - i * 0.12) / 0.4)
            if k <= 0: continue
            s = 150; c = Image.new("RGBA", (s, s), (0, 0, 0, 0))
            first = i == 0 and t >= tw - 0.1
            ImageDraw.Draw(c).ellipse((0, 0, s - 1, s - 1), fill=(BLUE if first else (236, 237, 242)) + (255,))
            nt = T(str(i + 1), 84, (255, 255, 255) if first else L_INK, 700); c.alpha_composite(nt, (int(s / 2 - nt.width / 2), int(s / 2 - nt.height / 2 - 4)))
            put(im, c, 140 + i * 200, 1040 + (1 - k) * 40, min(1, k * 1.5), 0.85 + 0.15 * k)
        put(im, head("sami", 170), 540, 1340, ease((t - t2) / 0.3))
        kl = spring((t - tw + 0.1) / 0.4)
        if kl > 0: put(im, pill("sounds backwards", 44, BLUE, padx=30, pady=14), 300, 1200 + (1 - kl) * 20, min(1, kl * 1.5))
        footnote(im, "Five rules · the camera, prices and timer in this video are illustrative", False, 1850)
    else:
        footnote(im, "Camera, prices and names are illustrative", False, 1850)
    return im

def sc_r1(t):
    im = bg(True); t0 = S("r1"); tb = S("r1b"); tm = WT("r1b", "more"); th = WT("r1b", "higher.")
    put_numeral(im, 1, "Start low", True, t, t0)
    if t < tb - 0.05:
        k = spring((t - WT("r1", "low.") + 0.1) / 0.4)
        if k > 0:
            c = stat("Starting price", "$1", "", 620, True, 170, LILAC); put(im, lift(c, True), 540, 1120 + (1 - k) * 30, min(1, k * 1.5))
        return foot1(im)
    w, h = 880, 640; win = window(w, h, "Same item · two starting prices", True)
    rows = (("High start", 2, "$", False), ("Low start", 5, "$$$", True))
    for i, (nm, nb, fin, low) in enumerate(rows):
        kr = spring((t - tb + 0.1 - i * 0.25) / 0.35)
        if kr <= 0: continue
        r = card(780, 200, True, 26, fill=(36, 42, 60)); r.alpha_composite(T(nm, 42, D_INK, 700), (30, 30))
        nshow = nb if not low else (2 if t < tm - 0.1 else min(5, 2 + int((t - tm + 0.1) / 0.15)))
        for j in range(nshow): r.alpha_composite(head(BIDDERS[j], 70), (30 + j * 58, 100))
        if t >= th - 0.1:
            kp = spring((t - th + 0.1 - (0 if low else 0.1)) / 0.35)
            pp = fade_in(pill("ended higher" if low else "ended lower", 40, GREEN_UI if low else (70, 76, 96), padx=22, pady=10), kp)
            r.alpha_composite(pp, (780 - 30 - pp.width, int(100 - pp.height / 2 + 20)))
        win.alpha_composite(fade_in(r, kr), (50, 110 + i * 240))
    k = ease((t - tb + 0.15) / 0.25); put(im, lift(win, True), 540, 1180, k, 0.96 + 0.04 * spring((t - tb + 0.15) / 0.5))
    if t >= th - 0.1: select_box(im, (540 - 440 + 50, 1180 - 320 + 350, 540 - 440 + 830, 1180 - 320 + 550), eout((t - th + 0.1) / 0.3))
    return foot1(im)

def foot1(im):
    footnote(im, "Ku, Galinsky & Murnighan, J. Pers. Soc. Psychol., 2006 · 179 rugs and 87 cameras", True, 1820)
    footnote(im, "Prices and bidder counts in the video are illustrative", True, 1858)
    return im

def sc_r2(t):
    im = bg(False); t0 = S("r2"); tr = WT("r2", "reserve."); tf = WT("r2", "floor."); tn = WT("r2", "doesn't")
    put_numeral(im, 2, "A reserve", False, t, t0)
    w, h = 880, 620; win = window(w, h, "Live auction · Camera · vintage", False)
    price = int(roll(t, tr, tn - tr, 60, 260) // 10 * 10)
    win.alpha_composite(T("HIGHEST BID", 24, GREY_TXT, 700, True), (60, 100))
    win.alpha_composite(T(money(price), 110, L_INK, 700), (60, 136))
    x0, x1, yb = 60, w - 60, 380; d = ImageDraw.Draw(win)
    d.rounded_rectangle((x0, yb, x1, yb + 50), radius=25, fill=(230, 231, 238, 255))
    fr = price / 500; d.rounded_rectangle((x0, yb, x0 + max(50, (x1 - x0) * fr), yb + 50), radius=25, fill=BLUE + (255,))
    xr = x0 + (x1 - x0) * 0.6; kr = clamp((t - tr + 0.1) / 0.3)
    if kr > 0:
        d.line([(xr, yb - 40), (xr, yb + 90)], fill=L_INK + (int(255 * kr),), width=6)
        rl = T("RESERVE", 26, L_INK, 700, True); win.alpha_composite(fade_in(rl, kr), (int(xr - rl.width / 2), yb + 100))
    if t >= tf - 0.1:
        fl = fade_in(pill("your floor", 30, VIOLET, padx=18, pady=8), spring((t - tf + 0.1) / 0.3)); win.alpha_composite(fl, (int(xr - fl.width / 2), yb - 100))
    if t >= tn - 0.05:
        kn = spring((t - tn + 0.05) / 0.35); pn = fade_in(pill("NOT SOLD", 40, RED_UI, padx=24, pady=10), kn); win.alpha_composite(pn, (w - 60 - pn.width, 150))
    k = ease((t - tr + 0.2) / 0.25); put(im, lift(win), 540, 1150, k, 0.96 + 0.04 * spring((t - tr + 0.2) / 0.5))
    footnote(im, "Below the reserve the item is “passed in” · Consumer Affairs Victoria", False, 1820)
    footnote(im, "Prices illustrative", False, 1858)
    return im

def sc_r3(t):
    im = bg(True); t0 = S("r3"); to = WT("r3", "one"); te = WT("r3", "extra"); tb = WT("r3", "best")
    put_numeral(im, 3, "One more buyer", True, t, t0)
    for j in range(3):
        k = spring((t - to + 0.1 - j * 0.1) / 0.35)
        if k > 0: put(im, head(BIDDERS[j], 130), 270 + j * 180, 900 + (1 - k) * 30, min(1, k * 1.5))
    kp = spring((t - WT("r3", "buyer") + 0.05) / 0.4)
    if kp > 0:
        put(im, head(BIDDERS[3], 130), 810, 900 + (1 - kp) * 30, min(1, kp * 1.5), 0.8 + 0.2 * kp)
        put(im, pill("+1", 36, GREEN_UI, padx=16, pady=6), 870, 830, min(1, kp * 1.5))
    if t >= te - 0.1:
        w, h = 880, 480; c = card(w, h, True, 30)
        for i, (lab, frac, col, ts) in enumerate((("Best negotiation", 0.55, (90, 96, 120), te - 0.1), ("Auction + 1 bidder", 0.85, GREEN_UI, tb - 0.1))):
            kb = eout((t - ts) / 0.5)
            if kb <= 0: continue
            c.alpha_composite(T(lab, 38, D_INK, 700), (50, 50 + i * 200))
            ImageDraw.Draw(c).rounded_rectangle((50, 110 + i * 200, 50 + max(40, (w - 100) * frac * kb), 170 + i * 200), radius=30, fill=col + (255,))
        k = ease((t - te + 0.15) / 0.25); put(im, lift(c, True), 540, 1360, k, 0.96 + 0.04 * spring((t - te + 0.15) / 0.5))
    footnote(im, "Bulow & Klemperer, American Economic Review, 1996 · bar lengths illustrative", True, 1858)
    return im

def sc_r4(t):
    im = bg(False); t0 = S("r4"); td = WT("r4", "deadline."); tp = WT("r4", "41%"); tl = WT("r4", "last")
    put_numeral(im, 4, "A deadline", False, t, t0)
    if t < tp - 0.15:
        secs = max(0, 30 - int((t - td) * 2)) if t >= td else 30
        w, h = 760, 420; win = window(w, h, "Ends in", False)
        tv = T(f"00:{secs:02d}", 160, RED_UI if t >= td else L_INK, 700); win.alpha_composite(tv, (int(w / 2 - tv.width / 2), 140))
        k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1150, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    else:
        v = roll(t, tp - 0.1, 0.9, 0, 41)
        c = stat("Agreements reached", f"{v:.0f}%", "", 820, False, 190, BLUE)
        k = spring((t - tp + 0.15) / 0.4); put(im, lift(c), 540, 1080 + (1 - k) * 30, min(1, k * 1.5), 0.96 + 0.04 * k)
        if t >= tl - 0.1:
            kp = spring((t - tl + 0.1) / 0.35); put(im, pill("in the last 30 seconds", 52, RED_UI, padx=30, pady=14), 540, 1080 + c.height / 2 + 110 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    footnote(im, "Roth, Murnighan & Schoumaker, American Economic Review, 1988", False, 1820)
    footnote(im, "Bargaining experiments, all four studies · timer illustrative", False, 1858)
    return im

def sc_r5(t):
    im = bg(True); t0 = S("r5"); ta = WT("r5", "anywhere"); tp = WT("r5", "81%"); to = WT("r5", "online.")
    put_numeral(im, 5, "Buyers from anywhere", True, t, t0)
    if t < tp - 0.15:
        put(im, head("sami", 170), 540, 1150, ease((t - t0) / 0.3))
        for j, (ang) in enumerate((200, 250, 300, 340, 20)):
            k = eout((t - ta + 0.1 - j * 0.08) / 0.5)
            if k <= 0: continue
            rr = 360 - 120 * k; x = 540 + rr * math.cos(math.radians(ang)); y = 1150 + rr * math.sin(math.radians(ang))
            put(im, head(BIDDERS[j], 100), x, y, min(1, k * 1.5))
    else:
        v = roll(t, tp - 0.1, 0.9, 0, 81)
        c = stat("Christie's · bids in 2024", f"{v:.0f}%", "", 820, True, 190, LILAC)
        k = spring((t - tp + 0.15) / 0.4); put(im, lift(c, True), 540, 1080 + (1 - k) * 30, min(1, k * 1.5), 0.96 + 0.04 * k)
        if t >= to - 0.15:
            kp = spring((t - to + 0.15) / 0.35); put(im, pill("placed online", 52, GREEN_UI, padx=30, pady=14), 540, 1080 + c.height / 2 + 110 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    footnote(im, "Christie's press release, 17 December 2024: 81% of all bids placed online", True, 1858)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tb = WT("tk", "bid.")
    p = sell_phone(t, 1.0, 1.0, lambda i: spring((t - t0 - 0.1 - i * 0.22) / 0.3))
    put(im, lift(p), 540, 1150, ease((t - t0) / 0.2))
    stamp_at(im, big_stamp("LET THEM BID", BLUE, 88, -8), 560, 1650, t, tb - 0.05)
    footnote(im, "Camera, prices and names are illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 28, BLUE), (540, 5, VIOLET), (750, 12, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

import math
FN = {"hook": sc_hook, "r1": sc_r1, "r2": sc_r2, "r3": sc_r3, "r4": sc_r4, "r5": sc_r5, "loop": sc_loop, "outro": sc_outro}

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
    s.pop(WT("h1", "pick") - 0.05, 0.04, 480); s.ding(WT("h1", "buyers") - 0.05, 1318, 0.03); s.thud(WT("h1", "do.") - 0.02, 0.08)
    for i in range(5): s.pop(WT("h2", "five") - 0.1 + i * 0.12, 0.03, 520 + i * 40)
    s.ding(WT("h2", "backwards") - 0.1, 1568, 0.03)
    for key in ("r1", "r2", "r3", "r4", "r5"): s.pop(S(key) - 0.05, 0.04, 640)
    s.pop(S("r1b") - 0.1, 0.03, 560); s.pop(S("r1b") + 0.15, 0.03, 600)
    for i in range(3): s.pop(WT("r1b", "more") - 0.1 + i * 0.15, 0.025, 560 + i * 40)
    s.ding(WT("r1b", "higher.") - 0.1, 1318, 0.03)
    for i in range(8): s.tick(WT("r2", "reserve.") + i * 0.35, 0.016)
    s.thud(WT("r2", "doesn't") - 0.05, 0.06)
    for i in range(3): s.pop(WT("r3", "one") - 0.1 + i * 0.1, 0.025, 520 + i * 30)
    s.ding(WT("r3", "buyer") - 0.05, 1568, 0.03); s.pop(WT("r3", "extra") - 0.1, 0.03, 500); s.pop(WT("r3", "best") - 0.1, 0.03, 620)
    for i in range(4): s.tick(WT("r4", "deadline.") + i * 0.5, 0.02)
    for i in range(5): s.tick(WT("r4", "41%") - 0.1 + i * 0.18, 0.018)
    s.ding(WT("r4", "last") - 0.1, 1318, 0.03)
    for i in range(5): s.pop(WT("r5", "anywhere") - 0.1 + i * 0.08, 0.025, 520 + i * 30)
    for i in range(5): s.tick(WT("r5", "81%") - 0.1 + i * 0.18, 0.018)
    s.ding(WT("r5", "online.") - 0.15, 1568, 0.03)
    for i in range(5): s.pop(S("tk") + i * 0.22, 0.025, 560 + i * 30)
    s.thud(WT("tk", "bid.") - 0.05, 0.07)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson29_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
