"""Auction short 17 (v3, quick, who: Sami): "The no-show". Problem: a buyer says "I'm on my way" and never comes.
Reframe (one fact): one booking platform's own data (Tock, Dec 2023 to Mar 2024): no-show rate 3% with a card hold, 1.7% with a
deposit, 0.9% fully prepaid; the more people put down, the more they show up. Lebanese law uses the same idea: to bid at a court
auction you first deposit an amount equal to the full opening price (CCP Art. 973). Fix: a small deposit when you bid, returned if
you're outbid (no amount stated). Takeaway: serious buyers don't mind a deposit; time-wasters do.
One story from first frame to last (Sami's chat, illustrative and labelled).
Run: python3 tools/lessons/lesson17.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson17_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "marimba", 17
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("bars", True, S("p1") - 0.1, S("s3") - 0.1), ("court", False, S("s3") - 0.1, S("f1") - 0.1),
      ("fix", True, S("f1") - 0.1, S("tk") - 0.1), ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
BUYER = ("K", GREEN_APP)

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def dim(layer, a):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * a))); return layer

def bubble(text, size=40, fill=(236, 237, 242), col=L_INK, right=False):
    tt = T(text, size, col, 600); w, h = tt.width + 56, tt.height + 36
    im = Image.new("RGBA", (w, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=fill + (255,))
    if right: d.polygon([(w - 26, h - 10), (w - 18, h + 12), (w - 58, h - 10)], fill=fill + (255,))
    else: d.polygon([(26, h - 10), (18, h + 12), (58, h - 10)], fill=fill + (255,))
    im.alpha_composite(tt, (28, 18)); return im

def sami_phone(t, minutes, t_strike=None, extra=None):
    """Sami's chat with a buyer; shared by the hook and the loop so the replay is seamless"""
    pw, ph = 640, 900; p = phone(pw, ph, False)
    p.alpha_composite(head(BUYER, 80), (40, 96)); p.alpha_composite(T("Buyer", 36, L_INK, 700), (136, 104))
    p.alpha_composite(T("asked about your sofa", 24, GREY_TXT, 600), (136, 146))
    ImageDraw.Draw(p).line([(30, 200), (pw - 30, 200)], fill=(228, 230, 236, 255), width=2)
    b1 = bubble("Still available?", 38); p.alpha_composite(b1, (40, 240))
    b2 = bubble("Yes! Come at 5.", 38, LILAC, (255, 255, 255), True); p.alpha_composite(b2, (pw - 40 - b2.width, 350))
    b3 = bubble("I'm on my way.", 44); p.alpha_composite(b3, (40, 460))
    if t_strike is not None and t >= t_strike - 0.05:
        k = eout((t - t_strike + 0.05) / 0.3); d = ImageDraw.Draw(p); y = 460 + 18 + 34
        d.line([(60, y), (60 + (b3.width - 40) * k, y)], fill=RED_UI + (255,), width=9)
    st = T(f"Waiting · {minutes} min", 30, RED_UI if minutes >= 60 else GREY_TXT, 700, True); p.alpha_composite(st, (40, 600))
    if extra is not None: p.alpha_composite(extra, (int(pw / 2 - extra.width / 2), 700))
    return p

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); th = WT("h1", "hour."); tn = WT("h1", "Nobody")
    mins = int(roll(t, WT("h1", "waited") - 0.1, th - WT("h1", "waited") + 0.35, 0, 60))
    p = sami_phone(t, mins)
    put(im, lift(p), 540, 1110, 1, 0.97 + 0.03 * spring(t / 0.5))
    put(im, head("sami", 150), 200, 1560, 1)
    stamp_at(im, big_stamp("NO-SHOW", RED_UI, 100, -8), 620, 1520, t, tn - 0.05)
    footnote(im, "Chat, item and names are illustrative", False, 1850)
    return im

BARS = (("Card hold", 3.0, "3%", "s1", "3%"), ("Deposit", 1.7, "1.7%", "s2", "1.7%."), ("Fully prepaid", 0.9, "0.9%", "s2", "0.9%."))

