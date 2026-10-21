"""Auction short 07 (v3, quick): "The winner's curse". Bazerman & Samuelson (1983): MBA students at Boston University bid in
48 sealed-bid auctions on jars worth $8; average guess $5.13, average winning bid $10.01, average loss $2.01. The name comes from
Atlantic Richfield engineers Capen, Clapp & Campbell (1971): "how should he feel if he won against 50 others?" "Ill."
Run: python3 tools/lessons/lesson07.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson07_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "marimba", 7
XF = 0.16
SC = [("hook", True, 0.0, S("s1") - 0.1), ("klass", False, S("s1") - 0.1, S("s2") - 0.1), ("guess", True, S("s2") - 0.1, S("s3") - 0.1),
      ("winner", False, S("s3") - 0.1, S("n1") - 0.1), ("curse", True, S("n1") - 0.1, S("q1") - 0.1), ("quote", False, S("q1") - 0.1, S("tk") - 0.1),
      ("fix", True, S("tk") - 0.1, S("e2") - 0.15), ("outro", True, S("e2") - 0.15, TOTAL)]
T_PAID = WT("h2", "$10.01.")
GREY_TXT = (110, 116, 130)

# ---------- drawings ----------
_JAR = {}
def jar(w=520):
    """a glass jar full of silver coins, with a lid"""
    if w in _JAR: return _JAR[w].copy()
    S2 = 2; h = int(w * 1.25); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    bx0, by0, bx1, by1 = W2 * 0.06, H2 * 0.16, W2 * 0.94, H2 * 0.98
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=int(W2 * 0.16), fill=(200, 218, 255, 70), outline=(190, 205, 240, 255), width=int(6 * S2))
    rng = np.random.default_rng(7); cr = W2 * 0.07
    rows = int((by1 - by0 - H2 * 0.16) / (cr * 1.2))
    for r in range(rows):                                                   # coins stacked from the bottom, slightly jumbled
        yy = by1 - cr * 1.4 - r * cr * 1.15
        n = int((bx1 - bx0 - cr * 1.6) / (cr * 1.9))
        for i in range(n):
            xx = bx0 + cr * 1.6 + i * cr * 1.9 + (r % 2) * cr * 0.9 + rng.uniform(-6, 6) * S2
            if xx > bx1 - cr * 1.2: continue
            sh = rng.uniform(0.55, 0.8); tone = int(rng.uniform(175, 225))
            d.ellipse((xx - cr, yy - cr * sh, xx + cr, yy + cr * sh), fill=(tone, tone + 4, tone + 14, 255), outline=(120, 128, 146, 255), width=int(3 * S2))
            d.ellipse((xx - cr * 0.55, yy - cr * sh * 0.55, xx + cr * 0.55, yy + cr * sh * 0.55), outline=(150, 158, 176, 255), width=int(2 * S2))
    d.rounded_rectangle((bx0 + W2 * 0.06, by0 + H2 * 0.04, bx0 + W2 * 0.12, by1 - H2 * 0.18), radius=int(W2 * 0.03), fill=(255, 255, 255, 90))   # glass shine
    d.rounded_rectangle((W2 * 0.12, H2 * 0.04, W2 * 0.88, H2 * 0.17), radius=int(W2 * 0.04), fill=BLUE + (255,))                                   # lid
    for i in range(5): d.line([(W2 * (0.18 + i * 0.16), H2 * 0.06), (W2 * (0.18 + i * 0.16), H2 * 0.15)], fill=(90, 150, 255, 255), width=int(4 * S2))
    im = im.resize((w, h), Image.LANCZOS); _JAR[w] = im; return im.copy()

def envelope(w=150, sealed=False):
    h = int(w * 0.66); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=10, fill=(255, 255, 255, 255), outline=(200, 204, 214, 255), width=3)
    d.line([(4, 6), (w / 2, h * 0.58), (w - 4, 6)], fill=(200, 204, 214, 255), width=3)
    if sealed: d.ellipse((w / 2 - 18, h * 0.58 - 18, w / 2 + 18, h * 0.58 + 18), fill=VIOLET + (255,))
    return im

def oil_rig(w=620, col=BLUE):
    """an offshore drilling platform on the sea, drawn in lines"""
    h = int(w * 1.0); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = col + (255,); lw = max(4, w // 90)
    deck = h * 0.62
    d.polygon([(w * 0.42, h * 0.06), (w * 0.47, h * 0.06), (w * 0.58, deck), (w * 0.31, deck)], outline=c, width=lw)          # derrick
    for i in range(1, 6):
        y = h * 0.06 + (deck - h * 0.06) * i / 6; xl = w * 0.42 - (w * 0.11) * i / 6; xr = w * 0.47 + (w * 0.11) * i / 6
        d.line([(xl, y), (xr, y)], fill=c, width=lw - 1)
        if i < 6: d.line([(xl, y), (w * 0.47 + (w * 0.11) * (i + 1) / 6, h * 0.06 + (deck - h * 0.06) * (i + 1) / 6)], fill=c, width=max(2, lw - 2))
    d.rectangle((w * 0.14, deck, w * 0.86, deck + h * 0.06), fill=c)                                                          # deck
    d.rectangle((w * 0.62, deck - h * 0.12, w * 0.80, deck), outline=c, width=lw)                                             # cabin
    for x in (0.2, 0.4, 0.6, 0.8): d.line([(w * x, deck + h * 0.06), (w * x, h * 0.94)], fill=c, width=lw + 2)              # legs
    d.line([(w * 0.2, h * 0.78), (w * 0.8, h * 0.78)], fill=c, width=lw - 1)
    for k in range(3):                                                                                                        # waves
        y = h * (0.86 + k * 0.05); pts = [(x, y + 8 * np.sin(x / w * 18 + k)) for x in np.linspace(0, w, 60)]
        d.line(pts, fill=(VIOLET if k == 1 else LILAC) + (255,), width=lw - 1)
    return im

def tag(label, value, w, dark, vcol=None, size=110):
    c = card(w, 250, dark, 30); lab = T(label, 26, D_MUTE if dark else GREY_TXT, 700, True); v = T(value, size, vcol or (D_INK if dark else L_INK), 700)
    c.alpha_composite(lab, (int(w / 2 - lab.width / 2), 40)); c.alpha_composite(v, (int(w / 2 - v.width / 2), 92)); return c

# ---------- scenes ----------
def sc_hook(t):
    im = bg(True); bob = 8 * np.sin(t * 2.2)
    put(im, lift(jar(500), True), 540, 900 + bob, 1, 0.97 + 0.03 * spring(t / 0.5))
    tw = WT("h1", "$8.")
    pk1 = 1 + 0.08 * np.sin(np.pi * clamp((t - tw) / 0.35)); pk2 = 1 + 0.1 * np.sin(np.pi * clamp((t - T_PAID) / 0.35))
    a = lift(tag("WORTH", "$8", 400, True), True); b = lift(tag("WINNERS PAID", "$10.01", 440, True, RED_UI), True)
    put(im, a, 315, 1450, 1, pk1); put(im, b, 775, 1450, 1, pk2)                   # both tags from frame 1: the cover shows the paradox
    if t >= T_PAID: select_box(im, (775 - b.width / 2 + 24, 1450 - b.height / 2 + 14, 775 + b.width / 2 - 24, 1450 + b.height / 2 - 14), eout((t - T_PAID) / 0.3), 1 - clamp((t - T_PAID - 1.0) / 0.3))
    return im

ROWS = (("nour", "Nour"), ("sami", "Sami"), (("B", VIOLET), "Bidder 3"), (("C", GREEN_APP), "Bidder 4"))
def sc_klass(t):
    im = bg(False); t0 = S("s1")
    w, h = 900, 1060; win = window(w, h, "Microeconomics class · Boston", False)
    win.alpha_composite(chip("an experiment · 48 auctions", False, 26), (50, 104))
    jr = jar(220); win.alpha_composite(jr, (w - jr.width - 50, 96))
    tb = WT("s1", "bid"); ts = WT("s1", "secret")
    for i, (who, name) in enumerate(ROWS):
        ti = tb - 0.1 + i * 0.22; k = spring((t - ti) / 0.4)
        if k <= 0: continue
        y = int(400 + i * 160 + (1 - k) * 30); row = card(800, 136, False, 24)
        row.alpha_composite(head(who, 96), (22, 20)); row.alpha_composite(T(name, 40, L_INK, 600), (140, 44))
        row.alpha_composite(envelope(130, t >= ts + i * 0.08), (640, 24)); win.alpha_composite(row, (50, y))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1130, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= ts: put(im, pill("sealed bids", 40, VIOLET), 540, 1740, ease((t - ts) / 0.2), 0.85 + 0.15 * spring((t - ts) / 0.4))
    footnote(im, "Bazerman & Samuelson, 1983 · names and rows illustrative", False, 1850)
    return im

def sc_guess(t):
    im = bg(True); t0 = S("s2"); tg = WT("s2", "guess"); tv = WT("s2", "$5.13.")
    put(im, pill("true value: $8", 40, (40, 46, 60)), 540, 600, ease((t - t0 + 0.1) / 0.2))
    k = spring((t - t0 + 0.1) / 0.45); v = roll(t, tg, tv + 0.3 - tg, 8, 5.13)
    c = stat("Their average guess", f"${v:.2f}", "below the true value" if t >= tv else "guessing…", 860, True, 190, LILAC if t >= tv else D_INK)
    put(im, lift(c, True), 540, 1080 + (1 - k) * 60, min(1, k * 1.5))
    if t >= tv + 0.3:
        ka = spring((t - tv - 0.3) / 0.4); put(im, T("↓", 160, LILAC, 700), 540, 1480 + (1 - ka) * -40, min(1, ka * 1.5))
    footnote(im, "Mean estimate $5.13 · Bazerman & Samuelson, 1983", True)
    return im

BIDS = (("nour", "Nour", "$10.40"), ("sami", "Sami", "$8.60"), (("B", VIOLET), "Bidder 3", "$7.10"), (("C", GREEN_APP), "Bidder 4", "$5.90"))
def sc_winner(t):
    im = bg(False); t0 = S("s3"); th = WT("s3", "highest"); tl_ = WT("s4", "$2.01,")
    if t < tl_ - 0.15:
        w, h = 880, 860; c = card(w, h, False, 30); c.alpha_composite(T("THE SEALED BIDS, OPENED", 26, GREY_TXT, 700, True), (50, 44))
        for i, (who, name, bid) in enumerate(BIDS):
            ti = t0 + 0.1 + (3 - i) * 0.25; kk = spring((t - ti) / 0.4)                 # lowest bid first, the highest lands last
            if kk <= 0: continue
            y = int(130 + i * 170 + (1 - kk) * 30); win_ = i == 0 and t >= th
            row = card(780, 140, False, 24, fill=(238, 234, 255) if win_ else None)
            row.alpha_composite(head(who, 96), (22, 22)); row.alpha_composite(T(name, 40, L_INK, 600), (140, 46))
            bv = T(bid, 56, VIOLET if win_ else L_INK, 700); row.alpha_composite(bv, (760 - bv.width - 30, 38))
            c.alpha_composite(row, (50, y))
        k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1080, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
        if t >= th: put(im, pill("WINNER", 38, VIOLET), 540, 1080 - 430 + 130 + 70, ease((t - th) / 0.2), 0.85 + 0.15 * spring((t - th) / 0.4))
        footnote(im, "Bids on screen are illustrative", False, 1850)
    else:
        k = spring((t - tl_ + 0.15) / 0.45); v = roll(t, tl_ - 0.1, 0.6, 0, 2.01)
        c = stat("The winner's average result", f"−${v:.2f}", "per auction, across 48 auctions", 860, False, 190, RED_UI)
        put(im, lift(c), 540, 1060 + (1 - k) * 60, min(1, k * 1.5))
        stamp_at(im, big_stamp("OVERPAID", RED_UI, 96, -8), 540, 1470, t, tl_ + 0.55)
        footnote(im, "Mean winning bid $10.01 on an $8 item · Bazerman & Samuelson, 1983", False, 1850)
    return im

def sc_curse(t):
    im = bg(True); t0 = S("n1"); ty = WT("n1", "1971,"); tc = WT("n1", "winner's")
    k = spring((t - t0 + 0.1) / 0.45)
    rig = oil_rig(560 if t < tc - 0.1 else 440)
    put(im, rig, 540, (1000 if t < tc - 0.1 else 820) + (1 - k) * 60, min(1, k * 1.5))
    if t < tc - 0.1:
        if t >= ty - 0.05: put(im, pill("1971 · bidding for oil fields", 40, VIOLET), 540, 1460, ease((t - ty + 0.05) / 0.2), 0.85 + 0.15 * spring((t - ty + 0.05) / 0.4))
    else:
        kk = spring((t - tc + 0.1) / 0.45); c = card(860, 260, True, 30)
        lab = T("THE WINNER'S CURSE", 78, LILAC, 700); c.alpha_composite(lab, (int(430 - lab.width / 2), 90))
        put(im, lift(c, True), 540, 1310 + (1 - kk) * 60, min(1, kk * 1.5), 0.9 + 0.1 * kk)
    footnote(im, "Capen, Clapp & Campbell, Atlantic Richfield engineers, 1971", True)
    return im

def sc_quote(t):
    im = bg(False); t0 = S("q1"); tf = WT("q1", "fifty"); tI = S("q2")
    if t < tI - 0.08:
        w, h = 880, 820; c = card(w, h, False, 30); c.alpha_composite(T("YOU WON AGAINST", 26, GREY_TXT, 700, True), (50, 44))
        n = int(clamp((t - tf + 0.05) / 0.9) * 50)
        if t >= tf - 0.05:
            cnt = T(f"{n} bidders", 72, L_INK, 700); c.alpha_composite(cnt, (50, 92))
        for i in range(51):
            r, col_ = divmod(i, 9); x = 70 + col_ * 86; y = 230 + r * 92
            if i == 0: c.alpha_composite(head("nour", 74), (x - 4, y - 4)); continue
            if i - 1 < n:
                ImageDraw.Draw(c).ellipse((x, y, x + 66, y + 66), fill=(BIDDER_COLS[i % 3] if i % 7 == 0 else (206, 210, 222)) + (255,))
        k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1070, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
        th = WT("q1", "How")
        if t >= th: put(im, pill("how should you feel?", 40, VIOLET), 540, 1580, ease((t - th) / 0.2), 0.85 + 0.15 * spring((t - th) / 0.4))
    else:
        k = spring((t - tI + 0.08) / 0.35); put(im, T("“ILL.”", 260, RED_UI, 700), 540, 1020, min(1, k * 1.6), 0.7 + 0.3 * k)
        put(im, pill("the engineers' answer", 36, (60, 66, 86)), 540, 1330, ease((t - tI) / 0.25))
    footnote(im, "Capen, Clapp & Campbell, 1971, p. 645 · dots illustrative", False, 1850)
    return im

def sc_fix(t):
    im = bg(True); t0 = S("tk"); tm = WT("tk", "maximum"); tst = WT("tk", "starts.")
    put(im, jar(300), 540, 720 + 6 * np.sin(t * 2.2), ease((t - t0 + 0.1) / 0.25))     # the same jar again: loops back to frame 1
    k = spring((t - t0 + 0.1) / 0.45); w = 860; c = card(w, 420, True, 30)
    c.alpha_composite(head("nour", 110), (44, 40)); c.alpha_composite(T("MY MAXIMUM", 26, D_MUTE, 700, True), (180, 50))
    v = roll(t, tm - 0.1, 0.6, 0, 7)
    c.alpha_composite(T(f"${v:.0f}" if t >= tm - 0.1 else "$ —", 120, LILAC if t >= tm else D_INK, 700), (180, 90))
    b = pill("Set before bidding", 38, VIOLET if t >= tst else (60, 66, 86)); c.alpha_composite(b, (44, 300))
    put(im, lift(c, True), 540, 1310 + (1 - k) * 60, min(1, k * 1.5))
    bx, by = 540 - w / 2 + 44 + b.width / 2, 1310 - 210 + 300 + b.height / 2
    if t >= tst - 0.7:
        e = eout((t - tst + 0.7) / 0.5); put(im, cursor(), bx + 220 - 200 * e + 20, by + 220 - 200 * e + 30)
    ripple(im, bx, by, (t - tst) / 0.5)
    footnote(im, "Example numbers", True)
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

FN = {"hook": sc_hook, "klass": sc_klass, "guess": sc_guess, "winner": sc_winner, "curse": sc_curse, "quote": sc_quote, "fix": sc_fix, "outro": sc_outro}

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
    s.pop(WT("h1", "$8."), 0.04, 650); s.ding(T_PAID + 0.3, 1318, 0.03)
    tb = WT("s1", "bid")
    for i in range(4): s.pop(tb - 0.1 + i * 0.22, 0.03, 520 + i * 50)
    s.pop(WT("s1", "secret"), 0.04, 700)
    tg, tv = WT("s2", "guess"), WT("s2", "$5.13.")
    for i in range(int((tv + 0.3 - tg) / 0.1)): s.tick(tg + i * 0.1, 0.01, 2400 - i * 30)
    s.ding(tv + 0.3, 1046, 0.025)
    for i in range(4): s.pop(S("s3") + 0.1 + (3 - i) * 0.25, 0.03, 500 + i * 40)
    s.ding(WT("s3", "highest"), 1568, 0.03)
    tl_ = WT("s4", "$2.01,")
    for i in range(6): s.tick(tl_ - 0.1 + i * 0.1, 0.01, 2000)
    s.thud(tl_ + 0.55, 0.08)
    s.pop(WT("n1", "1971,"), 0.04, 600); s.thud(WT("n1", "winner's"), 0.06)
    tf = WT("q1", "fifty")
    for i in range(9): s.tick(tf + i * 0.1, 0.01, 2200 + i * 40)
    s.pop(WT("q1", "How"), 0.04, 650); s.thud(S("q2"), 0.09)
    s.pop(WT("tk", "maximum"), 0.04, 700); s.ding(WT("tk", "starts."), 1318, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson07_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
