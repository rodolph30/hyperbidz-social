"""Auction short 30 (v3, standard, who: finale): "Seven problems, one fix". A fast recap montage of the campaign: seven
everyday buying and selling problems (Sami and Nour), each struck through as its auction fix lands (buyers compete; everyone
bids at once; a countdown; a small deposit; a track record; every bid in the open; the buyers decide). Then the perspective
close with three sourced numbers: 1,882 homes at auction in one October week in Australia's capital cities (Cotality);
about 8 million used cars up for auction in a year in Japan (USS); Tripoli's fish auction since 1958 (FAO). Ends on the
open question "So why do we still sell everything else by chat?" over the same card the video opens on, so the replay loops.
Run: python3 tools/lessons/lesson30.py /abs/out.mp4    Stills: python3 tools/lessons/peek.py <this> out.png 1,5,9"""
import sys, os
_OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import *
import music as MU
from founder_common import render
from lesson30_lines import LINES, SPEED

TL = N.Timeline(LINES, start=0.3, speed=SPEED); CAP = KCaps(TL)
S = lambda k: TL.t(k)[0]; E = lambda k: TL.t(k)[1]; WT = TL.wt
TOTAL = TL.end + 0.5
STYLE, SEED = "lofi", 30
XF = 0.16
PK = [f"p{i}" for i in range(1, 8)]
SC = [("hook", False, 0.0, S("p1") - 0.1)]
for i, k in enumerate(PK):
    nxt = PK[i + 1] if i < 6 else "au"
    SC.append((k, i % 2 == 0, S(k) - 0.1, S(nxt) - 0.1))
SC += [("au", False, S("au") - 0.1, S("jp") - 0.1), ("jp", True, S("jp") - 0.1, S("tr") - 0.1),
       ("tr", False, S("tr") - 0.1, S("q") - 0.1), ("loop", False, S("q") - 0.1, S("e2") - 0.15), ("outro", False, S("e2") - 0.15, TOTAL)]
GREY_TXT = (110, 116, 130)

# (who, problem shown, fix shown)
PROBS = [("sami", "“$4,500?”", "Buyers compete"),
         ("sami", "One buyer at a time", "Everyone bids at once"),
         ("sami", "“Is it still available?”", "A countdown everyone sees"),
         ("sami", "“I'm on my way.”", "A small deposit"),
         ("nour", "“Pay me first.”", "A track record you can check"),
         ("nour", "“DM for price”", "Every bid in the open"),
         ("sami", "“What's it worth?”", "The buyers decide")]
SUBS = ["first offer on a $9,000 car", "every chat starts from zero", "days pass, nobody decides", "…nobody comes",
        "a stranger wants the money", "a different price for everyone", "so you guess"]

def fade_in(layer, k):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * clamp(k * 1.5)))); return layer

def dim(layer, a):
    layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda q: int(q * a))); return layer

def fit(text, size, col, maxw, w=700):
    tt = T(text, size, col, w)
    while tt.width > maxw and size > 30: size -= 2; tt = T(text, size, col, w)
    return tt

def fix_time(key):
    ws = TL.words(key)
    for i, (s, b, t) in enumerate(ws):
        if s.endswith("?") and i + 1 < len(ws): return ws[i + 1][2]
    return ws[len(ws) // 2][2]

def tally(im, n_done, t_new, t, dark, y=1580):
    """seven dots: the problems counted so far"""
    for j in range(7):
        x = 540 + (j - 3) * 92; r = 30
        d = ImageDraw.Draw(im)
        filled = j < n_done or (t_new is not None and j == n_done and t >= t_new)
        if filled:
            k = 1.0 if j < n_done else spring((t - t_new) / 0.35); rr = r * (0.6 + 0.4 * k)
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=GREEN_UI + (255,))
        else:
            d.ellipse((x - r, y - r, x + r, y + r), outline=((70, 76, 96) if dark else (214, 216, 224)) + (255,), width=4)

def seven_card(t, k_fix=0.0):
    """the hook card, reused by the loop so the replay is seamless"""
    w, h = 860, 560; c = card(w, h, False, 34)
    c.alpha_composite(T("EVERYDAY PROBLEMS", 28, GREY_TXT, 700, True), (60, 56))
    c.alpha_composite(T("7", 260, L_INK, 700), (60, 96))
    c.alpha_composite(T("buying and selling", 44, GREY_TXT, 600), (60, 410))
    c.alpha_composite(head("sami", 150), (w - 60 - 150 - 120, 150))
    c.alpha_composite(head("nour", 150), (w - 60 - 150, 230))
    return c

