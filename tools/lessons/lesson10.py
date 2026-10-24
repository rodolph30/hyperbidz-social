"""Auction short 10 (v3, quick, who: Sami): "The first number wins". Problem: Sami posts his car and the first message is a
lowball. Reframe: first offers are anchors: whoever names the first number gets the better deal, and the first offer strongly
predicts the final price (Galinsky & Mussweiler, 2001); even real-estate agents were pulled by the list price and denied it
(Northcraft & Neale, 1987). Fix: in an auction the buyers name the numbers and each one is higher.
Run: python3 tools/lessons/lesson10.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson10_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "lofi", 10
XF = 0.16
SC = [("hook", False, 0.0, S("s1") - 0.1), ("exp", True, S("s1") - 0.1, S("s2") - 0.1), ("pred", False, S("s2") - 0.1, S("s3") - 0.1),
      ("agents", True, S("s3") - 0.1, S("r1") - 0.1), ("anchor", False, S("r1") - 0.1, S("f1") - 0.1), ("fix", True, S("f1") - 0.1, S("tk") - 0.1),
      ("take", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", True, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)

# ---------- drawings ----------
def car(w=420, col=BLUE):
    """a simple side-view hatchback"""
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

def anchor_icon(s=360, col=VIOLET):
    S2 = 2; W2 = s * S2; im = Image.new("RGBA", (W2, W2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = col + (255,); lw = int(W2 * 0.07)
    d.ellipse((W2 * 0.4, W2 * 0.02, W2 * 0.6, W2 * 0.22), outline=c, width=int(lw * 0.8))                       # ring
    d.line([(W2 * 0.5, W2 * 0.2), (W2 * 0.5, W2 * 0.9)], fill=c, width=lw)                                      # shank
    d.line([(W2 * 0.28, W2 * 0.34), (W2 * 0.72, W2 * 0.34)], fill=c, width=lw)                                  # stock
    d.arc((W2 * 0.12, W2 * 0.42, W2 * 0.88, W2 * 0.94), 20, 160, fill=c, width=lw)                             # arms
    for sx in (-1, 1):
        x = W2 * 0.5 + sx * W2 * 0.37; y = W2 * 0.81
        d.polygon([(x - sx * W2 * 0.02, y - W2 * 0.13), (x + sx * W2 * 0.09, y + W2 * 0.01), (x - sx * W2 * 0.08, y + W2 * 0.02)], fill=c)
    return im.resize((s, s), Image.LANCZOS)

def arrow(s=300, up=True, col=GREEN_UI):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(s * 0.5, s * 0.04), (s * 0.94, s * 0.48), (s * 0.66, s * 0.48), (s * 0.66, s * 0.96), (s * 0.34, s * 0.96), (s * 0.34, s * 0.48), (s * 0.06, s * 0.48)]
    if not up: pts = [(x, s - y) for x, y in pts]
    d.polygon(pts, fill=col + (255,)); return im

def bubble_msg(text, size=84, fill=(236, 237, 242), col=L_INK):
    tt = T(text, size, col, 700); w, h = tt.width + 70, tt.height + 46
    im = Image.new("RGBA", (w, h + 18), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=fill + (255,)); d.polygon([(26, h - 12), (20, h + 16), (60, h - 12)], fill=fill + (255,))
    im.alpha_composite(tt, (35, 23)); return im

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); ts = WT("h1", "set"); tl = WT("h1", "lowball")
    pw, ph = 620, 1100; p = phone(pw, ph, False)
    lc = card(540, 470, False, 26, fill=(246, 247, 251)); lc.alpha_composite(car(420), (60, 40))
    lc.alpha_composite(head("sami", 64), (30, 270)); lc.alpha_composite(T("Sami · Used car", 32, L_INK, 600), (110, 284))
    pr = T("$9,000", 76, L_INK, 700); lc.alpha_composite(pr, (30, 360)); p.alpha_composite(lc, (40, 110))
    p.alpha_composite(T("NEW MESSAGE", 22, GREY_TXT, 700, True), (50, 620))
    pk = 1 + 0.1 * np.sin(np.pi * clamp((t - tl) / 0.35))
    b = bubble_msg("$4,500?", 96, (255, 228, 233), RED_UI)
    bb = b.resize((int(b.width * pk), int(b.height * pk)), Image.LANCZOS); p.alpha_composite(bb, (50, 670))
    put(im, lift(p), 540, 1150, 1, 0.97 + 0.03 * spring(t / 0.5))
    if t >= ts:
        x0 = 540 - pw / 2 + 40 + 30; y = 1150 - ph / 2 + 110 + 360 + 46
        strike(im, x0 - 8, y, x0 + pr.width + 8, eout((t - ts) / 0.3))
    if t >= ts + 0.1: put(im, pill("the new starting point", 40, VIOLET), 540, 1150 + 400, ease((t - ts - 0.1) / 0.2), 0.85 + 0.15 * spring((t - ts - 0.1) / 0.4))
    footnote(im, "Car and prices are illustrative", False, 1850)
    return im

def sc_exp(t):
    im = bg(True); t0 = S("s1"); tf = WT("s1", "first"); tb = WT("s1", "better")
    w, h = 900, 760; win = window(w, h, "Negotiation experiment", True)
    for i, (who, name, role) in enumerate((("sami", "Sami", "SELLER"), ("nour", "Nour", "BUYER"))):
        k = spring((t - t0 - 0.05 - i * 0.2) / 0.4)
        if k <= 0: continue
        first = i == 0 and t >= tf
        row = card(800, 230, True, 24, fill=(36, 30, 70) if first else None)
        row.alpha_composite(head(who, 120), (28, 55)); row.alpha_composite(T(name, 46, D_INK, 600), (175, 60))
        row.alpha_composite(T(role, 24, D_MUTE, 700, True), (177, 126))
        if first:
            pp = pill("names the first number", 30, VIOLET); kk = spring((t - tf) / 0.35)
            pp = pp.resize((max(1, int(pp.width * (0.85 + 0.15 * kk))), max(1, int(pp.height * (0.85 + 0.15 * kk)))), Image.LANCZOS)
            row.alpha_composite(pp, (330, 58))
        win.alpha_composite(row, (50, int(130 + i * 290 + (1 - k) * 30)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win, True), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    stamp_at(im, big_stamp("BETTER DEAL", GREEN_UI, 84, -8), 540, 1640, t, tb)
    footnote(im, "Galinsky & Mussweiler, 2001 · 3 experiments · names illustrative", True)
    return im

DOTS = [(0.08, 0.12), (0.15, 0.2), (0.22, 0.18), (0.3, 0.33), (0.37, 0.3), (0.45, 0.46), (0.52, 0.5), (0.6, 0.55), (0.67, 0.7), (0.75, 0.68), (0.83, 0.82), (0.9, 0.86)]
def sc_pred(t):
    im = bg(False); t0 = S("s2"); tsg = WT("s2", "strong"); tfin = WT("s2", "final")
    w, h = 880, 860; c = card(w, h, False, 30); d = ImageDraw.Draw(c)
    c.alpha_composite(T("FINAL PRICE", 26, GREY_TXT, 700, True), (60, 44))
    ox, oy, ex, ey = 90, 760, 820, 110
    d.line([(ox, oy), (ex, oy)], fill=(200, 204, 214, 255), width=4); d.line([(ox, oy), (ox, ey)], fill=(200, 204, 214, 255), width=4)
    lab = T("FIRST OFFER →", 26, GREY_TXT, 700, True); c.alpha_composite(lab, (ex - lab.width, oy + 30))
    for i, (x, y) in enumerate(DOTS):
        k = spring((t - t0 - 0.05 - i * 0.12) / 0.3)
        if k <= 0: continue
        cx, cy, r = ox + x * (ex - ox), oy - y * (oy - ey), 18 * min(1, k)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(LILAC if i % 3 else BLUE) + (255,))
    kl = eout((t - tsg) / 0.6)
    if kl > 0:
        x1 = ox + 0.04 * (ex - ox) + kl * 0.9 * (ex - ox); y1 = oy - 0.06 * (oy - ey) - kl * 0.88 * (oy - ey)
        d.line([(ox + 0.04 * (ex - ox), oy - 0.06 * (oy - ey)), (x1, y1)], fill=VIOLET + (255,), width=10)
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tfin: put(im, pill("first offer → final price", 40, VIOLET), 540, 1640, ease((t - tfin) / 0.2), 0.85 + 0.15 * spring((t - tfin) / 0.4))
    footnote(im, "Dots illustrative · Galinsky & Mussweiler, 2001", False, 1850)
    return im

def house(s=260, col=BLUE):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s * 0.5, s * 0.06), (s * 0.95, s * 0.45), (s * 0.05, s * 0.45)], fill=col + (255,))
    d.rectangle((s * 0.15, s * 0.43, s * 0.85, s * 0.95), fill=col + (255,))
    d.rectangle((s * 0.42, s * 0.62, s * 0.58, s * 0.95), fill=(200, 220, 255, 255))
    for x in (0.22, 0.64): d.rectangle((s * x, s * 0.55, s * (x + 0.14), s * 0.69), fill=(200, 220, 255, 255))
    return im

def sc_agents(t):
    im = bg(True); t0 = S("s3"); tlp = WT("s3", "list"); tp = WT("s3", "pulled"); td = WT("s3", "denied")
    k0 = spring((t - t0 + 0.1) / 0.45); put(im, house(250), 540, 720 + (1 - k0) * 40, min(1, k0 * 1.5))
    w = 900; c = card(w, 430, True, 30); d = ImageDraw.Draw(c)
    bx0, bx1, by = 80, 820, 250
    d.rounded_rectangle((bx0, by - 8, bx1, by + 8), radius=8, fill=(60, 66, 86, 255))
    # the list price marker moves right on "pulled"; the agents' estimate follows it on "list"
    lp = 0.3 + 0.45 * eout((t - tp + 0.1) / 0.5); est = 0.3 + 0.38 * eout((t - tlp) / 0.7)
    lx = bx0 + lp * (bx1 - bx0); exn = bx0 + est * (bx1 - bx0)
    d.polygon([(lx, by - 20), (lx - 22, by - 56), (lx + 22, by - 56)], fill=VIOLET + (255,))
    ll = T("LIST PRICE", 26, LILAC, 700, True); c.alpha_composite(ll, (int(clamp(lx - ll.width / 2, 20, w - ll.width - 20)), by - 110))
    d.ellipse((exn - 22, by - 22, exn + 22, by + 22), fill=BLUE + (255,))
    el = T("AGENTS' ESTIMATE", 26, (150, 190, 255), 700, True); c.alpha_composite(el, (int(clamp(exn - el.width / 2, 20, w - el.width - 20)), by + 50))
    put(im, lift(c, True), 540, 1200 + (1 - k0) * 60, min(1, k0 * 1.5))
    if t >= td - 0.05:
        put(im, bubble_msg("“It didn’t affect me.”", 46, (40, 46, 60), D_INK), 540, 1560, ease((t - td + 0.05) / 0.2), 0.85 + 0.15 * spring((t - td + 0.05) / 0.4))
    stamp_at(im, big_stamp("IT DID", RED_UI, 90, -8), 540, 1700, t, td + 0.45)
    footnote(im, "Northcraft & Neale, 1987 · positions illustrative", True)
    return im

def sc_anchor(t):
    im = bg(False); t0 = S("r1"); tr = WT("r1", "rude"); ta = WT("r1", "anchor")
    up = eout((t - ta + 0.1) / 0.4)
    b = bubble_msg("$4,500?", 110, (255, 228, 233), RED_UI)
    put(im, lift(b), 540, 1000 - 340 * up, ease((t - t0 + 0.12) / 0.25), 1 - 0.25 * up)
    if t >= tr and t < ta - 0.1:
        rp = pill("rude?", 64, (60, 66, 86)); put(im, rp, 540, 1300, ease((t - tr) / 0.2))
        strike(im, 540 - rp.width / 2 + 10, 1302, 540 + rp.width / 2 - 10, eout((t - tr - 0.3) / 0.25), RED_UI, 10)
    if t >= ta - 0.1:
        kk = spring((t - ta + 0.1) / 0.45); ay = 1230 + (1 - kk) * -160
        ImageDraw.Draw(im).line([(540, 1000 - 340 + 70), (540, ay - 170)], fill=(150, 155, 166, 255), width=8)
        put(im, anchor_icon(380), 540, ay, min(1, kk * 1.5))
        put(im, pill("ANCHOR", 44, VIOLET), 540, 1560, ease((t - ta - 0.1) / 0.2), 0.85 + 0.15 * spring((t - ta - 0.1) / 0.4))
    footnote(im, "A first offer anchors the whole negotiation", False, 1850)
    return im

BIDS = ((("B", VIOLET), "Bidder 3", 4500), ("nour", "Nour", 5600), (("C", GREEN_APP), "Bidder 4", 6900), (("B", VIOLET), "Bidder 3", 8100), ("nour", "Nour", 9400))
def sc_fix(t):
    im = bg(True); t0 = S("f1"); tby = WT("f1", "buyers"); th = WT("f1", "higher")
    times = [tby - 0.1 + i * (th - tby) / 4.2 for i in range(5)]
    n = sum(1 for x in times if t >= x)
    w, h = 900, 1020; c = window(w, h, "Live auction · the same car", True)
    c.alpha_composite(car(230), (50, 100)); c.alpha_composite(head("sami", 70), (310, 130)); c.alpha_composite(T("Seller: Sami", 32, D_MUTE, 600), (395, 146))
    c.alpha_composite(T("CURRENT BID", 24, D_MUTE, 700, True), (50, 250))
    if n:
        prev = BIDS[n - 2][2] if n > 1 else 0; v = roll(t, times[n - 1], 0.3, prev, BIDS[n - 1][2])
        c.alpha_composite(T(money(v), 130, GREEN_UI if n > 1 else D_INK, 700), (50, 290))
    for j in range(min(n, 3)):
        i = n - 1 - j; who, name, amt = BIDS[i]; kk = spring((t - times[i]) / 0.35) if j == 0 else 1
        row = card(800, 130, True, 22, fill=(30, 40, 60) if j == 0 else None)
        row.alpha_composite(head(who, 84), (24, 23)); row.alpha_composite(T(name, 38, D_INK, 600), (130, 42))
        a_ = T(money(amt), 48, D_INK if j else GREEN_UI, 700); row.alpha_composite(a_, (770 - a_.width, 36))
        row.putalpha(row.getchannel("A").point(lambda p: int(p * (1 - 0.35 * j) * min(1, kk * 1.5))))
        c.alpha_composite(row, (50, int(500 + j * 150 + (1 - kk) * -30)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1140, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= th: put(im, pill("↑  every bid is higher", 42, GREEN_UI), 540, 1730, ease((t - th) / 0.2), 0.85 + 0.15 * spring((t - th) / 0.4))
    footnote(im, "Example numbers · names illustrative", True, 1850)
    return im

def sc_take(t):
    im = bg(False); t0 = S("tk"); tsw = WT("tk", "auction") - 0.2; tdn = WT("tk", "down."); tup = WT("tk", "up.")
    chat = t < tsw
    ts_ = t0 if chat else tsw; k = spring((t - ts_ + 0.1) / 0.45)
    c = card(860, 900, False, 30)
    lab = T("IN A CHAT" if chat else "IN AN AUCTION", 30, GREY_TXT, 700, True); c.alpha_composite(lab, (int(430 - lab.width / 2), 50))
    a, b = ("$9,000", "$4,500") if chat else ("$4,500", "$9,400")
    tr = T(f"{a}  →  {b}", 76, L_INK, 700); c.alpha_composite(tr, (int(430 - tr.width / 2), 120))
    tk_ = WT("tk", "pulls") if chat else WT("tk", "pushes"); ka = spring((t - tk_) / 0.45)
    if ka > 0:
        ar = arrow(420, not chat, RED_UI if chat else GREEN_UI); ar = ar.resize((max(1, int(420 * min(1, ka))),) * 2, Image.LANCZOS)
        c.alpha_composite(ar, (int(430 - ar.width / 2), int(470 - ar.height / 2 + 50 + (1 - ka) * (-60 if chat else 60))))
    put(im, lift(c), 540, 1130 + (1 - k) * 60, min(1, k * 1.5))
    footnote(im, "Example numbers", False, 1850)
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

FN = {"hook": sc_hook, "exp": sc_exp, "pred": sc_pred, "agents": sc_agents, "anchor": sc_anchor, "fix": sc_fix, "take": sc_take, "outro": sc_outro}

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
    s.pop(WT("h1", "lowball"), 0.04, 650); ts = WT("h1", "set"); s.tick(ts, 0.02, 1800); s.pop(ts + 0.1, 0.04, 560)
    for i in range(2): s.pop(S("s1") + 0.05 + i * 0.2, 0.03, 520 + i * 60)
    s.ding(WT("s1", "first"), 1318, 0.03); s.thud(WT("s1", "better"), 0.07)
    for i in range(len(DOTS)): s.tick(S("s2") + 0.05 + i * 0.12, 0.01, 2000 + i * 40)
    s.ding(WT("s2", "strong"), 1568, 0.03); s.pop(WT("s2", "final"), 0.04, 650)
    s.pop(WT("s3", "list"), 0.04, 600); s.tick(WT("s3", "pulled"), 0.02, 1800)
    s.pop(WT("s3", "denied"), 0.04, 700); s.thud(WT("s3", "denied") + 0.45, 0.08)
    s.pop(WT("r1", "rude"), 0.04, 620); s.thud(WT("r1", "anchor"), 0.09)
    tby, th = WT("f1", "buyers"), WT("f1", "higher")
    for i in range(5): s.pop(tby - 0.1 + i * (th - tby) / 4.2, 0.035, 560 + i * 70)
    s.ding(th, 1568, 0.03)
    s.thud(WT("tk", "down."), 0.07); s.whoosh(WT("tk", "auction") - 0.3, 0.3, 0.04); s.ding(WT("tk", "up."), 1318, 0.035)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson10_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
