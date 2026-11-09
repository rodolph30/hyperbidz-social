"""Auction short 25 (v3, quick, who: Sami): "Your home is full of money". Problem: Sami keeps his old phone in a drawer, just in
case. Reframe: the average American home holds 36 unused items worth $3,675 (eBay's Recommerce Report, via Forbes, 16 Mar 2021);
older iPhones lose about 10% of their resale value in the first month after a new model and 23% after three months (musicMagpie's
2021 depreciation report, via WalesOnline). Fix: put it up for auction now and let buyers compete while it's still worth something.
Takeaway: unused things aren't savings; they lose value every month. Loop: ends back on the 36 / $3,675 card.
Run: python3 tools/lessons/lesson25.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os, math
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson25_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "lofi", 25
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("drawer", True, S("p1") - 0.1, S("r1") - 0.1), ("drop", False, S("r1") - 0.1, S("f1") - 0.1),
      ("fix", True, S("f1") - 0.1, S("tk") - 0.1), ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
BUYERS = (("R", VIOLET), ("M", GREEN_APP), ("J", SILVER))

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def home_card(t, t_items, t_money):
    """one card: 36 unused items, then the $3,675 they're worth"""
    w, h = 860, 560; c = card(w, h, False, 30)
    lab = T("AVERAGE US HOME · UNUSED ITEMS", 26, (110, 116, 130), 700, True); c.alpha_composite(lab, (44, 40))
    n = int(round(roll(t, t_items, 0.8, 0, 36)))
    v = T(str(n), 200, L_INK, 700); c.alpha_composite(v, (44, 90))
    th = T("things", 54, (110, 116, 130), 600); c.alpha_composite(th, (60 + v.width, 90 + v.height - th.height - 14))
    if t >= t_money - 0.35:
        m = roll(t, t_money - 0.35, 0.9, 0, 3675); km = spring((t - t_money + 0.35) / 0.4)
        mv = fade_in(T("worth " + money(m), 100, GREEN_UI, 700), km); c.alpha_composite(mv, (44, int(370 + (1 - km) * 20)))
    return c

def sc_hook(t):
    im = bg(False); ti = -0.9; tm = WT("h1", "$3,675"); tsd = WT("h2", "drawer"); tsh = WT("h2", "shrinking.")
    c = home_card(t, ti, tm); put(im, lift(c), 540, 960, 1, 1.0 + 0.04 * (1 - spring(t / 0.45)))
    if t >= tm + 0.6: select_box(im, (130, 1040, 950, 1165), eout((t - tm - 0.6) / 0.3), 1, VIOLET)
    if t >= tsd - 0.15:
        ks = spring((t - tsd + 0.15) / 0.4); put(im, head("sami", 140), 540, 1420 + (1 - ks) * 30, min(1, ks * 1.5))
    if t >= tsh - 0.2:
        kq = spring((t - tsh + 0.2) / 0.4); put(im, pill("Shrinking every month", 46, VIOLET, padx=32, pady=14), 540, 1600 + (1 - kq) * 20, min(1, kq * 1.5))
    footnote(im, "Source: eBay Recommerce Report 2021, via Forbes", False, 1850)
    return im

def phone_icon(w=170, h=300, col=BLUE):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=(24, 26, 32, 255))
    d.rounded_rectangle((10, 10, w - 11, h - 11), radius=22, fill=col + (255,))
    d.rounded_rectangle((w / 2 - 30, 20, w / 2 + 30, 34), radius=7, fill=(24, 26, 32, 255))
    return im

