"""Auction short 13 (v3, quick, who: Nour): "The last-second loss". Problem: Nour leads an online auction for three days and is
outbid in the last second, with no time to answer. Reframe (one study): in 240 fixed-end online auctions, 89 had bids in the last
minute and 29 in the last ten seconds; in auctions where a late bid extends the clock, just one bid came in the last minute
(Roth & Ockenfels, AER 2002). Fix: a late bid adds time. Takeaway: a fair finish gives every bid an answer.
Built like L10 v2 / L11 / L12: one story from the first frame to the last, one study. Platforms are not named.
Run: python3 tools/lessons/lesson13.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson13_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "ambient", 13
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("ended", True, S("p1") - 0.1, S("s1") - 0.1), ("study", False, S("s1") - 0.1, S("s2") - 0.1),
      ("result", True, S("s2") - 0.1, S("s3") - 0.1), ("rule", False, S("s3") - 0.1, S("f1") - 0.1), ("skill", True, S("f1") - 0.1, S("f2") - 0.1),
      ("loop", False, S("f2") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
R_, M_ = ("R", VIOLET), ("M", GREEN_APP)

# ---------- drawings ----------
def camera_icon(w=200, col=BLUE, ink=(24, 28, 44)):
    S2 = 2; h = int(w * 0.7); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    d.rounded_rectangle((W2 * 0.3, H2 * 0.06, W2 * 0.58, H2 * 0.26), radius=14, fill=ink + (255,))
    d.rounded_rectangle((W2 * 0.04, H2 * 0.2, W2 * 0.96, H2 * 0.94), radius=36, fill=col + (255,))
    d.rectangle((W2 * 0.04, H2 * 0.42, W2 * 0.96, H2 * 0.5), fill=ink + (255,))
    cx, cy, r = W2 * 0.5, H2 * 0.57, H2 * 0.27
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ink + (255,)); r2 = r * 0.62
    d.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), fill=(70, 80, 110, 255)); r3 = r * 0.22
    d.ellipse((cx - r2 * 0.5 - r3, cy - r2 * 0.5 - r3, cx - r2 * 0.5 + r3, cy - r2 * 0.5 + r3), fill=(255, 255, 255, 200))
    d.ellipse((W2 * 0.8, H2 * 0.27, W2 * 0.88, H2 * 0.36), fill=(255, 255, 255, 230))
    return im.resize((w, h), Image.LANCZOS)

def clock_txt(sec, size=150, col=L_INK):
    sec = max(0, int(np.ceil(sec - 1e-6))); return T(f"{sec // 60}:{sec % 60:02d}", size, col, 700, True)

def fade_l(layer, k):
    layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def auction_phone(t, bids, sec, ended=False, added_t=None, stamp_t=None):
    """Nour's phone in an online auction: the item, the clock, the bids (newest on top). Shared by the hook and the loop scene."""
    pw, ph = 640, 1180; p = phone(pw, ph, False)
    vis = [b for b in bids if t >= b[0]]; top = vis[-1]
    lc = card(560, 280, False, 26, fill=(246, 247, 251)); lc.alpha_composite(camera_icon(190), (28, 70))
    lc.alpha_composite(T("Vintage camera", 36, L_INK, 600), (240, 38)); lc.alpha_composite(T("HIGHEST BID", 22, GREY_TXT, 700, True), (240, 92))
    lc.alpha_composite(T(money(top[2]), 76, L_INK, 700), (240, 120))
    lead = top[1] == "nour"; st = pill("You're leading" if lead else "Outbid", 28, GREEN_UI if lead else RED_UI, padx=18, pady=8)
    lc.alpha_composite(st, (240, 212)); p.alpha_composite(lc, (40, 100))
    tc = card(560, 270, False, 26, fill=(246, 247, 251))
    lab = T("ENDS IN", 24, GREY_TXT, 700, True)
    if not ended: tc.alpha_composite(lab, (int(280 - lab.width / 2), 28))
    tv = clock_txt(sec, 130, RED_UI if (sec <= 10 or ended) else L_INK); tc.alpha_composite(tv, (int(280 - tv.width / 2), 62))
    if added_t is not None and t >= added_t:
        ap = fade_l(pill("+ time added", 26, VIOLET, padx=16, pady=6), spring((t - added_t) / 0.35)); tc.alpha_composite(ap, (int(280 - ap.width / 2), 214))
    p.alpha_composite(tc, (40, 400))
    p.alpha_composite(T("BIDS", 22, GREY_TXT, 700, True), (60, 690))
    y = 730
    for (ti, who, amt) in reversed(vis[-3:]):
        k = spring((t - ti) / 0.35); row = Image.new("RGBA", (560, 120), (0, 0, 0, 0))
        row.alpha_composite(head(who, 76), (0, 20)); nm = "Nour" if who == "nour" else f"Bidder {who[0]}"
        row.alpha_composite(T(nm, 34, L_INK, 600), (100, 40)); a = T(money(amt), 44, L_INK, 700); row.alpha_composite(a, (540 - a.width, 34))
        p.alpha_composite(fade_l(row, k), (40, int(y + (1 - k) * 30))); y += 125
    if stamp_t is not None and t >= stamp_t:
        sp = big_stamp("ENDED", (150, 155, 166), 80, -6); sk = 1 + 0.5 * (1 - eout((t - stamp_t) / 0.22))
        sp = sp.resize((int(sp.width * sk), int(sp.height * sk)), Image.LANCZOS); sp.putalpha(sp.getchannel("A").point(lambda q: int(q * min(1, (t - stamp_t) / 0.06))))
        p.alpha_composite(sp, (int(pw / 2 - sp.width / 2), int(535 - sp.height / 2)))
    return p

