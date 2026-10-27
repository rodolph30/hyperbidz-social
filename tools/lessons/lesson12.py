"""Auction short 12 (v3, quick, who: Sami): "Is it still available?". Problem: Sami's listing gets "Is it still available?",
"I'll think about it", "Can you hold it till next week?"; days pass and nobody buys. Reframe (one fact): across four bargaining
experiments with a deadline, 41% of agreements came in the last 30 seconds, and 53% of those in the last 5 seconds (Roth,
Murnighan & Schoumaker, AER 1988). Fix: a countdown everyone can see. Takeaway: no deadline, no decision.
Built like L10 v2 / L11: one story from the first frame to the last, one fact.
Run: python3 tools/lessons/lesson12.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson12_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "marimba", 12
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("wait", True, S("p1") - 0.1, S("s1") - 0.1), ("exp", False, S("s1") - 0.1, S("s2") - 0.1),
      ("result", True, S("s2") - 0.1, S("f1") - 0.1), ("decide", False, S("f1") - 0.1, S("f2") - 0.1),
      ("count", True, S("f2") - 0.1, S("tk") - 0.1), ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)

# ---------- drawings ----------
def bike(w=200, col=BLUE, ink=(24, 28, 44)):
    S2 = 2; h = int(w * 0.62); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    r = H2 * 0.32; lw = max(4, int(W2 * 0.03)); c = ink + (255,); f = col + (255,)
    a, b = (W2 * 0.22, H2 * 0.64), (W2 * 0.78, H2 * 0.64)
    for (x, y) in (a, b): d.ellipse((x - r, y - r, x + r, y + r), outline=c, width=lw)
    seat, bar, crank = (W2 * 0.4, H2 * 0.22), (W2 * 0.7, H2 * 0.16), (W2 * 0.48, H2 * 0.64)
    for p, q in ((a, crank), (crank, seat), (seat, a), (seat, (W2 * 0.68, H2 * 0.3)), ((W2 * 0.68, H2 * 0.3), crank), ((W2 * 0.68, H2 * 0.3), b), ((W2 * 0.68, H2 * 0.3), bar)):
        d.line([p, q], fill=f, width=lw + 2)
    d.rounded_rectangle((seat[0] - W2 * 0.07, seat[1] - H2 * 0.05, seat[0] + W2 * 0.06, seat[1] + H2 * 0.01), radius=8, fill=c)
    d.line([(bar[0] - W2 * 0.04, bar[1]), (bar[0] + W2 * 0.07, bar[1] - H2 * 0.02)], fill=c, width=lw + 2)
    return im.resize((w, h), Image.LANCZOS)

def bubble(text, size=40, fill=(236, 237, 242), col=L_INK, right=False):
    tt = T(text, size, col, 600); w, h = tt.width + 56, tt.height + 36
    im = Image.new("RGBA", (w, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=fill + (255,))
    if right: d.polygon([(w - 26, h - 10), (w - 18, h + 12), (w - 58, h - 10)], fill=fill + (255,))
    else: d.polygon([(26, h - 10), (18, h + 12), (58, h - 10)], fill=fill + (255,))
    im.alpha_composite(tt, (28, 18)); return im

def timer(sec, size=150, col=L_INK):
    sec = max(0, int(np.ceil(sec - 1e-6))); return T(f"{sec // 60}:{sec % 60:02d}", size, col, 700, True)

BUYERS = (("R", VIOLET), ("M", GREEN_APP), ("J", SILVER))
def inbox_phone(t, msg_times, reply_t=None, stamp_t=None):
    """Sami's phone: his listing, then buyers' messages. Shared by the hook and the loop scene, so the replay is seamless."""
    pw, ph = 640, 1180; p = phone(pw, ph, False)
    lc = card(560, 250, False, 26, fill=(246, 247, 251)); lc.alpha_composite(bike(190), (30, 66))
    lc.alpha_composite(T("Bike · like new", 36, L_INK, 600), (250, 50)); lc.alpha_composite(T("$300", 84, L_INK, 700), (250, 100))
    lc.alpha_composite(head("sami", 44), (250, 196 - 10)); lc.alpha_composite(T("Sami", 28, GREY_TXT, 600), (304, 192 - 10))
    p.alpha_composite(lc, (40, 100))
    p.alpha_composite(T("MESSAGES", 22, GREY_TXT, 700, True), (60, 380))
    y = 425
    for i, ti in enumerate(msg_times):
        k = spring((t - ti) / 0.35)
        if k <= 0: continue
        nm, col = BUYERS[i % 3]; row = Image.new("RGBA", (560, 120), (0, 0, 0, 0)); row.alpha_composite(head((nm, col), 64), (0, 24))
        row.alpha_composite(bubble("Is it still available?", 38), (80, 6))
        row.putalpha(row.getchannel("A").point(lambda q: int(q * min(1, k * 1.5)))); p.alpha_composite(row, (40, int(y + (1 - k) * 30))); y += 130
    if reply_t is not None and t >= reply_t:
        k = spring((t - reply_t) / 0.4); b = bubble("Bidding ends Friday, 7 pm", 36, BLUE, (255, 255, 255), True)
        b.putalpha(b.getchannel("A").point(lambda q: int(q * min(1, k * 1.5)))); p.alpha_composite(b, (pw - 40 - b.width, int(y + 10 + (1 - k) * 30))); y += 120
    if stamp_t is not None and t >= stamp_t:
        st = big_stamp("NOT SOLD", (150, 155, 166), 70, -6); sk = 1 + 0.5 * (1 - eout((t - stamp_t) / 0.22))
        st = st.resize((int(st.width * sk), int(st.height * sk)), Image.LANCZOS); st.putalpha(st.getchannel("A").point(lambda q: int(q * min(1, (t - stamp_t) / 0.06))))
        p.alpha_composite(st, (int(pw / 2 - st.width / 2), int(min(y, 900) + 20 - (st.height - 120) / 2)))
    return p

# ---------- scenes ----------
HOOK_MSGS = lambda: (-1.0, WT("h1", "every") - 0.1, WT("h1", "day.") - 0.05)
def sc_hook(t):
    im = bg(False)
    put(im, lift(inbox_phone(t, HOOK_MSGS(), stamp_t=WT("h1", "buys."))), 540, 1170, 1, 0.97 + 0.03 * spring(t / 0.5))
    footnote(im, "Bike, price and messages are illustrative", False, 1850)
    return im

def sc_wait(t):
    im = bg(True); t0 = S("p1"); tk_ = WT("p1", "think"); th = WT("p1", "hold"); td = WT("p1", "Days")
    if t < td - 0.15:
        for i, (ti, txt, nm) in enumerate(((tk_ - 0.15, "I'll think about it.", BUYERS[1]), (th - 0.15, "Can you hold it till next week?", BUYERS[2]))):
            k = spring((t - ti) / 0.35)
            if k <= 0: continue
            row = Image.new("RGBA", (900, 150), (0, 0, 0, 0)); row.alpha_composite(head(nm, 90), (0, 30))
            row.alpha_composite(bubble(txt, 50, (30, 36, 52), D_INK), (110, 10))
            put(im, row, 540 + 0, 920 + i * 230 + (1 - k) * 30, min(1, k * 1.5))
    else:
        k = spring((t - td + 0.15) / 0.45); d = int(round(roll(t, td - 0.1, 1.0, 1, 12)))
        c = stat("Days listed", f"Day {d}", "Still no buyer", 760, True, 190)
        put(im, lift(c, True), 540, 1080 + (1 - k) * 50, min(1, k * 1.5), 0.92 + 0.08 * k)
        put(im, head("sami", 120), 540 + 300, 880 + (1 - k) * 50, min(1, k * 1.5))
    footnote(im, "Illustrative", True, 1850)
    return im

def sc_exp(t):
    im = bg(False); t0 = S("s1"); tpp = WT("s1", "people"); tdl = WT("s1", "deadline,"); t4 = WT("s1", "four")
    w, h = 900, 900; win = window(w, h, "Bargaining experiments · 1988", False)
    for i, (nm, col, txt) in enumerate((("A", SILVER, "$8?"), ("B", GREEN_APP, "$12?"))):
        k = spring((t - tpp + 0.1 - i * 0.15) / 0.35)
        if k <= 0: continue
        row = Image.new("RGBA", (420, 220), (0, 0, 0, 0)); row.alpha_composite(head((nm, col), 110), (155, 0))
        bb = bubble(txt, 40); row.alpha_composite(bb, (int(210 - bb.width / 2), 128))
        row.putalpha(row.getchannel("A").point(lambda q: int(q * min(1, k * 1.5)))); win.alpha_composite(row, (20 + i * 440, int(110 + (1 - k) * 30)))
    kc = spring((t - tdl + 0.15) / 0.4)
    if kc > 0:
        sec = 540 - 510 * clamp((t - tdl) / (S("s2") - tdl))       # the on-screen clock runs down towards the deadline
        c = card(560, 330, False, 28, fill=(246, 247, 251)); lab = T("TIME LEFT", 26, GREY_TXT, 700, True); c.alpha_composite(lab, (int(280 - lab.width / 2), 40))
        tv = timer(sec, 170, RED_UI if sec <= 30 else L_INK); c.alpha_composite(tv, (int(280 - tv.width / 2), 100))
        c.putalpha(c.getchannel("A").point(lambda q: int(q * min(1, kc * 1.5)))); win.alpha_composite(c, (170, int(400 + (1 - kc) * 30)))
    if t >= t4 - 0.1:
        kk = spring((t - t4 + 0.1) / 0.4); ch = pill("4 experiments", 36, VIOLET, padx=30, pady=12)
        ch.putalpha(ch.getchannel("A").point(lambda q: int(q * min(1, kk * 1.5)))); win.alpha_composite(ch, (int(w / 2 - ch.width / 2), 780))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Roth, Murnighan & Schoumaker, American Economic Review, 1988 · offers illustrative", False, 1850)
    return im

def sc_result(t):
    im = bg(True); t41 = WT("s2", "41%"); tm = WT("s2", "More"); tf = WT("s2", "five")
    if t < tm - 0.15:
        k = spring((t - t41 + 0.15) / 0.45); v = roll(t, t41 - 0.1, 0.9, 0, 41)
        c = card(860, 600, True, 30); lab = T("OF ALL THE DEALS", 30, D_MUTE, 700, True); c.alpha_composite(lab, (int(430 - lab.width / 2), 60))
        tv = T(f"{v:.0f}%", 240, LILAC, 700); c.alpha_composite(tv, (int(430 - tv.width / 2), 120))
        if t >= WT("s2", "last") - 0.1:
            kk = spring((t - WT("s2", "last") + 0.1) / 0.4); pp = pill("in the last 30 seconds", 44, VIOLET, padx=30, pady=14)
            pp.putalpha(pp.getchannel("A").point(lambda q: int(q * min(1, kk * 1.5)))); c.alpha_composite(pp, (int(430 - pp.width / 2), 450))
        put(im, lift(c, True), 540, 1080 + (1 - k) * 50, min(1, k * 1.5), 0.92 + 0.08 * k)
    else:
        k = spring((t - tm + 0.15) / 0.45); v = roll(t, tm, 0.9, 0, 53)
        c = card(860, 600, True, 30); lab = T("OF THOSE LATE DEALS", 30, D_MUTE, 700, True); c.alpha_composite(lab, (int(430 - lab.width / 2), 60))
        tv = T(f"{v:.0f}%", 240, GREEN_UI, 700); c.alpha_composite(tv, (int(430 - tv.width / 2), 120))
        if t >= tf - 0.15:
            kk = spring((t - tf + 0.15) / 0.4); pp = pill("in the last 5 seconds", 44, RED_UI, padx=30, pady=14)
            pp.putalpha(pp.getchannel("A").point(lambda q: int(q * min(1, kk * 1.5)))); c.alpha_composite(pp, (int(430 - pp.width / 2), 450))
        put(im, lift(c, True), 540, 1080 + (1 - k) * 50, min(1, k * 1.5), 0.92 + 0.08 * k)
    footnote(im, "Agreements in 4 bargaining experiments · Roth, Murnighan & Schoumaker, AER, 1988", True, 1850)
    return im

def sc_decide(t):
    im = bg(False); t0 = S("f1"); tr = WT("f1", "ready."); tt_ = WT("f1", "time")
    k1 = spring((t - t0 + 0.1) / 0.4)
    r1 = card(860, 200, False, 28); r1.alpha_composite(T("When they're ready", 64, L_INK, 700), (60, 60))
    if t >= tr + 0.1: r1.putalpha(r1.getchannel("A").point(lambda q: int(q * (1 - 0.45 * clamp((t - tr - 0.1) / 0.3)))))
    put(im, lift(r1), 540, 820 + (1 - k1) * 30, min(1, k1 * 1.5))
    if t >= tr + 0.05: strike(im, 540 - 330, 820, 540 + 250, eout((t - tr - 0.05) / 0.25), RED_UI, 10)
    k2 = spring((t - tt_ + 0.2) / 0.4)
    if k2 > 0:
        r2 = card(860, 400, False, 28); r2.alpha_composite(T("When time runs out", 64, L_INK, 700), (60, 50))
        tv = timer(3 - 3 * clamp((t - tt_) / 1.2), 160, RED_UI); r2.alpha_composite(tv, (int(430 - tv.width / 2), 170))
        put(im, lift(r2), 540, 1180 + (1 - k2) * 40, min(1, k2 * 1.5), 0.94 + 0.06 * k2)
    return im

def sc_count(t):
    im = bg(True); t0 = S("f2"); tc = WT("f2", "countdown."); tz = WT("f2", "zero,"); tdc = WT("f2", "decided.")
    w, h = 880, 1000; c = window(w, h, "Live auction", True)
    lc = card(800, 220, True, 24, fill=(30, 36, 52)); lc.alpha_composite(bike(200, LILAC, (200, 204, 214)), (30, 46)); lc.alpha_composite(T("Bike · like new", 36, D_INK, 600), (270, 40))
    bid = int(roll(t, t0, (tz - t0) * 0.95, 120, 340) // 10 * 10)
    lc.alpha_composite(T("HIGHEST BID", 22, D_MUTE, 700, True), (270, 100)); lc.alpha_composite(T(money(bid), 70, D_INK, 700), (270, 128)); c.alpha_composite(lc, (40, 100))
    kt = spring((t - tc + 0.3) / 0.4)
    if kt > 0:
        sec = 5 - 5 * clamp((t - (tz - 1.6)) / 1.6) if t >= tz - 1.6 else 5
        tv = timer(sec, 200, RED_UI if sec <= 3 else D_INK); lab = T("ENDS IN", 26, D_MUTE, 700, True)
        lay = Image.new("RGBA", (w, 300), (0, 0, 0, 0)); lay.alpha_composite(lab, (int(w / 2 - lab.width / 2), 10)); lay.alpha_composite(tv, (int(w / 2 - tv.width / 2), 50))
        lay.putalpha(lay.getchannel("A").point(lambda q: int(q * min(1, kt * 1.5)))); c.alpha_composite(lay, (0, int(360 + (1 - kt) * 20)))
    ke = spring((t - WT("f2", "everyone") + 0.15) / 0.4)
    if ke > 0:
        row = Image.new("RGBA", (w, 140), (0, 0, 0, 0)); xs = (0, 1, 2, 3)
        for i, who in enumerate(("nour", ("R", VIOLET), ("M", GREEN_APP), ("J", SILVER))):
            row.alpha_composite(head(who, 100), (int(w / 2 - 260 + i * 140), 0))
        lab = T("Same clock for everyone", 30, D_MUTE, 600); row.alpha_composite(lab, (int(w / 2 - lab.width / 2), 108))
        row.putalpha(row.getchannel("A").point(lambda q: int(q * min(1, ke * 1.5)))); c.alpha_composite(row, (0, int(720 + (1 - ke) * 20)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    stamp_at(im, big_stamp("SOLD", GREEN_UI, 110, -8), 790, 830, t, tdc - 0.1)
    footnote(im, "Example auction · item, bids and names illustrative", True, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tdl = WT("tk", "deadline,")
    put(im, lift(inbox_phone(t, (-1.0, t0 - 1.0, t0 - 1.0), reply_t=tdl - 0.1)), 540, 1170, ease((t - t0) / 0.2))
    footnote(im, "Bike, price and messages are illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 12, BLUE), (540, 41, VIOLET), (750, 5, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "wait": sc_wait, "exp": sc_exp, "result": sc_result, "decide": sc_decide, "count": sc_count, "loop": sc_loop, "outro": sc_outro}

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
    s.pop(WT("h1", "every") - 0.1, 0.035, 600); s.pop(WT("h1", "day.") - 0.05, 0.035, 650); s.thud(WT("h1", "buys."), 0.07)
    s.pop(WT("p1", "think") - 0.15, 0.035, 520); s.pop(WT("p1", "hold") - 0.15, 0.035, 560)
    for i in range(6): s.tick(WT("p1", "Days") - 0.1 + i * 0.15, 0.02)
    s.pop(WT("s1", "people") - 0.1, 0.03, 540); s.pop(WT("s1", "people") + 0.05, 0.03, 600); s.ding(WT("s1", "deadline,") - 0.15, 1318, 0.025)
    for i in range(8): s.tick(WT("s1", "deadline,") + 0.3 + i * 0.2, 0.015)
    s.pop(WT("s1", "four") - 0.1, 0.035, 640)
    for i in range(6): s.tick(WT("s2", "41%") - 0.1 + i * 0.13, 0.02)
    s.ding(WT("s2", "41%") + 0.8, 1568, 0.035); s.pop(WT("s2", "last") - 0.1, 0.035, 600)
    for i in range(6): s.tick(WT("s2", "More") + i * 0.13, 0.02)
    s.pop(WT("s2", "five") - 0.15, 0.035, 660); s.ding(WT("s2", "five") + 0.3, 1568, 0.03)
    s.thud(WT("f1", "ready.") + 0.05, 0.06); s.pop(WT("f1", "time") - 0.2, 0.035, 620)
    for i in range(3): s.tick(WT("f1", "time") + i * 0.4, 0.025)
    tz = WT("f2", "zero,")
    for i in range(5): s.tick(tz - 1.6 + i * 0.32, 0.03)
    s.pop(WT("f2", "everyone") - 0.15, 0.035, 600); s.thud(WT("f2", "decided.") - 0.1, 0.09); s.ding(WT("f2", "decided.") - 0.05, 1568, 0.035)
    s.pop(WT("tk", "deadline,") - 0.1, 0.035, 650); s.ding(WT("tk", "decision."), 1318, 0.025)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson12_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
