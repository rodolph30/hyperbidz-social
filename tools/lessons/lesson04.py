"""Auction short 04 (v3): "Why things end up at auction in Lebanon". Owner's change request (18 Oct 2026): not how auctions work
(everyone knows), but WHY things go to auction in Lebanon, WHEN and WHERE. Style v3: word captions + UI cards, whips.
Run: python3 tools/lessons/lesson04.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson04_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "pluck", 4
XF = 0.16
SC = [("hook", True, 0.0, S("a1") - 0.1), ("inherit", False, S("a1") - 0.1, S("b1") - 0.1), ("debt", True, S("b1") - 0.1, S("c1") - 0.1),
      ("goods", False, S("c1") - 0.1, S("w1") - 0.1), ("where", True, S("w1") - 0.1, S("w2") - 0.1), ("notice", False, S("w2") - 0.1, S("e2") - 0.15),
      ("outro", True, S("e2") - 0.15, TOTAL)]
LAND = (88, 168, 120)

# ---------- small drawings ----------
def land_shape(w, h, split_k=0.0, fail=0.0, t=0.0):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(0.08, 0.2), (0.5, 0.05), (0.93, 0.18), (0.97, 0.7), (0.62, 0.95), (0.12, 0.86), (0.03, 0.52)]
    d.polygon([(x * w, y * h) for x, y in pts], fill=LAND + (255,), outline=(60, 130, 90, 255))
    for i in range(5): d.ellipse((w * (0.2 + 0.13 * i) - 14, h * (0.35 + 0.08 * (i % 2)) - 14, w * (0.2 + 0.13 * i) + 14, h * (0.35 + 0.08 * (i % 2)) + 14), fill=(60, 140, 90, 255))
    d.rectangle((w * 0.62, h * 0.55, w * 0.78, h * 0.75), fill=(240, 236, 226, 255)); d.polygon([(w * 0.6, h * 0.56), (w * 0.7, h * 0.46), (w * 0.8, h * 0.56)], fill=(200, 90, 80, 255))
    if split_k > 0:                                                             # someone tries to split it in two
        jit = 6 * np.sin(t * 40) * fail; x0 = w * 0.48 + jit
        n = int(14 * clamp(split_k))
        for i in range(n): d.line([(x0 + 6 * np.sin(i), h * (0.04 + i * 0.07)), (x0 + 6 * np.sin(i + 0.5), h * (0.04 + i * 0.07 + 0.04))], fill=(255, 255, 255, 255), width=6)
    if fail > 0:
        c = (w / 2, h / 2); r = 70 * spring(fail)
        d.line([(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)], fill=RED_UI + (255,), width=18); d.line([(c[0] - r, c[1] + r), (c[0] + r, c[1] - r)], fill=RED_UI + (255,), width=18)
    return im

def plot_window(t, dark, hl_nour=0.0, split_k=0.0, fail=0.0):
    w, h = 880, 860; win = window(w, h, "Land registry · inherited plot", dark)
    win.alpha_composite(land_shape(780, 420, split_k, fail, t), (50, 100))
    for i, (who, nm, sh) in enumerate((("sami", "Sami", "50%"), ("nour", "Nour", "50%"))):
        y = 560 + i * 130; hl = hl_nour if who == "nour" else 0
        row = card(780, 110, dark, 22, fill=(tuple(int(a + (b - a) * hl) for a, b in zip(CARD_D if dark else (250, 250, 252), (54, 42, 108) if dark else (240, 235, 255)))))
        row.alpha_composite(head(who, 74), (18, 18)); row.alpha_composite(T(nm + " · co-owner", 34, D_INK if dark else L_INK, 600), (110, 34))
        row.alpha_composite(T(sh, 40, D_INK if dark else L_INK, 700), (780 - 110, 30)); win.alpha_composite(row, (50, y))
    return win

def icon_bank(s=150, col=(255, 255, 255)):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s * 0.1, s * 0.34), (s * 0.5, s * 0.08), (s * 0.9, s * 0.34)], fill=col + (255,))
    for i in range(4): x = s * (0.18 + i * 0.2); d.rectangle((x, s * 0.4, x + s * 0.1, s * 0.78), fill=col + (255,))
    d.rectangle((s * 0.08, s * 0.82, s * 0.92, s * 0.9), fill=col + (255,)); return im
def icon_doc(s=150, col=(255, 255, 255)):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * 0.2, s * 0.04, s * 0.8, s * 0.96), radius=10, fill=col + (255,))
    for i in range(5): d.rectangle((s * 0.3, s * (0.18 + i * 0.1), s * (0.7 if i % 2 else 0.62), s * (0.22 + i * 0.1)), fill=(150, 156, 176, 255))
    tt = T("$", int(s * 0.3), (30, 34, 46), 700); im.alpha_composite(tt, (int(s * 0.5 - tt.width / 2), int(s * 0.66))); return im
def icon_car(s=170, col=BLUE):
    im = Image.new("RGBA", (s, int(s * 0.7)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * 0.05, s * 0.28, s * 0.95, s * 0.52), radius=16, fill=col + (255,)); d.polygon([(s * 0.25, s * 0.3), (s * 0.35, s * 0.1), (s * 0.68, s * 0.1), (s * 0.8, s * 0.3)], fill=col + (255,))
    d.polygon([(s * 0.33, s * 0.28), (s * 0.4, s * 0.15), (s * 0.5, s * 0.15), (s * 0.5, s * 0.28)], fill=(220, 230, 255, 255)); d.polygon([(s * 0.53, s * 0.28), (s * 0.53, s * 0.15), (s * 0.64, s * 0.15), (s * 0.72, s * 0.28)], fill=(220, 230, 255, 255))
    for x in (0.27, 0.73): d.ellipse((s * x - s * 0.1, s * 0.42, s * x + s * 0.1, s * 0.62), fill=(30, 34, 46, 255))
    return im
def icon_sofa(s=170, col=VIOLET):
    im = Image.new("RGBA", (s, int(s * 0.7)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * 0.12, s * 0.1, s * 0.88, s * 0.42), radius=18, fill=tuple(min(255, c + 30) for c in col) + (255,))
    d.rounded_rectangle((s * 0.04, s * 0.3, s * 0.96, s * 0.56), radius=18, fill=col + (255,)); d.rectangle((s * 0.12, s * 0.56, s * 0.18, s * 0.66), fill=(60, 50, 90, 255)); d.rectangle((s * 0.82, s * 0.56, s * 0.88, s * 0.66), fill=(60, 50, 90, 255))
    return im
def icon_ring(s=170):
    im = Image.new("RGBA", (s, int(s * 0.7)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s / 2
    d.ellipse((c - s * 0.26, s * 0.18, c + s * 0.26, s * 0.66), outline=(226, 188, 112, 255), width=int(s * 0.07))
    d.polygon([(c - s * 0.1, s * 0.16), (c, s * 0.02), (c + s * 0.1, s * 0.16), (c, s * 0.26)], fill=(190, 225, 255, 255)); return im
def icon_court(s=220, col=(255, 255, 255)):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s * 0.06, s * 0.3), (s * 0.5, s * 0.06), (s * 0.94, s * 0.3)], fill=col + (255,)); d.rectangle((s * 0.08, s * 0.31, s * 0.92, s * 0.36), fill=col + (255,))
    for i in range(5): x = s * (0.14 + i * 0.16); d.rectangle((x, s * 0.4, x + s * 0.08, s * 0.8), fill=col + (255,))
    d.rectangle((s * 0.04, s * 0.84, s * 0.96, s * 0.92), fill=col + (255,)); return im

def newspaper(title, w=360, h=240, dark=False):
    c = card(w, h, dark, 18); d = ImageDraw.Draw(c); c.alpha_composite(T(title, 30, L_INK if not dark else D_INK, 700), (24, 22))
    d.line([(24, 70), (w - 24, 70)], fill=(200, 202, 210, 255), width=3)
    for i in range(5): d.rectangle((24, 90 + i * 26, (w - 24) if i % 3 else w * 0.6, 102 + i * 26), fill=(220, 222, 230, 255))
    d.rounded_rectangle((w - 150, 92, w - 24, 150), radius=6, outline=VIOLET + (255,), width=3); c.alpha_composite(T("AUCTION", 20, VIOLET, 700, True), (w - 140, 110))
    return c

def door(t, notice_k=0.0, w=420, h=700):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=10, fill=(120, 84, 60, 255)); d.rounded_rectangle((26, 26, w - 27, h - 27), radius=8, outline=(96, 66, 46, 255), width=8)
    d.ellipse((w - 70, h / 2 - 16, w - 38, h / 2 + 16), fill=(226, 188, 112, 255))
    if notice_k > 0:
        nw, nh = 250, 330; n = Image.new("RGBA", (nw, nh), (0, 0, 0, 0)); dn = ImageDraw.Draw(n); dn.rectangle((0, 0, nw - 1, nh - 1), fill=(250, 248, 240, 255))
        n.alpha_composite(T("PUBLIC", 28, L_INK, 700, True), (24, 22)); n.alpha_composite(T("AUCTION", 28, VIOLET, 700, True), (24, 56))
        for i in range(7): dn.rectangle((24, 110 + i * 26, nw - 24 - (40 if i % 2 else 0), 120 + i * 26), fill=(200, 202, 210, 255))
        dn.ellipse((nw / 2 - 7, 6, nw / 2 + 7, 20), fill=(229, 56, 84, 255))
        put(im, n.rotate(-3 * (1 - notice_k) + 2, expand=True, resample=Image.BICUBIC), w / 2 - 20, h * 0.38, min(1, notice_k * 2), 0.9 + 0.1 * spring(notice_k))
    return im

def section_pill(n, text, dark, t, t0):
    p = pill(f"{n}  ·  {text}", 40, VIOLET); return p

# ---------- scenes ----------
def sc_hook(t):
    im = bg(True); hl = ease((t - WT("h1", "cousin")) / 0.3)
    put(im, lift(plot_window(t, True, hl), True), 540, 1020, ease(t / 0.25), 0.96 + 0.04 * spring(t / 0.5))
    if t >= WT("h1", "cousin"): put(im, pill("wants to sell", 30, VIOLET), 760, 1020 - 430 + 560 + 130 + 55 - 70, ease((t - WT("h1", "cousin")) / 0.2))
    stamp_at(im, big_stamp("AUCTION", LILAC, 96, -8), 540, 860, t, WT("h1", "auction"))
    if t >= WT("h2", "three"):                                                   # three cards: the three ways (revealed later)
        for i in range(3):
            k = spring((t - WT("h2", "three") - i * 0.12) / 0.4)
            if k <= 0: continue
            c = card(250, 170, True, 22); c.alpha_composite(T(str(i + 1), 70, LILAC, 700), (30, 40)); c.alpha_composite(T("?", 70, D_MUTE, 700), (170, 40))
            put(im, lift(c, True), 540 + (i - 1) * 280, 1650 + (1 - k) * 80, min(1, k * 1.5))
    return im

def sc_inherit(t):
    im = bg(False); put(im, section_pill(1, "INHERITANCE", False, t, S("a1")), 540, 520, ease((t - S("a1")) / 0.2), 0.8 + 0.2 * spring((t - S("a1")) / 0.4))
    if t < S("a3") - 0.1:
        c = card(900, 430, False, 30); c.alpha_composite(T("CODE OF OBLIGATIONS AND CONTRACTS · ART. 840", 24, (110, 116, 130), 700, True), (50, 46))
        c.alpha_composite(T("No one is forced to", 64, L_INK, 700), (50, 120)); c.alpha_composite(T("stay a co-owner.", 64, VIOLET, 700), (50, 200))
        c.alpha_composite(T("Any co-owner can ask the court to end it.", 32, (100, 106, 120), 500), (50, 320))
        put(im, lift(c), 540, 1000, ease((t - S("a2") + 0.15) / 0.25), 0.95 + 0.05 * spring((t - S("a2") + 0.15) / 0.5))
        if t >= WT("a2", "co-owner"): select_box(im, (540 - 450 + 40, 1000 - 215 + 196, 540 - 450 + 40 + T("stay a co-owner.", 64, VIOLET, 700).width + 20, 1000 - 215 + 290), eout((t - WT("a2", "co-owner")) / 0.3))
    else:
        sk = ease((t - WT("a3", "split")) / 0.5); fail = clamp((t - WT("a3", "split") - 0.4) / 0.4)
        put(im, lift(plot_window(t, False, 0, sk, fail)), 540, 1080, ease((t - S("a3") + 0.1) / 0.25))
        stamp_at(im, big_stamp("PUBLIC AUCTION", VIOLET, 84, -7), 540, 900, t, WT("a3", "public"))
        footnote(im, "Code of Obligations and Contracts, Arts. 840 and 942 · Law 16/1982")
    return im

def sc_debt(t):
    im = bg(True); put(im, section_pill(2, "UNPAID DEBT", True, t, S("b1")), 540, 520, ease((t - S("b1")) / 0.2), 0.8 + 0.2 * spring((t - S("b1")) / 0.4))
    if t < S("b3") - 0.1:
        k1 = spring((t - WT("b2", "bank") + 0.1) / 0.4); k2 = spring((t - WT("b2", "court") + 0.1) / 0.4)
        bc = card(420, 420, True, 28); bc.alpha_composite(icon_doc(150), (135, 40)); bc.alpha_composite(T("Bank loan", 40, D_INK, 700), (50, 220)); bc.alpha_composite(pill("UNPAID", 26, RED_UI), (50, 290))
        if k1 > 0: put(im, lift(bc, True), 540 - 230, 1050 + (1 - k1) * 60, min(1, k1 * 1.5))
        cc = card(420, 420, True, 28); cc.alpha_composite(icon_court(170), (125, 30)); cc.alpha_composite(T("Court", 40, D_INK, 700), (50, 220)); cc.alpha_composite(T("request to sell", 30, D_MUTE, 500), (50, 280))
        if k2 > 0: put(im, lift(cc, True), 540 + 230, 1050 + (1 - k2) * 60, min(1, k2 * 1.5))
        if t >= WT("b2", "sell"): put(im, pill("SELL", 34, VIOLET), 540 + 230, 1050 + 160, ease((t - WT("b2", "sell")) / 0.2), 0.8 + 0.2 * spring((t - WT("b2", "sell")) / 0.4))
    else:
        c = card(900, 520, True, 30); d = ImageDraw.Draw(c)
        c.alpha_composite(T("VALUATION", 26, D_MUTE, 700, True), (50, 50)); d.rounded_rectangle((50, 100, 850, 160), radius=30, fill=(60, 66, 86, 255))
        c.alpha_composite(T("100%", 30, D_INK, 700), (70, 112))
        c.alpha_composite(T("BIDDING OPENS AT", 26, D_MUTE, 700, True), (50, 210)); kk = eout((t - WT("b3", "60%") + 0.3) / 0.8)
        d.rounded_rectangle((50, 260, 850, 320), radius=30, fill=(40, 46, 60, 255)); d.rounded_rectangle((50, 260, 50 + 800 * 0.6 * kk, 320), radius=30, fill=VIOLET + (255,))
        c.alpha_composite(T(f"{int(round(60 * kk))}%", 120, D_INK, 700), (50, 360))
        put(im, lift(c, True), 540, 1050, ease((t - S("b3") + 0.1) / 0.25))
        footnote(im, "Code of Civil Procedure, Arts. 948 and 965", True)
    return im

def sc_goods(t):
    im = bg(False); put(im, section_pill(3, "SEIZED GOODS", False, t, S("c1")), 540, 520, ease((t - S("c1")) / 0.2), 0.8 + 0.2 * spring((t - S("c1")) / 0.4))
    items = [("Car", icon_car(200), WT("c2", "Cars")), ("Furniture", icon_sofa(200), WT("c2", "furniture")), ("Gold & antiques", icon_ring(200), WT("c2", "jewelry"))]
    tg = WT("c2", "gold"); t90 = WT("c2", "90%")
    for i, (nm, ic, t0) in enumerate(items):
        k = spring((t - t0 + 0.1) / 0.4)
        if k <= 0: continue
        gold = i == 2 and t >= tg - 0.1
        c = card(300, 470, False, 26, fill=(255, 249, 232) if gold else None); c.alpha_composite(ic, (50, 50))
        c.alpha_composite(T(nm, 30, L_INK, 700), (28, 230))
        lab = "min 90%" if (i == 2 and t >= t90 - 0.1) else "min 60%"
        c.alpha_composite(pill(lab, 30, VIOLET if lab == "min 90%" else (236, 237, 242), (255, 255, 255) if lab == "min 90%" else (96, 102, 116)), (28, 300))
        c.alpha_composite(T("of its value", 24, (130, 136, 150), 500), (30, 370))
        x = 540 + (i - 1) * 320; put(im, lift(c), x, 1080 + (1 - k) * 60, min(1, k * 1.5), 1 + (0.06 * spring((t - tg) / 0.4) if gold else 0))
        if lab == "min 90%": select_box(im, (x - 150 + 20, 1080 - 235 + 292, x - 150 + 220, 1080 - 235 + 362), eout((t - t90 + 0.1) / 0.3))
    footnote(im, "Code of Civil Procedure, Arts. 928 and 929 (court sales of seized goods)")
    return im

def sc_where(t):
    im = bg(True)
    if t < WT("w1", "courthouse") - 0.1:
        b = window(820, 380, "", True); b.alpha_composite(T("www.", 110, D_MUTE, 700), (60, 120)); put(im, lift(b, True), 540, 1000, ease((t - S("w1")) / 0.25))
        if t >= WT("w1", "Not"): strike(im, 540 - 380, 1010, 540 + 380, eout((t - WT("w1", "Not")) / 0.35), RED_UI, 14); stamp_at(im, big_stamp("NOT ONLINE", RED_UI, 70, -8), 540, 1230, t, WT("w1", "online"))
    else:
        c = card(860, 620, True, 30); c.alpha_composite(icon_court(300), (280, 40))
        c.alpha_composite(T("Execution Department", 54, D_INK, 700), (70, 380)); c.alpha_composite(T("public session, before its head", 32, D_MUTE, 500), (70, 460))
        put(im, lift(c, True), 540, 1030, ease((t - WT("w1", "courthouse") + 0.1) / 0.25), 0.95 + 0.05 * spring((t - WT("w1", "courthouse") + 0.1) / 0.5))
        if t >= WT("w1", "Execution"): select_box(im, (540 - 430 + 60, 1030 - 310 + 370, 540 - 430 + 60 + T("Execution Department", 54, D_INK, 700).width + 20, 1030 - 310 + 450), eout((t - WT("w1", "Execution")) / 0.3))
        for i in range(4):
            k = spring((t - WT("w1", "Department") - i * 0.1) / 0.4)
            if k > 0: put(im, head(["sami", "nour", ("A", VIOLET), ("B", GREEN_APP)][i], 90), 540 + (i - 1.5) * 120, 1440, min(1, k * 1.5))
        footnote(im, "Code of Civil Procedure, Art. 975", True)
    return im

def sc_notice(t):
    im = bg(False)
    if t < S("p1") - 0.1:
        for i, (nm, t0) in enumerate((("Daily paper", WT("w2", "two")), ("Daily paper", WT("w2", "newspapers")), ("Official Gazette", WT("w2", "Gazette")))):
            k = spring((t - t0 + 0.1) / 0.4)
            if k > 0: put(im, lift(newspaper(nm, 320, 230)), 210 + i * 330, 760 + (1 - k) * 60, min(1, k * 1.5), 1, (i - 1) * 3)
        if t >= WT("w2", "paper,") - 0.1:
            put(im, lift(door(t, ease((t - WT("w2", "door.") + 0.2) / 0.4), 380, 640)), 540, 1330, ease((t - WT("w2", "paper,") + 0.1) / 0.25))
            put(im, chip("municipality", False, 24), 540, 1690, ease((t - WT("w2", "municipality's")) / 0.25))
        footnote(im, "Code of Civil Procedure, Arts. 969-971 · at least 10 days before the session")
    else:
        z = 1 + 0.25 * eout((t - S("p1")) / 1.2)
        put(im, lift(door(t, 1.0, 380, 640)), 540, 1100, 1, 1.25 * z)
        if t >= WT("p1", "read"): select_box(im, (540 - 190, 1100 - 330, 540 + 160, 1100 + 120), eout((t - WT("p1", "read")) / 0.3))
        stamp_at(im, big_stamp("AUCTION", VIOLET, 96, -8), 540, 1600, t, WT("p1", "auction"))
    return im

def sc_outro(t):
    im = bg(True); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 14, BLUE), (540, 27, VIOLET), (750, 8, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories"); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "inherit": sc_inherit, "debt": sc_debt, "goods": sc_goods, "where": sc_where, "notice": sc_notice, "outro": sc_outro}

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
    s.pop(WT("h1", "cousin"), 0.04, 700); s.thud(WT("h1", "auction"), 0.08)
    for i in range(3): s.pop(WT("h2", "three") + i * 0.12, 0.035, 600 + i * 80)
    for k in ("a1", "b1", "c1"): s.pop(S(k), 0.05, 500)
    s.ding(WT("a2", "co-owner"), 1318, 0.03); s.thud(WT("a3", "public"), 0.08)
    s.pop(WT("b2", "bank"), 0.04, 650); s.pop(WT("b2", "court"), 0.04, 750)
    for i in range(10): s.tick(WT("b3", "60%") - 0.3 + i * 0.08, 0.012, 2400)
    for w in ("Cars", "furniture", "jewelry"): s.pop(WT("c2", w), 0.04, 700)
    s.ding(WT("c2", "90%"), 1568, 0.03); s.thud(WT("w1", "online"), 0.07); s.ding(WT("w1", "Execution"), 1175, 0.03)
    for w in ("two", "newspapers", "Gazette"): s.pop(WT("w2", w), 0.04, 650)
    s.thud(WT("p1", "auction"), 0.08)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson04_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
