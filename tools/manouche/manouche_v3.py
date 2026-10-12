"""The Last One, ep.1 'The Last Manouche' — v3: hook, title slam, character tags, split-screen standoff,
rolling bid ticker, Marwan cut so the banknote never vanishes, driving beat. Usage: python3 manouche_v3.py out.mp4 [--stills t,...]"""
import subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import render as R
import mhelpers as M

W, H, FPS, SR = 1080, 1920, 30, 48000
WHITE, BG, NAVY = R.WHITE, R.BG, R.NAVY
OUT = sys.argv[1]
S = dict(hands=0.0, title=1.3, wide=2.0, uncle=3.0, maya=3.75, split=4.5, mw_a=6.0, mw_b=6.5, react=7.1, mw_d=7.5,
         once=8.0, twice=8.5, knock=9.0, after=9.7, end=11.0)
END = 3.6; TOTAL = S["end"] + END
BIDS = [(4.6, "ABOU SAMI", 200000), (5.1, "MAYA", 500000), (5.6, "ABOU SAMI", 1000000)]
MARWAN_BID = 6.6

def decode(src, t0, t1):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-i", src, "-t", str(t1 - t0), "-vf",
                          f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3); return [Image.frombytes("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]

HANDS = decode("clip1.mp4", 0.9, 2.4); OPEN = decode("take2.mp4", 0.0, 0.6); AFTER = decode("take2.mp4", 6.85, 8.0)
MW_A = decode("clip3.mp4", 0.3, 0.85); MW_B = decode("clip3.mp4", 2.6, 3.25)
UNCLE = M.cover(Image.open("A_uncle_eyes.jpg").convert("RGB")); GIRL = M.cover(Image.open("B_girl_eyes.jpg").convert("RGB"))
def soft_blur(im, x0, y0, x1, y1, r=16, feather=18):
    bl = im.filter(ImageFilter.GaussianBlur(r)); m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rectangle((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)), fill=255)
    return Image.composite(bl, im, m.filter(ImageFilter.GaussianBlur(feather)))
MARWAN = soft_blur(M.cover(Image.open("D_marwan.jpg").convert("RGB")), 0.70, 0.31, 0.87, 0.37)
PIN = M.cover(Image.open("E_pin.jpg").convert("RGB"))

def pick(fr, k): return fr[min(len(fr) - 1, max(0, int(k * (len(fr) - 1) + 0.5)))]
def crash(img, t, fx, fy, z0, z1, drift=0.05): return M.zoom(img, z0 + (z1 - z0) * R.ease_out(t / 0.18) + drift * t, fx, fy)

def band(img, fy, z, hgt=960):
    """1080 x hgt band of a 1080x1920 image, zoomed z around (0.5, fy)."""
    w, h = int(W * z), int(H * z); im = img.resize((w, h), Image.BICUBIC)
    cy = fy * h; t = int(min(max(cy - hgt / 2, 0), h - hgt)); l = (w - W) // 2
    return im.crop((l, t, l + W, t + hgt))

def split(t, z_add=0.0):
    k = t; im = Image.new("RGB", (W, H), BG)
    im.paste(band(UNCLE, 0.37, 1.35 + z_add + 0.04 * k), (0, 0)); im.paste(band(GIRL, 0.58, 1.2 + z_add + 0.04 * k), (0, 960))
    d = ImageDraw.Draw(im); d.rectangle((0, 954, W, 966), fill=(124, 92, 255)); return im

def base(t):
    if t < S["title"]: return M.zoom(pick(HANDS, t / S["title"]), 1.32, 0.5, 0.2)
    if t < S["wide"]:  # freeze on the frozen hands, slow push
        k = (t - S["title"]) / (S["wide"] - S["title"]); fr = ImageEnhance.Color(HANDS[-1]).enhance(0.75)
        return M.zoom(fr, 1.32 + 0.12 * R.ease_out(k), 0.5, 0.2)
    if t < S["uncle"]: k = (t - S["wide"]) / 1.0; return M.zoom(pick(OPEN, k), 1.0 + 0.07 * k, 0.5, 0.45)
    if t < S["maya"]: return crash(UNCLE, t - S["uncle"], 0.5, 0.37, 1.0, 1.3)
    if t < S["split"]: return crash(GIRL, t - S["maya"], 0.5, 0.58, 1.0, 1.15)
    if t < S["mw_a"]: return split(t - S["split"])
    if t < S["mw_b"]: return M.zoom(pick(MW_A, (t - S["mw_a"]) / 0.5), 1.55, 0.46, 0.5)
    if t < S["react"]:  # tight on the raised finger: the hand is already a fist, no banknote moment on screen
        k = (t - S["mw_b"]) / 0.6; return M.zoom(pick(MW_B, k), 2.05 + 0.08 * k, 0.40, 0.36)
    if t < S["mw_d"]: return split(t - S["react"], 0.25)
    if t < S["once"]:  # back to him, banknote in hand, still on his phone
        k = (t - S["mw_d"]) / 0.5; return M.zoom(MARWAN, 1.06 + 0.06 * k, 0.45, 0.6)
    if t < S["twice"]: return crash(UNCLE, t - S["once"], 0.5, 0.37, 1.55, 1.95, 0.1)
    if t < S["knock"]: return crash(GIRL, t - S["twice"], 0.5, 0.58, 1.35, 1.6, 0.1)
    if t < S["after"]:
        k = t - S["knock"]; z = 1.14 - 0.14 * R.ease_out(k / 0.07); sh = 26 * np.exp(-k * 11)
        return M.zoom(PIN, max(1.0, z) + 0.02, 0.6, 0.6, sh * np.sin(k * 90), sh * np.cos(k * 70))
    k = (t - S["after"]) / (S["end"] - S["after"]); return M.zoom(pick(AFTER, k), 1.0 + 0.05 * k, 0.5, 0.4)

def shadow(text, size, weight=700, fill=WHITE, mono=False):
    f = R.font(size, mono=True) if mono else R.font(size, weight)
    layer = R.text_layer(text, f, fill, tracking=4 if mono else 0)
    a = layer.getchannel("A").point(lambda v: int(v * 0.65))
    sh = Image.merge("RGBA", (*[Image.new("L", layer.size, 0)] * 3, a)).filter(ImageFilter.GaussianBlur(7))
    out = Image.new("RGBA", (layer.width + 24, layer.height + 24), (0, 0, 0, 0)); out.alpha_composite(sh, (12, 16)); out.alpha_composite(layer, (12, 12)); return out

def name_tag(name, line):
    n = R.text_layer(name, R.font(88, 700), WHITE); l = R.text_layer(line, R.font(42, 500), (225, 228, 240))
    w = max(n.width, l.width) + 90; h = n.height + l.height + 70
    im = M.glass(w, h, 28, fill=(11, 14, 20, 200)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((22, 26, 32, h - 26), radius=5, fill=(124, 92, 255, 255))
    im.alpha_composite(n, (56, 24)); im.alpha_composite(l, (58, 30 + n.height)); return im

TAGS = [(S["uncle"] + 0.15, S["maya"], name_tag("ABOU SAMI", "Regular since 1987.")),
        (S["maya"] + 0.15, S["split"], name_tag("MAYA", "3 exams tomorrow. Hasn't eaten.")),
        (S["mw_d"] + 0.05, S["once"], name_tag("MARWAN", "Didn't even look up."))]

def ticker(t):
    """rolling current-bid pill on the split divider."""
    cur = [b for b in BIDS if t >= b[0]]
    if not cur: return None
    at, who, val = cur[-1]; prev = cur[-2][2] if len(cur) > 1 else 0
    k = R.ease_out((t - at) / 0.28); v = int(round((prev + (val - prev) * k) / 1000) * 1000)
    num = R.text_layer(f"{v:,} LL", R.font(78, 700), WHITE); lab = R.text_layer(who + " BIDS", R.font(28, mono=True), (200, 205, 230), tracking=4)
    w = max(num.width, lab.width) + 100; h = num.height + lab.height + 54
    im = M.glass(w, h, 36, fill=(11, 14, 20, 225), border=(167, 139, 250, 255)); im.alpha_composite(lab, ((w - lab.width) // 2, 22)); im.alpha_composite(num, ((w - num.width) // 2, 26 + lab.height))
    pop = 1.0 + 0.12 * (1 - R.clamp((t - at) / 0.25)); return im, pop

def big_gradient(text, sub):
    num = R.text_layer(text, R.font(120, 700), WHITE); lab = R.text_layer(sub, R.font(30, mono=True), (235, 238, 255), tracking=4)
    w = max(num.width, lab.width) + 120; h = num.height + lab.height + 60
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=44, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(lab, ((w - lab.width) // 2, 24)); im.alpha_composite(num, ((w - num.width) // 2, 24 + lab.height)); return im

MW_PILL = big_gradient("$20", "MARWAN BIDS")

def overlay(im, t):
    im = im.convert("RGBA")
    if not (S["split"] <= t < S["mw_a"] or S["react"] <= t < S["mw_d"]): M.scrim(im, True, 460, 120); M.scrim(im, False, 600, 140)
    if t < S["title"] - 0.05:
        a = R.ease_out(t / 0.15) * (1 - R.clamp((t - (S["title"] - 0.2)) / 0.15))
        R.paste_center(im, shadow("1 manouche left.", 84), W / 2, 330, a)
    if S["title"] <= t < S["wide"]:
        k = (t - S["title"]) / 0.32; sc = 1.8 - 0.8 * R.stamp(k) if k < 1 else 1.0
        R.paste_center(im, shadow("THE LAST ONE", 132), W / 2, 820, R.clamp(k * 3), sc)
        R.paste_center(im, shadow("EP. 1  ·  THE MANOUCHE", 34, mono=True), W / 2, 950, R.ease_out((t - S["title"] - 0.25) / 0.2))
    if S["wide"] + 0.2 <= t < S["mw_d"] and not (S["split"] <= t < S["mw_a"] or S["react"] <= t < S["mw_d"]):
        lc = M.live_chip(t); R.paste_center(im, lc, 80 + lc.width / 2, 262, R.ease_out((t - S["wide"] - 0.2) / 0.25))
    for t0, t1, tag in TAGS:
        if t0 <= t < t1:
            k = (t - t0) / 0.25; x = 60 + tag.width / 2 - (1 - R.ease_out(k)) * 120
            R.paste_center(im, tag, x, 420 if t0 >= S["mw_d"] else 1330, R.clamp(k * 2))
    if S["split"] <= t < S["mw_a"]:
        r = ticker(t)
        if r: R.paste_center(im, r[0], W / 2, 960, 1.0, r[1])
    if t >= MARWAN_BID and t < S["react"]:
        k = (t - MARWAN_BID) / 0.3; sc = 1.6 - 0.6 * R.stamp(k) if k < 1 else 1.0
        R.paste_center(im, MW_PILL, W / 2, 1300, R.clamp(k * 3), sc)
    if S["react"] <= t < S["mw_d"]:
        R.paste_center(im, MW_PILL, W / 2, 960, 1.0, 0.85)
        R.paste_center(im, shadow("≈ 1,800,000 LL", 46, 600), W / 2, 1110, R.ease_out((t - S["react"]) / 0.2))
    if S["once"] <= t < S["knock"] + 0.1:
        lab = "GOING ONCE…" if t < S["twice"] else "GOING TWICE…"; last = S["once"] if t < S["twice"] else S["twice"]
        k = (t - last) / 0.25; a = 1 - R.clamp((t - S["knock"]) / 0.1)
        R.paste_center(im, M.chip(lab, (124, 92, 255, 150), (167, 139, 250, 255), size=46), W / 2, 280, a, 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
        aa = 0.25 + 0.45 * (0.5 - 0.5 * np.cos(2 * np.pi * (t - S["once"]) / 0.5))
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(fr).rectangle((0, 0, W - 1, H - 1), outline=(124, 92, 255, int(255 * aa)), width=20); im.alpha_composite(fr)
    if t >= S["knock"]:
        k = (t - S["knock"]) / 0.32; sc = 1.8 - 0.8 * R.stamp(k) if k < 1 else 1.0
        R.paste_center(im, M.stamp_text("SOLD.", 170), W / 2, 470, R.clamp(k * 3), sc)
        if t >= S["after"]:
            R.paste_center(im, shadow("to Marwan · $20", 58, 600), W / 2, 610, R.ease_out((t - S["after"]) / 0.25))
    if S["knock"] <= t < S["knock"] + 0.12: im = M.flash(im, 0.7 * (1 - (t - S["knock"]) / 0.12))
    for cut in (S["wide"], S["uncle"], S["maya"], S["split"], S["mw_a"], S["mw_b"], S["react"], S["mw_d"], S["once"], S["twice"]):
        if cut <= t < cut + 0.05: im = M.flash(im, 0.35)
    if t > S["end"] - 0.2: im = Image.blend(im, Image.new("RGBA", (W, H), BG + (255,)), R.clamp((t - (S["end"] - 0.2)) / 0.2))
    return im

def end_card(k):
    im = R.GRAD_BG.copy(); s = k / 0.42; sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, R.z_mark(190), W / 2, 500, R.clamp(s * 3), sc)
    for i, line in enumerate(["Someone always", "wants it more."]):
        a = R.ease_out((k - 0.35 - i * 0.22) / 0.3); R.paste_center(im, R.text_layer(line, R.font(100, 700), WHITE), W / 2, 760 + i * 118 + (1 - a) * 20, a)
    b = R.ease_out((k - 1.25) / 0.35)
    hy, bz = R.text_layer("HYPER", R.font(54, 500), (215, 225, 255), tracking=6), R.text_layer("BIDZ", R.font(54, 700), WHITE, tracking=6)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0)); wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    R.paste_center(im, wm, W / 2, 1100, b); R.wrap_center(im, "Live auctions for Lebanon. Coming soon.", R.font(46, 500), WHITE, 1185, alpha=b, max_w=900)
    c = R.ease_out((k - 1.65) / 0.35); R.paste_center(im, R.pill("Follow @hyperbidz", R.font(50, 700), NAVY, WHITE, pad=(52, 28)), W / 2, 1340, c, 0.94 + 0.06 * c)
    return im

def frame(t): return (end_card(t - S["end"]) if t >= S["end"] else overlay(base(t), t)).convert("RGB")

# ---------- sound: original score, 120 BPM ----------
def build_audio(path):
    n = int(TOTAL * SR); out = np.zeros(n); rng = np.random.default_rng(9)
    tt = lambda d: np.arange(int(d * SR)) / SR
    def add(sig, at, g=1.0):
        i = int(at * SR); j = min(n, i + len(sig))
        if i < n: out[i:j] += sig[: j - i] * g
    def lp(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
    def hp(x): return x - lp(x, 8)
    def pluck(f0, at, dur=0.9, g=0.5, damp=0.994):
        N = int(SR / f0); buf = rng.uniform(-1, 1, N); m = int(dur * SR); y = np.empty(m)
        for i in range(m): y[i] = buf[i % N]; buf[i % N] = damp * 0.5 * (buf[i % N] + buf[(i + 1) % N])
        add(y * np.minimum(1, (dur - np.arange(m) / SR) / 0.05), at, g)
    def kick(at, g=0.9):
        x = tt(0.35); f = 45 + 75 * np.exp(-x * 30); add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 9), at, g)
    def snare(at, g=0.45):
        x = tt(0.22); add(hp(rng.normal(0, 1, len(x))) * np.exp(-x * 22) + np.sin(2 * np.pi * 185 * x) * np.exp(-x * 30) * 0.5, at, g)
    def shaker(at, g=0.12):
        x = tt(0.06); add(hp(rng.normal(0, 1, len(x))) * np.exp(-x * 60), at, g)
    def swish(at, d=0.2, g=0.45):
        x = tt(d); add(lp(rng.normal(0, 1, len(x)), 5) * np.sin(np.pi * x / d) ** 2, at, g)
    def ding(at, f=(1318.5, 1568), g=0.25):
        for f0, dd in zip(f, (0, 0.08)):
            x = tt(0.4); add((np.sin(2 * np.pi * f0 * x) + 0.25 * np.sin(4 * np.pi * f0 * x)) * np.exp(-x * 10), at + dd, g)
    def boom(at, g=0.9):
        x = tt(0.9); add(np.sin(2 * np.pi * np.cumsum(38 + 50 * np.exp(-x * 8)) / SR) * np.exp(-x * 4) + lp(rng.normal(0, 1, len(x)), 20) * np.exp(-x * 10) * 0.5, at, g)
    def whistle(notes, at, g=0.15):
        t0 = at
        for f0, f1, d in notes:
            x = tt(d); f = f0 + (f1 - f0) * np.minimum(1, x / (0.6 * d)); vib = 1 + 0.012 * np.sin(2 * np.pi * 6 * x)
            env = np.minimum(1, x / 0.04) * np.minimum(1, (d - x) / 0.07); add(np.sin(2 * np.pi * np.cumsum(f * vib) / SR) * env, t0, g); t0 += d
    x = tt(S["end"]); add(lp(rng.normal(0, 1, len(x)), 400) * 0.9, 0)               # room tone
    # intro: rising whoosh into the freeze, twang + hit on the title
    x = tt(1.2); add(lp(rng.normal(0, 1, len(x)), 6) * (x / 1.2) ** 3, 0.1, 0.7)
    pluck(82.4, S["title"], 2.2, 0.7, 0.997); boom(S["title"], 0.6)
    whistle([(880, 1318.5, 0.35), (1318.5, 1174.7, 0.25), (1174.7, 880, 0.4)], S["title"] + 0.15, 0.13)
    # groove 2.0 -> 9.0 (beat = 0.5 s)
    riff = [82.4, 82.4, 98.0, 110.0, 82.4, 82.4, 123.5, 110.0]
    b = 0; t = S["wide"]
    while t < S["knock"] - 0.01:
        kick(t) if b % 2 == 0 else snare(t)
        if t >= S["once"]: kick(t + 0.25, 0.5)
        pluck(riff[b % 8], t, 0.45, 0.42)
        if t >= S["split"]: shaker(t + 0.25); pluck(riff[b % 8] * 2, t + 0.25, 0.25, 0.18)
        if t >= S["once"]: shaker(t + 0.125); shaker(t + 0.375)
        b += 1; t += 0.5
    for c in (S["uncle"], S["maya"], S["split"], S["mw_a"], S["mw_b"], S["react"], S["mw_d"], S["once"], S["twice"]): swish(c - 0.05)
    for at, _, _ in BIDS: ding(at)
    ding(MARWAN_BID, (1568, 2093), 0.32); boom(MARWAN_BID, 0.35)
    for t0, _, _ in TAGS: pluck(164.8, t0, 0.5, 0.25)
    # the hit: everything stops, wooden knock + boom, silence, then a slow twang on the reveal
    k = S["knock"]; out[int((k - 0.02) * SR):int((k + 0.5) * SR)] *= 0.1
    x = tt(0.5); add(np.sin(2 * np.pi * 165 * x) * np.exp(-x * 28) + np.sin(2 * np.pi * 96 * x) * np.exp(-x * 14) * 0.7 + lp(rng.normal(0, 1, len(x)), 2) * np.exp(-x * 90) * 0.8, k, 1.0)
    boom(k, 0.8); pluck(82.4, S["after"] + 0.05, 2.0, 0.55, 0.997)
    whistle([(1174.7, 880, 0.3), (880, 659.3, 0.55)], S["after"] + 0.35, 0.12)
    out[int((S["end"] - 0.05) * SR):] = 0
    x = tt(0.4); add(np.sin(2 * np.pi * 98 * x) * np.exp(-x * 11) * 0.6, S["end"] + 0.02)
    x = tt(END); env = np.minimum(1, x / 0.3) * np.exp(-np.maximum(0, x - 1.6) * 0.8)
    add(sum(np.sin(2 * np.pi * f * x) * a for f, a in ((164.8, .5), (196, .35), (246.9, .35), (329.6, .22))) * env * 0.3, S["end"] + 0.05)
    out[-int(0.25 * SR):] *= np.linspace(1, 0, int(0.25 * SR))
    out = np.tanh(out * 1.4) / np.tanh(1.4); out = out / (np.max(np.abs(out)) + 1e-9) * 0.89
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    if "--stills" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        ims = [frame(t).resize((216, 384)) for t in ts]; s = Image.new("RGB", (216 * len(ims), 384))
        for i, im in enumerate(ims): s.paste(im, (216 * i, 0))
        s.save("stills.jpg", quality=85); print("stills.jpg"); sys.exit()
    build_audio("manouche_v3.wav")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", "manouche_v3.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(round(TOTAL * FPS))): enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT, round(TOTAL, 2))
