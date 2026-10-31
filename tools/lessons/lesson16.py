"""Auction short 16 (v3, quick, who: Nour): "Afraid of overpaying?". Problem: Nour skips auctions because she's sure she'll
overpay. Reframe (one fact): in an open ascending auction each bidder stops at their limit, so the winner pays about the
second-highest bidder's limit plus one step (Vickrey 1961, via Lucking-Reiley, JEP 2000; EconPort); a stamp auction printed
the rule in 1893: "an advance of from 1c to 10c above the second highest bidder". Fix: set your maximum before it starts and
let the others stop first (callback to lesson 07). Takeaway: you pay one step above the last person who wanted it.
One story from first frame to last (Nour's bike auction, illustrative and labelled).
Run: python3 tools/lessons/lesson16.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson16_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "keys", 16
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("surprise", True, S("p1") - 0.1, S("s1") - 0.1), ("race", False, S("s1") - 0.1, S("s3") - 0.1),
      ("stamp", True, S("s3") - 0.1, S("f1") - 0.1), ("fix", False, S("f1") - 0.1, S("tk") - 0.1),
      ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
RIVALS = (("R", VIOLET), ("M", GREEN_APP))

def fade_in(layer, k):
    layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def dim(layer, a):
    layer.putalpha(layer.getchannel("A").point(lambda q: int(q * a))); return layer

# ---------- drawings ----------
def bike_icon(w=200, col=BLUE, ink=(24, 28, 44)):
    S2 = 2; h = int(w * 0.7); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    r = H2 * 0.3; lw = int(W2 * 0.045)
    for cx in (W2 * 0.24, W2 * 0.76):
        d.ellipse((cx - r, H2 * 0.62 - r, cx + r, H2 * 0.62 + r), outline=ink + (255,), width=lw)
    a, b, c, e = (W2 * 0.24, H2 * 0.62), (W2 * 0.48, H2 * 0.62), (W2 * 0.4, H2 * 0.3), (W2 * 0.68, H2 * 0.3)
    for p, q in ((a, c), (c, b), (b, e), (c, e), (e, (W2 * 0.76, H2 * 0.62)), (e, (W2 * 0.64, H2 * 0.12))):
        d.line([p, q], fill=col + (255,), width=lw)
    d.line([(W2 * 0.33, H2 * 0.22), (W2 * 0.47, H2 * 0.22)], fill=ink + (255,), width=int(lw * 1.4))
    d.line([(W2 * 0.58, H2 * 0.12), (W2 * 0.72, H2 * 0.1)], fill=ink + (255,), width=lw)
    return im.resize((w, h), Image.LANCZOS)

def bubble(text, size=40, fill=(236, 237, 242), col=L_INK, right=False):
    tt = T(text, size, col, 600); w, h = tt.width + 56, tt.height + 36
    im = Image.new("RGBA", (w, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=fill + (255,))
    if right: d.polygon([(w - 26, h - 10), (w - 18, h + 12), (w - 58, h - 10)], fill=fill + (255,))
    else: d.polygon([(26, h - 10), (18, h + 12), (58, h - 10)], fill=fill + (255,))
    im.alpha_composite(tt, (28, 18)); return im

def listing(price_txt, label="HIGHEST BID", delta=None, delta_col=GREEN_UI, k_delta=0.0, dark=False):
    """the bike listing card, shared by the hook and the loop so the replay is seamless"""
    lc = card(560, 260, dark, 26, fill=((30, 36, 52) if dark else (246, 247, 251)))
    lc.alpha_composite(bike_icon(190, BLUE if not dark else LILAC), (28, 66))
    ink = D_INK if dark else L_INK
    lc.alpha_composite(T("Bike · vintage", 34, ink, 600), (250, 40))
    lc.alpha_composite(T(label, 22, GREY_TXT, 700, True), (250, 92))
    lc.alpha_composite(T(price_txt, 84, ink, 700), (250, 118))
    if delta and k_delta > 0:
        dp = fade_in(pill(delta, 30, delta_col, padx=16, pady=8), k_delta); lc.alpha_composite(dp, (int(123 - dp.width / 2), 196 - int(10 * (1 - k_delta))))
    return lc

def nour_phone(t, price, label, msgs, delta=None, delta_col=GREEN_UI, t_delta=None):
    """msgs: [(t_show, text, right)]: right = Nour's own bubble"""
    pw, ph = 640, 960; p = phone(pw, ph, False)
    kd = spring((t - t_delta) / 0.35) if t_delta is not None else 0
    p.alpha_composite(listing(price, label, delta, delta_col, kd), (40, 100))
    p.alpha_composite(T("BIDDERS · 3", 22, GREY_TXT, 700, True), (60, 390))
    for j, who in enumerate(("nour", RIVALS[0], RIVALS[1])): p.alpha_composite(head(who, 86), (60 + j * 104, 440))
    y = 580
    for ts, txt, right in msgs:
        k = spring((t - ts) / 0.35)
        if k > 0:
            if right: b = fade_in(bubble(txt, 36, LILAC, (255, 255, 255), True), k); p.alpha_composite(b, (pw - 40 - b.width, int(y + (1 - k) * 30)))
            else: b = fade_in(bubble(txt, 36), k); p.alpha_composite(b, (40, int(y + (1 - k) * 30)))
        y += 120
    return p

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); to = WT("h1", "overpay.")
    p = nour_phone(t, "$450", "HIGHEST BID", [(-1.0, "What if I pay too much?", True)])
    put(im, lift(p), 540, 1120, 1, 0.97 + 0.03 * spring(t / 0.5))
    put(im, head("nour", 150), 220, 1560, 1)
    stamp_at(im, big_stamp("OVERPAY?", RED_UI, 96, -8), 600, 1500, t, to - 0.05)
    footnote(im, "Bike, bids and names are illustrative", False, 1850)
    return im

