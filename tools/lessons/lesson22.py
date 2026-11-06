"""Auction short 22 (v3, quick, who: Sami): "£45, then $450 million". Problem: Sami prices things by guessing, and a guess can
give away a fortune. Reframe (one story): the same painting sold for £45 in 1958 (mistaken for a copy) and for $450,312,500 at
Christie's in 2017, after 19 minutes and at least 45 bids (Christie's). Fix: nobody set that price, the bidders found it.
Takeaway: your price isn't what you ask, it's what people compete for. Let them bid. Loop: ends on the frame the video opens on.
Never draw the painting or any face: a covered frame, price tags and a clock.
Run: python3 tools/lessons/lesson22.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson22_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "marimba", 22
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("guess", True, S("p1") - 0.1, S("r1") - 0.1), ("y1958", False, S("r1") - 0.1, S("r2") - 0.1),
      ("y2017", True, S("r2") - 0.1, S("f1") - 0.1), ("found", False, S("f1") - 0.1, S("tk") - 0.1),
      ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
BUYERS = (("R", VIOLET), ("M", GREEN_APP), ("J", SILVER))

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def frame_prop(w=560, h=700):
    """an ornate-looking frame with a covered canvas (the painting is never shown)"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=18, fill=VIOLET + (255,))
    d.rounded_rectangle((22, 22, w - 23, h - 23), radius=12, fill=LILAC + (255,))
    d.rectangle((44, 44, w - 45, h - 45), fill=(22, 26, 38, 255))
    # draped cloth folds
    for i in range(5):
        x = 70 + i * (w - 140) / 4
        d.line([(x, 52), (x + (i - 2) * 18, h - 52)], fill=(40, 46, 64, 255), width=10)
    q = T("?", 200, (90, 98, 122), 700); im.alpha_composite(q, (int(w / 2 - q.width / 2), int(h / 2 - q.height / 2 - 10)))
    return im

def tag(text, size=64, fill=(255, 255, 255), col=L_INK):
    tt = T(text, size, col, 700); w, h = tt.width + 110, tt.height + 44
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(40, 0), (w - 1, 0), (w - 1, h - 1), (40, h - 1), (0, h / 2)], fill=fill + (255,))
    d.ellipse((20, h / 2 - 9, 38, h / 2 + 9), fill=STAGE + (255,)); im.alpha_composite(tt, (68, 22)); return im

def frame_scene(t, im, t_big=None, struck=True, t_strike=None):
    """the frame with the £45 tag; from t_big, the $450 million tag lands and £45 is struck. Shared by the hook and the loop."""
    put(im, lift(frame_prop()), 540, 1050, 1, 0.97 + 0.03 * spring(t / 0.5))
    small = tag("£45", 70); put(im, lift(small), 300, 1440)
    put(im, chip("1958", False, 26), 300, 1530)
    if t_strike is not None and t >= t_strike: strike(im, 220, 1440, 395, eout((t - t_strike) / 0.25), RED_UI, 10)
    if t_big is not None and t >= t_big:
        kb = spring((t - t_big) / 0.4); big = tag("$450 million", 70, GREEN_UI, (255, 255, 255))
        put(im, lift(big), 720, 1440 + (1 - kb) * 30, min(1, kb * 1.5))
        put(im, chip("2017", False, 26), 720, 1530, min(1, kb * 1.5))

def sc_hook(t):
    im = bg(False); tb = WT("h2", "$450 million.") - 0.1; tp = WT("h3", "price?")
    frame_scene(t, im, tb, t_strike=tb + 0.2)
    if t >= tp - 0.1:
        kq = spring((t - tp + 0.1) / 0.4); put(im, pill("Who set the price?", 48, L_INK, padx=34, pady=14), 540, 1690 + (1 - kq) * 20, min(1, kq * 1.5))
    footnote(im, "The painting is not shown", False, 1850)
    return im

