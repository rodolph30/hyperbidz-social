"""Auction short 08 (v3, quick): "Google's auction IPO". In Aug 2004 Google sold its first public shares through an online
(modified Dutch) auction that anyone could join from five shares; the price came in at $85, below the $108-$135 range; 19.6 million
shares, $1.67 billion raised; first-day close $100.34. Usually IPOs are priced by book-building (banks invite institutional investors).
Run: python3 tools/lessons/lesson08.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson08_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "ambient", 8
XF = 0.16
SC = [("hook", True, 0.0, S("s1") - 0.1), ("invite", False, S("s1") - 0.1, S("s2") - 0.1), ("open", True, S("s2") - 0.1, S("s3") - 0.1),
      ("price", False, S("s3") - 0.1, S("s5") - 0.1), ("raised", True, S("s5") - 0.1, S("s6") - 0.1), ("day1", False, S("s6") - 0.1, S("tk") - 0.1),
      ("lesson", True, S("tk") - 0.1, S("e2") - 0.15), ("outro", True, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)

# ---------- drawings ----------
_CERT = {}
def certificate(w=820):
    """a generic share certificate: guilloche border, 'SHARES' heading, seal. Name in plain type, no logo."""
    if w in _CERT: return _CERT[w].copy()
    h = int(w * 0.66); im = card(w, h, True, 26); d = ImageDraw.Draw(im)
    for i in range(3): d.rounded_rectangle((18 + i * 10, 18 + i * 10, w - 19 - i * 10, h - 19 - i * 10), radius=18, outline=((BLUE, VIOLET, LILAC)[i]) + (255,), width=3)
    for x in np.linspace(60, w - 60, 34):                                        # wavy guilloche band at top and bottom
        d.arc((x - 22, 52, x + 22, 92), 0, 180, fill=LILAC + (160,), width=2); d.arc((x - 22, h - 92, x + 22, h - 52), 180, 360, fill=LILAC + (160,), width=2)
    a = T("SHARES · CLASS A", 26, D_MUTE, 700, True); im.alpha_composite(a, (int(w / 2 - a.width / 2), 118))
    g = T("Google", 120, D_INK, 700); im.alpha_composite(g, (int(w / 2 - g.width / 2), 160))
    y = T("FIRST PUBLIC SHARES · 2004", 30, LILAC, 700, True); im.alpha_composite(y, (int(w / 2 - y.width / 2), 320))
    d.ellipse((w - 190, h - 200, w - 80, h - 90), fill=VIOLET + (255,)); d.ellipse((w - 176, h - 186, w - 94, h - 104), outline=(255, 255, 255, 200), width=3)
    for i in range(3): d.line([(80, h - 150 + i * 30), (80 + (300 - i * 70), h - 150 + i * 30)], fill=LINE_D + (255,), width=6)
    _CERT[w] = im; return im.copy()

def lock(s=120, col=(150, 155, 166)):
    im = Image.new("RGBA", (s, int(s * 1.2)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = col + (255,)
    d.arc((s * 0.2, 0, s * 0.8, s * 0.7), 180, 360, fill=c, width=int(s * 0.1)); d.line([(s * 0.2, s * 0.35), (s * 0.2, s * 0.55)], fill=c, width=int(s * 0.1))
    d.line([(s * 0.8, s * 0.35), (s * 0.8, s * 0.55)], fill=c, width=int(s * 0.1))
    d.rounded_rectangle((0, s * 0.5, s - 1, s * 1.2 - 1), radius=int(s * 0.12), fill=c); d.ellipse((s * 0.42, s * 0.72, s * 0.58, s * 0.88), fill=(255, 255, 255, 255))
    return im

# ---------- scenes ----------
def sc_hook(t):
    im = bg(True); bob = 6 * np.sin(t * 2.0)
    put(im, lift(certificate(840), True), 540, 930 + bob, 1, 0.97 + 0.03 * spring(t / 0.5))
    ta = WT("h1", "auction.")
    st = big_stamp("SOLD BY AUCTION", VIOLET, 84, -7)
    if t < ta: put(im, st, 560, 1330, 1)                                            # stamp already there on frame 1: the cover shows the hook
    else: put(im, st, 560, 1330, 1, 1 + 0.18 * np.sin(np.pi * clamp((t - ta) / 0.3)))
    ts = WT("h2", "surprise.")
    if t >= ts - 0.1:
        q = T("$ ???", 120, LILAC, 700); put(im, q, 540, 1620, ease((t - ts + 0.1) / 0.2), 0.8 + 0.2 * spring((t - ts + 0.1) / 0.4))
    footnote(im, "Certificate drawn for illustration", True)
    return im

FUNDS = ((("A", VIOLET), "Big fund A"), (("B", GREEN_APP), "Big fund B"), (("C", (150, 155, 166)), "Big fund C"))
def sc_invite(t):
    im = bg(False); t0 = S("s1"); tb = WT("s1", "big"); tbid = WT("s1", "bid")
    w, h = 900, 720; win = window(w, h, "New stock · invite only", False)
    lk = lock(70); win.alpha_composite(lk, (w - 110, 96))
    win.alpha_composite(chip("the usual way: book-building", False, 26), (50, 104))
    for i, (who, name) in enumerate(FUNDS):
        ti = tb - 0.1 + i * 0.2; k = spring((t - ti) / 0.4)
        if k <= 0: continue
        y = int(210 + i * 160 + (1 - k) * 30); row = card(800, 136, False, 24)
        row.alpha_composite(head(who, 96), (22, 20)); row.alpha_composite(T(name, 40, L_INK, 600), (140, 44))
        if t >= tbid + i * 0.1: p = pill("BID", 30, VIOLET); row.alpha_composite(p, (800 - p.width - 30, 44))
        win.alpha_composite(row, (50, y))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 960, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    tn = tbid + 0.25
    if t >= tn:                                                                      # Nour, outside the window: not invited
        kk = spring((t - tn) / 0.4); r = card(620, 130, False, 24, fill=(244, 244, 247))
        r.alpha_composite(head("nour", 90), (20, 20)); r.alpha_composite(T("Nour · not invited", 38, (150, 155, 166), 600), (130, 42))
        put(im, lift(r), 540, 1520 + (1 - kk) * 40, min(1, kk * 1.5))
    footnote(im, "Investopedia, Book Building · names illustrative", False, 1850)
    return im

def sc_open(t):
    im = bg(True); t0 = S("s2"); ta = WT("s2", "anyone"); tf = WT("s2", "five")
    k = spring((t - t0 + 0.1) / 0.45); pw, ph = 580, 1100; p = phone(pw, ph, True)
    p.alpha_composite(T("IPO auction · Aug 2004", 30, D_MUTE, 600), (60, 110))
    r = card(pw - 100, 150, True, 24); r.alpha_composite(head("nour", 100), (24, 25)); r.alpha_composite(T("Nour", 44, D_INK, 700), (150, 50))
    p.alpha_composite(r, (50, 180))
    p.alpha_composite(T("SHARES", 26, D_MUTE, 700, True), (60, 380))
    box = card(pw - 120, 190, True, 22, fill=(30, 35, 48)); n = T("5" if t >= tf - 0.05 else "–", 140, LILAC if t >= tf - 0.05 else D_MUTE, 700)
    box.alpha_composite(n, (40, 18)); p.alpha_composite(box, (60, 420))
    p.alpha_composite(T("minimum: 5 shares", 30, D_MUTE, 500), (60, 630))
    tb = tf + 0.55; bt = pill("Place bid", 44, VIOLET if t < tb else GREEN_APP, padx=60, pady=20); bx = pw // 2 - bt.width // 2; by = 780
    p.alpha_composite(bt, (bx, by))
    if t >= tb: ck = T("Bid sent", 36, GREEN_APP, 700); p.alpha_composite(ck, (pw // 2 - ck.width // 2, by + 120))
    put(im, lift(p, True), 540, 1200 + (1 - k) * 80, min(1, k * 1.5))
    if t >= ta - 0.05: put(im, pill("open to anyone", 40, BLUE), 540, 520, ease((t - ta + 0.05) / 0.2), 0.85 + 0.15 * spring((t - ta + 0.05) / 0.4))
    cx, cy = 540 - pw / 2 + bx + bt.width / 2, 1200 - ph / 2 + by + bt.height / 2
    if tb - 0.7 <= t < tb + 0.5:
        e = eout((t - tb + 0.7) / 0.5); put(im, cursor(), cx + 240 - 220 * e + 20, cy + 240 - 220 * e + 30)
    ripple(im, cx, cy, (t - tb) / 0.5)
    footnote(im, "Bids by internet, fax or phone; min. 5 shares · screen illustrative", True)
    return im

def sc_price(t):
    im = bg(False); t0 = S("s3"); te = WT("s3", "$135"); tl_ = WT("s4", "lower:"); t85 = WT("s4", "$85.")
    k = spring((t - t0 + 0.1) / 0.45)
    if t < tl_:
        v = 135; pk = 1 + 0.06 * np.sin(np.pi * clamp((t - te) / 0.35))
        c = stat("Google's estimate, per share", f"$108–${v:.0f}", "the range it announced", 900, False, 150)
        put(im, lift(c), 540, 1060 + (1 - k) * 60, min(1, k * 1.5), pk)
    else:
        v = roll(t, tl_, t85 + 0.2 - tl_, 135, 85)
        c = stat("What the bids set", f"${v:.0f}", "per share" if t >= t85 else "falling…", 900, False, 190, VIOLET if t >= t85 else L_INK)
        put(im, lift(c), 540, 1060, 1)
        old = T("$108–$135", 64, (150, 155, 166), 700); put(im, old, 540, 700)
        strike(im, 540 - old.width / 2 - 10, 704, 540 + old.width / 2 + 10, (t - tl_) / 0.3)
        stamp_at(im, big_stamp("BELOW THE RANGE", RED_UI, 80, -8), 540, 1480, t, t85 + 0.35)
    footnote(im, "LA Times, 19 Aug 2004", False, 1850)
    return im

def sc_raised(t):
    im = bg(True); t0 = S("s5"); tr = WT("s5", "raised"); tv = WT("s5", "$1.67")
    k = spring((t - t0 + 0.1) / 0.45); v = roll(t, tr - 0.1, tv + 0.6 - tr, 0, 1.67)
    c = stat("The sale raised", f"${v:.2f} billion", "19.6 million shares at $85", 940, True, 124, LILAC if t >= tv + 0.5 else D_INK)
    put(im, lift(c, True), 540, 1060 + (1 - k) * 60, min(1, k * 1.5))
    footnote(im, "Washington Times; Berkeley Tech. Law Journal, 2005", True)
    return im

def sc_day1(t):
    im = bg(False); t0 = S("s6"); tc = WT("s6", "closed"); tv = WT("s6", "$100.34.")
    w, h = 900, 900; c = card(w, h, False, 30); d = ImageDraw.Draw(c)
    c.alpha_composite(T("FIRST DAY OF TRADING · 19 AUG 2004", 26, GREY_TXT, 700, True), (50, 44))
    x0, x1, yb, yt = 90, 830, 760, 300; y85 = yb - (85 - 80) / 25 * (yb - yt); y100 = yb - (100.34 - 80) / 25 * (yb - yt)
    d.line([(x0, y85), (x1, y85)], fill=(200, 204, 214, 255), width=3)
    c.alpha_composite(T("$85 auction price", 28, GREY_TXT, 600), (x0, int(y85) + 12))
    pr = clamp((t - tc + 0.2) / (tv - tc + 0.5))
    pts = [(x0, y85), (x0 + 60, y100 + 10), (x0 + 200, y100 - 25), (x0 + 330, y100 + 40), (x0 + 470, y100 - 50), (x0 + 600, y100 + 15), (x1, y100)]
    seg = [pts[0]]; L = len(pts) - 1; f = pr * L
    for i in range(1, L + 1):
        if f >= i: seg.append(pts[i])
        else:
            a, b = pts[i - 1], pts[i]; u = f - (i - 1); seg.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)); break
    if pr > 0 and len(seg) > 1: d.line(seg, fill=GREEN_APP + (255,), width=10, joint="curve")
    if pr >= 1:
        d.ellipse((x1 - 16, y100 - 16, x1 + 16, y100 + 16), fill=GREEN_APP + (255,))
    v = roll(t, tc - 0.1, tv + 0.4 - tc, 85, 100.34)
    c.alpha_composite(T(f"${v:.2f}", 110, GREEN_APP if t >= tv else L_INK, 700), (50, 110))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1080, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tv + 0.4: put(im, pill("closing price, day one", 38, GREEN_APP), 540, 1620, ease((t - tv - 0.4) / 0.2), 0.85 + 0.15 * spring((t - tv - 0.4) / 0.4))
    footnote(im, "CNN Money, 19 Aug 2004 · line between open and close illustrative", False, 1850)
    return im

def sc_lesson(t):
    im = bg(True); t0 = S("tk"); to = WT("tk", "open."); tg = WT("tk", "Even")
    k = spring((t - t0 + 0.1) / 0.45)
    if t < tg - 0.1:
        c = card(880, 520, True, 30)
        c.alpha_composite(head("sami", 110), (60, 50)); c.alpha_composite(head("nour", 110), (190, 50))
        for i, who in enumerate((("A", VIOLET), ("B", GREEN_APP))): c.alpha_composite(head(who, 110), (320 + i * 130, 50))
        a = T("Anyone can bid", 70, D_INK, 700); c.alpha_composite(a, (60, 210))
        b = T("→ price set in the open", 56, LILAC if t >= to else D_MUTE, 700); c.alpha_composite(b, (60, 330))
        put(im, lift(c, True), 540, 1080 + (1 - k) * 60, min(1, k * 1.5))
        footnote(im, "Sami, Nour and bidders: our illustrative cast", True)
    else:
        kk = spring((t - tg + 0.1) / 0.45)                                           # back to the certificate of frame 1: the loop
        put(im, lift(certificate(840), True), 540, 930, min(1, kk * 1.5), 0.92 + 0.08 * kk)
        put(im, big_stamp("SOLD BY AUCTION", VIOLET, 84, -7), 560, 1330, min(1, kk * 1.5))
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

FN = {"hook": sc_hook, "invite": sc_invite, "open": sc_open, "price": sc_price, "raised": sc_raised, "day1": sc_day1, "lesson": sc_lesson, "outro": sc_outro}

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
    s.thud(WT("h1", "auction."), 0.06); s.ding(WT("h2", "surprise."), 1318, 0.03)
    tb = WT("s1", "big")
    for i in range(3): s.pop(tb - 0.1 + i * 0.2, 0.03, 520 + i * 50)
    s.pop(WT("s1", "bid") + 0.25, 0.03, 420)
    s.pop(WT("s2", "anyone") - 0.05, 0.04, 700); s.pop(WT("s2", "five"), 0.04, 760)
    tbb = WT("s2", "five") + 0.55; s.ding(tbb, 1568, 0.03)
    te = WT("s3", "$135")
    s.pop(te, 0.04, 700)
    tl_ = WT("s4", "lower:"); t85 = WT("s4", "$85.")
    for i in range(int((t85 + 0.2 - tl_) / 0.1)): s.tick(tl_ + i * 0.1, 0.01, 2400 - i * 40)
    s.thud(t85 + 0.35, 0.08)
    tr = WT("s5", "raised"); tv = WT("s5", "$1.67")
    for i in range(int((tv + 0.6 - tr) / 0.1)): s.tick(tr - 0.1 + i * 0.1, 0.01, 2000 + i * 30)
    s.ding(tv + 0.5, 1046, 0.025)
    tc = WT("s6", "closed"); tv2 = WT("s6", "$100.34.")
    for i in range(int((tv2 + 0.4 - tc) / 0.1)): s.tick(tc - 0.1 + i * 0.1, 0.01, 2100 + i * 30)
    s.ding(tv2 + 0.4, 1318, 0.03)
    s.ding(WT("tk", "open."), 1568, 0.03); s.thud(WT("tk", "Even"), 0.06)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson08_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