def sc_surprise(t):
    im = bg(True); t0 = S("p1"); tw = WT("p1", "winner"); td = WT("p1", "doesn't")
    k = spring((t - tw + 0.15) / 0.4)
    if k > 0:
        c = stat("The winner pays", "her limit", "", 820, True, 140)
        cx, cy = 540, 1080 + (1 - k) * 40
        put(im, lift(c, True), cx, cy, min(1, k * 1.5), 0.94 + 0.06 * k)
        if t >= td - 0.05:
            vy = cy - c.height / 2 + 40 + 26 + 26 + 26 + 108
            strike(im, cx - 410 + 44, vy, cx - 410 + 44 + 560, eout((t - td + 0.05) / 0.3), RED_UI, 12)
    else:
        put(im, head("nour", 200), 540, 1080, ease((t - t0 + 0.12) / 0.25))
    footnote(im, "Open (ascending) auction", True, 1850)
    return im

def sc_race(t):
    im = bg(False); t0 = S("s1"); tl = WT("s1", "limit."); t45 = WT("s2", "$450"); t50 = WT("s2", "$500"); t51 = WT("s2", "$510.")
    t70 = WT("s2", "$700.")
    if t < t45: price = int(roll(t, t0 + 0.3, t45 - t0 - 0.4, 380, 440) // 10 * 10)
    elif t < t50: price = 450
    elif t < t51: price = 500
    else: price = 510
    w, h = 900, 1000; win = window(w, h, "Live auction · Bike · vintage", False)
    lab = T("HIGHEST BID", 24, GREY_TXT, 700, True); win.alpha_composite(lab, (int(w / 2 - lab.width / 2), 90))
    pv = T(money(price), 130, L_INK, 700); win.alpha_composite(pv, (int(w / 2 - pv.width / 2), 128))
    rows = ((RIVALS[0], "$450", t45), (RIVALS[1], "$500", t50), ("nour", "$700", None))
    for i, (who, lim, tout) in enumerate(rows):
        y = 340 + i * 200
        out = tout is not None and t >= tout - 0.05
        row = card(800, 170, False, 28, fill=(246, 247, 251))
        row.alpha_composite(head(who, 110), (30, 30))
        nm = "Nour" if who == "nour" else f"Bidder {who[0]}"
        row.alpha_composite(T(nm, 40, L_INK, 700), (170, 36))
        kl = spring((t - tl + 0.25 - i * 0.1) / 0.35)
        if kl > 0:
            ch = fade_in(pill(f"limit {lim}", 30, (233, 227, 255) if who == "nour" else (236, 237, 242), (60, 40, 140) if who == "nour" else (96, 102, 116), 16, 8), kl)
            row.alpha_composite(ch, (170, 96))
        if out:
            ko = spring((t - tout + 0.05) / 0.3); oc = fade_in(pill("OUT", 34, RED_UI, padx=22, pady=8), ko); row.alpha_composite(oc, (800 - 40 - oc.width, 58))
            row = dim(row, 0.45 + 0.55 * (1 - ko))
        if who == "nour" and t >= t51 - 0.05:
            kw = spring((t - t51 + 0.05) / 0.3); oc = fade_in(pill("WINS", 34, GREEN_UI, padx=22, pady=8), kw); row.alpha_composite(oc, (800 - 40 - oc.width, 58))
        win.alpha_composite(row, (50, y))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1130, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= t70 - 0.1:
        select_box(im, (540 - 450 + 50 + 165, 1130 - 500 + 740 + 90, 540 - 450 + 50 + 400, 1130 - 500 + 740 + 150), eout((t - t70 + 0.1) / 0.3))
        kp = spring((t - t70) / 0.4); put(im, pill("$190 under her limit", 44, GREEN_UI, padx=30, pady=14), 540, 1700 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    footnote(im, "Example auction · bids, limits and names illustrative · 1 step = $10", False, 1850)
    return im

QUOTE = ("“each lot will be sold", "at an advance of from", "1c to 10c above the", "second highest bidder.”")

def sc_stamp(t):
    im = bg(True); t0 = S("s3"); ty = WT("s3", "1893"); tp = WT("s3", "promised"); ts = WT("s3", "second-highest")
    w, h = 900, 900; win = window(w, h, "Stamp auction · Massachusetts", True)
    ky = spring((t - ty + 0.1) / 0.4)
    yr = T("1893", 150, LILAC, 700); win.alpha_composite(fade_in(yr, ky), (int(w / 2 - yr.width / 2), int(110 + (1 - ky) * 20)))
    for i, ln in enumerate(QUOTE):
        kq = spring((t - tp + 0.1 - i * 0.18) / 0.4)
        if kq <= 0: continue
        lt = T(ln, 52, D_INK, 600); win.alpha_composite(fade_in(lt, kq), (int(w / 2 - lt.width / 2), int(360 + i * 92 + (1 - kq) * 16)))
    k = ease((t - t0 + 0.12) / 0.25); cy = 1110; put(im, lift(win, True), 540, cy, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= ts - 0.1:
        lt = T(QUOTE[3], 52, D_INK, 600); x0 = 540 - lt.width / 2 - 14; y0 = cy - h / 2 + 360 + 3 * 92 - 10
        select_box(im, (x0, y0, x0 + lt.width + 28, y0 + lt.height + 22), eout((t - ts + 0.1) / 0.3))
    footnote(im, "Wainwright & Lewis, Northampton, Mass., 1893 sale notice", True, 1820)
    footnote(im, "Quoted in Lucking-Reiley, Journal of Economic Perspectives, 2000", True, 1858)
    return im

def sc_fix(t):
    im = bg(False); t0 = S("f1"); tm = WT("f1", "maximum"); tst = WT("f1", "stop")
    c = stat("My max · set before it starts", "$700", "", 820, False, 150, (60, 40, 140))
    c.alpha_composite(head("nour", 120), (820 - 170, 40))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 900, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    cx = 540 + 330 - 230 * eout((t - tm + 0.6) / 0.5); cy = 1180 - 210 * eout((t - tm + 0.6) / 0.5)
    if tm - 0.6 <= t < tst - 0.3: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 330, 960, (t - tm) / 0.5)
    ks = spring((t - tst + 0.2) / 0.4)
    if ks > 0:
        row = Image.new("RGBA", (700, 200), (0, 0, 0, 0))
        for j, who in enumerate(RIVALS):
            kj = spring((t - tst + 0.2 - j * 0.15) / 0.35)
            hh = head(who, 140); hh = dim(hh, 1 - 0.6 * kj); row.alpha_composite(hh, (120 + j * 320, 10))
            if kj > 0: oc = fade_in(pill("stops", 30, RED_UI, padx=16, pady=6), kj); row.alpha_composite(oc, (int(190 + j * 320 - oc.width / 2), 150))
        put(im, row, 540, 1360, min(1, ks * 1.5))
    footnote(im, "Like lesson 7: decide your maximum first · amounts illustrative", False, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; ts = WT("tk", "step")
    p = nour_phone(t, "$510", "SOLD TO NOUR", [(-1.0, "What if I pay too much?", True), (WT("tk", "wanted") - 0.1, "Paid $510. Limit $700.", True)],
                   "+1 step", GREEN_UI, ts - 0.1)
    put(im, lift(p), 540, 1120, ease((t - t0) / 0.2))
    put(im, head("nour", 150), 220, 1560, 1)
    footnote(im, "Bike, bids and names are illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 16, BLUE), (540, 1, VIOLET), (750, 6, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "surprise": sc_surprise, "race": sc_race, "stamp": sc_stamp, "fix": sc_fix, "loop": sc_loop, "outro": sc_outro}

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
    s.thud(WT("h1", "overpay.") - 0.05, 0.08)
    s.pop(WT("p1", "winner") - 0.15, 0.035, 600); s.thud(WT("p1", "doesn't") - 0.05, 0.06)
    for i in range(3): s.pop(WT("s1", "limit.") - 0.25 + i * 0.1, 0.03, 560 + i * 40)
    for i in range(6): s.tick(S("s1") + 0.3 + i * 0.4, 0.018)
    s.pop(WT("s2", "$450") - 0.05, 0.04, 480); s.pop(WT("s2", "$500") - 0.05, 0.04, 520)
    s.ding(WT("s2", "$510.") - 0.05, 1318, 0.03); s.ding(WT("s2", "$700.") - 0.05, 1568, 0.03)
    s.pop(WT("s3", "1893") - 0.1, 0.04, 600)
    for i in range(4): s.pop(WT("s3", "promised") - 0.1 + i * 0.18, 0.025, 540 + i * 30)
    s.ding(WT("s3", "second-highest") - 0.1, 1568, 0.03)
    s.pop(WT("f1", "maximum"), 0.04, 680)
    for j in range(2): s.pop(WT("f1", "stop") - 0.2 + j * 0.15, 0.03, 500 - j * 40)
    s.pop(WT("tk", "step") - 0.1, 0.04, 680); s.ding(WT("tk", "wanted"), 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson16_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
