"""Auction short 04: "How a Lebanese court auction works" (CCP Arts. 965, 973, 975, 976). v3 style: word-by-word captions +
UI cards, light/dark scenes, whip transitions. No HyperBidz, no app UI. Neutral: explains how the law works, blames no one.
Run: python3 tools/lessons/lesson04.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson04_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "pluck", 4
XF = 0.16
SC = [("hook", True, 0.0, S("s0") - 0.1), ("steps", False, S("s0") - 0.1, S("s1") - 0.1), ("value", True, S("s1") - 0.1, S("s2") - 0.1),
      ("open", False, S("s2") - 0.1, S("s3") - 0.1), ("deposit", True, S("s3") - 0.1, S("s4") - 0.1), ("session", False, S("s4") - 0.1, S("b3") - 0.1),
      ("timer", True, S("b3") - 0.1, S("t1") - 0.1), ("lower", False, S("t1") - 0.1, S("e0") - 0.1), ("law", True, S("e0") - 0.1, S("e1") - 0.1),
      ("outro", True, S("e1") - 0.1, TOTAL)]

def pop_in(t, t0, d=0.4): return ease((t - t0) / 0.18), 0.85 + 0.15 * spring((t - t0) / d)

# ---------- props ----------
def building(w=300, h=380, dark=True):
    """a generic apartment block (no real address)"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 20, w - 1, h - 1), radius=18, fill=(BLUE if dark else (214, 226, 255)) + (255,))
    d.rectangle((w * 0.1, 0, w * 0.9, 34), fill=((36, 92, 200) if dark else (190, 206, 245)) + (255,))
    for r in range(5):
        for c in range(3):
            x = 34 + c * (w - 68) / 3 + 10; y = 56 + r * 58
            d.rounded_rectangle((x, y, x + (w - 68) / 3 - 20, y + 38), radius=6, fill=((255, 226, 150) if (r * 3 + c) % 4 == 1 else (24, 40, 86)) + (255,))
    d.rounded_rectangle((w / 2 - 34, h - 74, w / 2 + 34, h - 1), radius=8, fill=(24, 40, 86, 255)); return im