# ---------- scenes ----------
def sc_hook(t):
    im = bg(False); tf = WT("h1", "fix."); t2 = S("h2")
    put(im, lift(seven_card(t)), 540, 1000, 1.0, 0.97 + 0.03 * spring(t / 0.5))
    stamp_at(im, big_stamp("1 FIX", GREEN_UI, 110, -8), 760, 1330, t, tf - 0.05)
    if t >= t2 - 0.1:
        k = ease((t - t2 + 0.1) / 0.3)
        im2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); tally(im2, 0, None, t, False); im.alpha_composite(dim(im2, k))
        kl = spring((t - WT("h2", "lived.") + 0.1) / 0.4)
        if kl > 0: put(im, pill("count yours", 40, BLUE, padx=28, pady=12), 540, 1680 + (1 - kl) * 20, min(1, kl * 1.5))
    footnote(im, "Prices and chats in this video are illustrative", False, 1850)
    return im

def make_prob(i):
    key = PK[i]; who, prob, fix = PROBS[i]; dark = i % 2 == 0
    def sc(t):
        im = bg(dark); t0 = S(key); tf = fix_time(key)
        # problem card
        w, h = 880, 300; c = card(w, h, dark, 30)
        c.alpha_composite(head(who, 150), (40, 75))
        ink = D_INK if dark else L_INK
        pt = fit(prob, 58, ink, 620); c.alpha_composite(pt, (220, 80))
        c.alpha_composite(fit(SUBS[i], 32, D_MUTE if dark else GREY_TXT, 620, 500), (220, 100 + pt.height + 20))
        if t >= tf - 0.05:
            ks = eout((t - tf + 0.05) / 0.3)
            ImageDraw.Draw(c).line([(214, 80 + pt.height * 0.6), (214 + (pt.width + 12) * ks, 80 + pt.height * 0.6)], fill=RED_UI + (255,), width=9)
        kc = spring((t - t0 + 0.1) / 0.4); a = 1 - 0.35 * clamp((t - tf) / 0.4)
        put(im, lift(dim(c, a), dark), 540, 820 + (1 - kc) * 30, min(1, kc * 1.5), 0.96 + 0.04 * kc)
        # the fix
        kf = spring((t - tf + 0.05) / 0.4)
        if kf > 0:
            fc = card(880, 230, dark, 30, fill=(20, 60, 46) if dark else (232, 247, 240))
            fc.alpha_composite(T("THE FIX", 26, GREEN_UI, 700, True), (50, 40))
            fc.alpha_composite(fit(fix, 60, ink, 780), (50, 92))
            put(im, lift(fc, dark), 540, 1200 + (1 - kf) * 30, min(1, kf * 1.5), 0.9 + 0.1 * kf)
        tally(im, i, tf, t, dark)
        if i == 0: footnote(im, "Car and prices are illustrative", dark, 1850)
        return im
    return sc

def stat_scene(dark, key, label, word, val_fn, pill_word, pill_text, notes, chip_text=None, chip_word=None):
    def sc(t):
        im = bg(dark); t0 = S(key); tv = WT(key, word); tp = WT(key, pill_word)
        if chip_text:
            kc = spring((t - (WT(key, chip_word) if chip_word else t0) + 0.1) / 0.4)
            if kc > 0: put(im, chip(chip_text, dark, 30), 540, 760 + (1 - kc) * 20, min(1, kc * 1.5))
        k = spring((t - tv + 0.15) / 0.4)
        c = stat(label, val_fn(t, tv), "", 860, dark, 180, LILAC if dark else BLUE)
        if k > 0: put(im, lift(c, dark), 540, 1060 + (1 - k) * 30, min(1, k * 1.5), 0.96 + 0.04 * k)
        if t >= tp - 0.15:
            kp = spring((t - tp + 0.15) / 0.35)
            put(im, pill(pill_text, 48, GREEN_UI, padx=30, pady=14), 540, 1060 + c.height / 2 + 100 + (1 - kp) * 20, min(1, kp * 1.5), 0.9 + 0.1 * kp)
        for j, n in enumerate(notes): footnote(im, n, dark, 1820 + 38 * j if len(notes) > 1 else 1858)
        return im
    return sc

sc_au = stat_scene(False, "au", "Homes taken to auction · one week", "1,882",
                   lambda t, tv: f"{int(roll(t, tv - 0.1, 1.2, 0, 1882)):,}", "Australia's", "Australia's capital cities",
                   ["Cotality, week ending 25 October 2026: 1,882 capital city auctions"], "Australia · October 2026", None)
