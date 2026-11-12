"""Auction short 28 (v3, standard, who: Nour): "How to bid like a pro". Nour's five rules, one per beat, each carried by one
sourced fact or rule: 1 track record (eBay reputation experiment, +8.1%, Resnick et al. 2006); 2 set your maximum, you pay about
one step above the runner-up (Vickrey via Lucking-Reiley 2000); 3 the reserve is the seller's floor, below it the item is passed
in (Consumer Affairs Victoria); 4 a late bid adds time so everyone can answer (Amazon's rule, Roth & Ockenfels 2002); 5 the deposit
comes back if you don't win (Lebanese CCP Art. 977). Takeaway: decide first, then bid; a plan beats panic.
Opens and ends on the same phone (Nour's watch auction, illustrative and labelled) so the replay loops.
Run: python3 tools/lessons/lesson28.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson28_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "ambient", 28
XF = 0.16
SC = [("hook", False, 0.0, S("r1") - 0.1), ("r1", True, S("r1") - 0.1, S("r2") - 0.1), ("r2", False, S("r2") - 0.1, S("r3") - 0.1),
      ("r3", True, S("r3") - 0.1, S("r4") - 0.1), ("r4", False, S("r4") - 0.1, S("r5") - 0.1), ("r5", True, S("r5") - 0.1, S("tk") - 0.1),
      ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
RIVAL = ("R", VIOLET)

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def dim(layer, a):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * a))); return layer

# ---------- drawings ----------
def watch_icon(w=170, col=LILAC, ink=(24, 28, 44)):
    S2 = 2; im = Image.new("RGBA", (w * S2, w * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2 = w * S2; c = W2 / 2
    d.rounded_rectangle((c - W2 * 0.16, 0, c + W2 * 0.16, W2), radius=int(W2 * 0.06), fill=col + (255,))
    r = W2 * 0.3; d.ellipse((c - r, c - r, c + r, c + r), fill=(255, 255, 255, 255), outline=ink + (255,), width=int(W2 * 0.04))
    d.line([(c, c), (c, c - r * 0.65)], fill=ink + (255,), width=int(W2 * 0.035)); d.line([(c, c), (c + r * 0.45, c + r * 0.1)], fill=ink + (255,), width=int(W2 * 0.035))
    return im.resize((w, w), Image.LANCZOS)

def tick(s=60, col=GREEN_UI):
    S2 = 3; im = Image.new("RGBA", (s * S2, s * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); z = s * S2
    d.ellipse((0, 0, z - 1, z - 1), fill=col + (255,))
    d.line([(z * 0.27, z * 0.53), (z * 0.44, z * 0.7), (z * 0.75, z * 0.33)], fill=(255, 255, 255, 255), width=int(z * 0.1), joint="curve")
    return im.resize((s, s), Image.LANCZOS)

def numeral(n, text, dark):
    """the rule's headline: a numbered circle and two or three words"""
    s = 120; c = Image.new("RGBA", (s, s), (0, 0, 0, 0)); ImageDraw.Draw(c).ellipse((0, 0, s - 1, s - 1), fill=VIOLET + (255,))
    nt = T(str(n), 76, (255, 255, 255), 700); c.alpha_composite(nt, (int(s / 2 - nt.width / 2), int(s / 2 - nt.height / 2 - 4)))
    tt = T(text, 64, D_INK if dark else L_INK, 700); w = s + 30 + tt.width
    im = Image.new("RGBA", (w, s), (0, 0, 0, 0)); im.alpha_composite(c, (0, 0)); im.alpha_composite(tt, (s + 30, int(s / 2 - tt.height / 2 - 4)))
    return im

def put_numeral(im, n, text, dark, t, t0):
    k = spring((t - t0 + 0.05) / 0.4)
    if k > 0: put(im, numeral(n, text, dark), 540, 600 + (1 - k) * 30, min(1, k * 1.5), 0.9 + 0.1 * k)