def sc_guess(t):
    im = bg(True); t0 = S("p1"); tg = WT("p1", "guessing."); tf = WT("p1", "fortune.")
    pw, ph = 680, 1120; p = phone(pw, ph, True)
    p.alpha_composite(T("For sale", 36, D_MUTE, 700), (50, 110))
    th = Image.new("RGBA", (pw - 100, 420), (0, 0, 0, 0)); ImageDraw.Draw(th).rounded_rectangle((0, 0, pw - 101, 419), radius=24, fill=(30, 36, 52, 255))
    fr = frame_prop(260, 330); th.alpha_composite(fr, (int((pw - 100) / 2 - 130), 45)); p.alpha_composite(th, (50, 170))
    p.alpha_composite(T("Old painting", 50, D_INK, 700), (50, 620))
    p.alpha_composite(head("sami", 80), (pw - 140, 610))
    guesses = ["$30?", "$50?", "$80?"]
    gi = 0 if t < tg - 0.1 else min(2, int((t - tg + 0.1) / 0.35))
    p.alpha_composite(T("Price", 40, D_MUTE, 600), (50, 740))
    g = T(guesses[gi], 64, D_INK, 700); p.alpha_composite(g, (pw - 50 - g.width, 726))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(p, True), 540, 1130, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tg - 0.1:
        kk = spring((t - tg + 0.1) / 0.4); put(im, pill("Just a guess", 44, VIOLET, padx=30, pady=14), 540, 560 + (1 - kk) * 20, min(1, kk * 1.5))
    if t >= tf - 0.1:
        select_box(im, (600, 1275, 900, 1385), eout((t - tf + 0.1) / 0.3), 1, RED_UI)
    footnote(im, "Sami's listing and prices are illustrative", True, 1850)
    return im

def sc_y1958(t):
    im = bg(False); t0 = S("r1"); tc = WT("r1", "copy,"); tp = WT("r1", "£45.")
    vs = "£45" if t >= tp - 0.1 else "£ ?"
    c = stat("1958 · sold at auction", vs, "", 860, False, 200, L_INK)
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1040, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tc - 0.2:
        kc = spring((t - tc + 0.2) / 0.4); put(im, pill("Mistaken for a copy", 46, VIOLET, padx=30, pady=14), 540, 1330 + (1 - kc) * 20, min(1, kc * 1.5))
    footnote(im, "Source: Christie's", False, 1850)
    return im