def grid(t, t_on, hi=((None, 0, VIOLET),), dark=False, cols=20, rows=12, cell=34, gap=8):
    """240 small squares = 240 auctions; hi = [(start time, count, colour)] lights up the first `count` squares"""
    w = cols * (cell + gap) - gap; h = rows * (cell + gap) - gap; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    base = (52, 58, 76) if dark else (222, 225, 234)
    for i in range(cols * rows):
        k = clamp((t - t_on - i * 0.0035) / 0.15)
        if k <= 0: continue
        col = base
        for (th, n, c) in hi:
            if th is not None and t >= th + i * 0.006 and i < n: col = c
        x, y = (i % cols) * (cell + gap), (i // cols) * (cell + gap); r = cell * (0.6 + 0.4 * k) / 2
        d.rounded_rectangle((x + cell / 2 - r, y + cell / 2 - r, x + cell / 2 + r, y + cell / 2 + r), radius=8, fill=col + (int(255 * k),))
    return im

# ---------- scenes ----------
HOOK_BIDS = lambda: ((-9, R_, 160), (-8, "nour", 180), (WT("h1", "second.") - 0.25, M_, 190))
def sc_hook(t):
    im = bg(False); te = WT("h1", "second.") + 0.1
    sec = max(0.01, te - t) if t < te else 0
    put(im, lift(auction_phone(t, HOOK_BIDS(), sec, ended=t >= te, stamp_t=te + 0.15)), 540, 1170, 1, 0.97 + 0.03 * spring(t / 0.5))
    if t < WT("h1", "second.") - 0.3:
        put(im, pill("Leading for 3 days", 34, GREEN_UI, padx=24, pady=10), 540, 525)
    footnote(im, "Example auction · item, bids and names illustrative", False, 1850)
    return im

def sc_ended(t):
    im = bg(True); t0 = S("p1"); ta = WT("p1", "answer."); tz = WT("p1", "zero.")
    k = spring((t - t0 + 0.1) / 0.4)
    c = card(820, 560, True, 30); lab = T("AUCTION ENDED", 30, D_MUTE, 700, True); c.alpha_composite(lab, (int(410 - lab.width / 2), 50))
    tv = clock_txt(0, 220, RED_UI); c.alpha_composite(tv, (int(410 - tv.width / 2), 110))
    shake = 0
    if t >= ta: shake = int(14 * np.sin((t - ta) * 60) * max(0, 1 - (t - ta) / 0.4))
    bt = pill("Bid again", 46, (60, 66, 84), (140, 146, 160), padx=60, pady=20, r=24); c.alpha_composite(bt, (int(410 - bt.width / 2) + shake, 400))
    put(im, lift(c, True), 540, 1050 + (1 - k) * 40, min(1, k * 1.5), 0.94 + 0.06 * k)
    put(im, head("nour", 150), 540, 640 + (1 - k) * 40, min(1, k * 1.5))
    cx = 800 - 240 * eout((t - t0) / max(0.3, ta - t0 - 0.1)); cy = 1480 - 260 * eout((t - t0) / max(0.3, ta - t0 - 0.1))
    put(im, cursor(), cx + 20, cy + 30); ripple(im, 555, 1212, (t - ta) / 0.5, RED_UI)
    footnote(im, "Illustrative", True, 1850)
    return im

def sc_study(t):
    im = bg(False); t0 = S("s1"); t240 = WT("s1", "240"); tf = WT("s1", "fixed")
    w, h = 940, 860; win = window(w, h, "Last-minute bidding study · 2002", False)
    g = grid(t, t240 - 0.15); win.alpha_composite(g, (int(w / 2 - g.width / 2), 130))
    kn = spring((t - t240 + 0.1) / 0.4)
    if kn > 0:
        tv = fade_l(T(f"{int(roll(t, t240 - 0.1, 0.9, 0, 240))} auctions", 64, L_INK, 700), kn); win.alpha_composite(tv, (int(w / 2 - tv.width / 2), 660))
    if t >= tf - 0.1:
        ch = fade_l(pill("Fixed end time", 34, BLUE, padx=26, pady=10), spring((t - tf + 0.1) / 0.4)); win.alpha_composite(ch, (int(w / 2 - ch.width / 2), 760))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Roth & Ockenfels, American Economic Review, 2002", False, 1850)
    return im

def sc_result(t):
    im = bg(True); t89 = WT("s2", "89"); t29 = WT("s2", "29"); tten = WT("s2", "ten")
    first = t < t29 - 0.15
    c = card(900, 1000, True, 30)
    if first:
        v = roll(t, t89 - 0.1, 0.9, 0, 89); lab = T("HAD BIDS IN THE LAST MINUTE", 30, D_MUTE, 700, True); col = LILAC
    else:
        v = roll(t, t29 - 0.1, 0.8, 89, 29); lab = T("HAD BIDS IN THE LAST 10 SECONDS", 30, D_MUTE, 700, True); col = RED_UI
    c.alpha_composite(lab, (int(450 - lab.width / 2), 50)); tv = T(f"{v:.0f}", 230, col, 700); c.alpha_composite(tv, (int(450 - tv.width / 2), 100))
    hi = ((t89, 89, VIOLET),) if first else ((-99, 89, (70, 64, 120)), (t29, 29, RED_UI))
    g = grid(t, -99, hi, True); c.alpha_composite(g, (int(450 - g.width / 2), 430))
    sub = T("out of 240 auctions", 32, D_MUTE, 600); c.alpha_composite(sub, (int(450 - sub.width / 2), 940))
    k = spring((t - t89 + 0.25) / 0.45)
    put(im, lift(c, True), 540, 1110 + (1 - k) * 50, min(1, k * 1.5), 0.92 + 0.08 * k)
    footnote(im, "Fixed-end online auctions · Roth & Ockenfels, AER, 2002", True, 1850)
    return im

def sc_rule(t):
    im = bg(False); t0 = S("s3"); tl = WT("s3", "late"); ta = WT("s3", "adds"); t4 = S("s4"); t1 = WT("s4", "one.")
    if t < t4 - 0.1:
        w, h = 880, 760; win = window(w, h, "Late bid adds time", False)
        if t < ta: sec = max(1, 8 - (t - t0) * 2)
        else: sec = 600 - (t - ta)
        lab = T("ENDS IN", 26, GREY_TXT, 700, True); win.alpha_composite(lab, (int(w / 2 - lab.width / 2), 120))
        tv = clock_txt(sec, 190, RED_UI if sec <= 10 else L_INK); win.alpha_composite(tv, (int(w / 2 - tv.width / 2), 170))
        if t >= ta: win.alpha_composite(fade_l(pill("+ time added", 36, VIOLET, padx=26, pady=10), spring((t - ta) / 0.35)), (int(w / 2 - 140), 410))
        if t >= tl - 0.1:
            kb = spring((t - tl + 0.1) / 0.35); row = Image.new("RGBA", (600, 120), (0, 0, 0, 0)); row.alpha_composite(head(M_, 90), (0, 15))
            row.alpha_composite(T("Late bid", 40, L_INK, 600), (120, 36)); a = T("$190", 50, L_INK, 700); row.alpha_composite(a, (600 - a.width, 30))
            win.alpha_composite(fade_l(row, kb), (140, int(560 + (1 - kb) * 30)))
        k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
        footnote(im, "In the study, the clock ran until 10 minutes passed without a bid", False, 1850)
    else:
        k = spring((t - t4 + 0.1) / 0.45); c = card(860, 720, False, 30)
        lab = T("BIDS IN THE LAST MINUTE", 30, GREY_TXT, 700, True); c.alpha_composite(lab, (int(430 - lab.width / 2), 50))
        r1 = T("Fixed end:  89", 52, (150, 155, 166), 600); c.alpha_composite(r1, (int(430 - r1.width / 2), 120))
        r2 = T("Time added:", 52, L_INK, 600); c.alpha_composite(r2, (int(430 - r2.width / 2), 230))
        if t < t1 - 0.15: q = T("?", 300, (210, 213, 222), 700); c.alpha_composite(q, (int(430 - q.width / 2), 310))
        if t >= t1 - 0.15:
            kv = spring((t - t1 + 0.15) / 0.4); v = fade_l(T("1", 300, GREEN_UI, 700), kv); c.alpha_composite(v, (int(430 - v.width / 2), int(310 + (1 - kv) * 30)))
        put(im, lift(c), 540, 1110 + (1 - k) * 40, min(1, k * 1.5), 0.94 + 0.06 * k)
        if t >= WT("s4", "Bids") + 0.1: strike(im, 540 - 190, 1110 - 360 + 120 + 32, 540 + 190, eout((t - WT("s4", "Bids") - 0.1) / 0.3), RED_UI, 8)
        footnote(im, "240 auctions of each kind · Roth & Ockenfels, AER, 2002", False, 1850)
    return im

def sc_skill(t):
    im = bg(True); t0 = S("f1"); ts = WT("f1", "skill."); tr = WT("f1", "rule.")
    k1 = spring((t - t0 + 0.1) / 0.4)
    r1 = card(860, 220, True, 28); r1.alpha_composite(T("A last-second win", 40, D_MUTE, 600), (60, 34)); r1.alpha_composite(T("= skill", 80, D_INK, 700), (60, 96))
    if t >= ts + 0.1: r1.putalpha(r1.getchannel("A").point(lambda q: int(q * (1 - 0.45 * clamp((t - ts - 0.1) / 0.3)))))
    put(im, lift(r1, True), 540, 820 + (1 - k1) * 30, min(1, k1 * 1.5))
    if t >= ts + 0.05: strike(im, 540 - 370, 820 + 30, 540 - 370 + 330, eout((t - ts - 0.05) / 0.25), RED_UI, 10)
    k2 = spring((t - tr + 0.25) / 0.4)
    if k2 > 0:
        r2 = card(860, 220, True, 28); r2.alpha_composite(T("A last-second win", 40, D_MUTE, 600), (60, 34)); r2.alpha_composite(T("= the rule", 80, LILAC, 700), (60, 96))
        put(im, lift(r2, True), 540, 1130 + (1 - k2) * 40, min(1, k2 * 1.5), 0.94 + 0.06 * k2)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("f2"); tl = WT("f2", "late"); ta = WT("f2", "bid,") + 0.2; tb = WT("f2", "back.")
    bids = ((-9, R_, 160), (-8, "nour", 180), (tl - 0.1, M_, 190), (tb - 0.1, "nour", 200))
    sec = max(1, 3 - (t - t0)) if t < ta else 600 - (t - ta)
    put(im, lift(auction_phone(t, bids, sec, added_t=ta)), 540, 1170, ease((t - t0 + 0.1) / 0.2))
    footnote(im, "Example auction · item, bids and names illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 13, BLUE), (540, 89, VIOLET), (750, 29, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "ended": sc_ended, "study": sc_study, "result": sc_result, "rule": sc_rule, "skill": sc_skill, "loop": sc_loop, "outro": sc_outro}

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
    te = WT("h1", "second.") + 0.1
    for i in range(int(te / 1.0)): s.tick(te - 1.0 * (i + 1), 0.025)
    s.pop(WT("h1", "second.") - 0.25, 0.04, 640); s.thud(te + 0.15, 0.08)
    s.thud(WT("p1", "answer."), 0.06); s.thud(WT("p1", "zero."), 0.05)
    for i in range(10): s.tick(WT("s1", "240") - 0.15 + i * 0.09, 0.012)
    s.pop(WT("s1", "fixed") - 0.1, 0.035, 600)
    for i in range(6): s.tick(WT("s2", "89") - 0.1 + i * 0.13, 0.02)
    s.ding(WT("s2", "89") + 0.8, 1568, 0.03)
    for i in range(6): s.tick(WT("s2", "29") - 0.1 + i * 0.12, 0.02)
    s.ding(WT("s2", "ten") + 0.2, 1318, 0.03)
    s.pop(WT("s3", "late") - 0.1, 0.035, 620); s.ding(WT("s3", "adds"), 1568, 0.03)
    s.pop(S("s4") - 0.1, 0.035, 560); s.thud(WT("s4", "one.") - 0.15, 0.08); s.ding(WT("s4", "one.") - 0.1, 1568, 0.035)
    s.thud(WT("f1", "skill.") + 0.05, 0.06); s.pop(WT("f1", "rule.") - 0.25, 0.035, 620)
    s.pop(WT("f2", "late") - 0.1, 0.035, 600); s.ding(WT("f2", "bid,") + 0.2, 1318, 0.025); s.pop(WT("f2", "back.") - 0.1, 0.04, 680)
    s.ding(WT("tk", "answer."), 1568, 0.025)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson13_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
