"""Auction short 15 (v3, quick, who: Sami): "One more buyer". Problem: Sami sells his camera to one buyer at a time; every chat
starts from zero and he gives a little more each time ($500 -> $460 -> $420). Reframe (one fact): Bulow & Klemperer (AER 1996)
showed that, under standard assumptions, a simple public auction beats the best possible negotiation as long as it attracts
one extra bidder; "the value of negotiating skill is small relative to the value of additional competition."
Fix: everyone who wants it in one place, at one time. Takeaway: one more buyer beats the best negotiator. Let them bid.
Built like L12: one story from the first frame to the last (Sami's camera listing), one fact.
Run: python3 tools/lessons/lesson15.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson15_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "lofi", 15
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("chats", True, S("p1") - 0.1, S("s1") - 0.1), ("paper", False, S("s1") - 0.1, S("s2") - 0.1),
      ("extra", True, S("s2") - 0.1, S("s3") - 0.1), ("skill", False, S("s3") - 0.1, S("f1") - 0.1),
      ("room", True, S("f1") - 0.1, S("tk") - 0.1), ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
BUYERS = (("R", VIOLET), ("M", GREEN_APP), ("J", SILVER))

def fade_in(layer, k):
    layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

# ---------- drawings ----------
def cam_icon(w=200, col=BLUE, ink=(24, 28, 44)):
    S2 = 2; h = int(w * 0.7); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    d.rounded_rectangle((W2 * 0.3, H2 * 0.08, W2 * 0.6, H2 * 0.3), radius=16, fill=ink + (255,))
    d.rounded_rectangle((W2 * 0.04, H2 * 0.22, W2 * 0.96, H2 * 0.95), radius=40, fill=col + (255,))
    cx, cy, r = W2 * 0.5, H2 * 0.59, H2 * 0.27
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ink + (255,)); r2 = r * 0.62
    d.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), fill=(70, 80, 110, 255)); r3 = r * 0.22
    d.ellipse((cx - r2 * 0.5 - r3, cy - r2 * 0.5 - r3, cx - r2 * 0.5 + r3, cy - r2 * 0.5 + r3), fill=(255, 255, 255, 200))
    d.ellipse((W2 * 0.8, H2 * 0.3, W2 * 0.88, H2 * 0.38), fill=(255, 255, 255, 230))
    return im.resize((w, h), Image.LANCZOS)

def bubble(text, size=40, fill=(236, 237, 242), col=L_INK, right=False):
    tt = T(text, size, col, 600); w, h = tt.width + 56, tt.height + 36
    im = Image.new("RGBA", (w, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=fill + (255,))
    if right: d.polygon([(w - 26, h - 10), (w - 18, h + 12), (w - 58, h - 10)], fill=fill + (255,))
    else: d.polygon([(26, h - 10), (18, h + 12), (58, h - 10)], fill=fill + (255,))
    im.alpha_composite(tt, (28, 18)); return im

def listing(price_txt, label="$", old=None, delta=None, delta_col=RED_UI, k_delta=0.0, dark=False):
    """Sami's camera listing card, shared by the hook and the loop so the replay is seamless"""
    lc = card(560, 260, dark, 26, fill=((30, 36, 52) if dark else (246, 247, 251)))
    lc.alpha_composite(cam_icon(190, BLUE if not dark else LILAC), (28, 60))
    ink = D_INK if dark else L_INK
    lc.alpha_composite(T("Camera · like new", 34, ink, 600), (250, 40))
    lc.alpha_composite(T(label, 22, GREY_TXT, 700, True), (250, 92))
    pv = T(price_txt, 84, ink, 700); lc.alpha_composite(pv, (250, 118))
    if old is not None:
        lw_ = T(label, 22, GREY_TXT, 700, True).width; ov = T(old, 30, GREY_TXT, 600); ox = 250 + lw_ + 18; lc.alpha_composite(ov, (ox, 84))
        ImageDraw.Draw(lc).line([(ox - 4, 84 + ov.height // 2 + 2), (ox + ov.width + 4, 84 + ov.height // 2 + 2)], fill=RED_UI + (255,), width=4)
    if delta and k_delta > 0:
        dp = fade_in(pill(delta, 34, delta_col, padx=18, pady=8), k_delta); lc.alpha_composite(dp, (int(123 - dp.width / 2), 200 - int(10 * (1 - k_delta))))
    return lc

def sami_phone(t, pairs, price, old=None, delta=None, delta_col=RED_UI, t_delta=None, label="PRICE"):
    """pairs: [(t_buyer, buyer_text, t_reply, reply_text, buyer)] drawn as a chat under the listing"""
    pw, ph = 640, 960; p = phone(pw, ph, False)
    kd = spring((t - t_delta) / 0.35) if t_delta is not None else 0
    p.alpha_composite(listing(price, label, old, delta, delta_col, kd), (40, 100))
    p.alpha_composite(T("CHATS", 22, GREY_TXT, 700, True), (60, 390)); y = 435
    for tb, bt, tr, rt, who in pairs:
        k = spring((t - tb) / 0.35)
        if k > 0:
            row = Image.new("RGBA", (560, 110), (0, 0, 0, 0)); row.alpha_composite(head(who, 64), (0, 22)); row.alpha_composite(bubble(bt, 36), (80, 4))
            p.alpha_composite(fade_in(row, k), (40, int(y + (1 - k) * 30)))
        y += 115
        k2 = spring((t - tr) / 0.35)
        if k2 > 0:
            b = fade_in(bubble(rt, 36, BLUE, (255, 255, 255), True), k2); p.alpha_composite(b, (pw - 40 - b.width, int(y + (1 - k2) * 30)))
        y += 110
    return p

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); tb = WT("h1", "better"); tl = WT("h1", "less.")
    pairs = [(-1.0, "Can you do better?", -1.0, "OK, $460", BUYERS[0]), (tb - 0.1, "Can you do better?", WT("h1", "He") - 0.1, "OK, $420", BUYERS[1])]
    low = t >= tl - 0.05
    p = sami_phone(t, pairs, "$420" if low else "$500", "$500" if low else None, "−$80", RED_UI, tl - 0.05)
    put(im, lift(p), 540, 1120, 1, 0.97 + 0.03 * spring(t / 0.5))
    footnote(im, "Camera, prices and chats are illustrative", False, 1850)
    return im

def sc_chats(t):
    im = bg(True); ts = [WT("p1", "$500"), WT("p1", "$460"), WT("p1", "$420")]; to = WT("p1", "One"); tz = WT("p1", "zero.")
    i = 0
    for j, tj in enumerate(ts):
        if t >= tj - 0.12: i = j
    if t < to - 0.15:
        tj = ts[i]; k = spring((t - tj + 0.12) / 0.35)
        c = stat(f"Chat {i + 1} · one buyer", ("$500", "$460", "$420")[i], "", 760, True, 220, (D_INK, (255, 170, 180), RED_UI)[i])
        c.alpha_composite(head(BUYERS[i], 120), (760 - 170, 40))
        put(im, lift(c, True), 540, 1060 + (1 - k) * 40, min(1, k * 1.5), 0.94 + 0.06 * k)
        put(im, head("sami", 130), 540, 1420, 1)
    else:
        k = spring((t - to + 0.15) / 0.4)
        row = Image.new("RGBA", (900, 200), (0, 0, 0, 0))
        for j in range(3):
            kj = spring((t - to + 0.15 - j * 0.12) / 0.35)
            if kj > 0: row.alpha_composite(fade_in(head(BUYERS[j], 140), kj), (60 + j * 300, 30))
        put(im, row, 540, 900)
        for j in range(2):
            put(im, T("→", 70, D_MUTE, 700), 370 + j * 300, 900)
        kz = spring((t - tz + 0.15) / 0.4)
        if kz > 0:
            pp = pill("Every chat starts from zero", 46, VIOLET, padx=34, pady=16)
            put(im, pp, 540, 1200 + (1 - kz) * 30, min(1, kz * 1.5), 0.9 + 0.1 * kz)
        put(im, pill("One buyer at a time", 40, PILL_D, padx=30, pady=12), 540, 700, min(1, k * 1.5))
    footnote(im, "Prices illustrative", True, 1850)
    return im

def sc_paper(t):
    im = bg(False); t0 = S("s1"); tn = WT("s1", "negotiation,"); ta = WT("s1", "against")
    w, h = 920, 980; win = window(w, h, "American Economic Review · 1996", False)
    tt = T("“Auctions versus", 60, L_INK, 700); win.alpha_composite(tt, (int(w / 2 - tt.width / 2), 120))
    tt = T("Negotiations”", 60, L_INK, 700); win.alpha_composite(tt, (int(w / 2 - tt.width / 2), 196))
    tt = T("Bulow & Klemperer", 34, GREY_TXT, 600); win.alpha_composite(tt, (int(w / 2 - tt.width / 2), 290))
    for i, (tk_, lab) in enumerate(((tn - 0.2, "Best possible\nnegotiation"), (ta - 0.1, "Simple\nauction"))):
        k = spring((t - tk_) / 0.4)
        if k <= 0: continue
        c = card(400, 520, False, 26, fill=(246, 247, 251))
        for li, ln in enumerate(lab.split("\n")):
            lt = T(ln, 40, L_INK, 700); c.alpha_composite(lt, (int(200 - lt.width / 2), 40 + li * 52))
        if i == 0:
            c.alpha_composite(head("sami", 120), (60, 230)); c.alpha_composite(head(BUYERS[0], 120), (220, 230))
            lt = T("1 buyer", 32, GREY_TXT, 600); c.alpha_composite(lt, (int(200 - lt.width / 2), 400))
        else:
            for j, (n, col) in enumerate(((3, VIOLET), (7, GREEN_APP), (12, BLUE))):
                pd = paddle(n, col, 90); c.alpha_composite(pd, (40 + j * 115, 200))
            lt = T("everyone bids", 32, GREY_TXT, 600); c.alpha_composite(lt, (int(200 - lt.width / 2), 400))
        win.alpha_composite(fade_in(c, k), (40 + i * 440, int(390 + (1 - k) * 30)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(win), 540, 1130, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Bulow & Klemperer, “Auctions versus Negotiations”, American Economic Review, 1996", False, 1850)
    return im

def sc_extra(t):
    im = bg(True); t0 = S("s2"); tw = WT("s2", "wins,"); to = WT("s2", "one"); tb = WT("s2", "buyer.")
    w, h = 880, 760; c = window(w, h, "Simple auction", True)
    n = 4 if t >= to - 0.1 else 3
    xs0 = w / 2 - (n - 1) * 95
    for j in range(n):
        who = (BUYERS[0], BUYERS[1], BUYERS[2], ("+1", GREEN_UI))[j]
        kj = spring((t - to + 0.1) / 0.4) if j == 3 else 1
        hh = head(who, 150 if j == 3 else 130)
        if j == 3:
            hh = fade_in(hh, kj); sc = 0.6 + 0.4 * kj; hh = hh.resize((max(1, int(hh.width * sc)), max(1, int(hh.height * sc))), Image.LANCZOS)
        x = xs0 + j * 190 - (3 - j) * 0 if n == 4 else w / 2 - 190 + j * 190
        c.alpha_composite(hh, (int(x - hh.width / 2), int(260 - hh.height / 2)))
    if t >= tb - 0.15:
        kb = spring((t - tb + 0.15) / 0.4); pp = fade_in(pill("one extra buyer", 44, GREEN_UI, padx=30, pady=14), kb)
        c.alpha_composite(pp, (int(w / 2 - pp.width / 2), int(430 + (1 - kb) * 20)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1100, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    stamp_at(im, big_stamp("WINS", GREEN_UI, 110, -8), 540, 1340, t, tw - 0.05)
    footnote(im, "Under standard assumptions · Bulow & Klemperer, AER, 1996", True, 1850)
    return im

def sc_skill(t):
    im = bg(False); t0 = S("s3"); ts = WT("s3", "skill"); tc = WT("s3", "competition.")
    c = card(900, 560, False, 30)
    for i, (tk_, lab, frac, col) in enumerate(((ts - 0.2, "Negotiating skill", 0.16, SILVER), (tc - 0.2, "More competition", 0.92, VIOLET))):
        k = spring((t - tk_) / 0.4)
        if k <= 0: continue
        lt = fade_in(T(lab, 46, L_INK, 700), k); c.alpha_composite(lt, (60, 80 + i * 260))
        bw = int(780 * frac * eout((t - tk_) / 0.7)); y = 160 + i * 260
        if bw > 4: ImageDraw.Draw(c).rounded_rectangle((60, y, 60 + bw, y + 80), radius=24, fill=col + (255,))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "“The value of negotiating skill is small relative to the value of additional competition.”", False, 1820)
    footnote(im, "Bulow & Klemperer, AER, 1996 · bar lengths illustrative", False, 1858)
    return im

def sc_room(t):
    im = bg(True); t0 = S("f1"); te = WT("f1", "everyone"); tp = WT("f1", "place,"); tm = WT("f1", "time.")
    w, h = 880, 820; c = window(w, h, "Live auction", True)
    bid = int(roll(t, te, (E("f1") - te) * 0.95, 420, 580) // 10 * 10)
    lc = listing(money(bid), "HIGHEST BID", dark=True); c.alpha_composite(lc, (160, 100))
    for j, who in enumerate(("nour", BUYERS[0], BUYERS[1], BUYERS[2], ("A", BLUE))):
        kj = spring((t - te + 0.15 - j * 0.07) / 0.35)
        if kj > 0: c.alpha_composite(fade_in(head(who, 120), kj), (int(w / 2 - 340 + j * 150), int(460 + (1 - kj) * 30)))
    kp = spring((t - tp + 0.15) / 0.4)
    if kp > 0:
        pp = fade_in(pill("One place · one time", 46, VIOLET, padx=34, pady=16), kp); c.alpha_composite(pp, (int(w / 2 - pp.width / 2), int(680 + (1 - kp) * 20)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1110, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    footnote(im, "Example auction · item, bids and names illustrative", True, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tb = WT("tk", "bid.")
    v = 580 if t >= tb - 0.1 else int(roll(t, t0, 1.6, 540, 570) // 10 * 10)
    pw, ph = 640, 960; p = phone(pw, ph, False)
    kd = spring((t - tb + 0.1) / 0.35)
    p.alpha_composite(listing(money(v), "HIGHEST BID", None, "+$80", GREEN_UI, kd), (40, 100))
    p.alpha_composite(T("BIDDERS", 22, GREY_TXT, 700, True), (60, 390))
    for j, who in enumerate(("nour", BUYERS[0], BUYERS[1], BUYERS[2], ("A", BLUE))):
        p.alpha_composite(head(who, 86), (60 + j * 104, 440))
    b = bubble("Bidding ends Friday, 7 pm", 34, BLUE, (255, 255, 255), True); p.alpha_composite(b, (pw - 40 - b.width, 580))
    put(im, lift(p), 540, 1120, ease((t - t0) / 0.2))
    footnote(im, "Camera, prices and names are illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 15, BLUE), (540, 1, VIOLET), (750, 4, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "chats": sc_chats, "paper": sc_paper, "extra": sc_extra, "skill": sc_skill, "room": sc_room, "loop": sc_loop, "outro": sc_outro}

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
    s.pop(WT("h1", "better") - 0.1, 0.035, 600); s.pop(WT("h1", "He") - 0.1, 0.035, 650); s.thud(WT("h1", "less.") - 0.05, 0.07)
    for w_, f in (("$500", 520), ("$460", 480), ("$420", 440)): s.pop(WT("p1", w_) - 0.12, 0.04, f)
    for j in range(3): s.pop(WT("p1", "One") - 0.15 + j * 0.12, 0.03, 560 + j * 40)
    s.ding(WT("p1", "zero.") - 0.15, 1046, 0.025)
    s.pop(WT("s1", "negotiation,") - 0.2, 0.035, 600); s.pop(WT("s1", "against") - 0.1, 0.035, 660)
    s.thud(WT("s2", "wins,") - 0.05, 0.09); s.pop(WT("s2", "one") - 0.1, 0.04, 700); s.ding(WT("s2", "buyer.") - 0.1, 1568, 0.035)
    s.pop(WT("s3", "skill") - 0.2, 0.03, 520); s.pop(WT("s3", "competition.") - 0.2, 0.035, 660)
    for i in range(5): s.tick(WT("s3", "competition.") - 0.1 + i * 0.12, 0.02)
    for j in range(5): s.pop(WT("f1", "everyone") - 0.15 + j * 0.07, 0.025, 560 + j * 30)
    for i in range(8): s.tick(WT("f1", "everyone") + i * 0.3, 0.018)
    s.ding(WT("f1", "place,") - 0.1, 1318, 0.025)
    s.pop(WT("tk", "bid.") - 0.1, 0.04, 680); s.ding(WT("tk", "bid."), 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson15_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
