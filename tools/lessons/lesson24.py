"""Auction short 24 (v3, quick, who: Sami): "Your best buyer doesn't live on your street". Problem: Sami's post only reaches people
nearby, so his price is whatever his street will pay. Reframe: in 2024, 81% of bids at Christie's were placed online (Christie's,
17 Dec 2024); Lebanon's Ministry of Economy and Trade estimates 12 million people of Lebanese origin around the world. Fix: live
online bidding lets buyers from anywhere compete. Takeaway: your best buyer might be in Sydney. Loop: ends back on the 81% card.
Run: python3 tools/lessons/lesson24.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os, math
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson24_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "pluck", 24
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("street", True, S("p1") - 0.1, S("r1") - 0.1), ("world", False, S("r1") - 0.1, S("f1") - 0.1),
      ("fix", True, S("f1") - 0.1, S("tk") - 0.1), ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
BUYERS = (("R", VIOLET), ("M", GREEN_APP), ("J", SILVER))

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def stat81(t, t_roll=None, dark=False):
    return stat("Christie's · 2024 · all bids", "81%", "placed online", 860, dark, 220, BLUE)

def sc_hook(t):
    im = bg(False); t_roll = 0.0; to = WT("h1", "online."); tr = WT("h2", "room."); tp = WT("h2", "problem.")
    c = stat81(t, t_roll); put(im, lift(c), 540, 980, 1, 1.0 + 0.04 * (1 - spring(t / 0.45)))
    if t >= to - 0.1: select_box(im, (110, 1110, 640, 1180), eout((t - to + 0.1) / 0.3), 1, VIOLET)
    if t >= tr - 0.3:
        kq = spring((t - tr + 0.3) / 0.4); put(im, pill("Not in the room", 48, L_INK, padx=34, pady=14), 540, 1340 + (1 - kq) * 20, min(1, kq * 1.5))
    if t >= tp - 0.15:
        ks = spring((t - tp + 0.15) / 0.4); put(im, head("sami", 150), 540, 1560 + (1 - ks) * 30, min(1, ks * 1.5))
    footnote(im, "Source: Christie's, 17 Dec 2024", False, 1850)
    return im

def guitar(w=300, h=300):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = w * 0.42, h * 0.62
    d.ellipse((cx - 85, cy - 20, cx + 85, cy + 110), fill=VIOLET + (255,)); d.ellipse((cx - 65, cy - 95, cx + 65, cy + 20), fill=VIOLET + (255,))
    d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=(22, 26, 38, 255))
    d.line([(cx, cy), (w * 0.9, h * 0.08)], fill=LILAC + (255,), width=22)
    d.rounded_rectangle((w * 0.86, h * 0.0, w * 0.98, h * 0.14), radius=6, fill=LILAC + (255,))
    return im.rotate(-12, expand=False, resample=Image.BICUBIC)

def sc_street(t):
    im = bg(True); t0 = S("p1"); tn = WT("p1", "nearby"); ts = WT("p2", "street")
    pw, ph = 680, 1080; p = phone(pw, ph, True)
    p.alpha_composite(T("For sale", 36, D_MUTE, 700), (50, 110))
    th = Image.new("RGBA", (pw - 100, 380), (0, 0, 0, 0)); ImageDraw.Draw(th).rounded_rectangle((0, 0, pw - 101, 379), radius=24, fill=(30, 36, 52, 255))
    g = guitar(); th.alpha_composite(g, (int((pw - 100) / 2 - 150), 40)); p.alpha_composite(th, (50, 170))
    p.alpha_composite(T("Guitar", 54, D_INK, 700), (50, 580)); p.alpha_composite(head("sami", 80), (pw - 140, 572))
    # who saw it: a small radius, a few dots
    p.alpha_composite(T("Seen by", 36, D_MUTE, 600), (50, 700))
    if t >= tn - 0.15:
        kn = spring((t - tn + 0.15) / 0.4)
        ring = Image.new("RGBA", (pw - 100, 240), (0, 0, 0, 0)); d = ImageDraw.Draw(ring); cx, cy = (pw - 100) / 2, 120
        r = 40 + 70 * eout(kn); d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=LILAC + (200,), width=4)
        for a, rr in ((0.3, 50), (2.1, 70), (3.9, 40), (5.0, 85)):
            x, y = cx + rr * math.cos(a) * eout(kn), cy + rr * math.sin(a) * eout(kn) * 0.9
            d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=GREEN_APP + (255,))
        d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=BLUE + (255,))
        p.alpha_composite(fade_in(ring, kn), (50, 760))
        pc = fade_in(chip("Nearby only", True, 26), kn); p.alpha_composite(pc, (pw - 50 - pc.width, 700))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(p, True), 540, 1140, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= ts - 0.15:
        kk = spring((t - ts + 0.15) / 0.4); put(im, pill("Price = what one street will pay", 42, VIOLET, padx=30, pady=14), 540, 1730 + (1 - kk) * 20, min(1, kk * 1.5))
    footnote(im, "Sami's listing is illustrative", True, 1850)
    return im

DOTS = [(math.cos(i * 2.399) * (0.25 + 0.75 * ((i * 37) % 100) / 100), math.sin(i * 2.399) * (0.25 + 0.75 * ((i * 53) % 100) / 100)) for i in range(70)]

def sc_world(t):
    im = bg(False); t0 = S("r1"); tm = WT("r1", "12 million"); tw = WT("r1", "world.")
    # a simple globe of dots, filling as the number rolls
    gl = Image.new("RGBA", (720, 720), (0, 0, 0, 0)); d = ImageDraw.Draw(gl); R = 340
    d.ellipse((20, 20, 700, 700), fill=(236, 238, 246, 255), outline=(206, 210, 222, 255), width=3)
    for yy in (-0.5, 0, 0.5):
        hh = R * math.sqrt(1 - yy * yy); d.line([(360 - hh, 360 + yy * R), (360 + hh, 360 + yy * R)], fill=(214, 218, 230, 255), width=2)
    d.ellipse((360 - R * 0.45, 20, 360 + R * 0.45, 700), outline=(214, 218, 230, 255), width=2)
    nshow = int(len(DOTS) * clamp((t - tm + 0.4) / 1.4))
    for i, (x, y) in enumerate(DOTS[:nshow]):
        px, py = 360 + x * R * 0.9, 360 + y * R * 0.9; col = (BLUE, VIOLET, GREEN_APP, LILAC)[i % 4]
        d.ellipse((px - 9, py - 9, px + 9, py + 9), fill=col + (255,))
    k = ease((t - t0 + 0.12) / 0.25); put(im, gl, 540, 1000, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tm - 0.4:
        v = roll(t, tm - 0.4, 0.9, 0, 12); km = spring((t - tm + 0.4) / 0.4)
        c = stat("People of Lebanese origin worldwide", f"{int(round(v))} million", "estimate", 820, False, 120, VIOLET)
        put(im, lift(c), 540, 1615 + (1 - km) * 30, min(1, km * 1.5))
    if t >= tw - 0.1: select_box(im, (210, 670, 870, 1330), eout((t - tw + 0.1) / 0.3), 1, GREEN_UI)
    footnote(im, "Source: Lebanon's Ministry of Economy and Trade (estimate)", False, 1850)
    return im

def sc_fix(t):
    im = bg(True); t0 = S("f1"); ta = WT("f1", "anywhere"); tc = WT("f1", "compete")
    w, h = 880, 1000; c = window(w, h, "Live auction · Guitar", True)
    rows = [(BUYERS[0], "Beirut", "$300"), (BUYERS[1], "Paris", "$340"), (BUYERS[2], "Dubai", "$380"), (("S", GREEN_UI), "Sydney", "$420")]
    y = 110; t1 = S("f1") + 0.2
    for j, (who, place, amt) in enumerate(rows):
        kj = spring((t - t1 - j * 0.38) / 0.35)
        if kj <= 0: continue
        r = card(780, 150, True, 26, fill=(30, 36, 52)); r.alpha_composite(head(who, 100), (26, 25))
        r.alpha_composite(T(place, 40, D_INK, 700), (150, 30)); r.alpha_composite(T("bid", 28, D_MUTE, 600), (150, 82))
        a = T(amt, 60, GREEN_UI if j == 3 else D_INK, 700); r.alpha_composite(a, (780 - 40 - a.width, 40))
        c.alpha_composite(fade_in(r, kj), (50, int(y + (1 - kj) * 30))); y += 175
    if t >= tc - 0.15:
        kp = spring((t - tc + 0.15) / 0.4); pp = fade_in(pill("Buyers from anywhere", 44, VIOLET, padx=32, pady=16), kp)
        c.alpha_composite(pp, (int(w / 2 - pp.width / 2), int(850 + (1 - kp) * 20)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Example auction · bidders, places and bids illustrative", True, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tsy = WT("tk", "Sydney.")
    c = stat81(t, t0 - 1); put(im, lift(c), 540, 980, ease((t - t0) / 0.25), 0.97 + 0.03 * spring((t - t0) / 0.5))
    if t >= tsy - 0.15:
        ks = spring((t - tsy + 0.15) / 0.4)
        put(im, head(("S", GREEN_UI), 140), 380, 1420 + (1 - ks) * 30, min(1, ks * 1.5))
        put(im, pill("Top bid · Sydney", 50, GREEN_UI, padx=34, pady=16), 640, 1420 + (1 - ks) * 30, min(1, ks * 1.5))
    footnote(im, "Source: Christie's, 17 Dec 2024 · bidder illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 24, BLUE), (540, 8, VIOLET), (750, 12, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "street": sc_street, "world": sc_world, "fix": sc_fix, "loop": sc_loop, "outro": sc_outro}

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
    s.thud(0.05, 0.08); s.ding(0.1, 1318, 0.03); s.ding(WT("h1", "online.") - 0.1, 1175, 0.025)
    s.pop(WT("h2", "room.") - 0.3, 0.035, 560); s.pop(WT("h2", "problem.") - 0.15, 0.035, 640)
    s.pop(S("p1"), 0.03, 600); s.ding(WT("p1", "nearby") - 0.15, 1175, 0.025); s.pop(WT("p2", "street") - 0.15, 0.035, 620)
    tm = WT("r1", "12 million")
    for j in range(8): s.tick(tm - 0.4 + j * 0.11, 0.025)
    s.pop(tm - 0.4, 0.035, 600); s.ding(tm + 0.5, 1318, 0.03); s.ding(WT("r1", "world.") - 0.1, 1568, 0.025)
    for j in range(4): s.pop(S("f1") + 0.2 + j * 0.38, 0.03, 560 + j * 40)
    s.ding(WT("f1", "compete") - 0.15, 1318, 0.03)
    s.ding(S("tk") + 0.2, 1175, 0.025); s.pop(WT("tk", "Sydney.") - 0.15, 0.035, 640); s.ding(WT("tk", "Sydney."), 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson24_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