def sc_drawer(t):
    im = bg(True); t0 = S("p1"); tj = WT("p1", "just")
    w, h = 820, 620; dr = card(w, h, True, 28, fill=(30, 36, 52))
    d = ImageDraw.Draw(dr); d.rounded_rectangle((w / 2 - 110, 36, w / 2 + 110, 66), radius=15, fill=(70, 78, 98, 255))  # handle
    d.rounded_rectangle((40, 110, w - 40, h - 40), radius=20, fill=(20, 24, 36, 255))
    ph = phone_icon().rotate(-78, expand=True, resample=Image.BICUBIC); dr.alpha_composite(ph, (int(w / 2 - ph.width / 2), int(h / 2 + 20 - ph.height / 2)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(dr, True), 540, 1080, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    ks = spring((t - t0 - 0.2) / 0.4)
    if ks > 0: put(im, head("sami", 130), 540, 680 + (1 - ks) * 30, min(1, ks * 1.5))
    if t >= tj - 0.15:
        kk = spring((t - tj + 0.15) / 0.4); put(im, pill("Just in case", 50, VIOLET, padx=34, pady=16), 540, 1500 + (1 - kk) * 20, min(1, kk * 1.5))
    footnote(im, "Sami's drawer is illustrative", True, 1850)
    return im

def sc_drop(t):
    im = bg(False); t0 = S("r1"); t10 = WT("r1", "10%"); t23 = WT("r2", "23%")
    w, h = 860, 640; c = card(w, h, False, 30)
    c.alpha_composite(T("OLDER IPHONE · RESALE VALUE", 26, (110, 116, 130), 700, True), (44, 40))
    # value bar shrinking: 100% -> 90% -> 77%
    frac = 1.0
    if t >= t10 - 0.2: frac = roll(t, t10 - 0.2, 0.7, 1.0, 0.90)
    if t >= t23 - 0.2: frac = roll(t, t23 - 0.2, 0.7, 0.90, 0.77)
    bx0, by0, bw, bh = 44, 120, w - 88, 90; d = ImageDraw.Draw(c)
    d.rounded_rectangle((bx0, by0, bx0 + bw, by0 + bh), radius=20, fill=(236, 238, 246, 255))
    d.rounded_rectangle((bx0, by0, bx0 + bw * frac, by0 + bh), radius=20, fill=BLUE + (255,))
    # big drop number
    if t >= t10 - 0.2:
        pct = roll(t, t10 - 0.2, 0.6, 0, 10)
        if t >= t23 - 0.2: pct = roll(t, t23 - 0.2, 0.6, 10, 23)
        v = T(f"−{int(round(pct))}%", 220, RED_UI, 700); c.alpha_composite(v, (44, 260))
        when = "after 3 months" if t >= t23 - 0.2 else "first month after a new model"
        c.alpha_composite(T(when, 44, (110, 116, 130), 600), (50, 270 + v.height + 20))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1060, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= t23 + 0.3: select_box(im, (150, 1000, 700, 1235), eout((t - t23 - 0.3) / 0.3), 1, VIOLET)
    footnote(im, "Source: musicMagpie 2021 depreciation report, via WalesOnline", False, 1850)
    return im

def sc_fix(t):
    im = bg(True); t0 = S("f1"); tc = WT("f1", "compete"); tw = WT("f1", "worth")
    w, h = 880, 1000; c = window(w, h, "Live auction · Old phone", True)
    rows = [(BUYERS[0], "$120"), (BUYERS[1], "$135"), (BUYERS[2], "$150"), (("N", LILAC), "$165")]
    y = 110; t1 = S("f1") + 0.15
    for j, (who, amt) in enumerate(rows):
        kj = spring((t - t1 - j * 0.32) / 0.35)
        if kj <= 0: continue
        r = card(780, 150, True, 26, fill=(30, 36, 52)); r.alpha_composite(head(who, 100), (26, 25))
        r.alpha_composite(T(f"Bidder {j + 1}", 40, D_INK, 700), (150, 30)); r.alpha_composite(T("bid", 28, D_MUTE, 600), (150, 82))
        a = T(amt, 60, GREEN_UI if j == 3 else D_INK, 700); r.alpha_composite(a, (780 - 40 - a.width, 40))
        c.alpha_composite(fade_in(r, kj), (50, int(y + (1 - kj) * 30))); y += 175
    if t >= tw - 0.2:
        kp = spring((t - tw + 0.2) / 0.4); pp = fade_in(pill("Sold while it's worth something", 40, VIOLET, padx=30, pady=16), kp)
        c.alpha_composite(pp, (int(w / 2 - pp.width / 2), int(850 + (1 - kp) * 20)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Example auction · bidders and bids illustrative", True, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; ts = WT("tk", "savings."); tl = WT("tk", "lose")
    c = home_card(t, -5, -5); put(im, lift(c), 540, 960, ease((t - t0) / 0.25), 0.97 + 0.03 * spring((t - t0) / 0.5))
    if t >= ts - 0.15:
        kk = spring((t - ts + 0.15) / 0.4); put(im, pill("Not savings", 50, L_INK, padx=34, pady=16), 540, 1380 + (1 - kk) * 20, min(1, kk * 1.5))
    if t >= tl - 0.15:
        kk = spring((t - tl + 0.15) / 0.4); put(im, pill("Losing value every month", 46, VIOLET, padx=32, pady=14), 540, 1540 + (1 - kk) * 20, min(1, kk * 1.5))
    footnote(im, "Source: eBay Recommerce Report 2021, via Forbes", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 25, BLUE), (540, 7, VIOLET), (750, 14, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "drawer": sc_drawer, "drop": sc_drop, "fix": sc_fix, "loop": sc_loop, "outro": sc_outro}

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
    for j in range(2): s.tick(0.05 + j * 0.11, 0.025)
    tm = WT("h1", "$3,675")
    for j in range(8): s.tick(tm - 0.35 + j * 0.11, 0.025)
    s.ding(tm + 0.55, 1568, 0.03)
    s.pop(WT("h2", "drawer") - 0.15, 0.035, 600); s.pop(WT("h2", "shrinking.") - 0.2, 0.035, 520)
    s.pop(S("p1"), 0.03, 600); s.pop(WT("p1", "just") - 0.15, 0.035, 640)
    t10 = WT("r1", "10%"); t23 = WT("r2", "23%")
    for j in range(5): s.tick(t10 - 0.2 + j * 0.11, 0.025)
    s.thud(t10 + 0.3, 0.06)
    for j in range(5): s.tick(t23 - 0.2 + j * 0.11, 0.025)
    s.thud(t23 + 0.3, 0.07)
    tc = WT("f1", "compete")
    for j in range(4): s.pop(S("f1") + 0.15 + j * 0.32, 0.03, 560 + j * 40)
    s.ding(WT("f1", "worth") - 0.2, 1318, 0.03)
    s.pop(WT("tk", "savings.") - 0.15, 0.035, 600); s.ding(WT("tk", "lose") - 0.15, 1175, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson25_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
