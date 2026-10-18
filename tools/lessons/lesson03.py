"""Auction short 03: "The busiest minute on Wall Street" (the closing auction). v3 style: word-by-word captions + UI cards,
light/dark scenes, whip transitions (after the reference reel the owner shared on 18 Oct 2026). No HyperBidz, no app UI.
Run: python3 tools/lessons/lesson03.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson03_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "ambient", 3
XF = 0.16
SC = [("hook", True, 0.0, S("b1") - 0.1), ("book", False, S("b1") - 0.1, S("c1") - 0.15), ("clock", True, S("c1") - 0.15, S("c2") - 0.1),
      ("match", True, S("c2") - 0.1, S("n1") - 0.15), ("name", False, S("n1") - 0.15, S("n3") - 0.15), ("record", True, S("n3") - 0.15, S("t1") - 0.15),
      ("news", False, S("t1") - 0.15, S("e1") - 0.15), ("outro", True, S("e1") - 0.15, TOTAL)]

# ---------- 1. hook: the day's volume, then the 4 p.m. spike ----------
BARS = [0.34, 0.22, 0.18, 0.15, 0.13, 0.12, 0.12, 0.11, 0.12, 0.13, 0.15, 0.17, 0.2, 0.26]
def sc_hook(t):
    im = bg(True); w, h = 900, 760; win = window(w, h, "NYSE · shares traded, minute by minute", True); d = ImageDraw.Draw(win)
    x0, y0, x1, y1 = 60, 150, w - 60, h - 110; n = len(BARS) + 1; bw = (x1 - x0) / n
    for i, v in enumerate(BARS):
        k = spring((t - 0.15 - i * 0.05) / 0.4); hh = (y1 - y0) * 0.28 * v * k
        d.rounded_rectangle((x0 + i * bw + 6, y1 - hh, x0 + (i + 1) * bw - 6, y1), radius=6, fill=(70, 78, 104, 255))
    ks = spring((t - WT("h1", "auction") + 0.1) / 0.6); hh = (y1 - y0) * 0.98 * ks
    if hh > 2: d.rounded_rectangle((x0 + (n - 1) * bw + 4, y1 - hh, x1 - 2, y1), radius=8, fill=VIOLET + (255,))
    for lab, i in (("9:30 AM", 0), ("12:00", 6), ("4:00 PM", n - 1)):
        tt = T(lab, 24, D_MUTE, 600, True); win.alpha_composite(tt, (int(x0 + i * bw + bw / 2 - tt.width / 2), int(y1 + 22)))
    a = ease(t / 0.25); put(im, lift(win, True), 540, 960, a, 0.96 + 0.04 * spring(t / 0.5))
    if t >= WT("h2", "4"):
        k = (t - WT("h2", "4")); put(im, pill("4:00 PM", 44, VIOLET), 540 + w / 2 - 110, 960 - h / 2 + 150, ease(k / 0.2), 0.8 + 0.2 * spring(k / 0.4))
        select_box(im, (540 + w / 2 - 210, 960 - h / 2 + 116, 540 + w / 2 - 10, 960 - h / 2 + 184), eout(k / 0.3))
    footnote(im, "Bar heights are illustrative", True, 1440)
    return im

# ---------- 2. order book: Nour bids, Sami asks, they meet ----------
def book_row(side, price, qty, who=None, hl=False, w=380):
    im = card(w, 104, False, 22, fill=((233, 250, 241) if side == "bid" else (255, 236, 240)) if hl else (250, 250, 252), border=True)
    if who: im.alpha_composite(head(who, 66), (18, 19))
    else: im.alpha_composite(T(f"x{qty}", 26, (140, 146, 158), 600, True), (26, 36))
    tt = T(f"${price}", 46, GREEN_UI if side == "bid" else RED_UI); im.alpha_composite(tt, (w - tt.width - 26, 26)); return im

def sc_book(t):
    im = bg(False); w, h = 900, 760; win = window(w, h, "Order book · one stock", False)
    lb = T("BIDS · buy", 28, GREEN_UI, 700, True); la = T("ASKS · sell", 28, RED_UI, 700, True)
    win.alpha_composite(lb, (60, 110)); win.alpha_composite(la, (w - 60 - la.width, 110))
    t_n, t_s, t_meet, t_trade = WT("b2", "Nour"), WT("b2", "Sami"), WT("b3", "meets"), WT("b3", "trade")
    churn = int(max(0, t - S("b1")) * 7)                                       # all day long: orders come and go one by one
    for i in range(4):
        y = 170 + i * 124; nb = (i == 0 and t >= t_n); sa = (i == 0 and t >= t_s)
        bp = 101 - i; ap = 102 + i
        if nb and t >= t_meet + 0.25: bp = 102
        q1 = [300, 120, 450, 80, 200, 650][(i + churn) % 6]; q2 = [150, 500, 90, 260, 700, 40][(i * 2 + churn) % 6]
        r1 = book_row("bid", bp, q1, "nour" if nb else None, nb); r2 = book_row("ask", ap, q2, "sami" if sa else None, sa)
        win.alpha_composite(r1, (50, y)); win.alpha_composite(r2, (w - 50 - r2.width, y))
    put(im, lift(win), 540, 900, ease((t - S("b1") + 0.15) / 0.25))
    if t_meet + 0.25 <= t:                                                     # Nour raises to meet Sami: a line joins them
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line([(540 - 52, 900 - h / 2 + 170 + 52), (540 + 52, 900 - h / 2 + 170 + 52)], fill=GREEN_UI + (255,), width=10); im.alpha_composite(lay)
    if t >= t_trade - 0.15:
        k = t - t_trade + 0.15; put(im, pill("TRADE AT $102", 50, GREEN_UI), 540, 900 + h / 2 + 90, ease(k / 0.15), 0.7 + 0.3 * spring(k / 0.4))
    return im

# ---------- 3. 4 p.m.: the clock ----------
def clock_face(t, hh=4, mm=0, s=520):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s / 2
    d.ellipse((0, 0, s - 1, s - 1), fill=(21, 25, 34, 255), outline=(60, 66, 86, 255), width=6)
    for i in range(12):
        a = i / 12 * 2 * np.pi; r1, r2 = c * 0.82, c * 0.92
        d.line([(c + np.sin(a) * r1, c - np.cos(a) * r1), (c + np.sin(a) * r2, c - np.cos(a) * r2)], fill=(150, 156, 176, 255), width=6)
    ah = (hh % 12 + mm / 60) / 12 * 2 * np.pi; am = mm / 60 * 2 * np.pi
    d.line([(c, c), (c + np.sin(ah) * c * 0.5, c - np.cos(ah) * c * 0.5)], fill=(255, 255, 255, 255), width=16)
    d.line([(c, c), (c + np.sin(am) * c * 0.75, c - np.cos(am) * c * 0.75)], fill=LILAC + (255,), width=10)
    d.ellipse((c - 16, c - 16, c + 16, c + 16), fill=VIOLET + (255,)); return im

def sc_clock(t):
    im = bg(True); t0 = S("c1"); k = clamp((t - t0) / max(0.1, WT("c1", "4") - t0 + 0.4))
    mins = int(55 + 5 * eout(k)) % 60; hh = 3 if mins >= 55 and k < 1 else 4
    shake = 6 * np.sin(t * 60) * (1 - clamp((t - WT("c1", "4") - 0.4) / 0.6)) * (t > WT("c1", "4") + 0.3)
    put(im, clock_face(t, hh if k < 1 else 4, 0 if k >= 1 else mins), 540 + shake, 930)
    if t >= WT("c1", "4") + 0.3:
        kk = t - WT("c1", "4") - 0.3; put(im, pill("4:00 PM · CLOSING BELL", 40, VIOLET), 540, 1290, ease(kk / 0.2), 0.8 + 0.2 * spring(kk / 0.4))
    if t >= WT("c1", "different") - 0.1:
        put(im, chip("New York Stock Exchange", True, 26), 540, 1390, ease((t - WT("c1", "different") + 0.1) / 0.25))
    return im

# ---------- 4. every order in, one price out ----------
def ticket(kind, i, dark=True):
    col = VIOLET if kind == "BUY" else BLUE; c = card(250, 74, dark, 18, fill=col, border=False)
    tt = T(f"{kind}  #{i:03d}", 28, (255, 255, 255), 700, True); c.alpha_composite(tt, (22, 20)); return c

def sc_match(t):
    im = bg(True); tb, ts, tp, te = WT("c2", "buy"), WT("c2", "sell"), WT("c3", "one"), S("c4")
    if t < tp - 0.2:                                                            # tickets pile into two stacks
        for side, t0, x in (("BUY", tb - 0.3, 300), ("SELL", ts - 0.3, 780)):
            for i in range(9):
                k = spring((t - t0 - i * 0.07) / 0.35)
                if k <= 0: continue
                put(im, lift(ticket(side, 100 + i * 7)), x + (1 - k) * (-500 if side == "BUY" else 500), 1300 - i * 46, min(1, k * 2), 1, (i % 3 - 1) * 2)
            put(im, T(side + " ORDERS", 30, LILAC if side == "BUY" else (140, 180, 255), 700, True), x, 1420, ease((t - t0) / 0.3))
    else:                                                                       # demand and supply cross at one price
        k = eout((t - tp + 0.2) / 0.9); w, h = 900, 760; win = window(w, h, "All orders at 4:00 PM", True); d = ImageDraw.Draw(win)
        x0, y0, x1, y1 = 90, 140, w - 70, h - 90
        d.line([(x0, y0), (x0, y1), (x1, y1)], fill=(70, 78, 100, 255), width=3)
        win.alpha_composite(T("price", 24, D_MUTE, 600, True), (x0 - 10, y0 - 46)); win.alpha_composite(T("shares", 24, D_MUTE, 600, True), (x1 - 90, y1 + 18))
        n = 40; dem = [(x0 + (x1 - x0) * i / n, y0 + 30 + (y1 - y0 - 60) * (i / n) ** 0.9) for i in range(n + 1)]
        sup = [(x0 + (x1 - x0) * i / n, y1 - 30 - (y1 - y0 - 60) * (i / n) ** 0.9) for i in range(n + 1)]
        m = int(n * k)
        if m > 1: d.line(dem[:m + 1], fill=VIOLET + (255,), width=10); d.line(sup[:m + 1], fill=BLUE + (255,), width=10)
        win.alpha_composite(T("buyers", 26, LILAC, 700), (x0 + 30, y0 + 10)); win.alpha_composite(T("sellers", 26, (140, 180, 255), 700), (x0 + 30, y1 - 60))
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if k > 0.55:
            kk = (t - tp - 0.4); d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=(255, 255, 255, 255))
        put(im, lift(win, True), 540, 960, ease((t - tp + 0.2) / 0.25))
        if t >= WT("c3", "price"):
            kk = t - WT("c3", "price"); put(im, pill("$101.20", 48, (255, 255, 255), STAGE), 540 + 120, 960 - 380 + 140 + (y1 - y0) / 2 - 90, ease(kk / 0.15), 0.8 + 0.2 * spring(kk / 0.4))
            select_box(im, (540 + 120 - 120, 960 - 380 + 140 + (y1 - y0) / 2 - 130, 540 + 120 + 120, 960 - 380 + 140 + (y1 - y0) / 2 - 50), eout(kk / 0.3))
        if t >= te:                                                             # everyone trades at that price
            kk = t - te; grid = Image.new("RGBA", (860, 300), (0, 0, 0, 0))
            for i in range(30):
                r, c = divmod(i, 10); x, y = 43 + c * 86, 50 + r * 100; on = ease((kk - 0.3 - i * 0.01) / 0.15)
                who = "nour" if i == 3 else ("sami" if i == 16 else ([" ", "  "][i % 2], [VIOLET, BLUE, GREEN_APP][i % 3]))
                hd = head(who if isinstance(who, str) else (who[0], who[1]), 64); grid.alpha_composite(hd, (int(x - 32), int(y - 32)))
                if on > 0: ImageDraw.Draw(grid).ellipse((x + 12, y + 12, x + 36, y + 36), fill=GREEN_UI + (int(255 * on),))
            put(im, grid, 540, 1520, ease(kk / 0.25))
            if t >= WT("c4", "go") - 0.1: put(im, pill("ONE PRICE. ONE MATCH.", 40, GREEN_UI), 540, 1720, ease((t - WT("c4", "go") + 0.1) / 0.2), 0.8 + 0.2 * spring((t - WT("c4", "go") + 0.1) / 0.4))
    return im

# ---------- 5. its name + how big ----------
def sc_name(t):
    im = bg(False)
    if t < S("n2") - 0.1:
        c = card(880, 360, False, 30); c.alpha_composite(T("closing auction", 84, L_INK, 700), (50, 50)); c.alpha_composite(T("NOUN · MARKETS", 24, (120, 126, 140), 700, True), (54, 160))
        ImageDraw.Draw(c).line([(50, 214), (830, 214)], fill=LINE_L + (255,), width=2)
        c.alpha_composite(T("The auction that sets each stock's", 34, (60, 66, 80), 500), (50, 240)); c.alpha_composite(T("closing price at 4 p.m.", 34, (60, 66, 80), 500), (50, 286))
        put(im, lift(c), 540, 960, ease((t - S("n1") + 0.15) / 0.25), 0.94 + 0.06 * spring((t - S("n1") + 0.15) / 0.5))
    else:
        t0 = WT("n2", "$50"); v = roll(t, t0 - 0.6, 1.1, 0, 50)
        st = stat("US closing auctions · normal day, 2024", f"${v:,.0f} billion", "about 9% of all US trading that day", 900, False, 128)
        put(im, lift(st), 540, 940, ease((t - S("n2") + 0.1) / 0.25), 0.95 + 0.05 * spring((t - S("n2") + 0.1) / 0.5))
        bar = card(900, 64, False, 32); d = ImageDraw.Draw(bar); kk = eout((t - t0) / 0.8)
        d.rounded_rectangle((6, 6, 6 + (888) * 0.09 * kk, 58), radius=26, fill=VIOLET + (255,))
        bar.alpha_composite(T("9% of the day, in one auction", 26, (110, 116, 130), 600), (110, 16)); put(im, bar, 540, 1220, ease((t - t0) / 0.3))
        footnote(im, "Source: BMLL, \"Into the Close\" (2025), on 2024 US closing auctions")
    return im

# ---------- 6. the record ----------
def sc_record(t):
    im = bg(True); put(im, chip("March 20, 2026 · NYSE", True, 30), 540, 700, ease((t - S("n3")) / 0.25))
    t0 = WT("n3", "3.57"); v = roll(t, t0 - 0.2, 1.3, 0, 3_570_000_000)
    st = stat("One closing auction", f"{v:,.0f}", "shares, matched in a single auction", 920, True, 104)
    put(im, lift(st, True), 540, 960, ease((t - S("n3") + 0.1) / 0.25))
    stamp_at(im, big_stamp("RECORD", (255, 120, 140), 96, -8), 770, 1230, t, WT("n3", "shares"))
    footnote(im, "Source: NYSE, \"Behind the Record Volumes\" (2026)", True)
    return im

# ---------- 7. the closing price on the news ----------
def sc_news(t):
    im = bg(False); ph = phone(560, 1060, False); d = ImageDraw.Draw(ph)
    ph.alpha_composite(T("Markets", 44, L_INK), (50, 110)); ph.alpha_composite(T("Today · 4:00 PM", 26, (120, 126, 140), 600), (52, 170))
    rows = [("ACME Corp", "101.20", True), ("Globex", "58.04", False), ("Initech", "212.77", False), ("Umbrella", "33.90", False)]
    for i, (nm, px, main) in enumerate(rows):
        y = 240 + i * 150; c = card(470, 128, False, 22, fill=(246, 244, 255) if main else (250, 250, 252)); c.alpha_composite(T(nm, 34, L_INK, 600), (26, 22))
        c.alpha_composite(T("close", 22, (130, 136, 150), 600, True), (28, 76)); pt = T(px, 44, L_INK, 700); c.alpha_composite(pt, (470 - pt.width - 26, 36)); ph.alpha_composite(c, (45, y))
    put(im, lift(ph), 540, 1020, ease((t - S("t1") + 0.15) / 0.25), 0.95 + 0.05 * spring((t - S("t1") + 0.15) / 0.5))
    px_box = (540 - 280 + 45 + 470 - 200, 1020 - 530 + 240 + 20, 540 - 280 + 45 + 470 - 12, 1020 - 530 + 240 + 110)
    if t >= WT("t1", "price"): select_box(im, px_box, eout((t - WT("t1", "price")) / 0.3))
    tc = WT("t2", "set")
    cx = 540 + 320 - 260 * eout((t - S("t2") + 0.6) / 0.5); cy = 1020 + 300 - 470 * eout((t - S("t2") + 0.6) / 0.5)
    if t >= S("t2") - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, px_box[0] + 90, px_box[1] + 45, (t - tc + 0.1) / 0.5)
    if t >= tc - 0.1: put(im, pill("set by an auction", 38, VIOLET), 720, 1020 - 530 + 240 - 75, ease((t - tc + 0.1) / 0.15), 0.8 + 0.2 * spring((t - tc + 0.1) / 0.4))
    footnote(im, "Company names are made up")
    return im

# ---------- 8. paintings → companies, end ----------
def frame_art(s=360):
    im = Image.new("RGBA", (s, int(s * 1.2)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, s - 1, s * 1.2 - 1), fill=(201, 168, 92, 255)); d.rectangle((24, 24, s - 25, s * 1.2 - 25), fill=(30, 36, 60, 255))
    d.ellipse((s * 0.55, s * 0.18, s * 0.78, s * 0.41), fill=(250, 220, 140, 255)); d.polygon([(24, s * 1.2 - 25), (s * 0.4, s * 0.55), (s * 0.7, s * 0.9), (s - 25, s * 0.6), (s - 25, s * 1.2 - 25)], fill=(96, 120, 210, 255))
    return im

def sc_outro(t):
    im = bg(True); tp, tc = WT("e1", "paintings"), WT("e1", "price")
    if t < S("e2") - 0.1:
        ka = ease((t - S("e1") + 0.15) / 0.25); slide = eout((t - tc + 0.1) / 0.45)
        put(im, lift(frame_art(), True), 540 - 200 * slide, 960, ka * (1 - slide), 1 - 0.3 * slide)
        if t >= tp and slide < 1: stamp_at(im, big_stamp("SOLD", LILAC, 80, -10), 540 - 200 * slide + 90, 820, t, tp)
        if t >= tc - 0.1:
            for i in range(6):
                r, c = divmod(i, 2); k = spring((t - tc - i * 0.08) / 0.4)
                if k <= 0: continue
                tile = card(300, 150, True, 24); tile.alpha_composite(head((["A", "G", "I", "U", "S", "N"][i], [VIOLET, BLUE, GREEN_APP][i % 3]), 70), (22, 40))
                tile.alpha_composite(T(["101.20", "58.04", "212.77", "33.90", "77.15", "140.60"][i], 40, D_INK, 700), (110, 52))
                put(im, lift(tile, True), 540 + (c - 0.5) * 320, 780 + r * 180, min(1, k * 1.5), 0.9 + 0.1 * k)
    else:
        k = t - S("e2") + 0.1
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

FN = {"hook": sc_hook, "book": sc_book, "clock": sc_clock, "match": sc_match, "name": sc_name, "record": sc_record, "news": sc_news, "outro": sc_outro}

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
    s.pop(WT("h1", "auction"), 0.05, 400)
    for k, w in (("b2", "Nour"), ("b2", "Sami")): s.pop(WT(k, w), 0.04, 650)
    s.ding(WT("b3", "trade"), 1568, 0.035)
    for i in range(10): s.tick(S("b1") + 0.1 + i * 0.14, 0.01, 2400)
    s.ding(WT("c1", "4") + 0.3, 784, 0.06); s.ding(WT("c1", "4") + 0.3, 1175, 0.04)
    for i in range(9): s.tick(WT("c2", "buy") - 0.3 + i * 0.07, 0.015, 1500); s.tick(WT("c2", "sell") - 0.3 + i * 0.07, 0.015, 1800)
    s.pop(WT("c3", "price"), 0.05, 700); s.ding(WT("c4", "go"), 1318, 0.03)
    for i in range(12): s.tick(WT("n2", "$50") - 0.6 + i * 0.09, 0.012, 2600)
    for i in range(14): s.tick(WT("n3", "3.57") - 0.2 + i * 0.09, 0.012, 2600)
    s.thud(WT("n3", "shares"), 0.09); s.pop(WT("t2", "set"), 0.04, 900); s.thud(WT("e1", "paintings"), 0.06)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson03_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
