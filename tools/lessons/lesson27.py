"""Auction short 27 (v3, quick, who: perspective, Lebanon): "From the crier to the clock". Lebanese law still lets a court officer
call in "the municipality's crier" to auction seized goods (CCP Art. 930), and a property auction is announced in two daily
newspapers, the Official Gazette and on the municipality's door at least ten days ahead (Arts. 970-971). The crier's job was always
to make the sale public, because a price is only fair when everyone can bid. Online, that job is a countdown everyone can watch.
Takeaway: "An auction is only as fair as it is public." Loop: ends on the crier's megaphone from frame 1. Neutral: no criticism.
Run: python3 tools/lessons/lesson27.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os, math
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson27_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "marimba", 27
XF = 0.16
SC = [("hook", True, 0.0, S("c1") - 0.1), ("law", False, S("c1") - 0.1, S("c2") - 0.1), ("notice", True, S("c2") - 0.1, S("r1") - 0.1),
      ("why", False, S("r1") - 0.1, S("f1") - 0.1), ("clock", True, S("f1") - 0.1, S("tk") - 0.1), ("loop", True, S("tk") - 0.1, S("e2") - 0.15),
      ("outro", False, S("e2") - 0.15, TOTAL)]
MUTE_L = (110, 116, 130)
LAW_NOTE = "Source: Lebanese Code of Civil Procedure, Arts. 930, 970-971"

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def megaphone(s=420, col=BLUE, waves=0.0):
    """a plain megaphone with sound arcs; waves 0..1 animates the arcs outward"""
    im = Image.new("RGBA", (int(s * 1.6), s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cy = s / 2
    d.rounded_rectangle((s * 0.05, cy - s * 0.12, s * 0.30, cy + s * 0.12), radius=int(s * 0.05), fill=(200, 205, 225, 255))
    d.polygon([(s * 0.28, cy - s * 0.14), (s * 0.95, cy - s * 0.40), (s * 0.95, cy + s * 0.40), (s * 0.28, cy + s * 0.14)], fill=col + (255,))
    d.rounded_rectangle((s * 0.90, cy - s * 0.42, s * 1.0, cy + s * 0.42), radius=int(s * 0.04), fill=tuple(min(255, c + 50) for c in col) + (255,))
    d.rounded_rectangle((s * 0.30, cy + s * 0.10, s * 0.40, cy + s * 0.34), radius=int(s * 0.03), fill=(200, 205, 225, 255))
    for i in range(3):
        ph = (waves + i / 3) % 1.0; r = s * (0.18 + 0.32 * ph); a = int(230 * (1 - ph)) if waves > 0 else 160
        cx = s * 1.02
        d.arc((cx - r, cy - r, cx + r, cy + r), -40, 40, fill=LILAC + (a,), width=int(s * 0.035))
    return im

def icon_paper(s=120, gazette=False):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, s - 8, s - 8), radius=12, fill=((236, 238, 246) if not gazette else (233, 227, 255)) + (255,))
    d.rectangle((22, 22, s - 22, 44), fill=(VIOLET if gazette else L_INK) + (255,))
    for j in range(4): d.rectangle((22, 56 + j * 14, s - 22 - (30 if j == 3 else 0), 62 + j * 14), fill=(170, 175, 190, 255))
    return im

def icon_door(s=120):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((26, 8, s - 26, s - 6), radius=10, fill=BLUE + (255,))
    d.rectangle((40, 30, s - 40, 62), fill=(255, 255, 255, 255))   # the posted notice
    for j in range(3): d.rectangle((46, 36 + j * 8, s - 46, 39 + j * 8), fill=(150, 155, 170, 255))
    d.ellipse((s - 46, 74, s - 36, 84), fill=(255, 255, 255, 255))
    return im

def sc_hook(t):
    im = bg(True); tc = WT("h1", "crier"); ta = WT("h2", "auction.")
    m = megaphone(420, BLUE, (t * 0.9) % 1.0 + 0.001); k0 = spring(t / 0.45)
    put(im, pill("Lebanese law, Art. 930", 44, (40, 46, 60), D_INK, padx=30, pady=12), 540, 640, 1)
    put(im, m, 600, 940, 1, 1.0 + 0.06 * (1 - k0))
    if t >= tc - 0.25:
        kc = spring((t - tc + 0.25) / 0.4); put(im, pill("THE CRIER", 54, (54, 42, 108), LILAC, padx=34, pady=14), 540, 1250 + (1 - kc) * 20, min(1, kc * 1.5))
    if t >= ta - 0.3:
        kq = spring((t - ta + 0.3) / 0.4); put(im, pill("…the secret of every fair auction", 46, VIOLET, padx=32, pady=14), 540, 1430 + (1 - kq) * 20, min(1, kq * 1.5))
    footnote(im, "Source: Lebanese Code of Civil Procedure, Art. 930", True, 1850)
    return im

def sc_law(t):
    im = bg(False); t0 = S("c1"); tm = WT("c1", "municipality's")
    w, h = 880, 640; c = window(w, h, "Code of Civil Procedure · Art. 930", False)
    c.alpha_composite(T("SALE OF SEIZED GOODS", 26, MUTE_L, 700, True), (50, 110))
    c.alpha_composite(T("The court officer runs", 50, L_INK, 600), (50, 170))
    c.alpha_composite(T("the bidding, and may call in", 50, L_INK, 600), (50, 236))
    if t >= tm - 0.3:
        kq = spring((t - tm + 0.3) / 0.4)
        q = T("“the municipality’s crier”", 62, VIOLET, 700); c.alpha_composite(fade_in(q, kq), (50, int(350 + (1 - kq) * 16)))
        sb = Image.new("RGBA", (w, h), (0, 0, 0, 0)); select_box(sb, (40, 342, 60 + q.width, 350 + q.height + 14), eout((t - tm + 0.1) / 0.3), 1, VIOLET); c.alpha_composite(sb)
    c.alpha_composite(T("…or another crier he picks.", 40, MUTE_L, 500), (50, 500))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1040, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Source: Lebanese Code of Civil Procedure, Art. 930 (translated)", False, 1850)
    return im

def sc_notice(t):
    im = bg(True); t0 = S("c2"); t10 = WT("c3", "ten")
    rows = [(icon_paper(110), "2 daily newspapers", WT("c2", "notice")), (icon_paper(110, True), "The Official Gazette", WT("c2", "Official")),
            (icon_door(110), "The municipality's door", WT("c2", "municipality's"))]
    if t < t10 - 0.3:
        for j, (ic, txt, tw) in enumerate(rows):
            kj = spring((t - tw + 0.3) / 0.4)
            if kj <= 0: continue
            r = card(880, 190, True, 30, fill=(30, 36, 52)); r.alpha_composite(ic, (40, 40))
            tt = T(txt, 56, D_INK, 700); r.alpha_composite(tt, (190, 95 - tt.height // 2 - 4))
            put(im, lift(fade_in(r, kj), True), 540, 760 + j * 250 + (1 - kj) * 30)
        put(im, chip("A property auction is announced in", True, 30), 540, 560, ease((t - t0) / 0.3))
    else:
        k = spring((t - t10 + 0.3) / 0.45); n = int(round(roll(t, t10 - 0.3, 0.6, 0, 10)))
        s = stat("Announced at least", f"{n} days", "before the auction", 860, True, 200, LILAC); put(im, lift(s, True), 540, 1020 + (1 - k) * 30, min(1, k * 1.5))
    footnote(im, "Source: Lebanese Code of Civil Procedure, Arts. 970-971", True, 1850)
    return im

def sc_why(t):
    im = bg(False); t0 = S("r1"); te = WT("r1", "everyone")
    q = T("Why all that noise?", 72, L_INK, 700); put(im, q, 540, 640, ease((t - t0) / 0.25), 0.96 + 0.04 * spring((t - t0) / 0.5))
    who = ["sami", "nour", ("R", VIOLET), ("M", GREEN_APP), ("J", SILVER)]
    for j, wv in enumerate(who):
        kj = spring((t - (WT("r1", "price") - 0.2) - j * 0.15) / 0.35)
        if kj > 0:
            x = 540 + (j - 2) * 175; put(im, head(wv, 150), x, 1000 + (1 - kj) * 30, min(1, kj * 1.5))
    if t >= te - 0.1:
        kp = spring((t - te + 0.1) / 0.4); put(im, pill("Everyone can bid = a fair price", 48, GREEN_UI, padx=34, pady=16), 540, 1260 + (1 - kp) * 20, min(1, kp * 1.5))
    footnote(im, "Names and avatars are illustrative", False, 1850)
    return im

def sc_clock(t):
    im = bg(True); t0 = S("f1"); tc = WT("f1", "countdown"); ta = WT("f1", "anywhere.")
    w, h = 860, 560; c = window(w, h, "Live auction", True)
    c.alpha_composite(T("ENDS IN", 28, D_MUTE, 700, True), (60, 120))
    left = max(0, 2 * 3600 + 14 * 60 + 9 - (t - t0))
    hh, mm, ss = int(left // 3600), int(left % 3600 // 60), int(left % 60)
    c.alpha_composite(T(f"{hh:02d}:{mm:02d}:{ss:02d}", 150, D_INK, 700, True), (60, 170))
    c.alpha_composite(T("Every bid, every second, in the open", 32, D_MUTE, 500), (60, 400))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 960, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tc - 0.2: select_box(im, (150, 848, 930, 1012), eout((t - tc + 0.2) / 0.3), 1, VIOLET)
    if t >= ta - 0.9:
        for j, wv in enumerate(["nour", ("R", VIOLET), ("M", GREEN_APP), ("J", SILVER), "sami"]):
            kj = spring((t - (ta - 0.9) - j * 0.1) / 0.35)
            if kj > 0: put(im, head(wv, 110), 540 + (j - 2) * 140, 1420 + (1 - kj) * 26, min(1, kj * 1.5))
        put(im, pill("watching from anywhere", 40, (54, 42, 108), padx=28, pady=12), 540, 1580, ease((t - ta + 0.5) / 0.3))
    footnote(im, "Generic screen, illustrative", True, 1850)
    return im

def sc_loop(t):
    im = bg(True); t0 = S("tk") - 0.1; tp = WT("tk", "public.")
    put(im, megaphone(360, BLUE, (t * 0.9) % 1.0 + 0.001), 590, 900, ease((t - t0) / 0.25), 0.97 + 0.03 * spring((t - t0) / 0.5))
    if t >= tp - 0.15: stamp_at(im, big_stamp("PUBLIC", GREEN_UI, 120, -6), 540, 1320, t, tp - 0.15)
    footnote(im, LAW_NOTE, True, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 27, BLUE), (540, 9, VIOLET), (750, 15, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "law": sc_law, "notice": sc_notice, "why": sc_why, "clock": sc_clock, "loop": sc_loop, "outro": sc_outro}

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
    s.pop(WT("h1", "crier") - 0.25, 0.035, 600); s.ding(WT("h2", "auction.") - 0.3, 1568, 0.03)
    s.pop(S("c1"), 0.03, 600); s.ding(WT("c1", "municipality's") - 0.3, 1175, 0.03)
    for w_ in ("notice", "Official"): s.pop(WT("c2", w_) - 0.3, 0.035, 600)
    s.pop(WT("c2", "municipality's") - 0.3, 0.035, 640)
    t10 = WT("c3", "ten")
    for j in range(6): s.tick(t10 - 0.3 + j * 0.1, 0.025)
    s.ding(t10 + 0.3, 1568, 0.03)
    te = WT("r1", "everyone")
    for j in range(5): s.pop(WT("r1", "price") - 0.2 + j * 0.15, 0.03, 560 + j * 40)
    s.ding(te, 1318, 0.03)
    tc = WT("f1", "countdown")
    for j in range(int((E("f1") - S("f1")))): s.tick(S("f1") + j * 1.0, 0.02)
    s.pop(tc - 0.2, 0.035, 620)
    s.thud(WT("tk", "public.") - 0.15, 0.07)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson27_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
