"""Auction short 06 (v3, quick): "A $3.2 million fish". Tokyo's Toyosu New Year auction, 5 Jan 2026: a 243-kg bluefin tuna from
Oma sold for a record 510.3 million yen (about $3.2 million); the buyer expected 300-400 million; served at the usual menu price.
Run: python3 tools/lessons/lesson06.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson06_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "keys", 6
XF = 0.16
SC = [("hook", True, 0.0, S("s1") - 0.1), ("market", False, S("s1") - 0.1, S("b1") - 0.1), ("bids", True, S("b1") - 0.1, S("b3") - 0.1),
      ("quote", False, S("b3") - 0.1, S("w1") - 0.1), ("why", True, S("w1") - 0.1, S("w2") - 0.1), ("lesson", False, S("w2") - 0.1, S("e2") - 0.15),
      ("outro", True, S("e2") - 0.15, TOTAL)]
T_PRICE = WT("h1", "$3.2 million.")

# ---------- drawings ----------
_TUNA = {}
def tuna(w=860):
    """a bluefin tuna in profile: navy back, silver belly, forked tail, finlets"""
    if w in _TUNA: return _TUNA[w].copy()
    h = int(w * 0.42); S2 = 2; im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    W2, H2 = w * S2, h * S2; cy = H2 * 0.52
    body = [(W2 * (0.04 + 0.70 * i / 40), cy - H2 * 0.36 * np.sin(np.pi * (i / 40) ** 0.8) ** 1.1) for i in range(41)]
    belly = [(W2 * (0.04 + 0.70 * i / 40), cy + H2 * 0.30 * np.sin(np.pi * (i / 40) ** 0.8) ** 1.1) for i in range(40, -1, -1)]
    d.polygon(body + belly, fill=(206, 211, 222, 255))                                     # silver body
    back = body + [(W2 * (0.74 - 0.70 * i / 40), cy - H2 * 0.04 - H2 * 0.08 * np.sin(np.pi * (1 - i / 40))) for i in range(41)]
    d.polygon(back, fill=(26, 44, 92, 255))                                                # navy back
    d.line([(W2 * 0.12, cy - H2 * 0.03), (W2 * 0.70, cy - H2 * 0.02)], fill=(120, 150, 210, 255), width=int(6 * S2))   # blue lateral stripe
    d.polygon([(W2 * 0.72, cy - H2 * 0.05), (W2 * 0.97, cy - H2 * 0.46), (W2 * 0.86, cy), (W2 * 0.97, cy + H2 * 0.44), (W2 * 0.72, cy + H2 * 0.05)], fill=(26, 44, 92, 255))
    d.polygon([(W2 * 0.36, cy - H2 * 0.33), (W2 * 0.44, cy - H2 * 0.52), (W2 * 0.48, cy - H2 * 0.30)], fill=(26, 44, 92, 255))   # dorsal fin
    d.polygon([(W2 * 0.50, cy + H2 * 0.26), (W2 * 0.56, cy + H2 * 0.44), (W2 * 0.58, cy + H2 * 0.22)], fill=(150, 160, 185, 255))
    for i in range(6):                                                                     # yellow-edged finlets (navy here)
        x = W2 * (0.56 + i * 0.026); d.polygon([(x, cy - H2 * 0.22 + i * 6), (x + 14 * S2, cy - H2 * 0.28 + i * 6), (x + 18 * S2, cy - H2 * 0.18 + i * 6)], fill=(70, 96, 170, 255))
    d.polygon([(W2 * 0.20, cy + H2 * 0.02), (W2 * 0.33, cy + H2 * 0.10), (W2 * 0.22, cy + H2 * 0.12)], fill=(60, 84, 150, 255))   # pectoral fin
    d.ellipse((W2 * 0.085, cy - H2 * 0.12, W2 * 0.125, cy - H2 * 0.03), fill=(255, 255, 255, 255)); d.ellipse((W2 * 0.095, cy - H2 * 0.10, W2 * 0.118, cy - H2 * 0.05), fill=(11, 14, 20, 255))
    d.arc((W2 * 0.13, cy - H2 * 0.20, W2 * 0.20, cy + H2 * 0.16), 300, 60, fill=(150, 160, 185, 255), width=int(4 * S2))       # gill line
    im = im.resize((w, h), Image.LANCZOS); _TUNA[w] = im; return im.copy()

def sushi(s=260):
    """a nigiri on a white plate"""
    im = Image.new("RGBA", (s, int(s * 0.62)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); h = im.height
    d.ellipse((0, h * 0.45, s, h * 0.98), fill=(255, 255, 255, 255), outline=(220, 222, 230, 255), width=3)
    d.rounded_rectangle((s * 0.2, h * 0.36, s * 0.8, h * 0.72), radius=int(h * 0.16), fill=(246, 244, 238, 255))
    d.rounded_rectangle((s * 0.16, h * 0.14, s * 0.84, h * 0.50), radius=int(h * 0.18), fill=(214, 72, 104, 255))
    for i in range(3): d.line([(s * (0.32 + i * 0.16), h * 0.18), (s * (0.26 + i * 0.16), h * 0.46)], fill=(236, 130, 156, 255), width=4)
    return im

def clover(s=180, col=GREEN_APP):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s / 2; r = s * 0.2
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)): d.ellipse((c + dx * r - r, c + dy * r - r, c + dx * r + r, c + dy * r + r), fill=col + (255,))
    d.line([(c, c), (c + s * 0.2, c + s * 0.45)], fill=col + (255,), width=int(s * 0.06)); return im

def price_tag(text, dark=True, size=96, label="SOLD FOR"):
    v = T(text, size, D_INK if dark else L_INK, 700); lab = T(label, 28, D_MUTE if dark else (110, 116, 130), 700, True)
    c = card(v.width + 120, v.height + lab.height + 90, dark, 30); c.alpha_composite(lab, (60, 34)); c.alpha_composite(v, (60, 34 + lab.height + 18))
    ImageDraw.Draw(c).ellipse((22, 40, 40, 58), fill=VIOLET + (255,)); return c

def arrow_up(h=220, col=VIOLET, w=150):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((w * 0.34, h * 0.4, w * 0.66, h), fill=col + (255,)); d.polygon([(0, h * 0.45), (w, h * 0.45), (w / 2, 0)], fill=col + (255,)); return im

# ---------- scenes ----------
def sc_hook(t):
    im = bg(True); bob = 10 * np.sin(t * 2.2)
    put(im, lift(tuna(900), True), 540, 900 + bob, 1, 0.97 + 0.03 * spring(t / 0.5))
    pk = 1 + 0.08 * np.sin(np.pi * clamp((t - T_PRICE) / 0.35))                  # the tag is there from frame 1 (cover), pulses on the number
    tg = lift(price_tag("$3.2 million", True, 110), True); put(im, tg, 540, 1290, 1, pk)
    if t >= T_PRICE: select_box(im, (540 - tg.width / 2 + 20, 1290 - tg.height / 2 + 14, 540 + tg.width / 2 - 20, 1290 + tg.height / 2 - 10), eout((t - T_PRICE) / 0.3), 1 - clamp((t - T_PRICE - 1.2) / 0.3))
    tn = WT("h2", "normal")
    if t >= tn - 0.15:                                                           # the open loop: why sell it at normal prices?
        k = spring((t - tn + 0.15) / 0.45); c = card(640, 200, True, 28); c.alpha_composite(sushi(180), (30, 40))
        c.alpha_composite(T("normal price", 46, LILAC, 700), (240, 50)); c.alpha_composite(T("why?", 40, D_MUTE, 700), (240, 116))
        put(im, lift(c, True), 540, 1620 + (1 - k) * 80, min(1, k * 1.5))
    return im

def sc_market(t):
    im = bg(False); t0 = S("s1")
    w, h = 900, 1000; win = window(w, h, "Toyosu market · Tokyo", False)
    win.alpha_composite(chip("first auction of 2026", False, 26), (50, 110))
    tu = tuna(760); win.alpha_composite(tu, (int(w / 2 - tu.width / 2), 210))
    tk = WT("s2", "243-kilo")
    if t >= tk - 0.2:
        v = roll(t, tk - 0.2, 0.8, 0, 243); lab = T(f"{v:.0f} kg", 150, L_INK, 700)
        win.alpha_composite(lab, (int(w / 2 - lab.width / 2), 600))
        sub = T("bluefin tuna · caught off Oma, Japan", 32, (110, 116, 130), 500) if t >= WT("s2", "bluefin") - 0.1 else None
        if sub: win.alpha_composite(sub, (int(w / 2 - sub.width / 2), 850))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tk - 0.2:
        lab = T("243 kg", 150, L_INK, 700); select_box(im, (540 - lab.width / 2 - 14, 1120 - 500 + 600 - 4, 540 + lab.width / 2 + 14, 1120 - 500 + 600 + lab.height + 10), eout((t - tk) / 0.3))
    tj = WT("s1", "January")
    if t >= tj - 0.1 and t < WT("s2", "A") - 0.05:
        put(im, pill("5 Jan 2026 · around 5 a.m.", 38, VIOLET), 540, 560, ease((t - tj + 0.1) / 0.2), 0.85 + 0.15 * spring((t - tj + 0.1) / 0.4))
    footnote(im, "Toyosu New Year auction, 5 Jan 2026 · AP, Nippon TV, Mainichi")
    return im

def sc_bids(t):
    im = bg(True); t0 = S("b1"); tb = WT("b2", "bids"); tf = WT("b2", "¥510 million.")
    ex = stat("The buyer expected", "¥300–400M", "", 860, True, 120, D_INK if t < tb else D_MUTE)
    put(im, lift(ex, True), 540, 640, ease((t - t0 + 0.12) / 0.25), 0.95 + 0.05 * spring((t - t0 + 0.12) / 0.5))
    if t >= tb: strike(im, 540 - 430 + 44, 640 + 30, 540 - 430 + 44 + T("¥300–400M", 120, D_INK, 700).width, eout((t - tb) / 0.35), RED_UI, 10)
    if t >= tb - 0.1:
        v = roll(t, tb, tf + 0.2 - tb, 400, 510.3); k = spring((t - tb + 0.1) / 0.45)
        c = stat("The bids", f"¥{v:.0f}M" if t < tf + 0.2 else "¥510.3M", "≈ $3.2 million" if t >= tf + 0.2 else "climbing…", 860, True, 170, LILAC if t >= tf else D_INK)
        put(im, lift(c, True), 540, 1180 + (1 - k) * 60, min(1, k * 1.5))
        for i in range(int(clamp((t - tb) / 0.42, 0, 4)) + 1):                       # paddles go up, left and right
            if i > 4: break
            ti = tb + i * 0.42; kk = spring((t - ti) / 0.4)
            if kk <= 0: continue
            x = 220 if i % 2 == 0 else 860; col = BIDDER_COLS[i % 3]
            if t < ti + 0.9: put(im, paddle([14, 27, 8, 31, 5][i], col, 110), x, 1640 + (1 - kk) * 80, min(1, kk * 1.5) * (1 - clamp((t - ti - 0.6) / 0.3)))
        stamp_at(im, big_stamp("RECORD", RED_UI, 96, -8), 540, 1560, t, tf + 0.25)
    footnote(im, "Bids on screen are illustrative · final price: AP, Kyodo, Nippon TV", True)
    return im

def sc_quote(t):
    im = bg(False); t0 = S("b3"); te = E("b3")
    w, h = 900, 900; c = card(w, h, False, 30); d = ImageDraw.Draw(c)
    c.alpha_composite(T("THE PRICE, DURING THE BIDDING", 26, (110, 116, 130), 700, True), (50, 44))
    x0, y0, x1, y1 = 80, 780, 840, 150; k = clamp((t - t0) / (WT("b3", "it,”") - t0 + 0.2))
    pts = []
    for i in range(61):
        u = i / 60
        if u > k: break
        pts.append((x0 + (x1 - x0) * u, y0 - (y0 - y1) * (u ** 3.2)))
    d.line([(x0, y0), (x1, y0)], fill=LINE_L + (255,), width=3)
    if len(pts) > 1: d.line(pts, fill=VIOLET + (255,), width=12, joint="curve")
    if pts: d.ellipse((pts[-1][0] - 18, pts[-1][1] - 18, pts[-1][0] + 18, pts[-1][1] + 18), fill=VIOLET + (255,))
    if k >= 1: tg = pill("¥510.3M", 40, VIOLET); c.alpha_composite(tg, (int(x1 - tg.width + 10), int(y1 + 30)))
    put(im, lift(c), 540, 1060, ease((t - t0 + 0.12) / 0.25), 0.95 + 0.05 * spring((t - t0 + 0.12) / 0.5))
    tbo = WT("b3", "boss")
    if t >= tbo - 0.1: put(im, pill("the winning buyer, to reporters", 34, (60, 66, 86)), 540, 1600, ease((t - tbo + 0.1) / 0.2), 0.85 + 0.15 * spring((t - tbo + 0.1) / 0.4))
    footnote(im, "Quote: AP, 5 Jan 2026 · line is illustrative")
    return im

def sc_why(t):
    im = bg(True); t0 = S("w1"); tl_ = WT("w1", "good"); ti = WT("w1", "impress")
    if t < tl_ - 0.1:
        k = spring((t - t0 + 0.1) / 0.45); put(im, T("?", 380, LILAC, 700), 540, 1050 + (1 - k) * 60, min(1, k * 1.5), 0.9 + 0.1 * k)
    elif t < ti - 0.1:
        k = spring((t - tl_ + 0.1) / 0.45); c = card(700, 520, True, 30); cl = clover(240); c.alpha_composite(cl, (230, 50))
        lab = T("good luck", 80, D_INK, 700); c.alpha_composite(lab, (350 - lab.width // 2, 330))
        put(im, lift(c, True), 540, 1080 + (1 - k) * 60, min(1, k * 1.5))
        footnote(im, "“It's in part for good luck” · the buyer, AP", True)
    else:
        k = spring((t - ti + 0.1) / 0.45); c = card(860, 640, True, 30)
        c.alpha_composite(T("AT THE SUSHI CHAIN", 26, D_MUTE, 700, True), (50, 44)); c.alpha_composite(sushi(300), (50, 110))
        c.alpha_composite(T("Record tuna", 54, D_INK, 700), (390, 130)); c.alpha_composite(pill("usual menu price", 34, VIOLET), (390, 220))
        for i, who in enumerate(("nour", "sami", ("B", VIOLET), ("C", GREEN_APP))):
            kk = spring((t - ti - 0.15 - i * 0.12) / 0.4)
            if kk > 0:
                hd = head(who, 120); c.alpha_composite(hd, (70 + i * 190, int(440 + (1 - kk) * 30)))
        put(im, lift(c, True), 540, 1100 + (1 - k) * 60, min(1, k * 1.5))
        footnote(im, "Served at the usual price · Nippon TV, FOX Business", True)
    return im

def sc_lesson(t):
    im = bg(False); t0 = S("w2"); tl_ = WT("w2", "label."); tw = WT("w2", "wants")
    if t < tw - 0.15:
        k = spring((t - t0 + 0.1) / 0.45); tg = price_tag("fixed price", False, 100, "A LABEL")
        put(im, lift(tg), 540, 1050 + (1 - k) * 60, min(1, k * 1.5))
        if t >= tl_ - 0.05: stamp_at(im, big_stamp("NOT AT AN AUCTION", RED_UI, 64, -8), 540, 1340, t, tl_)
    else:                                                                        # loop back to the opening fish
        k = spring((t - tw + 0.15) / 0.45); put(im, lift(tuna(820)), 540, 920 + (1 - k) * 60, min(1, k * 1.5))
        if t >= tw + 0.15:
            kk = spring((t - tw - 0.15) / 0.45); c = card(720, 200, False, 28); c.alpha_composite(head("nour", 120), (40, 40))
            c.alpha_composite(T("how much", 40, (110, 116, 130), 600), (190, 40)); c.alpha_composite(T("someone wants it", 54, VIOLET, 700), (190, 96))
            put(im, lift(c), 540, 1330 + (1 - kk) * 60, min(1, kk * 1.5))
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

FN = {"hook": sc_hook, "market": sc_market, "bids": sc_bids, "quote": sc_quote, "why": sc_why, "lesson": sc_lesson, "outro": sc_outro}

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
    for i in range(10): s.tick(T_PRICE - 0.2 + i * 0.07, 0.012, 2400)
    s.ding(T_PRICE + 0.5, 1318, 0.03); s.pop(WT("h2", "normal"), 0.04, 650)
    s.pop(WT("s1", "January"), 0.04, 600)
    for i in range(10): s.tick(WT("s2", "243-kilo") - 0.2 + i * 0.08, 0.01, 2200)
    s.pop(WT("b2", "bids"), 0.04, 500)
    tb, tf = WT("b2", "bids"), WT("b2", "¥510 million.")
    for i in range(int((tf - tb) / 0.12)): s.tick(tb + i * 0.12, 0.01, 2000 + i * 25)
    for i in range(5): s.pop(tb + i * 0.42, 0.03, 520 + i * 40)
    s.thud(tf + 0.25, 0.08); s.ding(WT("b3", "boss"), 1175, 0.025)
    s.pop(WT("w1", "good"), 0.04, 700); s.pop(WT("w1", "impress"), 0.04, 600)
    s.thud(WT("w2", "label.") + 0.02, 0.07); s.ding(WT("w2", "wants"), 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson06_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
