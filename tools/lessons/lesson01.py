"""Auction lesson 01 (v2): "Haggle or bid?" Narrated explainer, drawn frame by frame (no AI video).
Owner's rules (16 Oct 2026): no HyperBidz, no app, no lesson/chapter tags; a narrator voice; one idea on screen at a time;
quiet music, different each video; app colours; the recurring cast (Sami the seller, Nour the buyer, the bidders).
Run from anywhere: python3 tools/lessons/lesson01.py /abs/out.mp4   (stills: python3 tools/lessons/peek.py <this> out.png 1,5,9)"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cast import *
import narration as N, music as MU
from founder_common import render
from lesson01_lines import LINES

TL = N.Timeline(LINES, start=0.5)
T = TL.t; WD = TL.word
TOTAL = TL.end + 0.6
STYLE, SEED = "keys", 1                       # music for this lesson (rotate styles across lessons)

def s_(k): return T(k)[0]
def e_(k): return T(k)[1]
SC = [("table", 0.0, s_("d1") - 0.3), ("define", s_("d1") - 0.3, s_("d3") - 0.3), ("auction", s_("d3") - 0.3, s_("s1") - 0.35),
      ("y1995", s_("s1") - 0.35, s_("s2") - 0.15), ("computer", s_("s2") - 0.15, WD("s2", "broken") - 0.25),
      ("pointer", WD("s2", "broken") - 0.25, s_("s4") - 0.3), ("email", s_("s4") - 0.3, s_("s6") - 0.3), ("ebay", s_("s6") - 0.3, s_("l1") - 0.35),
      ("lesson", s_("l1") - 0.35, s_("c1") - 0.3), ("callback", s_("c1") - 0.3, s_("e1") - 0.35), ("end", s_("e1") - 0.35, TOTAL)]

# ---------- set pieces (precomputed) ----------
BG_TABLE = app_stage(cone=(540, 40, 520, 1240)); table(BG_TABLE)
BG_PLAIN = app_stage(spot=(540, 900, 600, 700), spot_a=0.18)
BG_SPOT = app_stage(spot=(540, 1150, 420, 560), spot_a=0.2, cone=(540, 60, 330, 1300), floor_y=1460)
RADIO = shadowed(radio(330), 16, 12, 120)
ARROW = Image.new("RGBA", (110, 150), (0, 0, 0, 0)); _d = ImageDraw.Draw(ARROW); _d.rectangle((40, 0, 70, 92), fill=(255, 120, 130, 255)); _d.polygon([(8, 88), (102, 88), (55, 146)], fill=(255, 120, 130, 255))

def lerp_price(t, t0, t1, a, b, step=5):
    k = ease((t - t0) / max(0.01, t1 - t0)); v = a + (b - a) * k; return int(round(v / step) * step)

def talk_env(t, spans):
    for a, b in spans:
        if a <= t <= b: return max(0, np.sin((t - a) * 17)) * 0.9
    return 0

def headline_top(im, t, t0, t1, markup, y=330, size=80):
    a = fade(t, t0, t1, 0.3, 0.3)
    if a > 0: put(im, rich_c(markup, size, "serif", WHITE, LILAC, 960), 540, y, a, 0.96 + 0.04 * eout((t - t0) / 0.4))

def stamp_in(im, text, col, x, y, t0, t, size=72, rot=-10):
    if t >= t0: put(im, stamp(text, col, size, rot), x, y, min(1, (t - t0) / 0.08), 1 + 0.5 * (1 - eout((t - t0) / 0.25)))

# ---------- scenes ----------
def sc_table(t):
    im = BG_TABLE.copy(); put(im, RADIO, 540, 1092)
    # haggling: Nour offers, Sami counters (one bubble at a time)
    hag = [(WD("p2", "love"), "n", "$60?"), (WD("p2", "haggle"), "s", "$110"), (WD("p3", "quietly"), "n", "$70?"), (WD("p3", "sellers"), "s", "$100")]
    say = None
    for at, who, txt in hag:
        if t >= at: say = (at, who, txt)
    if say and t < e_("p3") + 0.3:
        at, who, txt = say; x = 230 if who == "s" else 870
        put(im, bubble(txt, 46, WHITE, STAGE, "left" if who == "s" else "right"), x, 735, min(1, (t - at) / 0.1), 0.85 + 0.15 * pop((t - at) / 0.3))
    # the price tag: $120, then it slides down to $85
    if t < s_("p5"): price = 120
    else: price = lerp_price(t, s_("p5") + 0.2, WD("p5", "Down"), 120, 85)
    tg = tag(f"${price}"); pulse = 1 + 0.08 * np.sin(np.clip((t - WD("p4", "starts")) / 0.6, 0, 1) * np.pi)
    put(im, tg, 690, 880, 1, pulse, 6 * np.sin(t * 1.5))
    if s_("p5") + 0.2 <= t < s_("d1"): put(im, ARROW, 880, 860 + 14 * np.sin(t * 5), ease((t - s_("p5") - 0.2) / 0.3))
    sold = t >= WD("p5", "Down")
    sami_mood = "sad" if sold else "happy"
    put(im, sami(sami_mood, 230, 1, talk_env(t, [(WD("p2", "haggle"), WD("p2", "haggle") + 0.5), (WD("p3", "sellers"), WD("p3", "sellers") + 0.5)]), int(t * 9) % 41 == 0), 205, 1100)
    put(im, nour("happy", 230, -1, talk_env(t, [(WD("p2", "love"), WD("p2", "love") + 0.5), (WD("p3", "quietly"), WD("p3", "quietly") + 0.5)]), int(t * 9) % 37 == 0), 875, 1100)
    # one buyer, one seller
    put(im, chip_label("BUYER"), 875, 1312, ease((t - WD("p4", "buyer")) / 0.25))
    put(im, chip_label("SELLER"), 205, 1312, ease((t - WD("p4", "seller")) / 0.25))
    if sold: stamp_in(im, "SOLD $85", (170, 176, 196), 470, 760, WD("p5", "Down"), t, 68, -10)
    # someone who'd have paid $140, never asked
    if t >= s_("p6"):
        a = ease((t - s_("p6")) / 0.4); g = bidder(2, 170); g.putalpha(g.getchannel("A").point(lambda v: int(v * 0.55)))
        put(im, g, 540, 520, a); put(im, bubble("I'd pay $140", 40, (220, 222, 232), STAGE, "left"), 640, 370, ease((t - WD("p6", "paid")) / 0.25))
        put(im, chip_label("NEVER ASKED", LILAC), 540, 660, ease((t - WD("p6", "never")) / 0.25))
    headline_top(im, t, 0.35, s_("p2") + 0.1, "Here's a [paradox.]")
    return im

CARD_W, CARD_H = 860, 500
def def_card(k_underline):
    im = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, CARD_W - 1, CARD_H - 1), radius=28, fill=(248, 247, 252, 255))
    im.alpha_composite(tl("price discovery", serif(84), STAGE), (56, 52)); im.alpha_composite(tl("noun · economics", mono(24), (110, 104, 140)), (60, 170))
    d.line([(56, 222), (CARD_W - 56, 222)], fill=(214, 210, 230, 255), width=2)
    lines = ["Finding out what something is", "really worth by letting buyers", "compete for it."]
    y = 252
    for i, ln in enumerate(lines):
        L = tl(ln, sans(42, 500), (40, 44, 60)); im.alpha_composite(L, (56, y))
        if i == 2 and k_underline > 0:
            w = tl("compete for it", sans(42, 500), (0, 0, 0)).width; d.line([(56, y + L.height + 4), (56 + w * k_underline, y + L.height + 4)], fill=VIOLET + (255,), width=7)
        y += 62
    return im

def sc_define(t):
    im = BG_PLAIN.copy(); k = ease((t - (WD("d1", "price") - 0.15)) / 0.4)
    if k > 0:
        c = shadowed(def_card(eout((t - WD("d2", "compete")) / 0.5)), 26, 20, 150)
        put(im, c, 540, 900, k, 0.94 + 0.06 * eout((t - WD("d1", "price")) / 0.5))
    else:
        put(im, rich_c("Economists have a name for it…", 54, "serif", MUTED_APP, LILAC, 900), 540, 900, ease((t - s_("d1") + 0.1) / 0.3))
    return im

def sc_auction(t, t0=None, end_sold=False):
    """the table again, now with bidders raising paddles; the tag climbs"""
    t0 = s_("d3") if t0 is None else t0
    im = BG_TABLE.copy(); put(im, RADIO, 540, 1092)
    for i, (x, n) in enumerate(((250, 14), (540, 27), (830, 8))):
        at = t0 + 0.25 + i * 0.45; k = eout((t - at) / 0.35)
        if k > 0: put(im, bidder_with_paddle(i, n, 150, k), x, 600 + (1 - k) * 120 - 10 * max(0, np.sin((t - at) * 6)) * (t - at < 1.2), k)
    price = lerp_price(t, t0 + 0.3, t0 + 1.9, 85, 140)
    tag_a = 1 - ease((t - WD("c2", "bid")) / 0.15) if end_sold else 1
    put(im, tag(f"${price}"), 690, 880, tag_a, 1, 6 * np.sin(t * 1.5))
    put(im, sami("happy", 230, 1, 0, int(t * 9) % 41 == 0), 205, 1100); put(im, nour("happy", 230, -1, 0, int(t * 9) % 37 == 0), 875, 1100)
    if end_sold: stamp_in(im, "SOLD $140", VIOLET, 560, 860, WD("c2", "bid"), t, 74, -9)
    return im

def marquee(t):
    yr = tl("1995", serif(230), WHITE); g = Image.new("RGBA", (yr.width + 80, yr.height + 80), (0, 0, 0, 0)); g.paste(VIOLET + (200,), (40, 40), yr.getchannel("A"))
    g = g.filter(ImageFilter.GaussianBlur(20)); g.alpha_composite(yr, (40, 40)); return g
def bulbs(w, t, seed):
    im = Image.new("RGBA", (w, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im); ph = np.random.default_rng(seed).uniform(0, 6.28, 22)
    for i in range(22):
        x = 14 + (w - 28) * i / 21; a = 0.5 + 0.5 * np.sin(t * 4 + ph[i]); d.ellipse((x - 7, 13, x + 7, 27), fill=(214, 206, 255, int(255 * a)))
    g = im.filter(ImageFilter.GaussianBlur(6)); g.alpha_composite(im); return g

def sc_1995(t):
    im = BG_PLAIN.copy(); a = ease((t - s_("s1") + 0.2) / 0.4)
    put(im, bulbs(760, t, 1), 540, 760, a); put(im, bulbs(760, t + 1.3, 2), 540, 1060, a)
    put(im, marquee(t), 540, 910, a, 0.9 + 0.1 * eout((t - s_("s1") + 0.2) / 0.6))
    put(im, tl("a true story", serif(64, True), LILAC), 540, 1190, ease((t - WD("s1", "true")) / 0.3))
    return im

def screen(title, lines, t, w=660, h=520, big=None, big_k=0.0):
    sc = crt(title, lines, w, h, t)
    if big and big_k > 0:
        e = tl(big, serif(150, True), LILAC); put(sc, e, w / 2, h * 0.47, big_k, 0.8 + 0.2 * pop(big_k))
    return shadowed(sc, 20, 16, 140)

def sc_computer(t):
    im = BG_PLAIN.copy(); a = ease((t - s_("s2") + 0.1) / 0.4)
    lines = [("> _", (150, 230, 170))]
    if t >= WD("s2", "listed"): lines = [("New listing:", (150, 230, 170)), ("Laser pointer", (230, 230, 240))]
    put(im, screen("AuctionWeb", lines, t), 540, 930, a, 0.95 + 0.05 * eout((t - s_("s2")) / 0.6))
    put(im, chip_label("CALIFORNIA, 1995", SILVER), 540, 1290, ease((t - WD("s2", "California")) / 0.3))
    return im

LP = laser_pointer(540)
def sc_pointer(t):
    im = BG_SPOT.copy(); put(im, pedestal(400, 360, (60, 66, 88)), 540, 1460)
    bob = 6 * np.sin(t * 2); x, y = 540, 1225 + bob
    t0 = WD("s2", "broken")
    if t0 + 0.2 < t < t0 + 1.3 and int(t * 14) % 3 != 0:                      # the beam stutters and dies
        b = Image.new("RGBA", (W, 40), (0, 0, 0, 0)); ImageDraw.Draw(b).rectangle((0, 16, W, 24), fill=(255, 60, 60, 200)); b = b.filter(ImageFilter.GaussianBlur(3))
        im.alpha_composite(b.crop((0, 0, W - 810, 40)), (int(x + 262), int(y - 20)))
    put(im, LP, x, y, ease((t - t0 + 0.25) / 0.3), 1, -6)
    tg = Image.new("RGBA", (230, 90), (0, 0, 0, 0)); ImageDraw.Draw(tg).rounded_rectangle((0, 0, 229, 89), radius=12, fill=(255, 255, 255, 255)); tg.alpha_composite(tl("BROKEN", sans(44, 700), (220, 50, 70)), (30, 18))
    put(im, tg, 380, 1350 + bob * 0.5, ease((t - WD("s2", "pointer")) / 0.3), 1, 10 * np.sin(t * 1.8))
    if t >= s_("s3") - 0.1:
        k = clamp((t - s_("s3") - 0.1) / 1.6); v = 14.83 * eout(k)
        pnl = Image.new("RGBA", (560, 200), (0, 0, 0, 0)); ImageDraw.Draw(pnl).rounded_rectangle((0, 0, 559, 199), radius=28, fill=(17, 20, 30, 235), outline=LILAC + (160,), width=3)
        pnl.alpha_composite(tl("WINNING BID", mono(24), LILAC), (40, 24)); n = tl(f"${v:,.2f}", sans(104, 700), WHITE); pnl.alpha_composite(n, ((560 - n.width) // 2, 56))
        put(im, pnl, 540, 640, ease((t - s_("s3") + 0.1) / 0.3), 0.9 + 0.1 * pop((t - s_("s3") + 0.1) / 0.35))
        stamp_in(im, "SOLD", VIOLET, 790, 880, WD("s3", "eighty"), t, 70, -12)
    return im

def sc_email(t):
    im = BG_PLAIN.copy(); w, h = 900, 640; win = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(win)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=24, fill=(246, 246, 250, 255)); d.rounded_rectangle((0, 0, w - 1, 80), radius=24, fill=(222, 222, 232, 255)); d.rectangle((0, 50, w - 1, 80), fill=(222, 222, 232, 255))
    for i, c in enumerate(((236, 96, 90), (240, 190, 70), (110, 200, 110))): d.ellipse((26 + i * 34, 28, 48 + i * 34, 50), fill=c + (255,))
    win.alpha_composite(tl("Re: laser pointer", sans(30, 600), (60, 64, 80)), (150, 22))
    if t >= s_("s4") + 0.1:
        b = bubble("You know it's broken, right?", 40, BLUE, WHITE, "right"); a = min(1, (t - s_("s4") - 0.1) / 0.12)
        b.putalpha(b.getchannel("A").point(lambda v: int(v * a))); win.alpha_composite(b, (w - b.width - 40, 130)); win.alpha_composite(tl("seller", mono(20), (120, 124, 140)), (w - 120, 250))
    if t >= WD("s5", "collector") - 0.5:
        full = "I'm a collector of broken laser pointers!"; n = min(len(full), int((t - WD("s5", "collector") + 0.5) * 24) + 1)
        b = bubble(full[:n], 38, (226, 222, 246), STAGE, "left", font=serif(42, True)); win.alpha_composite(b, (40, 320)); win.alpha_composite(tl("buyer", mono(20), (120, 124, 140)), (44, 448))
    put(im, shadowed(win, 26, 18, 150), 540, 900, ease((t - s_("s4") + 0.25) / 0.35), 0.95 + 0.05 * eout((t - s_("s4") + 0.25) / 0.5))
    return im

def sc_ebay(t):
    im = BG_PLAIN.copy(); k = ease((t - WD("s6", "became") + 0.1) / 0.35)
    put(im, screen("AuctionWeb" if k < 0.5 else "eBay", [] if k > 0 else [("1995", (150, 230, 170))], t, big="eBay", big_k=k), 540, 930)
    for i in range(10):
        a = np.sin((t - WD("s6", "became") - i * 0.07) * 4)
        if t > WD("s6", "became") + i * 0.07 and a > 0:
            ang = i * 0.63; r = 300 + 40 * (i % 3); put(im, _star(18 + 6 * (i % 3)), 540 + np.cos(ang) * r, 930 + np.sin(ang) * r * 0.62, a)
    return im
def _star(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); c = s / 2
    ImageDraw.Draw(im).polygon([(c, 0), (c + s * .14, c - s * .14), (s, c), (c + s * .14, c + s * .14), (c, s), (c - s * .14, c + s * .14), (0, c), (c - s * .14, c - s * .14)], fill=(230, 226, 255, 255)); return im

def sc_lesson(t):
    im = BG_PLAIN.copy(); p = Image.new("RGBA", (860, 760), (0, 0, 0, 0)); ImageDraw.Draw(p).rounded_rectangle((0, 0, 859, 759), radius=30, fill=(248, 247, 252, 255))
    p.alpha_composite(tl("THE LESSON", mono(28), (110, 104, 140)), (64, 64))
    y = 150
    if t >= WD("l1", "You") - 0.1:
        a = ease((t - WD("l1", "You") + 0.1) / 0.35)
        for ln in ("You don't know what", "your things are worth."):
            L = tl(ln, serif(66), STAGE); L.putalpha(L.getchannel("A").point(lambda v: int(v * a))); p.alpha_composite(L, (64, y)); y += 86
    y = 420
    if t >= s_("l2") - 0.1:
        a = ease((t - s_("l2") + 0.1) / 0.35); L = tl("The buyers do.", serif(104, True), VIOLET); L.putalpha(L.getchannel("A").point(lambda v: int(v * a))); p.alpha_composite(L, (64, y))
    put(im, shadowed(p, 30, 24, 170), 540, 900, ease((t - s_("l1") + 0.3) / 0.35))
    return im

def sc_callback(t):
    return sc_auction(t, t0=s_("c1"), end_sold=True)

def sc_end(t):
    im = BG_PLAIN.copy(); k = t - s_("e1") + 0.35
    for i, (x, n) in enumerate(((330, 14), (540, 27), (750, 8))):
        kk = eout((k - 0.1 - i * 0.15) / 0.35)
        if kk > 0: put(im, paddle(n, [BLUE, VIOLET, GREEN_APP][i], 120), x, 760 - 20 * kk, kk)
    put(im, rich_c("Follow to learn how auctions [really work.]", 76, "serif", WHITE, LILAC, 900), 540, 1060, ease((k - 0.3) / 0.5))
    if t > TOTAL - 0.5: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.5)) / 0.5)).convert("RGBA")
    return im

FN = {"table": sc_table, "define": sc_define, "auction": sc_auction, "y1995": sc_1995, "computer": sc_computer, "pointer": sc_pointer,
      "email": sc_email, "ebay": sc_ebay, "lesson": sc_lesson, "callback": sc_callback, "end": sc_end}

def scene_at(name, t, t0, t1):
    im = FN[name](t)
    if name not in ("end",): im = camera(im, t, t0, t1, 1.0, 1.04, (540, 980))
    if name != "end": subtitle(im, t, TL, 1600)
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
    s = Snd(TOTAL)                                                     # light sound effects only
    for _, t0, _ in SC[1:]: s.whoosh(t0 - 0.2, 0.4, 0.035)
    for k, w in (("p2", "love"), ("p2", "haggle"), ("p3", "quietly"), ("p3", "sellers")): s.pop(WD(k, w), 0.035, 600)
    for i in range(7): s.tick(s_("p5") + 0.25 + i * (WD("p5", "Down") - s_("p5") - 0.25) / 7, 0.018, 1900 - i * 90)
    s.thud(WD("p5", "Down"), 0.08)
    for i in range(3): s.pop(s_("d3") + 0.25 + i * 0.45, 0.03, 700)
    for i in range(12): s.tick(s_("s3") + 0.1 + i * 0.13, 0.014, 2400)
    s.ding(WD("s3", "eighty"), 1568, 0.03)
    for i in range(3): s.pop(s_("c1") + 0.25 + i * 0.45, 0.03, 700)
    s.thud(WD("c2", "bid"), 0.08); s.ding(WD("c2", "bid") + 0.05, 1568, 0.035)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-21, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson01_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