def plan_phone(t, ticks_k=None, stamp_t=None):
    """Nour's phone: the watch auction before it starts. Shared by the hook and the loop so the replay is seamless."""
    pw, ph = 640, 900; p = phone(pw, ph, False)
    lc = card(560, 250, False, 26, fill=(246, 247, 251)); lc.alpha_composite(watch_icon(170), (30, 40))
    lc.alpha_composite(T("Watch · vintage", 34, L_INK, 600), (230, 40))
    lc.alpha_composite(T("STARTS IN", 22, GREY_TXT, 700, True), (230, 96))
    lc.alpha_composite(T("10:00", 84, L_INK, 700), (230, 122))
    p.alpha_composite(lc, (40, 100))
    p.alpha_composite(T("BIDS PLACED", 22, GREY_TXT, 700, True), (60, 390)); p.alpha_composite(T("0", 84, L_INK, 700), (60, 420))
    p.alpha_composite(head("nour", 120), (pw - 60 - 120, 400))
    p.alpha_composite(T("MY PLAN", 22, GREY_TXT, 700, True), (60, 590))
    for i in range(5):
        x = 60 + i * 108; y = 640
        ImageDraw.Draw(p).ellipse((x, y, x + 80, y + 80), outline=(214, 216, 224, 255), width=4)
        nt = T(str(i + 1), 36, GREY_TXT, 700); p.alpha_composite(nt, (int(x + 40 - nt.width / 2), int(y + 40 - nt.height / 2 - 2)))
        if ticks_k is not None:
            kk = ticks_k(i)
            if kk > 0: tk_ = tick(84); p.alpha_composite(fade_in(tk_, kk), (x - 2, y - 2))
    return p

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); tb = WT("h1", "before"); t2 = S("h2") - 0.05; tf = WT("h2", "five"); tl = WT("h2", "Lebanese")
    kout = ease((t - t2) / 0.3)
    if kout < 1:
        p = plan_phone(t)
        put(im, lift(p), 540, 1150 - 40 * kout, 1 - kout, 0.97 + 0.03 * spring(t / 0.5))
        stamp_at(im, big_stamp("PLAN FIRST", VIOLET, 92, -8), 560, 1650, t, tb - 0.05)
    if t >= t2:
        for i in range(5):
            k = spring((t - tf + 0.1 - i * 0.12) / 0.4)
            if k <= 0: continue
            s = 150; c = Image.new("RGBA", (s, s), (0, 0, 0, 0))
            last = i == 4 and t >= tl - 0.1
            ImageDraw.Draw(c).ellipse((0, 0, s - 1, s - 1), fill=(VIOLET if last else (236, 237, 242)) + (255,))
            nt = T(str(i + 1), 84, (255, 255, 255) if last else L_INK, 700); c.alpha_composite(nt, (int(s / 2 - nt.width / 2), int(s / 2 - nt.height / 2 - 4)))
            put(im, c, 140 + i * 200, 1040 + (1 - k) * 40, min(1, k * 1.5), 0.85 + 0.15 * k)
        put(im, head("nour", 170), 540, 1340, ease((t - t2) / 0.3))
        kl = spring((t - tl + 0.1) / 0.4)
        if kl > 0: put(im, pill("from Lebanese law", 44, VIOLET, padx=30, pady=14), 940 - 180, 1200 + (1 - kl) * 20, min(1, kl * 1.5))
        footnote(im, "Five rules · the auction and prices in this video are illustrative", False, 1850)
    else:
        footnote(im, "Watch, prices and names are illustrative", False, 1850)
    return im

