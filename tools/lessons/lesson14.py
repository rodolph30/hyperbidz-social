"""Auction short 14 (v3, standard, who: perspective): "Australia sells its homes on Saturdays". Here, "auction" sounds like
trouble (a court sale, a seized apartment). There, it's a normal way to sell a home: 1,882 homes went to auction in Australia's
capital cities last week, a quiet week (3,236 a year ago) (Cotality, 26 Oct 2026); most are on a Saturday (SQM Research,
week ending 1 Nov 2026: Sydney + Melbourne 1,150 on Saturday vs 444 the rest of the week); some in front of the house (NSW
Government); a public sale with rules and a reserve (Consumer Affairs Victoria); and not every home sells: 48.4% last week.
Takeaway: here, auction sounds like trouble; there, it sounds like Saturday.
Run: python3 tools/lessons/lesson14.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson14_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "pluck", 14
XF = 0.16
SC = [("hook", False, 0.0, S("h2") - 0.1), ("quiet", True, S("h2") - 0.1, S("p1") - 0.1), ("here", False, S("p1") - 0.1, S("s1") - 0.1),
      ("there", True, S("s1") - 0.1, S("s2") - 0.1), ("sat", False, S("s2") - 0.1, S("s3") - 0.1), ("front", True, S("s3") - 0.1, S("f2") - 0.1),
      ("reserve", False, S("f2") - 0.1, S("n1") - 0.1), ("half", True, S("n1") - 0.1, S("tk") - 0.1), ("take", False, S("tk") - 0.1, S("e2") - 0.15),
      ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)

# ---------- drawings ----------
def fade_l(layer, k):
    layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def house(w=300, body=BLUE, roof=(24, 28, 44), win=(255, 255, 255)):
    """a simple generic house: body, roof, door, two windows"""
    S2 = 2; h = int(w * 0.92); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    d.polygon([(W2 * 0.02, H2 * 0.44), (W2 * 0.5, H2 * 0.02), (W2 * 0.98, H2 * 0.44)], fill=roof + (255,))
    d.rectangle((W2 * 0.72, H2 * 0.08, W2 * 0.82, H2 * 0.3), fill=roof + (255,))
    d.rounded_rectangle((W2 * 0.1, H2 * 0.4, W2 * 0.9, H2 * 0.99), radius=10, fill=body + (255,))
    d.rounded_rectangle((W2 * 0.42, H2 * 0.62, W2 * 0.58, H2 * 0.99), radius=10, fill=roof + (255,))
    for x0 in (0.17, 0.66):
        d.rounded_rectangle((W2 * x0, H2 * 0.54, W2 * (x0 + 0.17), H2 * 0.74), radius=8, fill=win + (235,))
    return im.resize((w, h), Image.LANCZOS)

def house_grid(t, t_on, cols=12, rows=8, cell=60, gap=12, dark=False):
    """small houses popping in, row by row (one icon stands for about 17 homes; marked as illustrative)"""
    w = cols * (cell + gap) - gap; h = rows * (cell + gap) - gap; im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cols_ = (BLUE, VIOLET, LILAC, GREEN_APP)
    for i in range(cols * rows):
        k = spring((t - t_on - i * 0.008) / 0.3)
        if k <= 0: continue
        hs = house(int(cell * (0.55 + 0.45 * min(1, k))), cols_[(i * 7) % 4], (34, 40, 58) if not dark else (200, 204, 214))
        x, y = (i % cols) * (cell + gap), (i // cols) * (cell + gap)
        im.alpha_composite(fade_l(hs, k), (int(x + cell / 2 - hs.width / 2), int(y + cell - hs.height)))
    return im

def sign(text="AUCTION", w=260):
    """a generic agent's board on a post"""
    h = int(w * 0.95); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((w * 0.47, h * 0.3, w * 0.53, h), fill=(120, 126, 140, 255))
    d.rounded_rectangle((0, 0, w - 1, h * 0.5), radius=16, fill=VIOLET + (255,))
    tt = T(text, int(w * 0.17), (255, 255, 255), 700); im.alpha_composite(tt, (int(w / 2 - tt.width / 2), int(h * 0.25 - tt.height / 2)))
    return im

