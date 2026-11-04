"""Auction short 20 (v3, quick, who: both): "The haggling tax". Problem: Sami asks $900, Nour offers $600, days of back and forth.
Reframe (one study): across five studies, 95% of people chose not to negotiate up to 51% of the time; negotiating only felt worth it
for savings of 21-36% of the price; businesses can raise prices 5-11% and more than half of consumers will pay it
(Hunsaker, Zhang & Lee 2025, via Indiana University / Newswise). Fix: open bidding, same rules for everyone.
Takeaway: haggling has a price, and both sides pay it. No haggling. Just bids. Loop: ends on the same receipt the video opens on.
Run: python3 tools/lessons/lesson20.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson20_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "lofi", 20
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("chat", True, S("p1") - 0.1, S("r1") - 0.1), ("study", False, S("r1") - 0.1, S("r3") - 0.1),
      ("raise", True, S("r3") - 0.1, S("f1") - 0.1), ("fix", False, S("f1") - 0.1, S("tk") - 0.1),
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

def receipt(t, mark_t=None, strike_t=None, end_t=None):
    """the receipt with a 'Haggling' line; shared by the hook and the loop so the replay is seamless"""
    w, h = 820, 900; c = card(w, h, False, 30); d = ImageDraw.Draw(c)
    tt = T("RECEIPT", 30, GREY_TXT, 700, True); c.alpha_composite(tt, (int(w / 2 - tt.width / 2), 60))
    for x in range(60, w - 60, 28): d.line([(x, 130), (x + 14, 130)], fill=LINE_L + (255,), width=3)
    c.alpha_composite(T("Item", 48, L_INK, 600), (70, 190)); v = T("$900", 48, L_INK, 700); c.alpha_composite(v, (w - 70 - v.width, 190))
    hc = RED_UI if (mark_t is not None and t >= mark_t) else L_INK
    c.alpha_composite(T("Haggling", 48, hc, 700), (70, 320)); q = T("+ ?", 56, hc, 700); c.alpha_composite(q, (w - 70 - q.width, 314))
    if strike_t is not None and t >= strike_t:
        ImageDraw.Draw(c).line([(60, 352), (60 + (w - 120) * eout((t - strike_t) / 0.3), 352)], fill=GREEN_UI + (255,), width=10)
    for x in range(60, w - 60, 28): d.line([(x, 470), (x + 14, 470)], fill=LINE_L + (255,), width=3)
    c.alpha_composite(T("Time", 40, GREY_TXT, 600), (70, 530)); tv = T("days", 40, GREY_TXT, 600); c.alpha_composite(tv, (w - 70 - tv.width, 530))
    c.alpha_composite(T("Paid by", 40, GREY_TXT, 600), (70, 640))
    c.alpha_composite(head("sami", 80), (w - 250, 625)); c.alpha_composite(head("nour", 80), (w - 150, 625))
    if end_t is not None and t >= end_t:
        kp = spring((t - end_t) / 0.4); p = fade_in(pill("Just bids", 50, GREEN_UI, padx=36, pady=16), kp)
        c.alpha_composite(p, (int(w / 2 - p.width / 2), int(770 + (1 - kp) * 20)))
    return c

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); tp = WT("h1", "price."); tpd = WT("h2", "paid")
    put(im, lift(receipt(t, tp - 0.1)), 540, 1150, 1, 0.97 + 0.03 * spring(t / 0.5))
    if t >= tp - 0.1: select_box(im, (120, 1015, 960, 1100), eout((t - tp + 0.1) / 0.3), 1, RED_UI)
    stamp_at(im, big_stamp("PAID", RED_UI, 110, -8), 760, 1500, t, tpd - 0.05)
    footnote(im, "Item and price are illustrative", False, 1850)
    return im

def sc_chat(t):
    im = bg(True); t0 = S("p1"); ta = WT("p1", "asks"); to = WT("p1", "offers"); td = WT("p1", "Days"); tb = WT("p1", "back")
    pw, ph = 680, 1180; p = phone(pw, ph, True)
    p.alpha_composite(head("sami", 60), (50, 100)); p.alpha_composite(T("Sami", 34, D_INK, 700), (126, 110))
    msgs = [(ta - 0.1, "$900", True), (to - 0.1, "$600?", False), (td - 0.25, "$850", True), (td - 0.05, "$650?", False),
            (tb - 0.1, "$820", True), (tb + 0.15, "$680?", False)]
    y = 220
    for ti, txt, right in msgs:
        k = spring((t - ti) / 0.35)
        if k <= 0: continue
        b = bubble(txt, 50, BLUE if right else (40, 46, 60), D_INK, right)
        row = Image.new("RGBA", (pw - 80, b.height + 10), (0, 0, 0, 0))
        if right: row.alpha_composite(b, (pw - 80 - b.width, 0))
        else: row.alpha_composite(head("nour", 64), (0, 20)); row.alpha_composite(b, (80, 0))
        p.alpha_composite(fade_in(row, k), (40, int(y + (1 - k) * 30))); y += 140
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(p, True), 540, 1180, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= td - 0.1:
        d = int(round(roll(t, td - 0.1, 0.9, 1, 3))); kk = spring((t - td + 0.1) / 0.4)
        put(im, pill(f"Day {d}", 46, VIOLET, padx=30, pady=14), 860, 640 + (1 - kk) * 20, min(1, kk * 1.5))
    footnote(im, "Names, prices and chat are illustrative", True, 1850)
    return im

def sc_study(t):
    im = bg(False); t0 = S("r1"); t5 = WT("r1", "studies,"); tp = WT("r1", "people"); th = WT("r1", "half")
    v = int(round(roll(t, t5 + 0.45, 0.8, 0, 95)))
    c = stat("People who chose not to negotiate", f"{v}%", "up to 51% of the time", 860, False, 210, VIOLET)
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1080, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= t5 - 0.15:
        kc = spring((t - t5 + 0.15) / 0.4); put(im, chip("5 studies", False, 30), 540, 780 + (1 - kc) * 20, min(1, kc * 1.5))
    if t >= th - 0.1:
        select_box(im, (130, 1215, 600, 1265), eout((t - th + 0.1) / 0.3))
    footnote(im, "Source: Hunsaker, Zhang & Lee, 2025 (Indiana University)", False, 1850)
    return im

def sc_worth(t):
    im = bg(True); t0 = S("r2"); ts = WT("r2", "save"); tpr = WT("r2", "price.")
    w, h = 880, 760; c = card(w, h, True, 30); d = ImageDraw.Draw(c)
    c.alpha_composite(T("SAVING NEEDED TO HAGGLE", 26, D_MUTE, 700, True), (60, 50))
    v = T("21–36%", 180, D_INK, 700); c.alpha_composite(fade_in(v, (t - ts + 0.2) / 0.25), (60, 110))
    x0, x1, y0, y1 = 60, w - 60, 420, 520
    d.rounded_rectangle((x0, y0, x1, y1), radius=30, fill=(30, 36, 52, 255))
    kb = eout((t - ts + 0.1) / 0.6)
    if kb > 0:
        a = x0 + (x1 - x0) * 0.21; b = a + (x1 - x0) * 0.15 * kb
        d.rounded_rectangle((x0, y0, a, y1), radius=30, fill=(60, 68, 88, 255)); d.rectangle((a, y0, b, y1), fill=LILAC + (255,))
    lb = T("of the price", 36, D_MUTE, 600); c.alpha_composite(lb, (60, 560))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c, True), 540, 1100, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tpr - 0.1:
        kp = spring((t - tpr + 0.1) / 0.4); put(im, head("nour", 130), 860, 1500 + (1 - kp) * 30, min(1, kp * 1.5))
    footnote(im, "Average across participants · Hunsaker, Zhang & Lee, 2025", True, 1850)
    return im

def tag(txt, w=560, h=300, col=L_INK):
    c = card(w, h, False, 40, fill=(255, 255, 255)); d = ImageDraw.Draw(c)
    d.ellipse((40, h / 2 - 22, 84, h / 2 + 22), fill=L_BG + (255,), outline=LINE_L + (255,), width=3)
    v = T(txt, 130, col, 700); c.alpha_composite(v, (int(w / 2 + 30 - v.width / 2), int(h / 2 - v.height / 2))); return c

def sc_raise(t):
    im = bg(True); t0 = S("r3"); tr = WT("r3", "raise"); tf = WT("r3", "five"); th = WT("r3", "half"); tpy = WT("r3", "pay")
    v = roll(t, tr, max(0.5, th - tr - 0.2), 100, 111)
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(tag(f"${int(v)}"), True), 540, 1000, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tf - 0.15:
        kc = spring((t - tf + 0.15) / 0.4); put(im, pill("+5–11%", 56, VIOLET, padx=34, pady=14), 540, 760 + (1 - kc) * 20, min(1, kc * 1.5))
    if t >= th - 0.15:
        kh = spring((t - th + 0.15) / 0.4); put(im, pill("More than half pay it", 46, (40, 46, 60), padx=32, pady=16), 540, 1300 + (1 - kh) * 20, min(1, kh * 1.5))
    stamp_at(im, big_stamp("HAGGLING TAX", RED_UI, 84, -7), 540, 1530, t, tpy - 0.05)
    footnote(im, "Source: Hunsaker, Zhang & Lee, 2025 · $100 tag illustrative", True, 1850)
    return im

def sc_fix(t):
    im = bg(False); t0 = S("f1"); te = WT("f1", "Everyone"); to = WT("f1", "open,"); ts = WT("f1", "same")
    w, h = 880, 1000; c = window(w, h, "Live auction", False)
    tk_ = WT("f1", "skips")
    if t < te - 0.05:
        ka = 1 - clamp((t - (te - 0.3)) / 0.25)
        b1 = bubble("$900", 64, BLUE, D_INK, True); b2 = bubble("$600?", 64, (236, 237, 242), L_INK)
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); lay.alpha_composite(b1, (w - 120 - b1.width, 280)); lay.alpha_composite(b2, (120, 470))
        if t >= tk_ - 0.05:
            ImageDraw.Draw(lay).line([(90, 450), (90 + (w - 180) * eout((t - tk_ + 0.05) / 0.3), 450)], fill=RED_UI + (255,), width=12)
        c.alpha_composite(fade_in(lay, ka / 1.5))
    rows = [("nour", "$620"), (BUYERS[0], "$660"), (BUYERS[1], "$710"), (("nour"), "$740")]
    y = 110
    for j, (who, amt) in enumerate(rows):
        kj = spring((t - te + 0.1 - j * 0.28) / 0.35)
        if kj <= 0: continue
        r = card(780, 150, False, 26, fill=(246, 246, 250)); r.alpha_composite(head(who, 100), (26, 25))
        r.alpha_composite(T("bid", 34, GREY_TXT, 600), (150, 52)); a = T(amt, 64, L_INK, 700); r.alpha_composite(a, (780 - 40 - a.width, 38))
        c.alpha_composite(fade_in(r, kj), (50, int(y + (1 - kj) * 30))); y += 175
    if t >= ts - 0.15:
        kp = spring((t - ts + 0.15) / 0.4); pp = fade_in(pill("Same rules for everyone", 44, VIOLET, padx=32, pady=16), kp)
        c.alpha_composite(pp, (int(w / 2 - pp.width / 2), int(850 + (1 - kp) * 20)))
    k = ease((t - t0 + 0.12) / 0.25); put(im, lift(c), 540, 1120, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    put(im, head("sami", 120), 930, 520, k)
    footnote(im, "Example auction · bids and names illustrative", False, 1850)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tb = WT("tk", "both"); tn = WT("tk", "No"); tj = WT("tk", "Just")
    put(im, lift(receipt(t, t0 - 1, tn - 0.05, tj - 0.1)), 540, 1150, ease((t - t0) / 0.2))
    if tb - 0.1 <= t < tn - 0.05: select_box(im, (680, 1310, 900, 1420), eout((t - tb + 0.1) / 0.3))
    footnote(im, "Item and price are illustrative", False, 1850)
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

FN = {"hook": sc_hook, "chat": sc_chat, "study": sc_study, "raise": sc_raise, "fix": sc_fix, "loop": sc_loop, "outro": sc_outro}

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
    s.ding(WT("h1", "price.") - 0.1, 1318, 0.03); s.thud(WT("h2", "paid") - 0.05, 0.08)
    for w_ in ("asks", "offers", "Days", "back"): s.pop(WT("p1", w_) - 0.1, 0.035, 600)
    for i in range(8): s.tick(WT("r1", "studies,") + 0.45 + i * 0.1, 0.018)
    s.pop(WT("r1", "studies,") - 0.15, 0.035, 520); s.ding(WT("r1", "half") - 0.1, 1568, 0.025)
    for i in range(6): s.tick(WT("r3", "raise") + i * 0.12, 0.018)
    s.pop(WT("r3", "five") - 0.15, 0.035, 640); s.pop(WT("r3", "half") - 0.15, 0.035, 560); s.thud(WT("r3", "pay") - 0.05, 0.08)
    for j in range(4): s.pop(WT("f1", "Everyone") - 0.1 + j * 0.28, 0.03, 560 + j * 40)
    s.ding(WT("f1", "same") - 0.15, 1318, 0.03); s.thud(WT("f1", "skips") - 0.05, 0.05)
    s.tick(WT("tk", "No") - 0.05, 0.03); s.ding(WT("tk", "Just") - 0.1, 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson20_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
