"""Auction short 09 (v3, standard): "The Lebanese 10% rule" (زيادة العشر). Lebanese Code of Civil Procedure Art. 978: if the winner
of a court property auction doesn't deposit the full price within three days of the award, a new session is announced (naming the
property, the price and the buyer); anyone who brings the price + one tenth (in full, or a bank guarantee) reopens the bidding from
there; if nobody does, the first buyer may still pay, with the costs of his delay, in that session; otherwise it goes straight back
to auction. Prices ($100,000 / $110,000) are illustrative.
Run: python3 tools/lessons/lesson09.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson09_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "pluck", 9
XF = 0.16
SC = [("hook", True, 0.0, S("s1") - 0.1), ("award", False, S("s1") - 0.1, S("s4") - 0.1), ("notice", True, S("s4") - 0.1, S("t1") - 0.1),
      ("takeover", False, S("t1") - 0.1, S("n1") - 0.1), ("nobody", True, S("n1") - 0.1, S("p1") - 0.1), ("point", False, S("p1") - 0.1, S("e2") - 0.15),
      ("outro", True, S("e2") - 0.15, TOTAL)]
GREY = (110, 116, 130)
STR = ("27", VIOLET)                                                                # the stranger: violet bidder, paddle 27
ILL = "Prices are illustrative · Code of Civil Procedure, Art. 978"

# ---------- drawings ----------
def apartment(s=220, col=BLUE):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * 0.18, s * 0.08, s * 0.82, s * 0.96), radius=10, fill=col + (255,))
    for r in range(4):
        for c in range(3): d.rounded_rectangle((s * (0.26 + c * 0.18), s * (0.16 + r * 0.17), s * (0.36 + c * 0.18), s * (0.27 + r * 0.17)), radius=3, fill=(220, 230, 255, 255))
    d.rectangle((s * 0.44, s * 0.8, s * 0.56, s * 0.96), fill=(30, 40, 80, 255)); return im

def row(who, name, price, dark, w=780, h=120, tag=None, hl=0.0):
    base = CARD_D if dark else (250, 250, 252); tgt = (54, 42, 108) if dark else (240, 235, 255)
    r = card(w, h, dark, 22, fill=tuple(int(a + (b - a) * hl) for a, b in zip(base, tgt)))
    r.alpha_composite(head(who, 80), (20, (h - 80) // 2)); ink = D_INK if dark else L_INK
    r.alpha_composite(T(name, 36, ink, 600), (120, h // 2 - 22))
    pt = T(price, 44, ink, 700); r.alpha_composite(pt, (w - 30 - pt.width, h // 2 - 26))
    if tag: r.alpha_composite(tag, (120 + T(name, 36, ink, 600).width + 18, h // 2 - tag.height // 2))
    return r

def result_card(t, dark=True, strike_k=0.0, top_k=0.0):
    w, h = 880, 620; win = window(w, h, "Court auction · Result", dark)
    win.alpha_composite(apartment(150), (50, 100)); ink = D_INK if dark else L_INK
    win.alpha_composite(T("Apartment", 46, ink, 700), (230, 120)); win.alpha_composite(T("public court sale", 30, D_MUTE if dark else GREY, 500), (230, 184))
    if top_k > 0:                                                                # the stranger's row slides in on top
        r = row(STR, "Bidder 27", "+10%", dark, tag=None, hl=0.6)
        put(win, r, w / 2, 340 + (1 - spring(top_k)) * -40, min(1, top_k * 2))
    ny = 340 + 140 * spring(top_k) if top_k > 0 else 340
    nr = row("nour", "Nour", money(100000), dark, tag=pill("WINNER", 24, GREEN_APP))
    put(win, nr, w / 2, ny)
    if strike_k > 0: strike(win, 60, int(ny), w - 60, strike_k, RED_UI, 10)
    return win

def day_tiles(t, k_days, dark=False):
    w, h = 880, 330; c = card(w, h, dark, 30); ink = D_INK if dark else L_INK
    c.alpha_composite(T("TO DEPOSIT THE FULL PRICE", 26, GREY, 700, True), (50, 40))
    for i in range(3):
        f = clamp(k_days * 3 - i); x = 50 + i * 270
        tile = card(240, 200, dark, 22, fill=tuple(int(a + (b - a) * f) for a, b in zip((246, 246, 250), (232, 226, 255))))
        tile.alpha_composite(T("DAY", 24, GREY, 700, True), (24, 24)); tile.alpha_composite(T(str(i + 1), 100, VIOLET if f > 0.5 else (200, 202, 212), 700), (24, 60))
        if f > 0: ImageDraw.Draw(tile).rounded_rectangle((24, 176, 24 + 192 * f, 186), radius=5, fill=VIOLET + (255,))
        c.alpha_composite(tile, (x, 100))
    return c

def notice_card(t, dark=True):
    w, h = 860, 720; c = card(w, h, False, 18, fill=(250, 248, 240)); d = ImageDraw.Draw(c)
    d.ellipse((w / 2 - 10, 14, w / 2 + 10, 34), fill=RED_UI + (255,))
    c.alpha_composite(T("PUBLIC NOTICE", 30, GREY, 700, True), (60, 60)); c.alpha_composite(T("New auction session", 58, L_INK, 700), (60, 110))
    d.line([(60, 200), (w - 60, 200)], fill=(210, 206, 196, 255), width=3)
    c.alpha_composite(apartment(110), (60, 230)); c.alpha_composite(T("Apartment", 44, L_INK, 700), (200, 262))
    c.alpha_composite(T("FIRST BUYER", 24, GREY, 700, True), (60, 390)); c.alpha_composite(head("nour", 80), (60, 430)); c.alpha_composite(T("Nour", 48, L_INK, 700), (160, 444))
    c.alpha_composite(T("FIRST PRICE", 24, GREY, 700, True), (60, 560)); c.alpha_composite(T(money(100000), 64, VIOLET, 700), (60, 596))
    return c

def check(s=56, col=GREEN_APP):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.ellipse((0, 0, s - 1, s - 1), fill=col + (255,))
    d.line([(s * 0.27, s * 0.52), (s * 0.44, s * 0.68), (s * 0.74, s * 0.34)], fill=(255, 255, 255, 255), width=max(4, s // 9)); return im

def pause_icon(s=200, col=L_INK):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * 0.22, s * 0.14, s * 0.42, s * 0.86), radius=12, fill=col + (255,)); d.rounded_rectangle((s * 0.58, s * 0.14, s * 0.78, s * 0.86), radius=12, fill=col + (255,))
    return im

def key_icon(s=150, col=(226, 188, 112)):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((s * 0.05, s * 0.3, s * 0.45, s * 0.7), outline=col + (255,), width=int(s * 0.1)); d.rectangle((s * 0.42, s * 0.45, s * 0.95, s * 0.55), fill=col + (255,))
    d.rectangle((s * 0.75, s * 0.55, s * 0.83, s * 0.7), fill=col + (255,)); d.rectangle((s * 0.87, s * 0.55, s * 0.95, s * 0.66), fill=col + (255,)); return im

# ---------- scenes ----------
def sc_hook(t):
    im = bg(True)
    if t < S("h2") - 0.05:
        sk = eout((t - WT("h1", "lose")) / 0.35); tk = clamp((t - WT("h1", "stranger") + 0.1) / 0.45)
        put(im, lift(result_card(t, True, sk, tk), True), 540, 1050, 1, 1.08 + 0.03 * spring(t / 0.5))
        stamp_at(im, big_stamp("+10%", LILAC, 120, -8), 800, 1460, t, WT("h1", "10%"))
        footnote(im, ILL, True)
    else:
        k = t - S("h2"); c = card(760, 640, True, 40); d = ImageDraw.Draw(c)
        tk = eout((t - WT("h2", "three")) / 0.9)
        d.arc((130, 60, 630, 560), -90, -90 + 360 * (1 - tk), fill=VIOLET + (255,), width=26)
        tt = T("3", 260, D_INK, 700); c.alpha_composite(tt, (380 - tt.width // 2, 150))
        dd = T("DAYS", 48, LILAC, 700, True); c.alpha_composite(dd, (380 - dd.width // 2, 440))
        put(im, lift(c, True), 540, 1080, ease(k / 0.25), 0.9 + 0.1 * spring(k / 0.45))
    return im

def sc_award(t):
    im = bg(False)
    if t < S("s3") - 0.1:
        w, h = 880, 700; win = window(w, h, "Court auction · Execution Department", False)
        win.alpha_composite(apartment(170), (50, 110)); win.alpha_composite(T("Apartment", 50, L_INK, 700), (250, 140)); win.alpha_composite(T("bidding", 30, GREY, 500), (250, 206))
        v = roll(t, WT("s1", "wins") - 0.2, 1.2, 60000, 100000); v = int(round(v / 1000) * 1000)
        win.alpha_composite(row("nour", "Nour", money(v), False, hl=ease((t - WT("s1", "Nour")) / 0.3)), (50, 340))
        if t >= WT("s2", "clock"):
            ck = card(780, 150, False, 22, fill=(246, 246, 250)); ck.alpha_composite(T("CLOCK STARTED", 28, VIOLET, 700, True), (40, 30))
            ck.alpha_composite(T("00:00:0" + str(min(9, int((t - WT("s2", "clock")) * 3))), 50, L_INK, 700, True), (40, 72)); put(win, ck, w / 2, 600, ease((t - WT("s2", "clock")) / 0.2))
        put(im, lift(win), 540, 1060, ease((t - S("s1") + 0.1) / 0.25), 0.95 + 0.05 * spring((t - S("s1") + 0.1) / 0.5))
        stamp_at(im, big_stamp("AWARDED", GREEN_APP, 96, -7), 540, 1560, t, WT("s2", "awards"))
        footnote(im, ILL)
    else:
        kd = clamp((t - WT("s3", "three")) / (E("s3") - WT("s3", "three") + 0.2))
        put(im, lift(day_tiles(t, kd)), 540, 980, ease((t - S("s3") + 0.1) / 0.25), 0.95 + 0.05 * spring((t - S("s3") + 0.1) / 0.5))
        if t >= WT("s3", "deposit"): put(im, pill("Deposit " + money(100000), 40, VIOLET), 540, 1290, ease((t - WT("s3", "deposit")) / 0.2), 0.8 + 0.2 * spring((t - WT("s3", "deposit")) / 0.4))
        footnote(im, "Code of Civil Procedure, Art. 978: three days from the award")
    return im

def sc_notice(t):
    im = bg(True)
    if t < WT("s4", "new") - 0.1:
        put(im, lift(day_tiles(t, 1.0, True), True), 540, 1000, 1)
        stamp_at(im, big_stamp("NOT PAID", RED_UI, 104, -8), 540, 1010, t, WT("s4", "doesn't,"))
    else:
        k = t - WT("s4", "new") + 0.1
        put(im, lift(notice_card(t), True), 540, 1080, ease(k / 0.25), 0.94 + 0.06 * spring(k / 0.5), -2 + 2 * ease(k / 0.5))
        x0, y0 = 540 - 430, 1080 - 360
        if t >= WT("s4", "name"): select_box(im, (x0 + 46, y0 + 420, x0 + 300, y0 + 524), eout((t - WT("s4", "name")) / 0.3))
        if t >= WT("s4", "price."): select_box(im, (x0 + 46, y0 + 584, x0 + 400, y0 + 690), eout((t - WT("s4", "price.")) / 0.3))
        footnote(im, "Code of Civil Procedure, Art. 978: the notice is published again", True)
    return im

def sc_takeover(t):
    im = bg(False)
    if t < S("t2") - 0.1:
        v = roll(t, WT("t1", "$110,000.") - 0.15, 0.6, 100000, 110000)
        c = stat("Bid to take over", money(int(round(v / 1000) * 1000)), "the first price + one tenth", 860, False, 170, VIOLET if v > 100000 else L_INK)
        put(im, lift(c), 540, 1050, ease((t - S("t1") + 0.1) / 0.25))
        kb = spring((t - WT("t1", "anyone")) / 0.45)
        if kb > 0: put(im, paddle(27, VIOLET, 130), 860, 760 + (1 - kb) * 80, min(1, kb * 1.5), 1, -8)
        if t >= WT("t1", "10%"): put(im, pill("+10%", 54, VIOLET), 300, 760, ease((t - WT("t1", "10%")) / 0.2), 0.8 + 0.2 * spring((t - WT("t1", "10%")) / 0.4))
        footnote(im, ILL)
    elif t < S("t3") - 0.1:
        c = card(880, 560, False, 30); c.alpha_composite(T("TO BID AT THIS SESSION", 26, GREY, 700, True), (50, 46))
        for i, (txt, w_) in enumerate((("The full amount, in hand", "full"), ("or a bank guarantee", "guarantee."))):
            y = 120 + i * 200; kk = ease((t - WT("t2", w_) + 0.1) / 0.25)
            r = card(780, 160, False, 22, fill=(246, 246, 250)); r.alpha_composite(T(txt, 44, L_INK, 700), (40, 52))
            if kk > 0.5: r.alpha_composite(check(64), (780 - 100, 48))
            if kk > 0: put(c, r, 440, y + 80, kk)
        put(im, lift(c), 540, 1060, ease((t - S("t2") + 0.1) / 0.25))
        footnote(im, "Code of Civil Procedure, Art. 978: no offer counts without it")
    else:
        w, h = 880, 640; win = window(w, h, "New session · bidding", False)
        bids = [(STR, "Bidder 27", 110000), (("B", GREEN_APP), "Bidder 8", 112000), (STR, "Bidder 27", 114000)]
        t0 = WT("t3", "starts")
        for i, (who, nm, p) in enumerate(bids):
            kk = spring((t - t0 - i * 0.45) / 0.4)
            if kk > 0: put(win, row(who, nm, money(p), False, hl=1.0 if i == min(2, int((t - t0) / 0.45)) else 0), w / 2, 160 + i * 150 + (1 - kk) * 30, min(1, kk * 1.5))
        put(im, lift(win), 540, 1080, ease((t - S("t3") + 0.1) / 0.25))
        if t >= WT("t3", "starts"): put(im, pill("BIDDING REOPENS", 36, VIOLET), 540, 700, ease((t - WT("t3", "starts")) / 0.2), 0.8 + 0.2 * spring((t - WT("t3", "starts")) / 0.4))
        footnote(im, ILL)
    return im

def sc_nobody(t):
    im = bg(True)
    if t < S("n2") - 0.1:
        if t < WT("n1", "Nour") - 0.1:
            c = card(860, 300, True, 30)
            for i in range(5):
                x = 70 + i * 150; ImageDraw.Draw(c).rounded_rectangle((x, 90, x + 110, 210), radius=18, outline=(70, 76, 96, 255), width=5)
            put(im, lift(c, True), 540, 1050, ease((t - S("n1") + 0.1) / 0.25))
            if t >= WT("n1", "nobody"): put(im, pill("NO +10% OFFER", 40, (60, 66, 86)), 540, 1290, ease((t - WT("n1", "nobody")) / 0.2))
        else:
            k = t - WT("n1", "Nour") + 0.1; c = card(860, 600, True, 30)
            c.alpha_composite(head("nour", 140), (50, 50)); c.alpha_composite(T("Nour", 56, D_INK, 700), (220, 70)); c.alpha_composite(T("first buyer", 30, D_MUTE, 500), (220, 140))
            c.alpha_composite(T("CAN STILL PAY", 26, LILAC, 700, True), (50, 250)); c.alpha_composite(T(money(100000), 84, D_INK, 700), (50, 296))
            if t >= WT("n1", "plus"): c.alpha_composite(T("+ the cost of the delay", 40, LILAC, 600), (50, 420))
            if t >= WT("n1", "session."): c.alpha_composite(chip("in that same session", True, 30), (50, 500))
            put(im, lift(c, True), 540, 1060, ease(k / 0.25), 0.95 + 0.05 * spring(k / 0.5))
    else:
        c = card(860, 520, True, 30); c.alpha_composite(apartment(220, VIOLET), (320, 60)); c.alpha_composite(T("Apartment", 50, D_INK, 700), (300, 330))
        put(im, lift(c, True), 540, 1040, ease((t - S("n2") + 0.1) / 0.25))
        stamp_at(im, big_stamp("BACK TO AUCTION", LILAC, 84, -7), 540, 1360, t, WT("n2", "straight"))
    footnote(im, "Code of Civil Procedure, Art. 978", True)
    return im

def sc_point(t):
    im = bg(False)
    if t < S("p2") - 0.1:
        c = card(860, 560, False, 30); d = ImageDraw.Draw(c)
        c.alpha_composite(T("THE SALE", 26, GREY, 700, True), (50, 46))
        pk = (t - S("p1")) * 0.25 % 1.0; d.rounded_rectangle((50, 110, 810, 160), radius=25, fill=(236, 237, 242, 255)); d.rounded_rectangle((50, 110, 50 + 760 * (0.3 + 0.6 * pk), 160), radius=25, fill=VIOLET + (255,))
        c.alpha_composite(pause_icon(220), (320, 220))
        put(im, lift(c), 540, 1050, ease((t - S("p1") + 0.1) / 0.25))
        if t >= WT("p1", "freeze"): strike(im, 540 - 200, 1050 + 50, 540 + 200, eout((t - WT("p1", "freeze")) / 0.3), RED_UI, 18)
        stamp_at(im, big_stamp("CAN'T FREEZE IT", RED_UI, 76, -7), 540, 1440, t, WT("p1", "sale."))
    else:
        c = card(880, 520, False, 30)
        for i, (txt, w_) in enumerate((("1   Win the bid", "Winning"), ("2   Pay", "Paying"))):
            kk = ease((t - WT("p2", w_) + 0.1) / 0.25); r = card(780, 170, False, 22, fill=(240, 235, 255) if kk > 0.5 else (246, 246, 250))
            r.alpha_composite(T(txt, 54, L_INK, 700), (40, 50))
            if kk > 0.5: r.alpha_composite(check(70), (780 - 110, 50))
            c.alpha_composite(r, (50, 60 + i * 210))
        put(im, lift(c), 540, 1020, ease((t - S("p2") + 0.1) / 0.25))
        kk = spring((t - WT("p2", "yours.")) / 0.45)
        if kk > 0: put(im, key_icon(170), 380, 1440, min(1, kk * 1.5), 0.6 + 0.4 * kk); put(im, head("nour", 150), 640, 1440, min(1, kk * 1.5))
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

FN = {"hook": sc_hook, "award": sc_award, "notice": sc_notice, "takeover": sc_takeover, "nobody": sc_nobody, "point": sc_point, "outro": sc_outro}

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
    s.thud(WT("h1", "10%"), 0.08); s.pop(WT("h1", "stranger"), 0.04, 700); s.pop(S("h2"), 0.05, 520)
    for i in range(8): s.tick(WT("h2", "three") + i * 0.11, 0.012, 2200)
    for i in range(10): s.tick(WT("s1", "wins") - 0.2 + i * 0.1, 0.012, 2400)
    s.thud(WT("s2", "awards"), 0.08); s.pop(WT("s2", "clock"), 0.04, 650)
    for i in range(3): s.pop(WT("s3", "three") + i * 0.35, 0.04, 600 + i * 90)
    s.thud(WT("s4", "doesn't,"), 0.08); s.pop(WT("s4", "new"), 0.05, 560); s.ding(WT("s4", "name"), 1175, 0.03); s.ding(WT("s4", "price."), 1318, 0.03)
    s.pop(WT("t1", "anyone"), 0.04, 700); s.pop(WT("t1", "10%"), 0.05, 760)
    for i in range(8): s.tick(WT("t1", "$110,000.") - 0.15 + i * 0.07, 0.012, 2400)
    s.ding(WT("t1", "$110,000."), 1568, 0.03); s.ding(WT("t2", "full"), 1318, 0.025); s.ding(WT("t2", "guarantee."), 1568, 0.025)
    for i in range(3): s.pop(WT("t3", "starts") + i * 0.45, 0.04, 640 + i * 60)
    s.pop(WT("n1", "nobody"), 0.04, 420); s.pop(WT("n1", "Nour"), 0.05, 650); s.thud(WT("n2", "straight"), 0.08)
    s.thud(WT("p1", "sale."), 0.08); s.ding(WT("p2", "Winning"), 1175, 0.03); s.ding(WT("p2", "Paying"), 1568, 0.035); s.pop(WT("p2", "yours."), 0.05, 760)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson09_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
