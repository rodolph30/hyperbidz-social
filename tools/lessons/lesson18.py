"""Auction short 18 (v3, quick, who: perspective): "Japan's used cars". Perspective: "auctions are for paintings or seized things".
In Japan, ordinary used cars are priced by dealer auctions: USS's Tokyo site handled more than 20,000 vehicles in single auctions
(Mar-Apr 2026) and reached the limit of its size; about 8 million vehicles were consigned to auctions in a year, USS alone a record
3.5 million (FY2025). Takeaway: when millions of cars need a fair price, a whole country uses auctions.
Run: python3 tools/lessons/lesson18.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson18_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "ambient", 18
XF = 0.16
SC = [("hook", False, 0.0, S("p1") - 0.1), ("myth", True, S("p1") - 0.1, S("s1") - 0.1), ("stats", False, S("s1") - 0.1, S("s3") - 0.1),
      ("full", True, S("s3") - 0.1, S("f1") - 0.1), ("lane", False, S("f1") - 0.1, S("tk") - 0.1),
      ("loop", False, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
CAR_COLS = (BLUE, VIOLET, LILAC, GREEN_APP, SILVER)

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def dim(layer, a):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * a))); return layer

_CAR = {}
def car(w=420, col=BLUE):
    """a simple side-view hatchback (same drawing as lesson 10)"""
    if (w, col) in _CAR: return _CAR[(w, col)]
    S2 = 2; h = int(w * 0.5); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    d.rounded_rectangle((W2 * 0.03, H2 * 0.42, W2 * 0.97, H2 * 0.78), radius=int(H2 * 0.12), fill=col + (255,))
    d.polygon([(W2 * 0.2, H2 * 0.45), (W2 * 0.32, H2 * 0.12), (W2 * 0.68, H2 * 0.12), (W2 * 0.84, H2 * 0.45)], fill=col + (255,))
    d.polygon([(W2 * 0.27, H2 * 0.43), (W2 * 0.35, H2 * 0.2), (W2 * 0.49, H2 * 0.2), (W2 * 0.49, H2 * 0.43)], fill=(200, 220, 255, 255))
    d.polygon([(W2 * 0.53, H2 * 0.43), (W2 * 0.53, H2 * 0.2), (W2 * 0.66, H2 * 0.2), (W2 * 0.77, H2 * 0.43)], fill=(200, 220, 255, 255))
    for x in (0.25, 0.76):
        d.ellipse((W2 * x - H2 * 0.2, H2 * 0.58, W2 * x + H2 * 0.2, H2 * 0.98), fill=(24, 26, 32, 255))
        d.ellipse((W2 * x - H2 * 0.09, H2 * 0.69, W2 * x + H2 * 0.09, H2 * 0.87), fill=SILVER + (255,))
    d.rounded_rectangle((W2 * 0.9, H2 * 0.5, W2 * 0.96, H2 * 0.58), radius=6, fill=(255, 230, 140, 255))
    _CAR[(w, col)] = im.resize((w, h), Image.LANCZOS); return _CAR[(w, col)]

COLS, ROWS = 7, 9
def lot(t, t_fill0, t_fill1, n_from=0, dark=False, title="Tokyo · one auction"):
    """the car lot window: a counter rolling to 20,000+ and a grid of cars filling up (shared by hook and loop)"""
    w, h = 900, 1180; win = window(w, h, title, dark)
    k = eout((t - t_fill0) / max(0.01, t_fill1 - t_fill0)) if t >= t_fill0 else 0
    n = int(n_from + (20000 - n_from) * k)
    num = T(f"{n:,}" + ("+" if n >= 20000 else ""), 150, D_INK if dark else L_INK, 700); win.alpha_composite(num, (int(w / 2 - num.width / 2), 96))
    lab = T("CARS UP FOR BIDDING", 26, D_MUTE if dark else GREY_TXT, 700, True); win.alpha_composite(lab, (int(w / 2 - lab.width / 2), 290))
    total = COLS * ROWS; shown = int(round(total * (n / 20000)))
    for i in range(shown):
        r, c = divmod(i, COLS); cw = 104
        win.alpha_composite(car(cw, CAR_COLS[(i * 3 + r) % 5]), (int(48 + c * 118), int(360 + r * 88)))
    return win

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); to = WT("h1", "one")
    win = lot(t, 0.0, to - 0.1, 16000)
    put(im, lift(win), 540, 1160, 1, 0.97 + 0.03 * spring(t / 0.5))
    if t >= to - 0.05:
        kp = spring((t - to + 0.05) / 0.35)
        put(im, pill("ONE AUCTION", 46, VIOLET, padx=32, pady=14), 540, 1780 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    footnote(im, "Source: USS Co., Tokyo site, Mar – Apr 2026 · car icons illustrative", False, 1870)
    return im

def sc_myth(t):
    im = bg(True); t0 = S("p1"); tp = WT("p1", "paintings."); ts = WT("p1", "seized"); to = WT("p1", "Ordinary"); tj = WT("p1", "Japan.")
    if t < to - 0.1:
        w, h = 860, 640; win = window(w, h, "Auctions are for…", True)
        for i, (txt, tw, tst) in enumerate((("Paintings", tp, ts - 0.15), ("Seized property", ts, to - 0.25))):
            ki = spring((t - tw + 0.1) / 0.35)
            if ki <= 0: continue
            y = 150 + i * 220; tt = T(txt, 76, D_INK, 700); win.alpha_composite(fade_in(tt, ki), (70, int(y + (1 - ki) * 20)))
        k = ease((t - t0 + 0.12) / 0.25); cx, cy = 540, 1060
        put(im, lift(win, True), cx, cy, k, 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
        for i, (txt, tw, tst) in enumerate((("Paintings", tp, ts - 0.15), ("Seized property", ts, to - 0.25))):
            if t >= tst:
                tt = T(txt, 76, D_INK, 700); y = cy - h / 2 + 150 + i * 220 + tt.height / 2 + 6
                strike(im, cx - w / 2 + 60, y, cx - w / 2 + 80 + tt.width, eout((t - tst) / 0.25))
        put(im, head("nour", 130), 220, 1520, ease((t - t0 - 0.1) / 0.3)); put(im, head("sami", 130), 380, 1520, ease((t - t0 - 0.2) / 0.3))
    else:
        ko = spring((t - to + 0.1) / 0.4)
        w, h = 860, 760; c = card(w, h, True)
        cr = car(620, BLUE); c.alpha_composite(cr, (int(w / 2 - cr.width / 2), 110))
        tt = T("Ordinary used cars", 64, D_INK, 700); c.alpha_composite(tt, (int(w / 2 - tt.width / 2), 470))
        if t >= tj - 0.1:
            kj = spring((t - tj + 0.1) / 0.35); pj = pill("Japan", 48, VIOLET, padx=34, pady=12)
            c.alpha_composite(fade_in(pj, kj), (int(w / 2 - pj.width / 2), int(590 + (1 - kj) * 14)))
        put(im, lift(c, True), 540, 1080 + (1 - ko) * 40, min(1, ko * 1.5), 0.94 + 0.06 * ko)
    return im

def sc_stats(t):
    im = bg(False); t0 = S("s1"); t8 = WT("s1", "8 million"); t35 = WT("s2", "3.5 million.")
    v = roll(t, t8 - 0.15, 0.7, 0, 8_000_000)
    k35 = eout((t - t35 + 0.2) / 0.6) if t >= t35 - 0.2 else 0
    st = stat("About · used cars at auction · Japan · a year", f"{int(v):,}", "", 900, False, 140)
    put(im, lift(dim(st, 1 - 0.55 * k35)), 540, 900, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    # the bar: whole market, then one group's share
    kb = ease((t - t8 - 0.2) / 0.4)
    if kb > 0:
        bw, bh = 900, 70; x0, y0 = 540 - bw / 2, 1180
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((x0, y0, x0 + bw * kb, y0 + bh), radius=35, fill=(214, 216, 226, 255))
        if k35 > 0: d.rounded_rectangle((x0, y0, x0 + bw * (3.5 / 8) * k35, y0 + bh), radius=35, fill=BLUE + (255,))
        im.alpha_composite(lay)
    if t >= t35 - 0.2:
        ks = spring((t - t35 + 0.2) / 0.4)
        lab = T("ONE GROUP, ONE YEAR", 28, GREY_TXT, 700, True); put(im, fade_in(lab, ks), 540, 1330)
        big = T(f"{roll(t, t35 - 0.2, 0.6, 0, 3.5):.1f} million", 120, BLUE, 700); put(im, fade_in(big, ks), 540, 1440 + (1 - ks) * 20)
        if t >= t35 + 0.6: stamp_at(im, big_stamp("RECORD", VIOLET, 70, -8), 760, 1590, t, t35 + 0.6)
    footnote(im, "Source: USS Co., FY2025 (Apr 2025 – Mar 2026), cars consigned to auction", False, 1870)
    return im

def sc_full(t):
    im = bg(True); t0 = S("s3"); tb = WT("s3", "busy,"); tr = WT("s3", "room.")
    w, h = 880, 1000; win = window(w, h, "Tokyo site · space used", True)
    kf = clamp((t - t0) / (tr - t0)); pct = int(60 + 40 * eout(kf))
    col = RED_UI if pct >= 100 else (VIOLET if pct < 90 else LILAC)
    num = T(f"{pct}%", 170, D_INK, 700); win.alpha_composite(num, (int(w / 2 - num.width / 2), 110))
    d = ImageDraw.Draw(win); bx, by, bw, bh = 70, 360, w - 140, 64
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=32, fill=(40, 46, 60, 255))
    d.rounded_rectangle((bx, by, bx + bw * pct / 100, by + bh), radius=32, fill=col + (255,))
    n = int(4 + 24 * eout(kf))
    for i in range(n):
        r, c = divmod(i, 7); win.alpha_composite(car(100, CAR_COLS[(i * 2 + r) % 5]), (int(60 + c * 112), int(490 + r * 110)))
    put(im, lift(win, True), 540, 1120, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    stamp_at(im, big_stamp("FULL", RED_UI, 130, -8), 540, 1300, t, tr - 0.05)
    footnote(im, "Source: USS Co. results presentation, May 2026 · meter illustrative", True, 1870)
    return im

BIDS = (("dealers", ("12", VIOLET), 820_000), ("bid,", ("7", GREEN_APP), 865_000), ("bids", ("31", BLUE), 905_000))
def sc_lane(t):
    im = bg(False); t0 = S("f1"); tp = WT("f1", "price.")
    w, h = 900, 1060; win = window(w, h, "Dealer auction · this week", False)
    cr = car(520, LILAC); win.alpha_composite(cr, (int(w / 2 - cr.width / 2), 110))
    # price line
    shown = 780_000
    for word, who, amt in BIDS:
        tw = WT("f1", word)
        if t >= tw - 0.1: shown = amt
    lab = T("CURRENT BID", 26, GREY_TXT, 700, True); win.alpha_composite(lab, (int(w / 2 - lab.width / 2), 400))
    pv = T(f"¥{shown:,}", 120, L_INK, 700); win.alpha_composite(pv, (int(w / 2 - pv.width / 2), 450))
    for i, (word, who, amt) in enumerate(BIDS):
        tw = WT("f1", word); ki = spring((t - tw + 0.1) / 0.35)
        if ki <= 0: continue
        x = 170 + i * 280; y = 700
        hd = head(who, 130); win.alpha_composite(fade_in(hd, ki), (int(x - 65), int(y + (1 - ki) * 20)))
        pl = pill(f"¥{amt:,}", 28, (236, 237, 242), L_INK, 16, 8); win.alpha_composite(fade_in(pl, ki), (int(x - pl.width / 2), y + 150))
    put(im, lift(win), 540, 1130, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    stamp_at(im, big_stamp("SOLD", GREEN_UI, 120, -8), 760, 860, t, tp - 0.05)
    footnote(im, "Example lane · bidders and bids illustrative", False, 1870)
    return im

def sc_loop(t):
    im = bg(False); t0 = S("tk") - 0.1; tf = WT("tk", "fair"); ta = WT("tk", "auctions.")
    win = lot(t, -1, 0, 20000)
    put(im, lift(win), 540, 1160, ease((t - t0) / 0.2))
    if t >= tf - 0.1:
        kp = spring((t - tf + 0.1) / 0.35)
        put(im, pill("Price: set by the bids", 44, GREEN_UI, padx=30, pady=14), 540, 1780 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    if t >= ta:
        x0 = 540 - 450 + 30; select_box(im, (x0, 1160 - 590 + 80, x0 + 840, 1160 - 590 + 270), eout((t - ta) / 0.3))
    footnote(im, "Source: USS Co., Tokyo site, Mar – Apr 2026 · car icons illustrative", False, 1870)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 18, BLUE), (540, 3, VIOLET), (750, 9, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "myth": sc_myth, "stats": sc_stats, "full": sc_full, "lane": sc_lane, "loop": sc_loop, "outro": sc_outro}

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
    for i in range(14): s.tick(0.3 + i * 0.22, 0.016)
    s.pop(WT("h1", "one") - 0.05, 0.04, 620)
    s.pop(WT("p1", "paintings.") - 0.1, 0.035, 600); s.pop(WT("p1", "seized") - 0.1, 0.035, 560)
    s.ding(WT("p1", "Ordinary") - 0.1, 1318, 0.03); s.pop(WT("p1", "Japan.") - 0.1, 0.04, 680)
    for i in range(6): s.tick(WT("s1", "8 million") - 0.15 + i * 0.11, 0.018)
    for i in range(5): s.tick(WT("s2", "3.5 million.") - 0.2 + i * 0.11, 0.018)
    s.thud(WT("s2", "3.5 million.") + 0.6, 0.06)
    s.thud(WT("s3", "room.") - 0.05, 0.08)
    for w_ in ("dealers", "bid,", "bids"): s.pop(WT("f1", w_) - 0.1, 0.035, 560)
    s.thud(WT("f1", "price.") - 0.05, 0.07); s.ding(WT("f1", "price.") + 0.05, 1568, 0.03)
    s.pop(WT("tk", "fair") - 0.1, 0.04, 680); s.ding(WT("tk", "auctions.") - 0.05, 1568, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson18_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