def sc_bars(t):
    im = bg(True); t0 = S("p1"); tm = WT("s2b", "more")
    w, h = 900, 1000; win = window(w, h, "No-show rate · one booking platform", True)
    lab = T("BOOKINGS THAT DIDN'T SHOW", 24, D_MUTE, 700, True); win.alpha_composite(lab, (int(w / 2 - lab.width / 2), 110))
    base, top = 860, 260; colw = 200
    d = ImageDraw.Draw(win); d.line([(60, base), (w - 60, base)], fill=(70, 76, 92, 255), width=3)
    for i, (name, v, txt, key, word) in enumerate(BARS):
        tw = WT(key, word); k = eout((t - tw + 0.15) / 0.45)
        cx = 170 + i * 280
        nm = T(name, 32, D_INK, 600); win.alpha_composite(nm, (int(cx - nm.width / 2), base + 24))
        if k <= 0: continue
        hh = (base - top) * (v / 3.0) * k; col = (RED_UI, VIOLET, GREEN_UI)[i]
        d.rounded_rectangle((cx - colw / 2, base - hh, cx + colw / 2, base), radius=18, fill=col + (255,))
        vt = T(txt, 64, D_INK, 700); win.alpha_composite(fade_in(vt, k), (int(cx - vt.width / 2), int(base - hh - 84)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win, True), 540, 1140, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tm - 0.1:
        kp = spring((t - tm + 0.1) / 0.4)
        put(im, pill("More money down  →  more people show up", 40, GREEN_UI, padx=30, pady=14), 540, 1730 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    footnote(im, "Source: Tock, its customers' bookings, Dec 2023 – Mar 2024", True, 1850)
    return im

def sc_court(t):
    im = bg(False); t0 = S("s3"); tb = WT("s3", "bid,"); tf = WT("s3", "full"); to = WT("s3", "opening")
    w, h = 880, 760; win = window(w, h, "Court auction · Lebanon", False)
    kb = spring((t - tb + 0.1) / 0.4)
    if kb > 0:
        l1 = T("Before you bid:", 44, GREY_TXT, 600); win.alpha_composite(fade_in(l1, kb), (int(w / 2 - l1.width / 2), int(150 + (1 - kb) * 16)))
    kd = spring((t - tf + 0.2) / 0.4)
    if kd > 0:
        l2 = T("Deposit", 120, L_INK, 700); win.alpha_composite(fade_in(l2, kd), (int(w / 2 - l2.width / 2), int(240 + (1 - kd) * 16)))
    ko = spring((t - to + 0.1) / 0.4)
    if ko > 0:
        l3 = T("= the full opening price", 56, (60, 40, 140), 700); win.alpha_composite(fade_in(l3, ko), (int(w / 2 - l3.width / 2), int(440 + (1 - ko) * 16)))
    k = ease((t - t0 + 0.12) / 0.25); cy = 1100; put(im, lift(win), 540, cy, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= to + 0.25:
        l3 = T("= the full opening price", 56, L_INK, 700); x0 = 540 - l3.width / 2 - 16; y0 = cy - h / 2 + 440 - 12
        select_box(im, (x0, y0, x0 + l3.width + 32, y0 + l3.height + 24), eout((t - to - 0.25) / 0.3))
    footnote(im, "Lebanese Code of Civil Procedure, Art. 973", False, 1850)
    return im

def sc_fix(t):
    im = bg(True); t0 = S("f1"); tb = WT("f1", "bid,"); tr = WT("f1", "returned"); tob = WT("f1", "outbid.")
    rows = ((("R", VIOLET), "$420"), (("M", BLUE), "$450"))
    w, h = 880, 640; win = window(w, h, "Live auction · Sofa", True)
    for i, (who, amt) in enumerate(rows):
        ki = spring((t - tb + 0.2 - i * 0.25) / 0.35)
        if ki <= 0: continue
        y = 110 + i * 250
        row = card(780, 210, True, 28, fill=(30, 36, 52))
        row.alpha_composite(head(who, 110), (30, 50))
        row.alpha_composite(T(f"Bid {amt}", 52, D_INK, 700), (170, 40))
        if i == 0 and t >= tr - 0.05:
            kr = spring((t - tr + 0.05) / 0.3)
            row.alpha_composite(fade_in(pill("Outbid · deposit returned", 30, GREEN_UI, padx=18, pady=8), kr), (170, 124))
        else:
            row.alpha_composite(fade_in(pill("Deposit in", 30, VIOLET, padx=18, pady=8), ki), (170, 124))
        if i == 0 and t >= tob - 0.05: row = dim(row, 0.55 + 0.45 * (1 - spring((t - tob) / 0.3)))
        win.alpha_composite(fade_in(row, ki), (50, int(y + (1 - ki) * 24)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win, True), 540, 1080, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    put(im, head("sami", 130), 900, 1480, ease((t - t0 - 0.2) / 0.3))
    footnote(im, "Example auction · bids and names illustrative", True, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; ts = WT("tk", "Serious"); tw = WT("tk", "Time-wasters")
    ks = spring((t - ts + 0.1) / 0.35)
    extra = fade_in(pill("Serious buyer: deposit in", 34, GREEN_UI, padx=22, pady=10), ks) if ks > 0 else None
    p = sami_phone(t, 60, tw - 0.05, extra)
    put(im, lift(p), 540, 1110, ease((t - t0) / 0.2))
    put(im, head("sami", 150), 200, 1560, 1)
    footnote(im, "Chat, item and names are illustrative", False, 1850)
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

FN = {"hook": sc_hook, "bars": sc_bars, "court": sc_court, "fix": sc_fix, "loop": sc_loop, "outro": sc_outro}

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
    for i in range(6): s.tick(WT("h1", "waited") + i * 0.12, 0.018)
    s.thud(WT("h1", "Nobody") - 0.05, 0.08)
    s.pop(S("p1"), 0.035, 600)
    for _, _, _, key, word in BARS: s.pop(WT(key, word) - 0.15, 0.04, 560)
    s.ding(WT("s2b", "more") - 0.1, 1568, 0.03)
    s.pop(WT("s3", "bid,") - 0.1, 0.035, 600); s.pop(WT("s3", "full") - 0.2, 0.04, 520); s.ding(WT("s3", "opening") - 0.1, 1318, 0.03)
    for j in range(2): s.pop(WT("f1", "bid,") - 0.2 + j * 0.25, 0.03, 540 + j * 40)
    s.ding(WT("f1", "returned") - 0.05, 1568, 0.03)
    s.pop(WT("tk", "Serious") - 0.1, 0.04, 680); s.thud(WT("tk", "Time-wasters") - 0.05, 0.06)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson17_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