def bubble(text, size=40, fill=(236, 237, 242), col=L_INK, right=False):
    tt = T(text, size, col, 600); w, h = tt.width + 56, tt.height + 36
    im = Image.new("RGBA", (w, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=fill + (255,))
    if right: d.polygon([(w - 26, h - 10), (w - 18, h + 12), (w - 58, h - 10)], fill=fill + (255,))
    else: d.polygon([(26, h - 10), (18, h + 12), (58, h - 10)], fill=fill + (255,))
    im.alpha_composite(tt, (28, 18)); return im

def bar_row(label, value, frac, col, w=760, dark=False, vtxt=None):
    """a labelled horizontal bar: label left, big number right, bar below"""
    row = Image.new("RGBA", (w, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
    row.alpha_composite(T(label, 38, D_MUTE if dark else GREY_TXT, 600), (0, 4))
    v = T(vtxt if vtxt is not None else f"{value:,.0f}", 64, col, 700); row.alpha_composite(v, (w - v.width, 0))
    d.rounded_rectangle((0, 110, w, 160), radius=25, fill=((40, 46, 60) if dark else (232, 233, 240)) + (255,))
    if frac > 0.01: d.rounded_rectangle((0, 110, max(50, w * frac), 160), radius=25, fill=col + (255,))
    return row

def donut(frac, s=420, col=GREEN_UI, base=(40, 46, 60), wd=46):
    S2 = 2; im = Image.new("RGBA", (s * S2, s * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); m = wd * S2
    d.ellipse((m / 2, m / 2, s * S2 - m / 2, s * S2 - m / 2), outline=base + (255,), width=m)
    if frac > 0.002: d.arc((m / 2, m / 2, s * S2 - m / 2, s * S2 - m / 2), -90, -90 + 360 * frac, fill=col + (255,), width=m)
    return im.resize((s, s), Image.LANCZOS)

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); tw = WT("h1", "auction")
    w, h = 960, 1040; win = window(w, h, "Homes taken to auction · one week", False)
    v = roll(t, -0.7, 1.4, 0, 1882); tv = T(f"{v:,.0f}", 190, L_INK, 700); win.alpha_composite(tv, (int(w / 2 - tv.width / 2), 100))
    g = house_grid(t, -0.9); win.alpha_composite(g, (int(w / 2 - g.width / 2), 330))
    if t >= tw - 0.3:
        ch = fade_l(pill("Australia's capital cities", 34, BLUE, padx=26, pady=10), spring((t - tw + 0.3) / 0.4)); win.alpha_composite(ch, (int(w / 2 - ch.width / 2), 935))
    put(im, lift(win), 540, 1130, 1, 0.97 + 0.03 * spring(t / 0.5))
    footnote(im, "Week ending 25 Oct 2026 · Cotality (preliminary) · icons illustrative", False, 1850)
    return im

def sc_quiet(t):
    im = bg(True); t0 = S("h2"); tq = WT("h2", "quiet"); ty = WT("h2", "year")
    k = spring((t - t0 + 0.1) / 0.45); c = card(900, 700, True, 30)
    lab = T("HOMES TAKEN TO AUCTION IN ONE WEEK", 28, D_MUTE, 700, True); c.alpha_composite(lab, (int(450 - lab.width / 2), 50))
    r1 = bar_row("Last week", 1882, 1882 / 3236 * eout((t - t0 + 0.1) / 0.6), LILAC, 780, True); c.alpha_composite(r1, (60, 140))
    if t >= ty - 0.15:
        kk = eout((t - ty + 0.15) / 0.9); r2 = bar_row("Same week, 2025", 3236, kk, (150, 155, 166), 780, True, f"{roll(t, ty - 0.15, 0.9, 0, 3236):,.0f}")
        c.alpha_composite(fade_l(r2, spring((t - ty + 0.15) / 0.35)), (60, 380))
    put(im, lift(c, True), 540, 1080 + (1 - k) * 40, min(1, k * 1.5), 0.94 + 0.06 * k)
    if t >= tq - 0.1: put(im, pill("a quiet week", 40, VIOLET, padx=30, pady=12), 540, 1520, ease((t - tq + 0.1) / 0.2), 0.8 + 0.2 * spring((t - tq + 0.1) / 0.4))
    footnote(im, "Combined capital cities · Cotality, 26 Oct 2026", True, 1850)
    return im

def sc_here(t):
    im = bg(False); t0 = S("p1"); t2 = S("p2"); tc = WT("p2", "court"); ts = WT("p2", "seized")
    if t < t2 - 0.1:
        for i, (ti, who, txt, right) in enumerate(((t0 - 0.05, "sami", "There's an auction on our street.", False),
                                                   (WT("p1", "trouble.") - 0.25, "nour", "Oh no. What happened?", True))):
            k = spring((t - ti) / 0.35)
            if k <= 0: continue
            row = Image.new("RGBA", (960, 160), (0, 0, 0, 0)); b = bubble(txt, 44, BLUE if right else (255, 255, 255), (255, 255, 255) if right else L_INK, right)
            if right: row.alpha_composite(b, (960 - 120 - b.width, 14)); row.alpha_composite(head(who, 100), (860, 40))
            else: row.alpha_composite(head(who, 100), (0, 40)); row.alpha_composite(b, (120, 14))
            put(im, row, 540, 880 + i * 260 + (1 - k) * 30, min(1, k * 1.5))
        footnote(im, "Illustrative", False, 1850)
    else:
        k = spring((t - t2 + 0.1) / 0.45); c = card(860, 640, False, 30)
        lab = T("WHAT \"AUCTION\" BRINGS TO MIND HERE", 28, GREY_TXT, 700, True); c.alpha_composite(lab, (int(430 - lab.width / 2), 50))
        for j, (tj, txt) in enumerate(((tc - 0.15, "A court sale"), (ts - 0.3, "A seized apartment"))):
            kj = spring((t - tj) / 0.35)
            if kj > 0:
                r = fade_l(T(txt, 72, L_INK, 700), kj); c.alpha_composite(r, (int(430 - r.width / 2), int(170 + j * 200 + (1 - kj) * 20)))
        put(im, lift(c), 540, 1080 + (1 - k) * 40, min(1, k * 1.5), 0.94 + 0.06 * k)
        put(im, head("nour", 110), 540 + 340, 650 + (1 - k) * 40, min(1, k * 1.5))
    return im

def sc_there(t):
    im = bg(True); t0 = S("s1"); th = WT("s1", "home.")
    k = spring((t - t0 + 0.1) / 0.45)
    put(im, house(520, BLUE, (200, 204, 214)), 470, 1080 + (1 - k) * 60, min(1, k * 1.5), 0.9 + 0.1 * k)
    ks = spring((t - th + 0.3) / 0.4)
    if ks > 0: put(im, sign("AUCTION", 280), 860, 1180 + (1 - ks) * 80, min(1, ks * 1.5))
    put(im, chip("Australia", True, 30), 540, 1500, ease((t - t0) / 0.3))
    footnote(im, "Illustrative", True, 1850)
    return im

def sc_sat(t):
    im = bg(False); t0 = S("s2"); tday = WT("s2", "day:"); tsat = WT("s2", "Saturday.")
    w, h = 900, 760; win = window(w, h, "Auctions this week · Sydney + Melbourne", False)
    k1 = eout((t - t0) / 0.8); r2 = bar_row("Rest of the week", 444, 444 / 1150 * k1, (150, 155, 166), 780); win.alpha_composite(r2, (60, 420))
    if t >= tday - 0.2:
        kk = eout((t - tday + 0.2) / 0.9); col = VIOLET if t >= tsat - 0.1 else BLUE
        r1 = bar_row("Saturday", 1150, kk, col, 780, False, f"{roll(t, tday - 0.2, 0.9, 0, 1150):,.0f}"); win.alpha_composite(r1, (60, 150))
        if t >= tsat - 0.1: select_box(win, (50, 136, 850, 316), eout((t - tsat + 0.1) / 0.3))
    put(im, lift(win), 540, 1110, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Scheduled auctions, week ending 1 Nov 2026 · SQM Research", False, 1850)
    return im

BIDS = (("register", None), ("loud.", "$1.10M"), ("hears", "$1.12M"), ("number.", "$1.15M"))
def sc_front(t):
    im = bg(True); t0 = S("s3"); tr = WT("f1", "register.")
    k = spring((t - t0 + 0.1) / 0.45)
    put(im, house(440, BLUE, (200, 204, 214)), 540, 830 + (1 - k) * 50, min(1, k * 1.5))
    for i, x in enumerate((260, 540, 820)):
        kb = spring((t - t0 - 0.25 - i * 0.12) / 0.4)
        if kb <= 0: continue
        rk = clamp((t - tr + 0.2 - i * 0.12) / 0.35); b = bidder_with_paddle(i, [7, 12, 31][i], 170, rk)
        put(im, b, x, 1330 + (1 - kb) * 60, min(1, kb * 1.5))
    shown_ = [(WT("f1", w_) - 0.1, b) for w_, b in BIDS[1:]]
    vis = [(ti, b) for ti, b in shown_ if t >= ti]
    if vis:
        ti, b = vis[-1]; i = len(vis) - 1; kk = spring((t - ti) / 0.3)
        bb = bubble(b, 64, (255, 255, 255), L_INK, i % 2 == 1); put(im, bb, [330, 750, 540][i], 1100 - (1 - kk) * 20, min(1, kk * 1.5), 0.85 + 0.15 * kk)
    footnote(im, "Illustrative · bids in Australian dollars", True, 1850)
    return im

def sc_reserve(t):
    im = bg(False); t0 = S("f2"); trv = WT("f2", "reserve,"); tw = WT("f2", "wins.")
    k = spring((t - t0 + 0.1) / 0.45); w, h = 900, 760; c = card(w, h, False, 30)
    lab = T("BIDDING", 28, GREY_TXT, 700, True); c.alpha_composite(lab, (int(w / 2 - lab.width / 2), 50))
    frac = 0.35 + 0.5 * eout((t - t0) / max(0.6, tw - t0 - 0.2)); d = ImageDraw.Draw(c)
    x0, x1, y0, y1 = 70, w - 70, 330, 400
    d.rounded_rectangle((x0, y0, x1, y1), radius=35, fill=(232, 233, 240, 255))
    met = frac >= 0.68
    d.rounded_rectangle((x0, y0, x0 + (x1 - x0) * frac, y1), radius=35, fill=(GREEN_UI if met else BLUE) + (255,))
    rx = x0 + (x1 - x0) * 0.68; d.line([(rx, y0 - 50), (rx, y1 + 30)], fill=L_INK + (255,), width=6)
    if t >= trv - 0.4:
        rl = fade_l(T("Seller's reserve", 34, L_INK, 600), spring((t - trv + 0.4) / 0.35)); c.alpha_composite(rl, (int(rx - rl.width / 2), 220))
    if met:
        mp = pill("Reserve met", 34, GREEN_UI, padx=24, pady=10); c.alpha_composite(mp, (int(w / 2 - mp.width / 2), 470))
    put(im, lift(c), 540, 1110 + (1 - k) * 40, min(1, k * 1.5), 0.94 + 0.06 * k)
    stamp_at(im, big_stamp("SOLD", GREEN_UI, 120, -8), 540, 1340, t, tw - 0.1)
    footnote(im, "Illustrative · below the reserve, the home isn't sold at auction", False, 1850)
    return im

def sc_half(t):
    im = bg(True); t0 = S("n1"); th = WT("n1", "half")
    k = spring((t - t0 + 0.1) / 0.45); c = card(860, 900, True, 30)
    lab = T("SOLD AT AUCTION LAST WEEK", 28, D_MUTE, 700, True); c.alpha_composite(lab, (int(430 - lab.width / 2), 50))
    f = roll(t, t0 + 0.2, max(0.6, th - t0 - 0.1), 0, 0.484); dn = donut(f, 520); c.alpha_composite(dn, (int(430 - 260), 150))
    v = T(f"{f * 100:.1f}%", 110, LILAC if t >= th - 0.1 else D_INK, 700); c.alpha_composite(v, (int(430 - v.width / 2), int(410 - v.height / 2)))
    sub = T("of capital-city homes taken to auction", 32, D_MUTE, 600); c.alpha_composite(sub, (int(430 - sub.width / 2), 770))
    put(im, lift(c, True), 540, 1110 + (1 - k) * 40, min(1, k * 1.5), 0.94 + 0.06 * k)
    footnote(im, "Preliminary clearance rate, week ending 25 Oct 2026 · Cotality", True, 1850)
    return im

def sc_take(t):
    im = bg(False); t0 = S("tk"); tt_ = WT("tk", "trouble."); tth = WT("tk", "There,"); ts = WT("tk", "Saturday.")
    k1 = spring((t - t0 + 0.1) / 0.4)
    r1 = card(860, 230, False, 28); r1.alpha_composite(T("HERE · \"AUCTION\" SOUNDS LIKE", 28, GREY_TXT, 700, True), (60, 36))
    r1.alpha_composite(T("trouble", 84, (150, 155, 166), 700), (60, 96))
    put(im, lift(r1), 540, 830 + (1 - k1) * 30, min(1, k1 * 1.5))
    k2 = spring((t - tth + 0.15) / 0.4)
    if k2 > 0:
        r2 = card(860, 230, False, 28); r2.alpha_composite(T("THERE · IT SOUNDS LIKE", 28, GREY_TXT, 700, True), (60, 36))
        if t >= ts - 0.15:
            sv = fade_l(T("Saturday", 84, VIOLET, 700), spring((t - ts + 0.15) / 0.35)); r2.alpha_composite(sv, (60, 96))
        put(im, lift(r2), 540, 1140 + (1 - k2) * 40, min(1, k2 * 1.5), 0.94 + 0.06 * k2)
    if t >= ts - 0.1: put(im, house(150, VIOLET), 860, 1150, ease((t - ts + 0.1) / 0.25), 0.8 + 0.2 * spring((t - ts + 0.1) / 0.4))
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 7, BLUE), (540, 12, VIOLET), (750, 31, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "quiet": sc_quiet, "here": sc_here, "there": sc_there, "sat": sc_sat, "front": sc_front, "reserve": sc_reserve,
      "half": sc_half, "take": sc_take, "outro": sc_outro}

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
    for i in range(10): s.tick(0.05 + i * 0.1, 0.015)
    s.pop(WT("h1", "auction") - 0.3, 0.035, 600); s.ding(WT("h1", "cities.") , 1318, 0.025)
    s.pop(WT("h2", "quiet") - 0.1, 0.035, 620)
    for i in range(7): s.tick(WT("h2", "year") - 0.15 + i * 0.12, 0.02)
    s.pop(S("p1") - 0.05, 0.035, 640); s.pop(WT("p1", "trouble.") - 0.25, 0.035, 700)
    s.thud(WT("p2", "court") - 0.15, 0.05); s.thud(WT("p2", "seized") - 0.3, 0.05)
    s.pop(WT("s1", "home.") - 0.3, 0.04, 600)
    for i in range(7): s.tick(WT("s2", "day:") - 0.2 + i * 0.12, 0.02)
    s.ding(WT("s2", "Saturday."), 1568, 0.035)
    for w_, _ in BIDS[1:]: s.pop(WT("f1", w_) - 0.1, 0.04, 660)
    s.pop(WT("f2", "reserve,") - 0.4, 0.03, 560); s.thud(WT("f2", "wins.") - 0.1, 0.08); s.ding(WT("f2", "wins."), 1568, 0.03)
    for i in range(8): s.tick(S("n1") + 0.2 + i * 0.15, 0.015)
    s.ding(WT("n1", "half"), 1318, 0.025)
    s.pop(WT("tk", "There,") - 0.15, 0.035, 620); s.ding(WT("tk", "Saturday."), 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson14_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