def sc_r1(t):
    im = bg(True); t0 = S("r1"); tb = S("r1b"); tp = WT("r1b", "8.1%"); te = WT("r1b", "established")
    put_numeral(im, 1, "Track record", True, t, t0)
    if t < tb - 0.05:
        k = spring((t - WT("r1", "track") + 0.1) / 0.4)
        if k > 0:
            c = card(760, 300, True, 30); c.alpha_composite(head(("D", BLUE), 130), (40, 40))
            c.alpha_composite(T("Seller", 46, D_INK, 700), (200, 50))
            for j in range(5):
                st = Image.new("RGBA", (50, 50), (0, 0, 0, 0)); ImageDraw.Draw(st).ellipse((4, 4, 46, 46), fill=GREEN_APP + (255,)); c.alpha_composite(st, (200 + j * 62, 120))
            c.alpha_composite(T("past sales · reviews", 32, D_MUTE, 500), (44, 210))
            put(im, lift(c, True), 540, 1120 + (1 - k) * 30, min(1, k * 1.5))
        return foot1(im)
    w, h = 880, 640; win = window(w, h, "Same dealer · same postcards", True)
    rows = (("New name", "no history", False), ("Established name", "long track record", True))
    for i, (nm, sub, est) in enumerate(rows):
        kr = spring((t - WT("r1b", "same") + 0.1 - i * 0.2) / 0.35)
        if kr <= 0: continue
        r = card(780, 200, True, 26, fill=(36, 42, 60)); r.alpha_composite(head(("D", BLUE), 110), (30, 45))
        r.alpha_composite(T(nm, 42, D_INK, 700), (170, 48)); r.alpha_composite(T(sub, 30, D_MUTE, 500), (170, 112))
        if est and t >= tp - 0.1:
            kp = spring((t - tp + 0.1) / 0.35); v = roll(t, tp - 0.1, 0.9, 0, 8.1)
            pp = fade_in(pill(f"+{v:.1f}%", 52, GREEN_UI, padx=24, pady=12), kp); r.alpha_composite(pp, (780 - 30 - pp.width, int(100 - pp.height / 2)))
        win.alpha_composite(fade_in(r, kr), (50, 110 + i * 240))
    k = ease((t - tb + 0.15) / 0.25); put(im, lift(win, True), 540, 1180, k, 0.96 + 0.04 * spring((t - tb + 0.15) / 0.5))
    if t >= te - 0.1: select_box(im, (540 - 440 + 50, 1180 - 320 + 350, 540 - 440 + 830, 1180 - 320 + 550), eout((t - te + 0.1) / 0.3))
    return foot1(im)

def foot1(im):
    footnote(im, "Resnick, Zeckhauser, Swanson & Lockwood, Experimental Economics, 2006", True, 1820)
    footnote(im, "eBay field experiment · difference in what buyers paid: 8.1%", True, 1858)
    return im