def sc_y2017(t):
    im = bg(True); t0 = S("r2"); tm = WT("r2", "19"); tb = WT("r2", "45"); tf = WT("r3", "$450.3 million.")
    w, h = 900, 980; c = window(w, h, "New York · 2017", True)
    # clock + bids row
    mins = roll(t, tm - 0.4, 0.8, 0, 19); clk = card(380, 170, True, 24, fill=(30, 36, 52))
    clk.alpha_composite(T("BIDDING", 24, D_MUTE, 700, True), (30, 24)); clk.alpha_composite(T(f"{int(mins)} min", 60, D_INK, 700), (30, 70))
    nb = int(roll(t, tb - 0.4, 0.8, 0, 45)); bd = card(380, 170, True, 24, fill=(30, 36, 52))
    bd.alpha_composite(T("BIDS", 24, D_MUTE, 700, True), (30, 24)); bd.alpha_composite(T(f"{nb}+" if nb >= 45 else f"{nb}", 60, D_INK, 700), (30, 70))
    km = clamp((t - tm + 0.4) / 0.25); kb2 = clamp((t - tb + 0.4) / 0.25)
    if km > 0: c.alpha_composite(fade_in(clk, km), (50, 110))
    if kb2 > 0: c.alpha_composite(fade_in(bd, kb2), (w - 50 - 380, 110))
    # price rolls from the $75M opening bid to the hammer
    c.alpha_composite(T("CURRENT BID", 28, D_MUTE, 700, True), (60, 360))
    t_roll = S("r2") + 0.3
    if t < tf - 0.1:
        v = roll(t, t_roll, (tf - 0.1) - t_roll, 75_000_000, 400_000_000)
    else:
        v = roll(t, tf - 0.1, 0.6, 400_000_000, 450_312_500)
    vt = T(money(v), 104, GREEN_UI if t >= tf + 0.4 else D_INK, 700); c.alpha_composite(vt, (int(w / 2 - vt.width / 2), 420))
    c.alpha_composite(T("Opened at $75 million", 30, D_MUTE, 500), (60, 580))
    if t >= tf - 0.1:
        kp = spring((t - tf + 0.1) / 0.4); pp = fade_in(pill("Same painting as the £45 one", 36, VIOLET, padx=28, pady=12), kp)
        c.alpha_composite(pp, (int(w / 2 - pp.width / 2), int(700 + (1 - kp) * 20)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    stamp_at(im, big_stamp("SOLD", GREEN_UI, 110, -7), 540, 1700, t, tf + 0.6)
    footnote(im, "Source: Christie's, 15 Nov 2017 · price includes fees", True, 1850)
    return im

def sc_found(t):
    im = bg(False); t0 = S("f1"); tn = WT("f1", "Nobody"); tb = WT("f1", "bidders")
    sp = tag("Set price", 64); put(im, lift(sp), 540, 760, ease((t - t0 + 0.12) / 0.25))
    if t >= tn: strike(im, 400, 760, 700, eout((t - tn) / 0.3), RED_UI, 12)
    for i, (x, n, who) in enumerate(((290, 12, BUYERS[0]), (540, 9, BUYERS[1]), (790, 7, BUYERS[2]))):
        kk = spring((t - tb + 0.25 - i * 0.12) / 0.45)
        if kk > 0:
            put(im, paddle(n, who[1], 120), x, 1150 + (1 - kk) * 60, min(1, kk * 1.5))
            put(im, head(who, 120), x, 1390 + (1 - kk) * 60, min(1, kk * 1.5))
    tfd = WT("f1", "found")
    if t >= tfd - 0.1:
        kp = spring((t - tfd + 0.1) / 0.4); put(im, pill("The bidders found it", 50, GREEN_UI, padx=34, pady=16), 540, 1620 + (1 - kp) * 20, min(1, kp * 1.5))
    footnote(im, "Bidders are illustrative", False, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tl_ = WT("tk", "Let")
    frame_scene(t, im, t0 + 0.4, t_strike=t0 + 0.6)
    tc = WT("tk", "compete")
    if t >= tc - 0.1: select_box(im, (478, 1368, 962, 1512), eout((t - tc + 0.1) / 0.3), 1, GREEN_UI)
    if t >= tl_ - 0.1:
        kq = spring((t - tl_ + 0.1) / 0.4); put(im, pill("Let them bid.", 56, VIOLET, padx=38, pady=16), 540, 1690 + (1 - kq) * 20, min(1, kq * 1.5))
    footnote(im, "The painting is not shown", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 17, BLUE), (540, 1, VIOLET), (750, 7, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "guess": sc_guess, "y1958": sc_y1958, "y2017": sc_y2017, "found": sc_found, "loop": sc_loop, "outro": sc_outro}

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
    s.pop(WT("h1", "same") - 0.1, 0.035, 600); tb = WT("h2", "$450 million.") - 0.1
    s.ding(tb, 1318, 0.03); s.tick(tb + 0.2, 0.03); s.pop(WT("h3", "price?") - 0.1, 0.035, 560)
    tg = WT("p1", "guessing.")
    for j in range(3): s.tick(tg - 0.1 + j * 0.35, 0.03)
    s.pop(tg - 0.1, 0.03, 600); s.ding(WT("p1", "fortune.") - 0.1, 1175, 0.025)
    s.pop(WT("r1", "copy,") - 0.2, 0.035, 560); s.ding(WT("r1", "£45.") - 0.1, 1318, 0.03); s.pop(WT("r1", "£45.") - 0.1, 0.03, 640)
    for j in range(5): s.tick(WT("r2", "19") - 0.4 + j * 0.15, 0.025)
    for j in range(5): s.tick(WT("r2", "45") - 0.4 + j * 0.15, 0.025)
    tf = WT("r3", "$450.3 million.")
    for j in range(6): s.tick(tf - 0.1 + j * 0.1, 0.025)
    s.thud(tf + 0.6, 0.09); s.ding(tf + 0.65, 1568, 0.03)
    s.tick(WT("f1", "Nobody"), 0.03)
    for j in range(3): s.pop(WT("f1", "bidders") - 0.25 + j * 0.12, 0.03, 560 + j * 40)
    s.ding(WT("f1", "found") - 0.1, 1318, 0.03)
    s.ding(S("tk") + 0.3, 1175, 0.025); s.pop(WT("tk", "Let") - 0.1, 0.035, 640); s.ding(WT("tk", "Let"), 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson22_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
