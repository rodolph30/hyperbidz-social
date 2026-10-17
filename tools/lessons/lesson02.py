"""Auction lesson 02: "The day Rome was sold". Quick pace (speed 1.08), music marimba seed 2. Drawn frame by frame (no AI video).
Owner's rules (16 Oct 2026): no HyperBidz, no app, no tags; narrator; one idea on screen at a time; app colours; Sami + Nour + bidders;
real people are never drawn as faces (the two Roman bidders are shown only as offers on placards).
Run: python3 tools/lessons/lesson02.py /abs/out.mp4   (stills: python3 tools/lessons/peek.py <this> out.png 1,5,9)"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cast import *
import narration as N, music as MU
from founder_common import render
from lesson02_lines import LINES

TL = N.Timeline(LINES, start=0.15, speed=1.08)
T = TL.t; WD = TL.word
TOTAL = TL.end + 0.3
STYLE, SEED = "marimba", 2

def s_(k): return T(k)[0]
def e_(k): return T(k)[1]
SC = [("crown", 0.0, s_("i1") - 0.25), ("english", s_("i1") - 0.25, s_("s1") - 0.25), ("camp", s_("s1") - 0.25, s_("s3") - 0.25),
      ("bids", s_("s3") - 0.25, s_("s5") - 0.25), ("days", s_("s5") - 0.25, s_("t1") - 0.25), ("word", s_("t1") - 0.25, s_("t2") - 0.25),
      ("callback", s_("t2") - 0.25, TOTAL)]

# ---------- set pieces ----------
BG_TABLE = app_stage(cone=(540, 40, 520, 1240)); table(BG_TABLE)
BG_PLAIN = app_stage(spot=(540, 900, 600, 700), spot_a=0.18)
BG_SPOT = app_stage(spot=(540, 1100, 440, 560), spot_a=0.22, cone=(540, 60, 340, 1260), floor_y=1400)
RADIO = shadowed(radio(300), 16, 12, 120)
PED = pedestal(420, 330, (60, 66, 88))

def up_arrow(col=GREEN_APP, w=110, h=150):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(w / 2, 0), (w - 4, h * 0.42), (4, h * 0.42)], fill=col + (255,)); d.rectangle((w * 0.36, h * 0.4, w * 0.64, h), fill=col + (255,)); return im
ARROW = up_arrow()

def _leaf(L, col):
    im = Image.new("RGBA", (L, int(L * 0.42)), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((0, 0, L - 1, int(L * 0.42) - 1), fill=col + (255,))
    ImageDraw.Draw(im).line([(L * 0.08, L * 0.21), (L * 0.9, L * 0.21)], fill=(0, 90, 60, 160), width=2); return im
def wreath(s=520):
    """a laurel wreath (the emperor's crown), in the app's green with a violet ribbon"""
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); c = s / 2; r = s * 0.33; d = ImageDraw.Draw(im); L = int(s * 0.17)
    for side in (1, -1):                                          # left branch (side 1) and its mirror
        for i in range(11):
            th = np.radians(100 + i * 15.5)                       # from near the bottom, round the side, to the top
            px = c + side * r * np.cos(th); py = c + r * np.sin(th)
            dx, dy = -np.sin(th) * side, np.cos(th)               # direction the branch grows
            base = np.degrees(np.arctan2(-dy, dx))
            col = GREEN_APP if i % 2 == 0 else (0, 132, 84)
            for off in (-1, 1):
                lf = _leaf(L, col).rotate(base + off * 32, expand=True, resample=Image.BICUBIC)
                ox = np.cos(th) * side * off * s * 0.045; oy = np.sin(th) * off * s * 0.045
                im.alpha_composite(lf, (int(px + ox - lf.width / 2), int(py + oy - lf.height / 2)))
    d.polygon([(c - 30, c + r + 6), (c + 30, c + r + 6), (c + 16, c + r + 90), (c, c + r + 62), (c - 16, c + r + 90)], fill=VIOLET + (255,))
    d.ellipse((c - 26, c + r - 16, c + 26, c + r + 28), fill=LILAC + (255,))
    return im
WREATH = shadowed(wreath(520), 20, 14, 140)

def headline_top(im, t, t0, t1, markup, y=330, size=90, fin=0.3):
    a = ease((t - t0) / fin) if fin > 0 else 1.0
    a *= 1 - ease((t - (t1 - 0.25)) / 0.25)
    if a > 0: put(im, rich_c(markup, size, "serif", WHITE, LILAC, 960), 540, y, a)

def stamp_in(im, text, col, x, y, t0, t, size=72, rot=-10):
    if t >= t0: put(im, stamp(text, col, size, rot), x, y, min(1, (t - t0) / 0.08), 1 + 0.5 * (1 - eout((t - t0) / 0.25)))

def big_tag(text, w=380, h=150):
    return price_tag(text, w, h, fill=(255, 255, 255), tcol=STAGE, f=sans(int(h * 0.42), 700))

def crown_set(im, t, tag_text, tag_a=1.0, wreath_dy=0.0, wreath_rot=0.0, wreath_a=1.0):
    put(im, PED, 540, 1235)
    bob = 8 * np.sin(t * 1.8)
    put(im, WREATH, 540, 900 + bob + wreath_dy, wreath_a, 1, wreath_rot)
    if tag_text: put(im, big_tag(tag_text), 760, 1130 + bob * 0.4, tag_a, 1, 8 * np.sin(t * 1.4) - 6)

# ---------- scenes ----------
def sc_crown(t):
    im = BG_SPOT.copy()
    crown_set(im, t, "FOR SALE")
    put(im, chip_label("ROME, 193 AD", SILVER), 540, 1470, 1)
    stamp_in(im, "SOLD", VIOLET, 250, 600, WD("h1", "auction"), t, 84, 12)
    headline_top(im, t, 0.0, s_("h2") + 0.1, "Rome was sold [at auction.]", size=80, fin=0)        # on screen from frame one (the cover)
    if t >= s_("h2"):                                                                    # the open loop: who won, and what did he get?
        put(im, rich_c("What did the winner [get?]", 84, "serif", WHITE, LILAC, 960), 540, 330, ease((t - s_("h2")) / 0.3))
    return im

def sc_english(t):
    im = BG_TABLE.copy(); put(im, RADIO, 540, 1100)
    put(im, rich_c("The [English auction]", 72, "serif", WHITE, LILAC, 960), 540, 300, ease((t - s_("i1") + 0.1) / 0.3))
    t0 = s_("i2"); raises = [t0 + 0.0, t0 + 0.4, t0 + 0.8, WD("i3", "last")]
    who = [0, 1, 2, 3]; xs = [180, 400, 640, 880]
    up = sum(1 for r in raises if t >= r) - 1
    for i in range(3):
        k = 1.0 if up == i else 0.0
        put(im, bidder_with_paddle(i, [14, 27, 8][i], 130, eout((t - raises[i]) / 0.25) if up == i else 0), xs[i], 600, 1)
    nk = eout((t - raises[3]) / 0.25) if up >= 3 else 0
    nb = nour("happy", 150, 0, 0, int(t * 9) % 37 == 0); p = paddle(31, LILAC, 92)
    box = Image.new("RGBA", (260, 350), (0, 0, 0, 0)); box.alpha_composite(nb, (10, 350 - nb.height)); box.alpha_composite(p, (160, int(350 - nb.height - p.height * 0.55 * nk + p.height * 0.35) - 0))
    put(im, box, xs[3], 600)
    price = [40, 50, 60, 70][max(0, up)] if t >= raises[0] else 40
    put(im, tag(f"${price}"), 700, 900, 1, 1 + 0.08 * (t >= raises[0]) * max(0, 1 - (t - raises[max(0, up)]) / 0.3), 6 * np.sin(t * 1.5))
    if t >= WD("i2", "up") - 0.1 and t < raises[3]: put(im, ARROW, 900, 900 - 16 * np.sin(t * 6), ease((t - WD("i2", "up") + 0.1) / 0.2), 0.8)
    put(im, sami("happy", 220, 0.6, 0, int(t * 9) % 41 == 0), 210, 1110)
    if t >= raises[3] + 0.35: stamp_in(im, "LAST BID WINS", VIOLET, 640, 1430, raises[3] + 0.35, t, 60, -6)
    return im

def gate(w=700, h=780):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c1, c2 = (52, 60, 84, 255), (70, 78, 104, 255)
    d.rectangle((0, 70, w, h), fill=c1); d.rectangle((0, 40, w, 90), fill=c2)
    for i in range(9): d.rectangle((i * w / 9 + 8, 0, i * w / 9 + w / 9 - 8, 46), fill=c2)
    aw = w * 0.42; d.rectangle(((w - aw) / 2, h * 0.42, (w + aw) / 2, h), fill=(16, 19, 28, 255)); d.ellipse(((w - aw) / 2, h * 0.42 - aw / 2, (w + aw) / 2, h * 0.42 + aw / 2), fill=(16, 19, 28, 255))
    for x in (w * 0.12, w * 0.82): d.rectangle((x, 150, x + 46, h), fill=c2)
    return im
GATE = gate()

def placard(title, val, col, w=330, h=200):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, w - 1, h - 1), radius=22, fill=(17, 20, 30, 235), outline=col + (200,), width=4)
    a = tl(title, mono(22), col); im.alpha_composite(a, ((w - a.width) // 2, 24))
    b = tl(val, sans(64, 700), WHITE); im.alpha_composite(b, ((w - b.width) // 2, 78)); return im

def sc_camp(t):
    im = BG_PLAIN.copy(); put(im, GATE, 540, 1060, ease((t - s_("s1") + 0.25) / 0.35))
    put(im, chip_label("THE EMPEROR'S GUARD", SILVER), 540, 1510, ease((t - WD("s1", "guard")) / 0.3))
    if t >= s_("s2") - 0.1:
        a = ease((t - s_("s2") + 0.1) / 0.3)
        k = clamp((t - s_("s2")) / max(0.5, e_("s2") - s_("s2"))); step = int(k * 7.999)       # they outbid each other in turns
        for side, (x, lab, col) in enumerate(((250, "BIDDER 1", BLUE), (830, "BIDDER 2", LILAC))):
            on = step % 2 == side; pk = (1 - clamp((k * 8 - step) * 3)) if on else 0
            put(im, placard(lab, "RAISES" if on else "...", col), x, 520, a * (1 if on else 0.55), 1 + 0.1 * pk)
    if t >= WD("s2", "Soldiers") - 0.1:                                  # a messenger runs offers back and forth
        ph = (t - WD("s2", "Soldiers")) * 1.6; x = 540 + 260 * np.sin(ph * np.pi); y = 1370 - 30 * abs(np.cos(ph * np.pi * 4))
        put(im, bubble("More?", 36, WHITE, STAGE, "left" if np.cos(ph * np.pi) > 0 else "right"), x, y - 120, 1)
        dot = Image.new("RGBA", (70, 70), (0, 0, 0, 0)); ImageDraw.Draw(dot).ellipse((0, 0, 69, 69), fill=SILVER + (255,)); put(im, dot, x, y)
    return im

def counter_panel(val, label, col=LILAC, w=880, h=360):
    p = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(p).rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=(17, 20, 30, 240), outline=col + (170,), width=4)
    a = tl(label, mono(28), col); p.alpha_composite(a, ((w - a.width) // 2, 34))
    n = tl(f"{val:,}", sans(170, 700), WHITE); p.alpha_composite(n, ((w - n.width) // 2, 92)); return p

def sc_bids(t):
    im = BG_PLAIN.copy(); t0 = s_("s3"); j = WD("s4", "jumped")
    if t < j: v = int(round(20000 * eout((t - t0) / 1.2) / 500) * 500); col = BLUE; who = "BIDDER 1 · SESTERCES PER SOLDIER"
    else: v = 25000; col = LILAC; who = "BIDDER 2 · SESTERCES PER SOLDIER"
    pnl = counter_panel(max(0, v), who, col)
    put(im, shadowed(pnl, 24, 18, 150), 540, 900, ease((t - t0 + 0.2) / 0.3), 1 + (0.12 * (1 - eout((t - j) / 0.3)) if t >= j else 0))
    if j - 0.05 <= t: put(im, rich_c("+5,000", 92, "sans", GREEN_APP, GREEN_APP, 600), 540, 640, ease((t - j) / 0.2) * (1 - ease((t - j - 1.3) / 0.3)), 1, 0)
    if t >= WD("s4", "five"): stamp_in(im, "WINNING BID", VIOLET, 560, 1170, WD("s4", "five"), t, 64, -7)
    return im

def sc_days(t):
    im = BG_SPOT.copy(); t0 = WD("s5", "Sixty"); t1 = WD("s5", "overthrown")
    fall = eout((t - t1) / 0.6) if t >= t1 else 0
    crown_set(im, t, None, 1, wreath_dy=520 * ein(clamp((t - t1) / 0.6)), wreath_rot=-40 * fall, wreath_a=1 - ease((t - t1 - 0.35) / 0.3))
    if t >= s_("s5") and t < t0: put(im, rich_c("He [won.]", 110, "serif", WHITE, LILAC, 900), 540, 360, ease((t - s_("s5")) / 0.25))
    if t >= t0 - 0.1:
        d = 1 + int(65 * clamp((t - t0) / max(0.3, t1 - t0)))
        cal = Image.new("RGBA", (380, 300), (0, 0, 0, 0)); g = ImageDraw.Draw(cal); g.rounded_rectangle((0, 0, 379, 299), radius=24, fill=(248, 247, 252, 255)); g.rounded_rectangle((0, 0, 379, 74), radius=24, fill=VIOLET + (255,)); g.rectangle((0, 50, 379, 74), fill=VIOLET + (255,))
        a = tl("DAY", mono(30), WHITE); cal.alpha_composite(a, ((380 - a.width) // 2, 18)); n = tl(str(d), sans(150, 700), STAGE); cal.alpha_composite(n, ((380 - n.width) // 2, 92))
        put(im, shadowed(cal, 20, 14, 140), 540, 380, ease((t - t0 + 0.1) / 0.25))
    if t >= t1: stamp_in(im, "OVERTHROWN", (200, 204, 216), 540, 960, t1 + 0.15, t, 70, -8)
    return im

def sc_word(t):
    im = BG_PLAIN.copy(); w, h = 860, 560
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, fill=(248, 247, 252, 255))
    c.alpha_composite(tl("auction", serif(120), STAGE), (60, 50)); c.alpha_composite(tl("from Latin  augere", mono(40), (110, 104, 140)), (66, 200))
    d.line([(60, 270), (w - 60, 270)], fill=(214, 210, 230, 255), width=2)
    k = ease((t - WD("t1", "increase") + 0.2) / 0.35)
    if k > 0:
        L = tl("to increase", serif(104, True), VIOLET); L.putalpha(L.getchannel("A").point(lambda v: int(v * k))); c.alpha_composite(L, (60, 320))
        ar = up_arrow(VIOLET, 80, 110); ar.putalpha(ar.getchannel("A").point(lambda v: int(v * k))); c.alpha_composite(ar, (w - 150, 330 - int(20 * k)))
    put(im, shadowed(c, 26, 20, 150), 540, 900, ease((t - s_("t1") + 0.2) / 0.35), 0.94 + 0.06 * eout((t - s_("t1")) / 0.5))
    return im

def sc_callback(t):
    """back to the crown: the bids climb (as in Dio, gradually, then the jump), and the last frames match frame one"""
    im = BG_SPOT.copy(); t0 = s_("t2") + 0.2; tu = WD("t3", "Up")
    if t < tu: v = int(round(20000 * eout((t - t0) / max(0.4, tu - t0 - 0.2)) / 1000) * 1000)
    else: v = 25000
    loop_k = ease((t - (TOTAL - 0.45)) / 0.4)                             # settle back into the opening frame for a seamless replay
    crown_set(im, t, "FOR SALE" if (loop_k > 0.5 or v < 1000) else f"{v:,}")
    if s_("t2") <= t < s_("e1"): put(im, ARROW, 860, 1000 - 18 * np.sin(t * 6), ease((t - s_("t2")) / 0.25), 1, 0)
    if t >= tu: stamp_in(im, "UP", GREEN_APP, 220, 570, tu, t, 96, 12) if loop_k < 0.5 else stamp_in(im, "SOLD", VIOLET, 250, 600, 0, t, 84, 12)
    if t >= s_("e1") - 0.1 and loop_k < 1:
        put(im, rich_c("Follow to learn how auctions [really work.]", 76, "serif", WHITE, LILAC, 900), 540, 340, ease((t - s_("e1") + 0.1) / 0.35) * (1 - loop_k))
    if loop_k > 0:
        put(im, rich_c("Rome was sold [at auction.]", 80, "serif", WHITE, LILAC, 960), 540, 330, loop_k); put(im, chip_label("ROME, 193 AD", SILVER), 540, 1470, loop_k)
    return im

FN = {"crown": sc_crown, "english": sc_english, "camp": sc_camp, "bids": sc_bids, "days": sc_days, "word": sc_word, "callback": sc_callback}

def scene_at(name, t, t0, t1):
    im = FN[name](t)
    im = camera(im, t, t0, t1, 1.0, 1.04, (540, 960))
    subtitle(im, t, TL, 1650)
    return im

XF = 0.18
def frame(t):
    for i, (name, t0, t1) in enumerate(SC):
        if t0 <= t < t1 or i == len(SC) - 1:
            if i > 0 and t < t0 + XF:
                pn, p0, p1 = SC[i - 1]; return zoom_through(scene_at(pn, t, p0, p1), scene_at(name, t, t0, t1), (t - (t0 - XF)) / (2 * XF))
            if i < len(SC) - 1 and t > t1 - XF:
                nn, n0, n1 = SC[i + 1]; return zoom_through(scene_at(name, t, t0, t1), scene_at(nn, t, n0, n1), (t - (t1 - XF)) / (2 * XF))
            return scene_at(name, t, t0, t1).convert("RGB")
    return Image.new("RGB", (W, H))

def audio(path):
    s = Snd(TOTAL)
    for _, t0, _ in SC[1:]: s.whoosh(t0 - 0.2, 0.4, 0.035)
    s.thud(WD("h1", "auction"), 0.08); s.ding(WD("h1", "auction") + 0.04, 1568, 0.03)
    t0 = s_("i2")
    for r in (t0, t0 + 0.4, t0 + 0.8, WD("i3", "last")): s.pop(r, 0.035, 650)
    s.thud(WD("i3", "last") + 0.35, 0.06)
    for i in range(10): s.tick(s_("s2") + 0.6 + i * 0.32, 0.012, 2100)
    for i in range(12): s.tick(s_("s3") + i * 0.1, 0.013, 2300)
    s.pop(WD("s4", "jumped"), 0.05, 800); s.thud(WD("s4", "five"), 0.08)
    a, b = WD("s5", "Sixty"), WD("s5", "overthrown")
    for i in range(10): s.tick(a + i * (b - a) / 10, 0.014, 1900)
    s.thud(b + 0.3, 0.1)
    s.ding(WD("t1", "increase"), 1760, 0.025)
    for i in range(8): s.tick(s_("t2") + 0.2 + i * 0.3, 0.012, 2000 + i * 60)
    s.thud(WD("t3", "Up"), 0.08); s.ding(WD("t3", "Up") + 0.04, 2093, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-21, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson02_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
