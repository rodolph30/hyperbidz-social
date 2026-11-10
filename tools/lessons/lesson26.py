"""Auction short 26 (v3, quick, who: Sami): "Start low, end high". Problem: Sami fears a low starting price means a low sale.
Reframe: Ku, Galinsky & Murnighan (JPSP 2006), six studies; on real eBay data for 179 Persian rugs and 87 Nikon cameras, lower
starting prices drew more bids and bidders and ended higher; with a misspelled name (little traffic) low starts ended low.
Fix: start low, set a reserve as the floor (lesson 19), get it seen. Takeaway: "In a chat, start high. In an auction, start low,
and let them bid." Loop: ends back on the start-low / end-high card from frame 1.
Run: python3 tools/lessons/lesson26.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os, math
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson26_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "keys", 26
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("problem", True, S("p1") - 0.1, S("r1") - 0.1), ("study", False, S("r1") - 0.1, S("r3") - 0.1),
      ("typo", True, S("r3") - 0.1, S("f1") - 0.1), ("fix", False, S("f1") - 0.1, S("tk") - 0.1), ("loop", False, S("tk") - 0.1, S("e2") - 0.15),
      ("outro", False, S("e2") - 0.15, TOTAL)]
BUYERS = (("R", VIOLET), ("M", GREEN_APP), ("J", SILVER), ("K", BLUE), ("N", LILAC))
MUTE_L = (110, 116, 130)

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def bar_row(c, y, label, word, frac, col, wcol, w):
    c.alpha_composite(T(label, 26, MUTE_L, 700, True), (44, y))
    d = ImageDraw.Draw(c); bx, by, bw, bh = 44, y + 50, w - 88, 76
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=20, fill=(236, 238, 246, 255))
    if frac > 0.02: d.rounded_rectangle((bx, by, bx + max(40, bw * frac), by + bh), radius=20, fill=col + (255,))
    if word: c.alpha_composite(T(word, 64, wcol, 700), (44, by + bh + 14))

def price_card(t, t_start, t_end, end_frac=0.92, end_word="Higher", end_col=GREEN_UI, title="SAME AUCTION, TWO PRICES"):
    """starting price: a short blue bar ("Low"); final price: a long bar ("Higher")"""
    w, h = 860, 620; c = card(w, h, False, 30)
    c.alpha_composite(T(title, 26, MUTE_L, 700, True), (44, 40))
    ks = spring((t - t_start) / 0.45) if t >= t_start else 0
    bar_row(c, 110, "STARTING PRICE", "Low" if ks > 0.2 else "", 0.18 * ks, BLUE, BLUE, w)
    ke = spring((t - t_end) / 0.6) if t >= t_end else 0
    bar_row(c, 360, "FINAL PRICE", end_word if ke > 0.2 else "", end_frac * ke, end_col, end_col, w)
    return c

def sc_hook(t):
    im = bg(False); ts = WT("h1", "Start"); tl = WT("h1", "lower."); tt = WT("h2", "mistake")
    c = price_card(t, -0.5, -0.3); put(im, lift(c), 540, 980, 1, 1.0 + 0.04 * (1 - spring(t / 0.45)))
    if t >= tl - 0.2: select_box(im, (135, 1160, 390, 1262), eout((t - tl + 0.2) / 0.3), 1, VIOLET)
    if t >= tt - 0.2:
        kq = spring((t - tt + 0.2) / 0.4); put(im, pill("…one spelling mistake flips it", 46, RED_UI, padx=32, pady=14), 540, 1430 + (1 - kq) * 20, min(1, kq * 1.5))
    footnote(im, "Source: Ku, Galinsky & Murnighan, 2006", False, 1850)
    return im

def rug(w=520, h=320):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=14, fill=(54, 42, 108, 255))
    d.rounded_rectangle((18, 18, w - 19, h - 19), radius=10, outline=LILAC + (255,), width=8)
    d.rounded_rectangle((40, 40, w - 41, h - 41), radius=8, fill=(38, 64, 140, 255))
    cx, cy = w / 2, h / 2
    for s, col in ((110, VIOLET), (72, LILAC), (36, (255, 255, 255))):
        d.polygon([(cx, cy - s), (cx + s * 1.5, cy), (cx, cy + s), (cx - s * 1.5, cy)], fill=col + (255,))
    for x in range(10, w - 6, 22):
        d.line([(x, h - 2), (x, h + 0)], fill=(200, 200, 210, 255), width=3)
    return im

def sc_problem(t):
    im = bg(True); t0 = S("p1"); tl = WT("p1", "low")
    w, h = 820, 760; c = window(w, h, "Listing · Persian rug", True)
    r = rug(); c.alpha_composite(r, (int(w / 2 - r.width / 2), 110))
    c.alpha_composite(T("STARTING PRICE", 26, D_MUTE, 700, True), (60, 480))
    c.alpha_composite(T("$50", 120, D_INK, 700), (60, 520))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1080, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    ks = spring((t - t0 - 0.15) / 0.4)
    if ks > 0: put(im, head("sami", 130), 540, 600 + (1 - ks) * 30, min(1, ks * 1.5))
    if t >= tl - 0.15:
        kk = spring((t - tl + 0.15) / 0.4); put(im, pill("Low start = low sale?", 48, VIOLET, padx=34, pady=16), 540, 1560 + (1 - kk) * 20, min(1, kk * 1.5))
    footnote(im, "Sami's rug and price are illustrative", True, 1850)
    return im

def study_card(t):
    w, h = 860, 640; c = card(w, h, False, 30); t179 = WT("r1", "179"); t87 = WT("r1", "87")
    c.alpha_composite(T("REAL ONLINE AUCTIONS STUDIED", 26, MUTE_L, 700, True), (44, 40))
    n = int(round(roll(t, S("r1") + 0.2, max(0.8, t179 - S("r1") - 0.1), 0, 179))); v = T(str(n), 170, L_INK, 700); c.alpha_composite(v, (44, 90))
    c.alpha_composite(T("Persian rugs", 50, MUTE_L, 600), (64 + v.width, 90 + v.height - 70))
    if t >= t87 - 0.35:
        km = spring((t - t87 + 0.35) / 0.4); m = int(round(roll(t, t87 - 0.35, 0.7, 0, 87)))
        v2 = fade_in(T(str(m), 170, L_INK, 700), km); c.alpha_composite(v2, (44, int(350 + (1 - km) * 20)))
        c.alpha_composite(fade_in(T("cameras", 50, MUTE_L, 600), km), (64 + T("87", 170, L_INK, 700).width, 350 + v2.height - 70))
    return c

def result_card(t):
    w, h = 860, 700; c = card(w, h, False, 30); t0 = S("r2"); tb = WT("r2", "bidders,"); th = WT("r2", "higher.")
    c.alpha_composite(T("LOW STARTING PRICE", 26, MUTE_L, 700, True), (44, 40))
    c.alpha_composite(T("More bidders", 64, L_INK, 700), (44, 90))
    for j, who in enumerate(BUYERS):
        kj = spring((t - (tb - 0.5) - j * 0.14) / 0.35)
        if kj > 0: c.alpha_composite(fade_in(head(who, 120), kj), (44 + j * 150, int(200 + (1 - kj) * 24)))
    if t >= th - 0.6:
        d = ImageDraw.Draw(c); bx, by, bw, bh = 44, 400, w - 88, 76
        c.alpha_composite(T("FINAL PRICE", 26, MUTE_L, 700, True), (44, 350))
        ke = spring((t - th + 0.6) / 0.6)
        d.rounded_rectangle((bx, by + 10, bx + bw, by + 10 + bh), radius=20, fill=(236, 238, 246, 255))
        d.rounded_rectangle((bx, by + 10, bx + max(40, bw * 0.92 * ke), by + 10 + bh), radius=20, fill=GREEN_UI + (255,))
        if ke > 0.3: c.alpha_composite(T("Higher ↑", 72, GREEN_UI, 700), (44, by + bh + 34))
    return c

def sc_study(t):
    im = bg(False); t0 = S("r1"); t2 = S("r2") - 0.15
    if t < t2:
        c = study_card(t); k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1060, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    else:
        c = result_card(t); k = spring((t - t2) / 0.4); put(im, lift(c), 540, 1060 + (1 - k) * 40, min(1, k * 1.6))
    footnote(im, "Source: Ku, Galinsky & Murnighan, JPSP 2006 (eBay data)", False, 1850)
    return im

def sc_typo(t):
    im = bg(True); t0 = S("r3"); tm = WT("r3", "misspelled."); tf = WT("r3", "Few"); tl = WT("r3", "stayed")
    w, h = 860, 170; sb = card(w, h, True, 85, fill=(30, 36, 52))
    d = ImageDraw.Draw(sb); d.ellipse((50, 55, 104, 109), outline=D_MUTE + (255,), width=7); d.line([(96, 102), (122, 128)], fill=D_MUTE + (255,), width=8)
    word = T("Persain rug", 64, D_INK, 600); sb.alpha_composite(word, (150, 85 - word.height // 2))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(sb, True), 540, 820, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tm - 0.2:   # red squiggle under the misspelling
        ks = eout((t - tm + 0.2) / 0.4); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
        x0 = 540 - w / 2 + 150; x1 = x0 + word.width; pts = []
        for i in range(int((x1 - x0) * ks / 6) + 1): x = x0 + i * 6; pts.append((x, 870 + 8 * math.sin(i * 1.2)))
        if len(pts) > 1: dd.line(pts, fill=RED_UI + (255,), width=6)
        im.alpha_composite(lay)
    if t >= tf - 0.2:
        kf = spring((t - tf + 0.2) / 0.4); put(im, pill("Few people found it", 46, (54, 42, 108), padx=32, pady=14), 540, 1060 + (1 - kf) * 20, min(1, kf * 1.5))
    if t >= tl - 0.5:
        kc = spring((t - tl + 0.5) / 0.45)
        c = card(820, 260, True, 28, fill=(30, 36, 52)); c.alpha_composite(T("FINAL PRICE", 26, D_MUTE, 700, True), (40, 34))
        dd = ImageDraw.Draw(c); dd.rounded_rectangle((40, 84, 780, 160), radius=20, fill=(44, 50, 66, 255))
        dd.rounded_rectangle((40, 84, 40 + 740 * 0.2 * kc + 40, 160), radius=20, fill=BLUE + (255,))
        if kc > 0.3: c.alpha_composite(T("Low", 56, BLUE, 700), (40, 176))
        put(im, lift(fade_in(c, kc), True), 540, 1400 + (1 - kc) * 30)
    footnote(im, "Source: Ku, Galinsky & Murnighan, 2006 · search bar illustrative", True, 1850)
    return im

def sc_fix(t):
    im = bg(False); t0 = S("f1")
    steps = [("1", "Start low", WT("f1", "start")), ("2", "Set a reserve: your floor", WT("f1", "reserve")), ("3", "Get it seen", WT("f1", "seen."))]
    for j, (n, txt, tw) in enumerate(steps):
        kj = spring((t - tw + 0.25) / 0.4)
        if kj <= 0: continue
        r = card(860, 190, False, 30); d = ImageDraw.Draw(r); d.ellipse((36, 45, 136, 145), fill=(VIOLET if j != 1 else GREEN_UI) + (255,))
        nn = T(n, 56, (255, 255, 255), 700); r.alpha_composite(nn, (86 - nn.width // 2, 95 - nn.height // 2 - 4))
        tt = T(txt, 56, L_INK, 700); r.alpha_composite(tt, (170, 95 - tt.height // 2 - 4))
        put(im, lift(fade_in(r, kj)), 540, 760 + j * 260 + (1 - kj) * 30)
    put(im, head("sami", 120), 540, 520, ease((t - t0) / 0.3))
    footnote(im, "A reserve: the lowest price the seller accepts (lesson 19)", False, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tc = WT("tk", "chat,"); ta = WT("tk", "auction,")
    c = price_card(t, -5, -5); put(im, lift(c), 540, 900, ease((t - t0) / 0.25), 0.97 + 0.03 * spring((t - t0) / 0.5))
    if t >= tc - 0.15:
        kk = spring((t - tc + 0.15) / 0.4); put(im, pill("Chat: start high", 46, L_INK, padx=32, pady=14), 540, 1340 + (1 - kk) * 20, min(1, kk * 1.5))
    if t >= ta - 0.15:
        kk = spring((t - ta + 0.15) / 0.4); put(im, pill("Auction: start low", 46, VIOLET, padx=32, pady=14), 540, 1490 + (1 - kk) * 20, min(1, kk * 1.5))
    footnote(im, "Source: Ku, Galinsky & Murnighan, 2006", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 26, BLUE), (540, 7, VIOLET), (750, 14, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "problem": sc_problem, "study": sc_study, "typo": sc_typo, "fix": sc_fix, "loop": sc_loop, "outro": sc_outro}

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
    s.thud(0.05, 0.08); s.ding(0.1, 1318, 0.03)
    tl = WT("h1", "lower."); s.ding(tl - 0.1, 1568, 0.03); s.pop(WT("h2", "mistake") - 0.2, 0.035, 520)
    s.pop(S("p1"), 0.03, 600); s.pop(WT("p1", "low") - 0.15, 0.035, 640)
    t179 = WT("r1", "179"); t87 = WT("r1", "87")
    for j in range(int((t179 - S("r1")) / 0.15)): s.tick(S("r1") + 0.2 + j * 0.15, 0.022)
    for j in range(6): s.tick(t87 - 0.35 + j * 0.11, 0.025)
    tb = WT("r2", "bidders,")
    for j in range(5): s.pop(tb - 0.5 + j * 0.14, 0.03, 560 + j * 40)
    s.ding(WT("r2", "higher.") - 0.2, 1568, 0.035)
    s.thud(WT("r3", "misspelled.") - 0.1, 0.06); s.pop(WT("r3", "Few") - 0.2, 0.035, 520); s.thud(WT("r3", "stayed") - 0.3, 0.05)
    for w_ in ("start", "reserve", "seen."): s.pop(WT("f1", w_) - 0.25, 0.035, 600)
    s.pop(WT("tk", "chat,") - 0.15, 0.035, 600); s.ding(WT("tk", "auction,") - 0.15, 1175, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson26_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
