"""Auction short 23 (v3, quick, who: perspective, Lebanon): "Tripoli's fish auction". Perspective: "auctions are rare in Lebanon".
FAO: fish auctions at the ports of Dora, Ouzai, Saida, Tripoli and Sour; Tripoli's Sidawi auction was founded in 1958 in a building
about 400 years old with stone arches; its customers are private consumers, restaurants and fishmongers.
Takeaway: Lebanon already sells its fish by auction. Fast, fair, in the open.
Run: python3 tools/lessons/lesson23.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os, math
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson23_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "ambient", 23
XF = 0.16
SC = [("hook", True, 0.0, S("p1") - 0.1), ("myth", False, S("p1") - 0.1, S("s1") - 0.1), ("ports", True, S("s1") - 0.1, S("s2") - 0.1),
      ("crowd", False, S("s2") - 0.1, S("f1") - 0.1), ("bids", True, S("f1") - 0.1, S("tk") - 0.1),
      ("loop", True, S("tk") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)
SRC = "Source: FAO, Fishery and Aquaculture Country Profile, Lebanon (2024)"

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

_F = {}
def fish(w=200, col=SILVER):
    """a simple side-view fish"""
    if (w, col) in _F: return _F[(w, col)]
    S2 = 2; h = int(w * 0.46); im = Image.new("RGBA", (w * S2, h * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); W2, H2 = w * S2, h * S2
    d.polygon([(W2 * 0.70, H2 * 0.5), (W2 * 0.99, H2 * 0.08), (W2 * 0.92, H2 * 0.5), (W2 * 0.99, H2 * 0.92)], fill=tuple(max(0, c - 40) for c in col) + (255,))
    d.ellipse((W2 * 0.02, H2 * 0.12, W2 * 0.82, H2 * 0.88), fill=col + (255,))
    d.polygon([(W2 * 0.35, H2 * 0.16), (W2 * 0.52, H2 * 0.0), (W2 * 0.58, H2 * 0.18)], fill=tuple(max(0, c - 40) for c in col) + (255,))
    d.ellipse((W2 * 0.13, H2 * 0.36, W2 * 0.21, H2 * 0.52), fill=(255, 255, 255, 255)); d.ellipse((W2 * 0.155, H2 * 0.40, W2 * 0.195, H2 * 0.48), fill=(11, 14, 20, 255))
    d.arc((W2 * 0.22, H2 * 0.2, W2 * 0.42, H2 * 0.8), 300, 60, fill=(255, 255, 255, 120), width=6)
    _F[(w, col)] = im.resize((w, h), Image.LANCZOS); return _F[(w, col)]

def crate(w=360, n=3, cols=(SILVER, LILAC, BLUE)):
    """a crate with fish in it"""
    h = int(w * 0.62); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(n):
        f = fish(int(w * 0.62), cols[i % len(cols)]); im.alpha_composite(f, (int(w * 0.08 + (i % 2) * w * 0.28), int(h * 0.02 + i * h * 0.14)))
    d.rounded_rectangle((0, h * 0.42, w, h), radius=14, fill=(54, 42, 108, 255))
    for k in range(3): d.line([(16, h * 0.55 + k * h * 0.14), (w - 16, h * 0.55 + k * h * 0.14)], fill=(124, 92, 255, 255), width=5)
    return im

_H = {}
def hall(w=920, h=900):
    """the auction hall: a stone wall with three arches, crates under them (a drawing, not a photo)"""
    if (w, h) in _H: return _H[(w, h)]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    stone, joint = (54, 60, 78), (34, 38, 52)
    d.rounded_rectangle((0, 0, w, h), radius=24, fill=stone + (255,))
    for r in range(0, h, 58):
        off = 0 if (r // 58) % 2 == 0 else 60
        d.line([(0, r), (w, r)], fill=joint + (255,), width=4)
        for x in range(-off, w, 120): d.line([(x, r), (x, r + 58)], fill=joint + (255,), width=4)
    aw = (w - 4 * 40) / 3; top = 170
    for i in range(3):
        x0 = 40 + i * (aw + 40); x1 = x0 + aw
        d.rectangle((x0, top + aw / 2, x1, h), fill=(16, 19, 28, 255))
        d.pieslice((x0, top, x1, top + aw), 180, 360, fill=(16, 19, 28, 255))
        d.arc((x0 - 14, top - 14, x1 + 14, top + aw + 14), 180, 360, fill=LILAC + (255,), width=14)
        d.line([(x0 - 7, top + aw / 2), (x0 - 7, h)], fill=LILAC + (255,), width=14); d.line([(x1 + 7, top + aw / 2), (x1 + 7, h)], fill=LILAC + (255,), width=14)
        c = crate(int(aw * 0.84), 3, ((SILVER, LILAC, BLUE), (BLUE, SILVER, VIOLET), (LILAC, BLUE, SILVER))[i]); im.alpha_composite(c, (int(x0 + aw * 0.08), int(h - c.height - 30)))
    _H[(w, h)] = im; return im

def hall_scene(t, k_in, pill_txt, pill_col, tp=None):
    im = bg(True)
    put(im, lift(hall(), True), 540, 1080, k_in, 0.96 + 0.04 * k_in)
    if pill_txt:
        kp = spring((t - tp) / 0.35) if tp is not None else 1
        put(im, pill(pill_txt, 48, pill_col, padx=34, pady=14), 540, 1660 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    return im

# ---------- scenes ----------
def sc_hook(t):
    t58 = WT("h2", "1958"); t400 = WT("h2", "400")
    if t < t58 - 0.1: im = hall_scene(t, 1, "TRIPOLI · FISH AUCTION", VIOLET)
    elif t < t400 - 0.1: im = hall_scene(t, 1, "SINCE 1958", BLUE, t58 - 0.1)
    else: im = hall_scene(t, 1, "ARCHES ≈ 400 YEARS OLD", GREEN_UI, t400 - 0.1)
    footnote(im, SRC + " · drawing illustrative", True, 1870)
    return im

def sc_myth(t):
    im = bg(False); t0 = S("p1"); tr = WT("p1", "rare"); tl = WT("p1", "Look")
    w, h = 860, 560; win = window(w, h, "Auctions in Lebanon are…", False)
    tt = T("Rare?", 120, L_INK, 700); win.alpha_composite(tt, (int(w / 2 - tt.width / 2), 210))
    put(im, lift(win), 540, 1000, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tl - 0.05:
        cx = 540; y = 1000 - h / 2 + 210 + tt.height / 2 + 2
        strike(im, cx - tt.width / 2 - 20, y, cx + tt.width / 2 + 20, eout((t - tl + 0.05) / 0.25))
    put(im, head("nour", 130), 400, 1460, ease((t - tr) / 0.3)); put(im, head("sami", 130), 680, 1460, ease((t - tr - 0.1) / 0.3))
    return im

# ports from north to south on a schematic coast (sea on the left)
PORTS = (("Tripoli", 0.10, "Tripoli."), ("Dora", 0.40, "Dora."), ("Ouzai", 0.48, "Ouzai."), ("Saida", 0.66, "Saida."), ("Sour", 0.86, "Sour."))
def sc_ports(t):
    im = bg(True); t0 = S("s1"); tf = WT("s1", "Fish")
    w, h = 900, 1180; win = window(w, h, "Lebanon's coast · fish auctions", True)
    d = ImageDraw.Draw(win); y0, y1 = 120, h - 60
    pts = [(300 + 40 * math.sin(i / 3.0) + i * 6, y0 + (y1 - y0) * i / 20) for i in range(21)]
    d.polygon([(0, 71), (pts[0][0], 71)] + pts + [(pts[-1][0], h), (0, h)], fill=(22, 34, 64, 255))
    d.line(pts, fill=BLUE + (255,), width=6)
    sea = T("SEA", 26, D_MUTE, 700, True); win.alpha_composite(sea, (110, int(h / 2)))
    for name, fy, word in PORTS:
        tw = WT("s1", word); ki = spring((t - tw + 0.1) / 0.35)
        if ki <= 0: continue
        y = y0 + (y1 - y0) * fy; x = 300 + 40 * math.sin(fy * 20 / 3.0) + fy * 120
        r = 22 * min(1.2, ki); d.ellipse((x - r, y - r, x + r, y + r), fill=LILAC + (255,))
        lab = T(name, 54, D_INK, 700); win.alpha_composite(fade_in(lab, ki), (int(x + 50), int(y - lab.height / 2 + (1 - ki) * 12)))
    put(im, lift(win, True), 540, 1110, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tf - 0.1:
        kp = spring((t - tf + 0.1) / 0.35)
        put(im, pill("5 ports · 5 fish auctions", 46, VIOLET, padx=32, pady=14), 540, 1770 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
    footnote(im, SRC + " · map schematic", True, 1870)
    return im

WHO = (("Restaurants,", ("R", VIOLET), "Restaurant"), ("fishmongers,", ("F", GREEN_APP), "Fishmonger"), ("families.", "nour", "Family"))
def sc_crowd(t):
    im = bg(False); t0 = S("s2"); tc = WT("s2", "same")
    w, h = 900, 1150; win = window(w, h, "One crate · up for bids", False)
    c = crate(420); win.alpha_composite(c, (int(w / 2 - c.width / 2), 110))
    for i, (word, who, lab) in enumerate(WHO):
        tw = WT("s2", word); ki = spring((t - tw + 0.1) / 0.35)
        if ki <= 0: continue
        y = 450 + i * 210; hd = head(who, 140); win.alpha_composite(fade_in(hd, ki), (int(110 + (1 - ki) * 30), y))
        tt = T(lab, 60, L_INK, 700); win.alpha_composite(fade_in(tt, ki), (290, int(y + 70 - tt.height / 2)))
        pl = pill("BIDDING", 26, PILL_L, VIOLET, 16, 8); win.alpha_composite(fade_in(pl, ki), (w - 90 - pl.width, int(y + 70 - pl.height / 2)))
    put(im, lift(win), 540, 1110, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    if t >= tc - 0.05: select_box(im, (540 - 230, 1110 - h / 2 + 100, 540 + 230, 1110 - h / 2 + 110 + c.height + 10), eout((t - tc + 0.05) / 0.3))
    footnote(im, "Customers as listed by FAO · people illustrative", False, 1870)
    return im

BIDS = (("wait.", ("R", VIOLET), 40), ("bids", ("F", GREEN_APP), 46), ("price,", "nour", 52), ("spot,", ("R", VIOLET), 58))
def sc_bids(t):
    im = bg(True); t0 = S("f1"); te = WT("f1", "everyone.")
    w, h = 900, 1150; win = window(w, h, "One crate · live", True)
    c = crate(380); win.alpha_composite(c, (int(w / 2 - c.width / 2), 100))
    shown, who_now = 34, None
    for word, who, amt in BIDS:
        if t >= WT("f1", word) - 0.1: shown, who_now = amt, who
    lab = T("CURRENT BID", 26, D_MUTE, 700, True); win.alpha_composite(lab, (int(w / 2 - lab.width / 2), 380))
    pv = T(f"${shown}", 150, D_INK, 700); win.alpha_composite(pv, (int(w / 2 - pv.width / 2), 425))
    if who_now is not None:
        hd = head(who_now, 120); win.alpha_composite(hd, (int(w / 2 - 60), 640))
    sl = head("sami", 110); win.alpha_composite(sl, (90, h - 200))
    st = T("Seller", 40, D_MUTE, 700); win.alpha_composite(st, (220, int(h - 145 - st.height / 2)))
    eye = pill("everyone sees every bid", 30, PILL_D, (255, 255, 255), 20, 10)
    if t >= te - 0.1: win.alpha_composite(fade_in(eye, spring((t - te + 0.1) / 0.35)), (w - 70 - eye.width, int(h - 145 - eye.height / 2)))
    put(im, lift(win, True), 540, 1110, ease((t - t0 + 0.12) / 0.25), 0.96 + 0.04 * spring((t - t0 + 0.12) / 0.5))
    stamp_at(im, big_stamp("SOLD", GREEN_UI, 120, -8), 760, 900, t, te + 0.25)
    footnote(im, "Example sale · bids and people illustrative", True, 1870)
    return im

def sc_loop(t):
    tf = WT("tk", "Fast,")
    if t < tf - 0.1: im = hall_scene(t, 1, "TRIPOLI · FISH AUCTION", VIOLET)
    else: im = hall_scene(t, 1, "Fast · fair · in the open", GREEN_UI, tf - 0.1)
    footnote(im, SRC + " · drawing illustrative", True, 1870)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 23, BLUE), (540, 5, VIOLET), (750, 8, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "myth": sc_myth, "ports": sc_ports, "crowd": sc_crowd, "bids": sc_bids, "loop": sc_loop, "outro": sc_outro}

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
    s.ding(WT("h1", "auction.") - 0.05, 1318, 0.03)
    s.pop(WT("h2", "1958") - 0.1, 0.04, 620); s.pop(WT("h2", "400") - 0.1, 0.04, 680)
    s.thud(WT("p1", "Look") - 0.05, 0.05)
    for _, _, word in PORTS: s.pop(WT("s1", word) - 0.1, 0.035, 600)
    s.ding(WT("s1", "Fish") - 0.05, 1568, 0.03)
    for word, _, _ in WHO: s.pop(WT("s2", word) - 0.1, 0.035, 560)
    for word, _, _ in BIDS: s.tick(WT("f1", word) - 0.1, 0.02)
    s.thud(WT("f1", "everyone.") + 0.25, 0.07); s.ding(WT("f1", "everyone.") + 0.35, 1568, 0.03)
    s.pop(WT("tk", "Fast,") - 0.1, 0.04, 680)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson23_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
