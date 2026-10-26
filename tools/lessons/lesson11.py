"""Auction short 11 (v3, quick, who: Nour): "Paying a stranger first". Problem: Nour finds a phone online and the seller wants
the money first; she has never met him and he has no reviews. Reframe (one fact): in a controlled field experiment one dealer
sold matched postcard lots under his established name and under brand-new names; buyers paid 8.1% more to the established
name (Resnick, Zeckhauser, Swanson & Lockwood, Experimental Economics, 2006). Fix: an online auction can show every seller's
past sales and reviews for anyone to check. Takeaway: trust isn't a feeling, it's a track record you can check.
Built like L10 v2: one story from the first frame to the last, one fact.
Run: python3 tools/lessons/lesson11.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson11_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "keys", 11
XF = 0.16
T_LOOP = WT("tk", "Before") - 0.15
SC = [("hook", False, 0.0, S("p1") - 0.1), ("stranger", True, S("p1") - 0.1, S("s1") - 0.1), ("exp", False, S("s1") - 0.1, S("s2") - 0.1),
      ("result", True, S("s2") - 0.1, S("f1") - 0.1), ("fix", False, S("f1") - 0.1, S("tk") - 0.1),
      ("take", True, S("tk") - 0.1, T_LOOP), ("loop", False, T_LOOP, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
AMBER = (255, 196, 61)   # review stars only (a UI convention, not a palette colour)

# ---------- drawings ----------
def handset(w=200, col=SLATE):
    """a simple smartphone, front view"""
    S2 = 2; h = int(w * 1.9); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    d.rounded_rectangle((0, 0, W2 - 1, H2 - 1), radius=int(W2 * 0.16), fill=col + (255,))
    d.rounded_rectangle((W2 * 0.07, H2 * 0.05, W2 * 0.93, H2 * 0.95), radius=int(W2 * 0.1), fill=(70, 110, 220, 255))
    d.polygon([(W2 * 0.07, H2 * 0.55), (W2 * 0.93, H2 * 0.25), (W2 * 0.93, H2 * 0.95), (W2 * 0.07, H2 * 0.95)], fill=(124, 92, 255, 255))
    d.rounded_rectangle((W2 * 0.38, H2 * 0.075, W2 * 0.62, H2 * 0.105), radius=12, fill=(10, 10, 14, 255))
    return im.resize((w, h), Image.LANCZOS)

def postcards(w=300):
    """a small fanned stack of vintage postcards"""
    S2 = 2; h = int(w * 0.8); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); W2, H2 = w * S2, h * S2
    for i, (rot, col) in enumerate(((-10, (214, 222, 240)), (6, (226, 232, 246)), (-2, (250, 250, 252)))):
        c = Image.new("RGBA", (int(W2 * 0.72), int(H2 * 0.62)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); cw, ch = c.size
        d.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=10, fill=col + (255,), outline=(190, 196, 210, 255), width=4)
        d.rectangle((cw * 0.07, ch * 0.1, cw * 0.55, ch * 0.9), fill=(150, 175, 230, 255))
        d.polygon([(cw * 0.07, ch * 0.9), (cw * 0.25, ch * 0.5), (cw * 0.38, ch * 0.7), (cw * 0.47, ch * 0.55), (cw * 0.55, ch * 0.9)], fill=(100, 130, 200, 255))
        d.rectangle((cw * 0.75, ch * 0.1, cw * 0.92, ch * 0.32), outline=(160, 140, 230, 255), width=4)
        for k in range(3): d.line([(cw * 0.62, ch * (0.5 + k * 0.13)), (cw * 0.92, ch * (0.5 + k * 0.13))], fill=(170, 176, 190, 255), width=4)
        c = c.rotate(rot, expand=True, resample=Image.BICUBIC); im.alpha_composite(c, (int(W2 / 2 - c.width / 2 + (i - 1) * 20), int(H2 / 2 - c.height / 2)))
    return im.resize((w, h), Image.LANCZOS)

def star(s=40, col=AMBER, on=True):
    im = Image.new("RGBA", (s * 2, s * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s
    pts = [(c + c * 0.95 * np.cos(np.pi / 2 + i * np.pi / 5) * (1 if i % 2 == 0 else 0.45), c - c * 0.95 * np.sin(np.pi / 2 + i * np.pi / 5) * (1 if i % 2 == 0 else 0.45)) for i in range(10)]
    d.polygon(pts, fill=(col if on else (200, 204, 214)) + (255,)); return im.resize((s, s), Image.LANCZOS)

def stars(n=5, s=40, on=5):
    im = Image.new("RGBA", (n * (s + 6), s), (0, 0, 0, 0))
    for i in range(n): im.alpha_composite(star(s, AMBER, i < on), (i * (s + 6), 0))
    return im

def check(s=60, col=GREEN_UI):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.ellipse((0, 0, s - 1, s - 1), fill=col + (255,))
    d.line([(s * 0.27, s * 0.52), (s * 0.43, s * 0.68), (s * 0.74, s * 0.34)], fill=(255, 255, 255, 255), width=max(3, s // 9)); return im

def heart(s=200, col=LILAC):
    S2 = 2; W2 = s * S2; im = Image.new("RGBA", (W2, W2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = col + (255,)
    d.ellipse((W2 * 0.06, W2 * 0.12, W2 * 0.54, W2 * 0.6), fill=c); d.ellipse((W2 * 0.46, W2 * 0.12, W2 * 0.94, W2 * 0.6), fill=c)
    d.polygon([(W2 * 0.09, W2 * 0.45), (W2 * 0.91, W2 * 0.45), (W2 * 0.5, W2 * 0.92)], fill=c)
    return im.resize((s, s), Image.LANCZOS)

def qhead(s=90):
    return head(("?", (150, 155, 166)), s)

def bubble_msg(text, size=72, fill=(236, 237, 242), col=L_INK):
    parts = [T(x, size, col, 700) for x in text.split("\n")]
    tt = Image.new("RGBA", (max(p.width for p in parts), sum(p.height for p in parts) + 8 * (len(parts) - 1)), (0, 0, 0, 0)); y = 0
    for p_ in parts: tt.alpha_composite(p_, (0, y)); y += p_.height + 8
    w, h = tt.width + 70, tt.height + 46
    im = Image.new("RGBA", (w, h + 18), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=fill + (255,)); d.polygon([(26, h - 12), (20, h + 16), (60, h - 12)], fill=fill + (255,))
    im.alpha_composite(tt, (35, 23)); return im

def chat_phone(t, pulse_t, button_t=None):
    """Nour's phone: the listing, then the seller's message (shared by the hook and the loop scene, so the replay is seamless)"""
    pw, ph = 640, 1180; p = phone(pw, ph, False)
    lc = card(560, 400, False, 26, fill=(246, 247, 251)); lc.alpha_composite(handset(140), (40, 45))
    lc.alpha_composite(T("Phone · like new", 36, L_INK, 600), (220, 70)); lc.alpha_composite(T("$600", 92, L_INK, 700), (220, 125))
    lc.alpha_composite(qhead(60), (220, 280)); lc.alpha_composite(T("Seller · new", 30, GREY_TXT, 600), (295, 293))
    p.alpha_composite(lc, (40, 110))
    p.alpha_composite(T("MESSAGE FROM SELLER", 22, GREY_TXT, 700, True), (60, 560))
    pk = 1 + 0.08 * np.sin(np.pi * clamp((t - pulse_t) / 0.35))
    b = bubble_msg("Send the money\nfirst.", 54, (255, 228, 233), RED_UI)
    bb = b.resize((int(b.width * pk), int(b.height * pk)), Image.LANCZOS)
    p.alpha_composite(bb, (44, 612))
    if button_t is not None and t >= button_t:
        kk = spring((t - button_t) / 0.4); bt = pill("View seller's record", 40, VIOLET, padx=34, pady=18)
        bt = bt.resize((max(1, int(bt.width * (0.85 + 0.15 * kk))), max(1, int(bt.height * (0.85 + 0.15 * kk)))), Image.LANCZOS)
        p.alpha_composite(bt, (int(pw / 2 - bt.width / 2), 900))
    else:
        p.alpha_composite(head("nour", 70), (pw - 40 - 70, 900)); tt = T("Nour", 30, GREY_TXT, 600); p.alpha_composite(tt, (pw - 130 - tt.width, 918))
    return p

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False)
    put(im, lift(chat_phone(t, WT("h1", "money"))), 540, 1170, 1, 0.97 + 0.03 * spring(t / 0.5))
    footnote(im, "Phone, price and seller are illustrative", False, 1850)
    return im

def sc_stranger(t):
    im = bg(True); t0 = S("p1"); tr = WT("p1", "reviews."); th = WT("p1", "history."); ty = WT("p1", "you")
    w, h = 860, 760; c = window(w, h, "Seller profile", True)
    c.alpha_composite(qhead(150), (60, 120)); c.alpha_composite(T("Seller", 52, D_INK, 700), (240, 140)); c.alpha_composite(T("Never met", 32, D_MUTE, 600), (242, 210))
    for i, (ti, lab) in enumerate(((tr, "REVIEWS"), (th, "PAST SALES"))):
        k = spring((t - ti + 0.05) / 0.35)
        if k <= 0: continue
        row = card(740, 150, True, 22, fill=(30, 36, 52))
        row.alpha_composite(T(lab, 28, D_MUTE, 700, True), (40, 58)); v = T("0", 96, RED_UI, 700); row.alpha_composite(v, (700 - v.width, 16))
        row.putalpha(row.getchannel("A").point(lambda p: int(p * min(1, k * 1.5)))); c.alpha_composite(row, (60, int(330 + i * 180 + (1 - k) * 30)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1020, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= ty - 0.1:
        kk = spring((t - ty + 0.1) / 0.4); bt = pill("Pay $600?", 60, RED_UI, padx=44, pady=20)
        put(im, bt, 540, 1580, min(1, kk * 1.5), 0.85 + 0.15 * kk)
        cx = 540 + 330 - 150 * eout((t - ty) / 0.5); cy = 1580 + 160 - 120 * eout((t - ty) / 0.5)
        wob = 14 * np.sin((t - ty) * 9) if t > ty + 0.5 else 0       # the cursor hesitates
        put(im, cursor(), cx + 20 + wob, cy + 30)
    footnote(im, "Illustrative", True, 1850)
    return im

def listing(name, sub, good, k):
    c = card(400, 520, False, 26, fill=(246, 247, 251)); c.alpha_composite(postcards(300), (50, 30))
    c.alpha_composite(T("Vintage postcards", 28, GREY_TXT, 600), (40, 290))
    if k > 0:
        a = min(1, k * 1.5); lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
        lay.alpha_composite(head(("D", SILVER), 56), (40, 350)); lay.alpha_composite(T(name, 32, L_INK, 700), (108, 348)); lay.alpha_composite(T(sub, 24, GREY_TXT, 600), (108, 388))
        if good: lay.alpha_composite(stars(5, 34, 5), (40, 450))
        else: lay.alpha_composite(chip("no history"), (40, 450))
        lay.putalpha(lay.getchannel("A").point(lambda p: int(p * a))); c.alpha_composite(lay)
    return c

def sc_exp(t):
    im = bg(False); t0 = S("s1"); td = WT("s1", "dealer"); tp = WT("s1", "postcards"); to = WT("s1", "own"); tn = WT("s1", "new")
    w, h = 920, 900; win = window(w, h, "Field experiment · 2006", False)
    kd = spring((t - td + 0.1) / 0.35)
    if kd > 0:
        r = card(820, 120, False, 22, fill=(246, 247, 251)); r.alpha_composite(head(("D", SILVER), 80), (24, 20)); r.alpha_composite(T("One dealer", 40, L_INK, 700), (124, 36))
        r.putalpha(r.getchannel("A").point(lambda p: int(p * min(1, kd * 1.5)))); win.alpha_composite(r, (50, int(100 + (1 - kd) * 20)))
    for i, (tt_, nm, sb, good) in enumerate(((to, "His own name", "Track record", True), (tn, "A new name", "Brand new", False))):
        kc = spring((t - tp + 0.15 - i * 0.12) / 0.4)
        if kc <= 0: continue
        L = listing(nm, sb, good, spring((t - tt_ + 0.1) / 0.35))
        L.putalpha(L.getchannel("A").point(lambda p: int(p * min(1, kc * 1.5)))); win.alpha_composite(L, (40 + i * 440, int(270 + (1 - kc) * 40)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Resnick, Zeckhauser, Swanson & Lockwood, Experimental Economics, 2006", False, 1850)
    return im

def sc_result(t):
    im = bg(True); t0 = S("s2"); ts = WT("s2", "seller,"); tp = WT("s2", "postcards."); t8 = WT("s2", "8.1%"); tr = WT("s2", "track")
    if t < t8 - 0.15:
        for i, (ti, txt) in enumerate(((ts, "Same seller"), (tp, "Same postcards"))):
            k = spring((t - ti + 0.05) / 0.35)
            if k <= 0: continue
            r = card(760, 170, True, 26); r.alpha_composite(check(90), (40, 40)); r.alpha_composite(T(txt, 62, D_INK, 700), (160, 46))
            put(im, lift(r, True), 540, 900 + i * 230 + (1 - k) * 30, min(1, k * 1.5))
    else:
        k = spring((t - t8 + 0.15) / 0.45); v = roll(t, t8 - 0.1, 0.9, 0.0, 8.1)
        c = card(860, 560, True, 30)
        lab = T("BUYERS PAID", 30, D_MUTE, 700, True); c.alpha_composite(lab, (int(430 - lab.width / 2), 60))
        tv = T(f"+{v:.1f}%", 230, GREEN_UI, 700); c.alpha_composite(tv, (int(430 - tv.width / 2), 120))
        if t >= tr - 0.1:
            kk = spring((t - tr + 0.1) / 0.4); pp = pill("to the name with a track record", 36, VIOLET)
            pp.putalpha(pp.getchannel("A").point(lambda p: int(p * min(1, kk * 1.5)))); c.alpha_composite(pp, (int(430 - pp.width / 2), 430))
        put(im, lift(c, True), 540, 1080 + (1 - k) * 50, min(1, k * 1.5), 0.92 + 0.08 * k)
    footnote(im, "Same seller, matched lots · 8.1% of the selling price · Resnick et al., 2006", True, 1850)
    return im

SALES = (("Camera", 5), ("Bike", 5), ("Headphones", 4))
def sc_fix(t):
    im = bg(False); t0 = S("f1"); tps = WT("f1", "past"); trv = WT("f1", "reviews,"); tan = WT("f1", "anyone"); tch = WT("f1", "check.")
    w, h = 900, 1040; c = window(w, h, "Seller profile · public", False)
    c.alpha_composite(head(("S", GREEN_APP), 130), (50, 110)); c.alpha_composite(T("Seller", 50, L_INK, 700), (210, 120))
    n = int(round(roll(t, tps - 0.1, 0.8, 0, 48)))
    c.alpha_composite(T(f"{n} past sales", 34, GREY_TXT, 600), (212, 190))
    kr = spring((t - trv + 0.1) / 0.4)
    for i, (item, st) in enumerate(SALES):
        ki = spring((t - tps - 0.05 - i * 0.18) / 0.35)
        if ki <= 0: continue
        row = card(800, 140, False, 22, fill=(246, 247, 251))
        row.alpha_composite(T("SOLD", 22, GREEN_UI, 700, True), (34, 30)); row.alpha_composite(T(item, 40, L_INK, 600), (34, 66))
        if kr > 0:
            ss = stars(5, 40, st); ss.putalpha(ss.getchannel("A").point(lambda p: int(p * min(1, kr * 1.5)))); row.alpha_composite(ss, (760 - ss.width, 50))
        row.putalpha(row.getchannel("A").point(lambda p: int(p * min(1, ki * 1.5)))); c.alpha_composite(row, (50, int(330 + i * 170 + (1 - ki) * 30)))
    if t >= tan - 0.2:
        kk = spring((t - tan + 0.2) / 0.4); bt = pill("Open to everyone", 38, VIOLET, padx=30, pady=14)
        bt.putalpha(bt.getchannel("A").point(lambda p: int(p * min(1, kk * 1.5)))); c.alpha_composite(bt, (int(w / 2 - bt.width / 2), 880))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tan - 0.2:
        cx = 540 + 300 - 160 * eout((t - tan + 0.2) / 0.45); cy = 1110 + 460 - 120 * eout((t - tan + 0.2) / 0.45)
        put(im, cursor(), cx + 20, cy + 30)
        ripple(im, 670, 1500, (t - tch) / 0.5)
    footnote(im, "Example profile · names, items and reviews illustrative", False, 1850)
    return im

def sc_take(t):
    im = bg(True); t0 = S("tk"); tf = WT("tk", "feeling."); tr = WT("tk", "track"); tc = WT("tk", "check.")
    if t < tr - 0.2:
        k = spring((t - t0 + 0.1) / 0.45); put(im, heart(300), 540, 1000 + (1 - k) * 40, min(1, k * 1.5))
        put(im, pill("a feeling", 64, (60, 66, 86), padx=40, pady=16), 540, 1300, ease((t - tf + 0.1) / 0.2))
        if t >= tf + 0.15: strike(im, 540 - 190, 1302, 540 + 190, eout((t - tf - 0.15) / 0.25), RED_UI, 10)
    else:
        k = spring((t - tr + 0.2) / 0.45); c = card(820, 560, True, 30)
        lab = T("A TRACK RECORD", 30, D_MUTE, 700, True); c.alpha_composite(lab, (int(410 - lab.width / 2), 50))
        for i, (txt, ti) in enumerate((("Past sales", tr + 0.1), ("Reviews", tr + 0.4), ("Open to check", tc))):
            kk = spring((t - ti) / 0.35)
            if kk <= 0: continue
            ck = check(80); c.alpha_composite(ck, (90, int(140 + i * 130 + (1 - kk) * 20))); c.alpha_composite(T(txt, 56, D_INK, 700), (200, int(146 + i * 130 + (1 - kk) * 20)))
        put(im, lift(c, True), 540, 1120 + (1 - k) * 60, min(1, k * 1.5))
    return im

def sc_loop(t):
    im = bg(False); tm = WT("tk", "money"); tb = WT("tk", "send") - 0.1
    put(im, lift(chat_phone(t, tm, tb)), 540, 1170, ease((t - T_LOOP) / 0.2))
    tf = WT("tk", "first.")
    cx = 540 + 330 - 230 * eout((t - tb) / 0.5); cy = 1515 + 250 - 250 * eout((t - tb) / 0.5)
    if t >= tb: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 610, 1515, (t - tf) / 0.5)
    footnote(im, "Phone, price and seller are illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
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

FN = {"hook": sc_hook, "stranger": sc_stranger, "exp": sc_exp, "result": sc_result, "fix": sc_fix, "take": sc_take, "loop": sc_loop, "outro": sc_outro}

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
    s.pop(WT("h1", "money"), 0.04, 650)
    s.pop(WT("p1", "reviews.") - 0.05, 0.035, 520); s.pop(WT("p1", "history.") - 0.05, 0.035, 480); s.pop(WT("p1", "you") - 0.1, 0.035, 600)
    s.pop(WT("s1", "dealer") - 0.1, 0.03, 540); s.pop(WT("s1", "postcards") - 0.15, 0.03, 600); s.pop(WT("s1", "postcards") - 0.03, 0.03, 640)
    s.ding(WT("s1", "own") - 0.1, 1318, 0.025)
    s.pop(WT("s2", "seller,") - 0.05, 0.035, 560); s.pop(WT("s2", "postcards.") - 0.05, 0.035, 620)
    for i in range(6): s.tick(WT("s2", "8.1%") - 0.1 + i * 0.13, 0.02) if hasattr(s, "tick") else None
    s.ding(WT("s2", "8.1%") + 0.8, 1568, 0.035); s.pop(WT("s2", "track") - 0.1, 0.035, 640)
    for i in range(3): s.pop(WT("f1", "past") - 0.05 + i * 0.18, 0.03, 560 + i * 60)
    s.ding(WT("f1", "reviews,"), 1318, 0.025); s.pop(WT("f1", "anyone") - 0.2, 0.035, 620)
    s.thud(WT("tk", "feeling.") + 0.15, 0.07)
    for i, ti in enumerate((WT("tk", "track") + 0.1, WT("tk", "track") + 0.4, WT("tk", "check."))): s.pop(ti, 0.035, 600 + i * 70)
    s.ding(WT("tk", "check."), 1568, 0.03); s.pop(WT("tk", "send") - 0.1, 0.035, 640)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson11_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