def sc_r2(t):
    im = bg(False); t0 = S("r2"); tm = WT("r2", "maximum"); tr = WT("r2", "runner-up,"); tn = WT("r2", "not"); ty = WT("r2", "You")
    put_numeral(im, 2, "Your maximum", False, t, t0)
    c = stat("My max · set before it starts", "$700", "", 820, False, 150, (60, 40, 140)); c.alpha_composite(head("nour", 120), (820 - 170, 40))
    k = spring((t - tm + 0.15) / 0.4)
    if k > 0: put(im, lift(c), 540, 930 + (1 - k) * 30, min(1, k * 1.5), 0.96 + 0.04 * k)
    if t >= ty - 0.1:
        r = card(820, 170, False, 28, fill=(246, 247, 251)); r.alpha_composite(head(RIVAL, 110), (30, 30))
        r.alpha_composite(T("Runner-up", 40, L_INK, 700), (170, 34)); r.alpha_composite(T("stops at $500", 32, GREY_TXT, 600), (170, 92))
        if t >= tr - 0.05: oc = fade_in(pill("OUT", 34, RED_UI, padx=22, pady=8), spring((t - tr + 0.05) / 0.3)); r.alpha_composite(oc, (820 - 40 - oc.width, 58))
        kr = spring((t - ty + 0.1) / 0.35); put(im, lift(fade_in(r, kr)), 540, 1240 + (1 - kr) * 20)
    if t >= WT("r2", "pay") - 0.05:
        kp = spring((t - WT("r2", "pay") + 0.05) / 0.4); put(im, pill("You pay $510", 56, GREEN_UI, padx=34, pady=16), 540, 1460 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    if t >= tn - 0.05:
        kp = spring((t - tn + 0.05) / 0.4); put(im, pill("$190 under your limit", 40, (233, 227, 255), (60, 40, 140), 26, 12), 540, 1600 + (1 - kp) * 20, min(1, kp * 1.5))
    footnote(im, "Amounts illustrative · 1 step = $10 · Vickrey; Lucking-Reiley, J. Econ. Perspectives, 2000", False, 1850)
    return im

def sc_r3(t):
    im = bg(True); t0 = S("r3"); tr = WT("r3", "reserve."); tf = WT("r3", "floor."); tb = WT("r3", "Below"); tn = WT("r3", "nothing")
    put_numeral(im, 3, "The reserve", True, t, t0)
    w, h = 880, 620; win = window(w, h, "Live auction · Watch · vintage", True)
    price = int(roll(t, tr, tn - tr, 200, 440) // 10 * 10)
    lab = T("HIGHEST BID", 24, D_MUTE, 700, True); win.alpha_composite(lab, (60, 100))
    win.alpha_composite(T(money(price), 110, D_INK, 700), (60, 136))
    x0, x1, yb = 60, w - 60, 380; d = ImageDraw.Draw(win)
    d.rounded_rectangle((x0, yb, x1, yb + 50), radius=25, fill=(40, 46, 64, 255))
    fr = (price - 0) / 800; d.rounded_rectangle((x0, yb, x0 + max(50, (x1 - x0) * fr), yb + 50), radius=25, fill=LILAC + (255,))
    xr = x0 + (x1 - x0) * 0.6
    kr = clamp((t - tr + 0.1) / 0.3)
    if kr > 0:
        d.line([(xr, yb - 40), (xr, yb + 90)], fill=(255, 255, 255, int(255 * kr)), width=6)
        rl = T("RESERVE", 26, D_INK, 700, True); win.alpha_composite(fade_in(rl, kr), (int(xr - rl.width / 2), yb + 100))
    if t >= tf - 0.1:
        fl = fade_in(pill("seller's floor", 30, (60, 66, 86), padx=18, pady=8), spring((t - tf + 0.1) / 0.3)); win.alpha_composite(fl, (int(xr - fl.width / 2), yb - 100))
    if t >= tn - 0.05:
        kn = spring((t - tn + 0.05) / 0.35); pn = fade_in(pill("NOT SOLD", 40, RED_UI, padx=24, pady=10), kn); win.alpha_composite(pn, (w - 60 - pn.width, 150))
    k = ease((t - tr + 0.2) / 0.25); put(im, lift(win, True), 540, 1150, k, 0.96 + 0.04 * spring((t - tr + 0.2) / 0.5))
    footnote(im, "Below the reserve the item is “passed in” · Consumer Affairs Victoria", True, 1820)
    footnote(im, "Prices illustrative", True, 1858)
    return im

def sc_r4(t):
    im = bg(False); t0 = S("r4"); tl = WT("r4", "late"); ta = WT("r4", "adds"); tan = WT("r4", "answer.")
    put_numeral(im, 4, "Time added", False, t, t0)
    if t < ta - 0.05: secs = max(2, int(5 - (t - t0)))
    else: secs = max(0, 120 - int((t - ta) * 1))
    w, h = 880, 760; win = window(w, h, "Live auction · Watch · vintage", False)
    lab = T("ENDS IN", 24, GREY_TXT, 700, True); win.alpha_composite(lab, (int(w / 2 - lab.width / 2), 100))
    added = t >= ta - 0.05
    tv = T(f"{secs // 60:02d}:{secs % 60:02d}", 140, GREEN_UI if added else RED_UI, 700); win.alpha_composite(tv, (int(w / 2 - tv.width / 2), 136))
    if added:
        kp = spring((t - ta + 0.05) / 0.35); pp = fade_in(pill("+ time added", 36, GREEN_UI, padx=22, pady=10), kp); win.alpha_composite(pp, (int(w / 2 - pp.width / 2), 320))
    rows = ((RIVAL, "Bidder R", "$520", tl - 0.1), ("nour", "Nour", "$530", tan - 0.3))
    for i, (who, nm, amt, ts) in enumerate(rows):
        kr = spring((t - ts) / 0.35)
        if kr <= 0: continue
        r = card(780, 140, False, 26, fill=(246, 247, 251)); r.alpha_composite(head(who, 96), (24, 22))
        r.alpha_composite(T(nm, 40, L_INK, 700), (150, 44)); at = T(amt, 52, L_INK, 700); r.alpha_composite(at, (780 - 40 - at.width, 38))
        win.alpha_composite(fade_in(r, kr), (50, 420 + i * 160))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1200, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Timer and bids illustrative · Amazon's auctions ran until 10 minutes passed with no bid", False, 1820)
    footnote(im, "Roth & Ockenfels, American Economic Review, 2002", False, 1858)
    return im

def sc_r5(t):
    im = bg(True); t0 = S("r5"); td = WT("r5", "deposit"); tc = WT("r5", "Lebanese"); ts = WT("r5", "session")
    put_numeral(im, 5, "Deposit back", True, t, t0)
    if t < tc - 0.1:
        put(im, head("nour", 180), 300, 1150, ease((t - t0) / 0.3))
        k = eout((t - td - 0.1) / 0.8)
        if t >= td - 0.2:
            put(im, pill("DEPOSIT", 46, GREEN_UI, padx=28, pady=14), 820 - 240 * k, 1150 - 120 * math.sin(math.pi * k), min(1, (t - td + 0.2) / 0.2))
            if k >= 1: put(im, pill("back to you", 38, (40, 46, 60), D_INK, 24, 10), 440, 1340, ease((t - td - 0.9) / 0.25))
    else:
        w, h = 880, 640; win = window(w, h, "Code of Civil Procedure · Art. 977", True)
        yr = T("Lebanon", 90, LILAC, 700); kq = spring((t - tc + 0.1) / 0.4); win.alpha_composite(fade_in(yr, kq), (int(w / 2 - yr.width / 2), int(110 + (1 - kq) * 20)))
        for i, ln in enumerate(("Didn't win?", "Take your deposit back", "when the session ends.")):
            kl = spring((t - WT("r5", "bidders") + 0.1 - i * 0.25) / 0.4)
            if kl <= 0: continue
            lt = T(ln, 54, D_INK, 600); win.alpha_composite(fade_in(lt, kl), (int(w / 2 - lt.width / 2), int(290 + i * 92 + (1 - kl) * 16)))
        k = ease((t - tc + 0.2) / 0.25); cy = 1150; put(im, lift(win, True), 540, cy, k, 0.96 + 0.04 * spring((t - tc + 0.2) / 0.5))
        if t >= ts - 0.1:
            lt = T("when the session ends.", 54, D_INK, 600); x0 = 540 - lt.width / 2 - 14; y0 = cy - h / 2 + 290 + 2 * 92 - 10
            select_box(im, (x0, y0, x0 + lt.width + 28, y0 + lt.height + 22), eout((t - ts + 0.1) / 0.3))
    footnote(im, "Arts. 973 and 977, paraphrased: bidders deposit the opening price first;", True, 1820)
    footnote(im, "those who aren't the last bidder may withdraw it once the session ends", True, 1858)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tp = WT("tk", "plan")
    p = plan_phone(t, lambda i: spring((t - t0 - 0.1 - i * 0.22) / 0.3))
    put(im, lift(p), 540, 1150, ease((t - t0) / 0.2))
    stamp_at(im, big_stamp("PLAN FIRST", VIOLET, 92, -8), 560, 1650, t, tp - 0.05)
    footnote(im, "Watch, prices and names are illustrative", False, 1850)
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
    s.thud(WT("h1", "before") - 0.05, 0.08)
    for i in range(5): s.pop(WT("h2", "five") - 0.1 + i * 0.12, 0.03, 520 + i * 40)
    s.ding(WT("h2", "Lebanese") - 0.1, 1568, 0.03)
    for key in ("r1", "r2", "r3", "r4", "r5"): s.pop(S(key) - 0.05, 0.04, 640)
    s.pop(WT("r1b", "same") - 0.1, 0.03, 560); s.pop(WT("r1b", "same") + 0.1, 0.03, 600)
    for i in range(5): s.tick(WT("r1b", "8.1%") - 0.1 + i * 0.18, 0.018)
    s.ding(WT("r1b", "8.1%") + 0.8, 1318, 0.03)
    s.pop(WT("r2", "maximum") - 0.15, 0.04, 600); s.pop(WT("r2", "runner-up,") - 0.05, 0.04, 480)
    s.ding(WT("r2", "pay") - 0.05, 1318, 0.03); s.pop(WT("r2", "not") - 0.05, 0.035, 680)
    for i in range(8): s.tick(WT("r3", "reserve.") + i * 0.35, 0.016)
    s.thud(WT("r3", "nothing") - 0.05, 0.06)
    for i in range(3): s.tick(S("r4") + 0.3 + i * 1.0, 0.02)
    s.pop(WT("r4", "late") - 0.1, 0.04, 520); s.ding(WT("r4", "adds") - 0.05, 1568, 0.03); s.pop(WT("r4", "answer.") - 0.3, 0.04, 640)
    s.pop(WT("r5", "deposit") - 0.2, 0.04, 600); s.ding(WT("r5", "deposit") + 0.75, 1318, 0.03)
    for i in range(3): s.pop(WT("r5", "bidders") - 0.1 + i * 0.25, 0.025, 540 + i * 30)
    s.ding(WT("r5", "session") - 0.1, 1568, 0.03)
    for i in range(5): s.pop(S("tk") + i * 0.22, 0.025, 560 + i * 30)
    s.thud(WT("tk", "plan") - 0.05, 0.07)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson28_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