sc_jp = stat_scene(True, "jp", "Used cars up for auction · one year", "eight",
                   lambda t, tv: f"{roll(t, tv - 0.1, 1.0, 0, 8):.0f} million", "used", "Japan · dealer auctions",
                   ["USS Co., FY2025 results presentation, May 2026", "Vehicles consigned across Japan's auction market"])
sc_tr = stat_scene(False, "tr", "Fish auction in Mina-Tripoli · since", "1958.",
                   lambda t, tv: f"{int(roll(t, tv - 0.1, 0.9, 2026, 1958))}", "1958.", "Open all year",
                   ["FAO country profile, Lebanon: fish auctions at Dora, Ouzai, Saida, Tripoli and Sour"], "Lebanon · Tripoli", None)

def sc_loop(t):
    im = bg(False); t0 = S("q") - 0.1; te = WT("q", "else"); tc = WT("q", "chat?")
    put(im, lift(seven_card(t)), 540, 1000, ease((t - t0) / 0.2))
    stamp_at(im, big_stamp("1 FIX", GREEN_UI, 110, -8), 760, 1330, t, te - 0.05)
    tally(im, 7, None, t, False)
    kq = spring((t - tc + 0.1) / 0.4)
    if kq > 0: put(im, pill("by chat?", 48, BLUE, padx=30, pady=14), 540, 1690 + (1 - kq) * 20, min(1, kq * 1.5))
    footnote(im, "Prices and chats in this video are illustrative", False, 1850)
    return im

def sc_outro(t):
    im = bg(False); k = t - S("e2") + 0.15
    for i, (x, n, col) in enumerate(((330, 30, BLUE), (540, 7, VIOLET), (750, 1, GREEN_APP))):
        kk = spring((k - i * 0.12) / 0.45)
        if kk > 0: put(im, paddle(n, col, 120), x, 760 + (1 - kk) * 80, min(1, kk * 1.5))
    put(im, sami("happy", 200), 380, 1300, ease(k / 0.3)); put(im, nour("happy", 200), 700, 1300, ease(k / 0.3))
    fk = (t - WT("e2", "Follow")); put(im, pill("+  Follow", 52, VIOLET), 540, 1020, ease(fk / 0.2), 0.8 + 0.2 * spring(fk / 0.4))
    tcl = WT("e2", "stories."); cx = 540 + 260 - 200 * eout((t - tcl + 0.6) / 0.5); cy = 1020 + 260 - 230 * eout((t - tcl + 0.6) / 0.5)
    if t >= tcl - 0.6: put(im, cursor(), cx + 20, cy + 30)
    ripple(im, 560, 1030, (t - tcl) / 0.5)
    if t > TOTAL - 0.45: im = Image.blend(im.convert("RGB"), Image.new("RGB", (W, H), STAGE), clamp((t - (TOTAL - 0.45)) / 0.45)).convert("RGBA")
    return im

FN = {"hook": sc_hook, "au": sc_au, "jp": sc_jp, "tr": sc_tr, "loop": sc_loop, "outro": sc_outro}
for i, k in enumerate(PK): FN[k] = make_prob(i)

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
    s.thud(WT("h1", "fix.") - 0.05, 0.08)
    for j in range(7): s.pop(S("h2") + j * 0.06, 0.02, 520 + j * 30)
    s.ding(WT("h2", "lived.") - 0.1, 1318, 0.03)
    for i, k in enumerate(PK):
        tf = fix_time(k); s.pop(S(k) - 0.05, 0.04, 600); s.thud(tf - 0.05, 0.05); s.ding(tf + 0.1, 1318 if i % 2 else 1568, 0.03)
    for k, w in (("au", "1,882"), ("jp", "eight"), ("tr", "1958.")):
        for j in range(5): s.tick(WT(k, w) - 0.1 + j * 0.18, 0.018)
    s.ding(WT("au", "Australia's") - 0.1, 1568, 0.03); s.ding(WT("jp", "used") - 0.1, 1318, 0.03); s.ding(WT("tr", "1958.") + 0.8, 1568, 0.03)
    s.thud(WT("q", "else") - 0.05, 0.07); s.ding(WT("q", "chat?") - 0.1, 1318, 0.03)
    sfx = s.buf[: int(TOTAL * N.SR)]
    voice = TL.voice_track(TOTAL); bed = MU.make(TOTAL, STYLE, SEED); speak = TL.speaking(TOTAL)
    out = MU.mix(voice, bed, speak, sfx * 0.6, bed_db=-20, duck_db=-7)
    import wave
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(N.SR); w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    wav = "/tmp/lesson30_audio.wav"
    if "--stills" not in sys.argv: audio(wav)
    render(frame, TOTAL, wav, _OUT)