def bar(w, frac, k, dark, label="", col=VIOLET):
    c = card(w, 74, dark, 37); d = ImageDraw.Draw(c)
    d.rounded_rectangle((7, 7, 7 + (w - 14) * frac * clamp(k), 66), radius=31, fill=col + (255,)) if k > 0.02 else None
    if label: tt = T(label, 28, (255, 255, 255) if k > 0.5 else (D_MUTE if dark else (110, 116, 130)), 700); c.alpha_composite(tt, (34, 37 - tt.height // 2))
    return c

def gavel(s=170):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); g = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    d.rounded_rectangle((s * 0.18, s * 0.2, s * 0.72, s * 0.44), radius=12, fill=(120, 86, 60, 255))
    d.rounded_rectangle((s * 0.4, s * 0.4, s * 0.5, s * 0.92), radius=6, fill=(150, 110, 78, 255))
    im.alpha_composite(g.rotate(-30, resample=Image.BICUBIC, center=(s / 2, s / 2))); return im

def bid_row(who, name, amount, w=760, hl=False, dim=False, dark=False):
    c = card(w, 118, dark, 24, fill=((233, 250, 241) if hl else (250, 250, 252)) if not dark else ((18, 52, 40) if hl else CARD_D))
    c.alpha_composite(head(who, 74), (22, 22)); ink = (170, 174, 184) if dim else (D_INK if dark else L_INK)
    c.alpha_composite(T(name, 36, ink, 600), (118, 38)); tt = T(amount, 46, ink, 700); c.alpha_composite(tt, (w - tt.width - 30, 30)); return c

# ---------- 1. hook: 60% of the valuation, then a 15-minute clock ----------
def sc_hook(t):
    im = bg(True); w, h = 900, 980; win = window(w, h, "Court auction · apartment", True)
    b = building(300, 380, True); win.alpha_composite(b, (int(w / 2 - 150), 110))
    t6 = 0.6; k = eout((t - t6 + 0.5) / 0.8)
    win.alpha_composite(T("VALUATION", 24, D_MUTE, 700, True), (60, 540)); win.alpha_composite(bar(w - 120, 1.0, 1.0, True, "100%", (60, 66, 86)), (60, 580))
    win.alpha_composite(T("OPENING PRICE", 24, D_MUTE, 700, True), (60, 690)); win.alpha_composite(bar(w - 120, 0.6, k, True, "", VIOLET), (60, 730))
    v = roll(t, t6 - 0.5, 0.8, 0, 60); vt = T(f"{v:.0f}%", 120, (255, 255, 255), 700)
    if t >= t6 - 0.5: win.alpha_composite(vt, (int(60 + (w - 120) * 0.6 * k - vt.width - 10) if k > 0.5 else 70, 830))
    put(im, lift(win, True), 540, 1010, 1.0, 0.97 + 0.03 * spring(t / 0.5))
    tc = WT("h2", "clock")
    if t >= tc:
        al, sc = pop_in(t, tc); put(im, pill("15:00", 56, GREEN_UI), 540 + 300, 1010 - 300, al, sc)
    footnote(im, "Lebanese Code of Civil Procedure, Arts. 965 and 976", True, 1560)
    return im

# ---------- 2. four steps ----------
STEPS = ["Valuation", "Opening price", "Deposit", "Public bidding"]
def sc_steps(t):
    im = bg(False); t0 = S("s0")
    for i, s in enumerate(STEPS):
        k = spring((t - t0 - 0.15 - i * 0.16) / 0.4)
        if k <= 0: continue
        c = card(760, 130, False, 28); num = pill(str(i + 1), 44, VIOLET, padx=30); c.alpha_composite(num, (26, 65 - num.height // 2))
        c.alpha_composite(T(s, 50, L_INK, 700), (130, 36)); put(im, lift(c), 540 + (1 - k) * 200, 680 + i * 170, min(1, k * 1.6))
    return im

# ---------- 3. step one: valued ----------
def sc_value(t):
    im = bg(True); put(im, lift(building(300, 380, True), True), 540, 760, ease((t - S("s1") + 0.1) / 0.25), 0.9 + 0.1 * spring((t - S("s1") + 0.1) / 0.5))
    tv = WT("s1", "valued")
    if t >= tv - 0.1:
        al, sc = pop_in(t, tv - 0.1); put(im, select_box_layer((300 + 40, 380 + 40)), 540, 760, al)
    t2 = WT("s1", "$200"); v = roll(t, t2 - 0.3, 0.8, 0, 200_000)
    if t >= tv:
        st = stat("Estimated value", money(v), "", 760, True, 110); put(im, lift(st, True), 540, 1220, ease((t - tv) / 0.25))
    footnote(im, "Amounts are illustrative", True, 1500)
    return im

def select_box_layer(size):
    w, h = size; lay = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((10, 10, w + 9, h + 9), outline=VIOLET + (255,), width=3)
    for hx, hy in ((10, 10), (w + 9, 10), (10, h + 9), (w + 9, h + 9)): d.rectangle((hx - 7, hy - 7, hx + 7, hy + 7), fill=(255, 255, 255, 255), outline=VIOLET + (255,), width=3)
    return lay

# ---------- 4. step two: opening price = six tenths ----------
def sc_open(t):
    im = bg(False); t0 = S("s2"); ts, t12 = WT("s2", "six"), WT("s2", "$120")
    v = 200_000 - 80_000 * eout((t - t12 + 0.4) / 0.8) if t >= t12 - 0.4 else 200_000
    st = stat("Opening price", money(v), "six tenths of the valuation", 860, False, 130, VIOLET if t >= t12 else None)
    put(im, lift(st), 540, 860, ease((t - t0 + 0.1) / 0.25), 0.95 + 0.05 * spring((t - t0 + 0.1) / 0.5))
    # ten blocks, six of them light up
    for i in range(10):
        on = ease((t - ts - i * 0.06) / 0.15) if i < 6 else 0; x = 540 - 4.5 * 84 + i * 84
        c = card(70, 70, False, 14, fill=VIOLET if on > 0.5 else (226, 227, 234), border=False); put(im, c, x, 1170, ease((t - t0) / 0.3))
    if t >= ts: put(im, T("6 / 10", 56, VIOLET, 700), 540, 1290, ease((t - ts - 0.4) / 0.2))
    footnote(im, "CCP Art. 965 · amounts are illustrative")
    return im

# ---------- 5. step three: Nour deposits the opening price ----------
def sc_deposit(t):
    im = bg(True); w, h = 860, 640; win = window(w, h, "Deposit to bid", True); t0 = S("s3"); td, tg = WT("s3", "deposits"), WT("s3", "guarantee")
    r = bid_row("nour", "Nour", money(roll(t, td - 0.2, 0.7, 0, 120_000)), 760, t >= td + 0.6, False, True); win.alpha_composite(r, (50, 110))
    win.alpha_composite(T("= the full opening price", 32, D_MUTE, 600), (60, 260))
    if t >= td + 0.6:
        p = pill("READY TO BID", 40, GREEN_UI); win.alpha_composite(p, (int(w / 2 - p.width / 2), 340))
    if t >= tg - 0.15:
        c = pill("or a bank guarantee", 34, PILL_D, LILAC); kk = ease((t - tg + 0.15) / 0.2); c2 = c.copy(); c2.putalpha(c2.getchannel("A").point(lambda a: int(a * kk)))
        win.alpha_composite(c2, (int(w / 2 - c.width / 2), 470))
    put(im, lift(win, True), 540, 960, ease((t - t0 + 0.1) / 0.25), 0.95 + 0.05 * spring((t - t0 + 0.1) / 0.5))
    footnote(im, "CCP Art. 973 · amount is illustrative", True, 1400)
    return im

# ---------- 6. step four: public bidding before the judge ----------
def sc_session(t):
    im = bg(False); t0 = S("s4")
    if t < S("b1") - 0.05:                                                         # the public session
        put(im, lift(gavel(260)), 540, 860, *pop_in(t, WT("s4", "bidding")))
        tp = WT("s4", "public")
        if t >= tp: put(im, pill("PUBLIC SESSION", 46, VIOLET), 540, 1110, *pop_in(t, tp))
        tj = WT("s4", "judge")
        if t >= tj: put(im, chip("before the judge", False, 30), 540, 1210, ease((t - tj) / 0.2))
        return im
    w, h = 880, 860; win = window(w, h, "Public session", False); tc = WT("b1", "calls")
    win.alpha_composite(head("sami", 96), (50, 100)); win.alpha_composite(T("Sami · crier", 30, (110, 116, 130), 600), (164, 128))
    if t >= tc:
        bb = bubble("$120,000!", 44, (236, 237, 242), L_INK); kk = ease((t - tc) / 0.15); bb2 = bb.copy(); bb2.putalpha(bb2.getchannel("A").point(lambda a: int(a * kk)))
        win.alpha_composite(bb2, (w - bb.width - 50, 100))
    tb, tn, tx = WT("b2", "bidder"), WT("b2", "Nour"), WT("b2", "cancels")
    if t >= tb:
        k = spring((t - tb) / 0.4); r = bid_row(("27", GREEN_APP), "Bidder 27", "$125,000", 780, t < tn, t >= tx, False)
        win.alpha_composite(r, (50, int(300 + (1 - k) * 40)))
        if t >= tx:
            lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); strike(lay, 70, 359, 810, eout((t - tx) / 0.3), RED_UI, 8); win.alpha_composite(lay)
    if t >= tn:
        k = spring((t - tn) / 0.4); r = bid_row("nour", "Nour", "$130,000", 780, True, False, False); win.alpha_composite(r, (50, int(450 + (1 - k) * 40)))
    put(im, lift(win), 540, 980, ease((t - S("b1") + 0.05) / 0.2))
    if t >= tx: put(im, pill("each bid cancels the one before", 36, RED_UI), 540, 1300, *pop_in(t, tx))
    footnote(im, "CCP Art. 975 · bids are illustrative")
    return im

# ---------- 7. fifteen minutes, then the last highest bid wins ----------
def sc_timer(t):
    im = bg(True); t0 = S("b3"); ta, tl_, tw = WT("b3", "After"), WT("b3", "last"), WT("b3", "wins")
    left = 15 * 60 * (1 - eout((t - ta) / max(0.4, tl_ - ta))) if t >= ta else 900
    s = 500; ring = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(ring)
    d.ellipse((0, 0, s - 1, s - 1), outline=(40, 46, 60, 255), width=24)
    if left > 1: d.arc((0, 0, s - 1, s - 1), -90, -90 + 360 * left / 900, fill=VIOLET + (255,), width=24)
    tt = T(f"{int(left // 60):02d}:{int(left % 60):02d}", 120, (255, 255, 255), 700, True); ring.alpha_composite(tt, (s // 2 - tt.width // 2, s // 2 - tt.height // 2))
    put(im, ring, 540, 860, ease((t - t0 + 0.1) / 0.2), 0.95 + 0.05 * spring((t - t0 + 0.1) / 0.5))
    if t >= tl_:
        r = bid_row("nour", "Nour", "$130,000", 760, True, False, True); put(im, lift(r, True), 540, 1270, *pop_in(t, tl_))
    stamp_at(im, big_stamp("SOLD", GREEN_UI, 96, -8), 790, 640, t, tw)
    footnote(im, "CCP Art. 976", True, 1500)
    return im

# ---------- 8. nobody bids: the price is lowered, and it's tried again ----------
def sc_lower(t):
    im = bg(False); t0 = S("t1"); tn, tlw, tag_, tbuy = WT("t1", "nobody"), WT("t1", "lowered"), WT("t1", "again"), WT("t1", "buys")
    old = card(760, 300, False, 30); old.alpha_composite(T("OPENING PRICE", 26, (110, 116, 130), 700, True), (44, 40))
    old.alpha_composite(T("$120,000", 120, L_INK if t < tlw else (170, 174, 184), 700), (44, 90))
    put(im, lift(old), 540, 820, ease((t - t0 + 0.1) / 0.25))
    if t >= tlw: strike(im, 540 - 336, 820 + 40, 540 - 336 + 470, eout((t - tlw) / 0.3), RED_UI, 10)
    if tn <= t < tlw: stamp_at(im, big_stamp("NO BIDS", RED_UI, 80, -8), 760, 690, t, tn + 0.2)
    if t >= tlw + 0.3:
        nw = card(760, 220, False, 30, fill=(246, 244, 255)); nw.alpha_composite(T("NEW, LOWER PRICE", 26, VIOLET, 700, True), (44, 34))
        nw.alpha_composite(T("below $120,000", 72, VIOLET, 700), (44, 92)); put(im, lift(nw), 540, 1110, *pop_in(t, tlw + 0.3))
    if t >= tag_: put(im, pill("NEW SESSION, RE-ADVERTISED", 36, VIOLET), 540, 1330, *pop_in(t, tag_))
    if t >= tbuy: stamp_at(im, big_stamp("SOLD", GREEN_UI, 100, -8), 540, 1500, t, tbuy)
    footnote(im, "CCP Art. 976 · the judge sets the reduction")
    return im

# ---------- 9. it's in the law ----------
def sc_law(t):
    im = bg(True); t0 = S("e0"); tw = WT("e0", "written"); w, h = 760, 900
    doc = card(w, h, True, 26); d = ImageDraw.Draw(doc)
    doc.alpha_composite(T("CODE OF CIVIL PROCEDURE", 26, D_MUTE, 700, True), (50, 50)); doc.alpha_composite(T("Lebanon · Decree-Law 90/1983", 30, D_INK, 600), (50, 96))
    for i, (art, lab) in enumerate((("965", "Opening price"), ("973", "Deposit"), ("975", "Public bidding"), ("976", "15 minutes"))):
        y = 200 + i * 160; on = t >= tw + i * 0.12
        if on: d.rounded_rectangle((36, y - 14, w - 36, y + 118), radius=18, fill=PILL_D + (255,))
        doc.alpha_composite(T(f"Art. {art}", 40, LILAC if on else D_INK, 700), (60, y)); doc.alpha_composite(T(lab, 30, D_MUTE, 600), (60, y + 60))
        for j in range(2): d.rounded_rectangle((380, y + 14 + j * 40, w - 70 - j * 90, y + 32 + j * 40), radius=9, fill=(48, 54, 72, 255))
    put(im, lift(doc, True), 540, 1050, ease((t - t0 + 0.1) / 0.25), 0.95 + 0.05 * spring((t - t0 + 0.1) / 0.5))
    return im

# ---------- 10. why it works + end card ----------
def sc_outro(t):
    im = bg(True)
    if t < S("e2") - 0.1:
        for i, (wd, txt, col) in enumerate((("Open", "Open bidding", BLUE), ("one", "One public price", VIOLET), ("best", "Best offer wins", GREEN_UI))):
            tt = WT("e1", wd)
            if t >= tt - 0.1: put(im, pill(txt, 52, col, padx=34, pady=18), 540, 820 + i * 170, *pop_in(t, tt - 0.1))
    else:
        k = t - S("e2") + 0.1
        for i, (x, n, col) in enumerate(((330, 14, BLUE), (540, 27, VIOLET), (750, 8, GREEN_APP))):
            kk = spring((k - i * 0.12) / 0.45)
            if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
        put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
        fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
        tcl = WT("e2", "stories"); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
        if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
        ripple(im, 560, 1030, (t - tcl) / 0.5)
        if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "steps": sc_steps, "value": sc_value, "open": sc_open, "deposit": sc_deposit, "session": sc_session,
      "timer": sc_timer, "lower": sc_lower, "law": sc_law, "outro": sc_outro}

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
    for i in range(8): s.tick(0.1 + i * 0.08, 0.012, 2600)
    s.pop(WT("h2", "clock"), 0.05, 700); s.ding(0.6, 1175, 0.03)
    for i in range(4): s.pop(S("s0") + 0.15 + i * 0.16, 0.04, 500 + i * 120)
    for i in range(10): s.tick(WT("s1", "$200") - 0.3 + i * 0.08, 0.012, 2600)
    for i in range(6): s.tick(WT("s2", "six") + i * 0.06, 0.015, 1800)
    s.ding(WT("s3", "deposits") + 0.6, 1318, 0.04); s.pop(WT("s3", "guarantee"), 0.04, 800)
    s.thud(WT("s4", "bidding"), 0.06); s.pop(WT("b1", "calls"), 0.05, 600)
    s.pop(WT("b2", "bidder"), 0.04, 650); s.pop(WT("b2", "Nour"), 0.05, 900); s.tick(WT("b2", "cancels"), 0.03, 1200)
    for i in range(16): s.tick(WT("b3", "After") + i * 0.1, 0.01, 2200)
    s.thud(WT("b3", "wins"), 0.09); s.ding(WT("b3", "wins") + 0.05, 1568, 0.035)
    s.thud(WT("t1", "nobody") + 0.2, 0.06); s.pop(WT("t1", "again"), 0.04, 700); s.thud(WT("t1", "buys"), 0.07)
    s.ding(WT("e0", "written"), 1175, 0.03)
    for w_ in ("Open", "one", "best"): s.pop(WT("e1", w_) - 0.1, 0.04, 800)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson04_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
