"""Auction short 21 (v3, quick, who: Nour): "DM for price". Problem: Nour asks a price and gets "DM", then her friend gets a
different number. Reframe (one rule): in Victoria, Australia, from 1 Oct 2026 the seller's reserve price must be published 7 days
before a home auction or the auction can't go ahead; the government's stated purpose is to end the frustration of learning "the
house was never in their price range" (Consumer Affairs Victoria; Hansard 14 Aug 2026). Fix: open bids, the same number for
everyone. Takeaway: when the price is public, nobody gets a special price. Loop: ends on the listing the video opens on.
Run: python3 tools/lessons/lesson21.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson21_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
def WX(key, word):
    """exact (normalised) word match, for short words like 'Or'"""
    for s_, e_, t_ in TL.words(key):
        if N._norm(s_) == N._norm(word): return t_
    return TL.wt(key, word)
TOTAL = TL.end + 0.5
STYLE, SEED = "keys", 21
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("chat", True, S("p1") - 0.1, S("r1") - 0.1), ("law", False, S("r1") - 0.1, S("r2") - 0.1),
      ("reason", True, S("r2") - 0.1, S("f1") - 0.1), ("fix", False, S("f1") - 0.1, S("tk") - 0.1),
      ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
BUYERS = (("R", VIOLET), ("M", GREEN_APP), ("J", SILVER))

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def bubble(text, size=40, fill=(236, 237, 242), col=L_INK, right=False):
    tt = T(text, size, col, 600); w, h = tt.width + 56, tt.height + 36
    im = Image.new("RGBA", (w, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=fill + (255,))
    if right: d.polygon([(w - 26, h - 10), (w - 18, h + 12), (w - 58, h - 10)], fill=fill + (255,))
    else: d.polygon([(26, h - 10), (18, h + 12), (58, h - 10)], fill=fill + (255,))
    im.alpha_composite(tt, (28, 18)); return im

def house(w=300, h=220):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(w / 2, 0), (w - 10, h * 0.45), (10, h * 0.45)], fill=VIOLET + (255,))
    d.rectangle((40, h * 0.45, w - 40, h - 1), fill=BLUE + (255,))
    d.rectangle((w / 2 - 28, h * 0.62, w / 2 + 28, h - 1), fill=(255, 255, 255, 255))
    d.rectangle((62, h * 0.55, 112, h * 0.72), fill=LILAC + (255,)); d.rectangle((w - 112, h * 0.55, w - 62, h * 0.72), fill=LILAC + (255,))
    return im

def listing(t, show_t=None, end_t=None):
    """a home listing whose price says 'DM'; shared by the hook and the loop so the replay is seamless"""
    w, h = 820, 960; c = card(w, h, False, 30)
    top = Image.new("RGBA", (w - 60, 330), (0, 0, 0, 0)); ImageDraw.Draw(top).rounded_rectangle((0, 0, w - 61, 329), radius=22, fill=(236, 233, 252, 255))
    top.alpha_composite(house(), (int((w - 60) / 2 - 150), 70)); c.alpha_composite(top, (30, 30))
    c.alpha_composite(T("Home for sale", 52, L_INK, 700), (60, 400))
    c.alpha_composite(T("Auction on Saturday", 38, GREY_TXT, 600), (60, 475))
    ImageDraw.Draw(c).line([(60, 560), (w - 60, 560)], fill=LINE_L + (255,), width=3)
    c.alpha_composite(T("Reserve price", 44, GREY_TXT, 600), (60, 610))
    ks = 0 if show_t is None else clamp((t - show_t) / 0.3)
    if ks < 1:
        p = pill("DM", 52, (236, 237, 242), RED_UI, padx=34, pady=12); p = fade_in(p, (1 - ks) / 1.5)
        c.alpha_composite(p, (w - 60 - p.width, 596))
    if ks > 0:
        v = fade_in(T("$700,000", 60, L_INK, 700), ks); c.alpha_composite(v, (w - 60 - v.width, 596))
    c.alpha_composite(T("Seen by", 40, GREY_TXT, 600), (60, 740))
    c.alpha_composite(head("nour", 80), (w - 250, 722)); c.alpha_composite(head(BUYERS[1], 80), (w - 150, 722))
    if end_t is not None and t >= end_t:
        kp = spring((t - end_t) / 0.4); p = fade_in(pill("No special prices", 46, GREEN_UI, padx=34, pady=14), kp)
        c.alpha_composite(p, (int(w / 2 - p.width / 2), int(850 + (1 - kp) * 20)))
    return c

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); tc = WT("h1", "can't"); tb = WT("h2", "best")
    put(im, lift(listing(t)), 540, 1170, 1, 0.97 + 0.03 * spring(t / 0.5))
    tp = WT("h1", "price,")
    if t >= tp - 0.1: select_box(im, (560, 1270, 960, 1370), eout((t - tp + 0.1) / 0.3), 1, RED_UI)
    stamp_at(im, big_stamp("NO AUCTION", RED_UI, 84, -5), 540, 1590, t, tc - 0.05)
    if t >= tb - 0.1:
        kq = spring((t - tb + 0.1) / 0.4); put(im, pill("Why?", 50, VIOLET, padx=34, pady=14), 540, 1745 + (1 - kq) * 20, min(1, kq * 1.5))
    footnote(im, "Listing and price are illustrative", False, 1850)
    return im

def sc_chat(t):
    im = bg(True); t0 = S("p1"); ta = WT("p1", "asks"); tr = WT("p1", "reply:"); tf = WT("p1", "friend"); td = WT("p1", "different")
    pw, ph = 680, 1180; p = phone(pw, ph, True)
    p.alpha_composite(T("Apartment for sale", 36, D_INK, 700), (50, 110))
    msgs = [(ta - 0.1, "How much?", True), (tr + 0.1, "DM", False), (tf - 0.35, "$210,000", False)]
    y = 220
    for ti, txt, right in msgs:
        k = spring((t - ti) / 0.35)
        if k <= 0: continue
        b = bubble(txt, 50, BLUE if right else (40, 46, 60), D_INK, right)
        row = Image.new("RGBA", (pw - 80, b.height + 10), (0, 0, 0, 0))
        if right: row.alpha_composite(head("nour", 64), (pw - 80 - 64, 20)); row.alpha_composite(b, (pw - 80 - 84 - b.width, 0))
        else: row.alpha_composite(b, (0, 0))
        p.alpha_composite(fade_in(row, k), (40, int(y + (1 - k) * 30))); y += 150
    if t >= tf - 0.1:
        kf = spring((t - tf + 0.1) / 0.4)
        r = card(pw - 80, 200, True, 26, fill=(30, 36, 52)); r.alpha_composite(head(BUYERS[1], 90), (24, 55))
        r.alpha_composite(T("Her friend was told", 32, D_MUTE, 600), (136, 50))
        v = T("$185,000", 56, D_INK, 700); r.alpha_composite(v, (136, 98))
        p.alpha_composite(fade_in(r, kf), (40, int(720 + (1 - kf) * 30)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(p, True), 540, 1180, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= td - 0.1:
        kk = spring((t - td + 0.1) / 0.4); put(im, pill("Different number", 46, RED_UI, padx=30, pady=14), 540, 1640 + (1 - kk) * 20, min(1, kk * 1.5))
    footnote(im, "Names, prices and chat are illustrative", True, 1850)
    return im

def sc_law(t):
    im = bg(False); t0 = S("r1"); tv = WT("r1", "Victoria,"); ts = WT("r1", "7"); tb = WT("r1", "before"); tn = WX("r1", "Or")
    vs = "7 days" if t >= ts - 0.1 else "? days"
    c = stat("Reserve price public", vs, "before a home auction", 860, False, 190, VIOLET)
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1060, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tv - 0.15:
        kc = spring((t - tv + 0.15) / 0.4); put(im, chip("Victoria, Australia · since Oct 2026", False, 28), 540, 790 + (1 - kc) * 20, min(1, kc * 1.5))
    if t >= tb - 0.1: select_box(im, (125, 1180, 650, 1240), eout((t - tb + 0.1) / 0.3))
    stamp_at(im, big_stamp("OR NO AUCTION", RED_UI, 90, -7), 540, 1500, t, tn - 0.05)
    footnote(im, "Source: Consumer Affairs Victoria, 2026", False, 1850)
    return im

def sc_reason(t):
    im = bg(True); t0 = S("r2"); tfr = WT("r2", "buyers"); tnv = WT("r2", "never")
    w, h = 900, 640; c = card(w, h, True, 30)
    c.alpha_composite(T("THE STATED PURPOSE", 26, D_MUTE, 700, True), (60, 50))
    q = T("“", 160, LILAC, 700); c.alpha_composite(q, (50, 70))
    lines = [("…buyers go to an auction", D_INK), ("and learn that the house", D_INK), ("was never in their", LILAC), ("price range.”", LILAC)]
    for i, (ln, col) in enumerate(lines):
        tk_ = tfr - 0.2 + i * 0.18 if i < 2 else tnv - 0.15 + (i - 2) * 0.2
        c.alpha_composite(fade_in(T(ln, 50, col, 700), (t - tk_) / 0.25), (60, 230 + i * 80))
    c.alpha_composite(T("Victorian Government, Parliament, 14 Aug 2026", 26, D_MUTE, 500), (60, h - 70))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1080, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tnv - 0.1:
        kp = spring((t - tnv + 0.1) / 0.4); put(im, head("nour", 140), 540, 1550 + (1 - kp) * 30, min(1, kp * 1.5))
    footnote(im, "Source: Hansard, Parliament of Victoria", True, 1850)
    return im

def sc_fix(t):
    im = bg(False); t0 = S("f1"); te = WT("f1", "Every"); ts = WT("f1", "Same")
    w, h = 880, 1000; c = window(w, h, "Open auction", False)
    rows = [(BUYERS[0], "$640,000"), ("nour", "$660,000"), (BUYERS[1], "$680,000"), ("nour", "$700,000")]
    y = 110; t1 = WT("f1", "open")
    for j, (who, amt) in enumerate(rows):
        kj = spring((t - t1 + 0.1 - j * 0.3) / 0.35)
        if kj <= 0: continue
        r = card(780, 150, False, 26, fill=(246, 246, 250)); r.alpha_composite(head(who, 100), (26, 25))
        r.alpha_composite(T("bid", 34, GREY_TXT, 600), (150, 52)); a = T(amt, 60, L_INK, 700); r.alpha_composite(a, (780 - 40 - a.width, 40))
        c.alpha_composite(fade_in(r, kj), (50, int(y + (1 - kj) * 30))); y += 175
    if t >= te - 0.1:
        kc = spring((t - te + 0.1) / 0.4); pc = fade_in(chip("Every bid public", False, 28), kc)
        c.alpha_composite(pc, (int(w / 2 - pc.width / 2), 820))
    if t >= ts - 0.15:
        kp = spring((t - ts + 0.15) / 0.4); pp = fade_in(pill("Same number, for everyone", 44, VIOLET, padx=32, pady=16), kp)
        c.alpha_composite(pp, (int(w / 2 - pp.width / 2), int(880 + (1 - kp) * 20)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Example auction · bids and names illustrative", False, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tpb = WT("tk", "public,"); tsp = WT("tk", "special")
    put(im, lift(listing(t, tpb - 0.1, tsp - 0.1)), 540, 1170, ease((t - t0) / 0.2))
    if tpb - 0.1 <= t < tsp - 0.1: select_box(im, (560, 1270, 960, 1370), eout((t - tpb + 0.1) / 0.3), 1, GREEN_UI)
    footnote(im, "Listing and price are illustrative", False, 1850)
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

FN = {"hook": sc_hook, "chat": sc_chat, "law": sc_law, "reason": sc_reason, "fix": sc_fix, "loop": sc_loop, "outro": sc_outro}

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
    s.ding(WT("h1", "price,") - 0.1, 1318, 0.03); s.thud(WT("h1", "can't") - 0.05, 0.08); s.pop(WT("h2", "best") - 0.1, 0.035, 600)
    s.pop(WT("p1", "asks") - 0.1, 0.035, 600); s.pop(WT("p1", "reply:") + 0.1, 0.035, 520); s.pop(WT("p1", "friend") - 0.35, 0.035, 560)
    s.pop(WT("p1", "friend") - 0.1, 0.035, 640); s.ding(WT("p1", "different") - 0.1, 1175, 0.025)
    s.pop(WT("r1", "Victoria,") - 0.15, 0.035, 520)
    s.ding(WT("r1", "7") - 0.1, 1318, 0.03)
    s.thud(WX("r1", "Or") - 0.05, 0.08)
    s.pop(WT("r2", "buyers") - 0.2, 0.03, 560); s.ding(WT("r2", "never") - 0.15, 1568, 0.025)
    for j in range(4): s.pop(WT("f1", "open") - 0.1 + j * 0.3, 0.03, 560 + j * 40)
    s.ding(WT("f1", "Same") - 0.15, 1318, 0.03)
    s.tick(WT("tk", "public,") - 0.1, 0.03); s.ding(WT("tk", "special") - 0.1, 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson21_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
