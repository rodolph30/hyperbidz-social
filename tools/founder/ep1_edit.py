"""Founder series Ep. 1 'They bid': message flood (the old way) swept away by live bids.
Usage: python3 ep1_edit.py out.mp4 [--stills t,...]"""
import subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/manouche")
import render as R
import mhelpers as M

W, H, FPS, SR = 1080, 1920, 30, 48000
WHITE, BG, NAVY = R.WHITE, R.BG, R.NAVY
OUT = sys.argv[1]
CLIP = 8.0; XF = 0.35; END = 3.6; T_END = CLIP; TOTAL = CLIP + END
CAPS = [(0.0, 1.0, ["You posted it."]), (1.05, 2.15, ["12 messages."]), (2.2, 3.55, ["\"Is it still available?\""]),
        (3.65, 5.15, ["Not one", "[real offer.]"]), (5.25, 7.95, ["On HyperBidz, they don't", "message… [they bid.]"])]
BUBBLES = [(2.25, "Is it still available?", 150, 1010, -3), (2.5, "Is it still available??", 560, 1130, 2), (2.7, "still available?", 230, 1250, -2),
           (2.9, "Is it available bro", 600, 1360, 3), (3.1, "$40, final?", 300, 1080, 1), (3.3, "I'll pass by tomorrow", 520, 1230, -2)]
SWEEP = 5.3
BIDS = [(5.6, "Maya", 160), (6.0, "Karim", 185), (6.4, "Rami", 210), (6.8, "Nour", 240), (7.2, "Elie", 275)]

def decode():
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "src.mp4", "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3); return [Image.frombytes("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]
FR = decode()

def caption(lines):
    f = R.font(72, 700); out = []
    for ln in lines:
        parts = []
        for chunk in ln.replace("[", "|[").replace("]", "]|").split("|"):
            if chunk: parts.append((chunk[1:-1], True) if chunk.startswith("[") else (chunk, False))
        layers = [R.text_layer(p, f, (167, 139, 250) if h else WHITE) for p, h in parts]
        w = sum(l.width for l in layers) - 4 * (len(layers) - 1); im = Image.new("RGBA", (w, max(l.height for l in layers)), (0, 0, 0, 0)); x = 0
        for l in layers: im.alpha_composite(l, (x, 0)); x += l.width - 4
        out.append(im)
    w = max(o.width for o in out) + 80; h = sum(o.height for o in out) + 46
    box = M.glass(w, h, 30, fill=(11, 14, 20, 195), border=(255, 255, 255, 30)); y = 23
    for o in out: box.alpha_composite(o, ((w - o.width) // 2, y)); y += o.height - 6
    return box

def old_bubble(text, rot):
    """generic grey messenger bubble: 'the old way'."""
    tl = R.text_layer(text, R.font(40, 500), (30, 32, 38)); w, h = tl.width + 56, tl.height + 34
    im = Image.new("RGBA", (w + 20, h + 26), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, 10 + w, 10 + h), radius=h // 2, fill=(232, 233, 238, 245))
    d.polygon([(30, 8 + h), (22, 22 + h), (48, 8 + h)], fill=(232, 233, 238, 245))
    im.alpha_composite(tl, (38, 26)); return im.rotate(rot, resample=Image.BICUBIC, expand=True)
OLD = [(at, old_bubble(t, r), x, y) for at, t, x, y, r in BUBBLES]

def bid_row(name, amount, top=False):
    hl = R.text_layer(name, R.font(36, 500), WHITE); am = R.text_layer(f"${amount}", R.font(44, 700), WHITE)
    lab = R.text_layer("BID", R.font(22, mono=True), (235, 238, 255), tracking=3)
    w, h = 28 + 64 + 22 + hl.width + 22 + lab.width + 14 + am.width + 36, 100
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=50, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m) if top else im.paste(Image.new("RGBA", (w, h), (49, 38, 98, 235)), (0, 0), m)
    d = ImageDraw.Draw(im); d.ellipse((24, 18, 88, 82), fill=(255, 255, 255, 255))
    ini = R.text_layer(name[0], R.font(34, 700), NAVY); im.alpha_composite(ini, (56 - ini.width // 2, 48 - ini.height // 2))
    x = 110; im.alpha_composite(hl, (x, (h - hl.height) // 2)); x += hl.width + 22
    im.alpha_composite(lab, (x, (h - lab.height) // 2 + 2)); x += lab.width + 14; im.alpha_composite(am, (x, (h - am.height) // 2 - 1)); return im
ROWS = [(at, bid_row(n, a), bid_row(n, a, True)) for at, n, a in BIDS]

def counter_chip(n, offers=None):
    """message counter pill, top-left; 'real offers: 0' variant."""
    if offers is None: txt = f"{n} MESSAGES"
    else: txt = "REAL OFFERS: 0"
    tl = R.text_layer(txt, R.font(30, mono=True), WHITE, tracking=3); w, h = tl.width + 96, tl.height + 34
    im = M.glass(w, h, h // 2, fill=(20, 22, 32, 225), border=(255, 255, 255, 50)); d = ImageDraw.Draw(im)
    cx, cy = 34, h // 2; d.rounded_rectangle((cx - 16, cy - 13, cx + 16, cy + 9), radius=8, outline=(255, 255, 255, 255), width=3); d.polygon([(cx - 8, cy + 8), (cx - 12, cy + 16), (cx, cy + 8)], fill=(255, 255, 255, 255))
    im.alpha_composite(tl, (66, 17)); return im

def listing_card():
    t1 = R.text_layer("Vintage film camera", R.font(40, 700), WHITE); t2 = R.text_layer("$150 · Posted just now", R.font(30, 500), (200, 204, 218))
    w, h = max(t1.width, t2.width) + 170, 130; im = M.glass(w, h, 30, fill=(20, 22, 32, 230), border=(255, 255, 255, 45)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((22, 20, 112, 110), radius=18, fill=(60, 64, 78, 255))  # thumbnail block with a simple camera glyph
    d.rounded_rectangle((40, 48, 94, 88), radius=8, outline=(220, 222, 230, 255), width=4); d.ellipse((56, 56, 78, 78), outline=(220, 222, 230, 255), width=4); d.rectangle((48, 42, 62, 48), fill=(220, 222, 230, 255))
    im.alpha_composite(t1, (136, 26)); im.alpha_composite(t2, (136, 76)); return im
LISTING = listing_card()

def ticker(t):
    cur = [b for b in BIDS if t >= b[0]]
    if not cur: return None
    lab = R.text_layer(f"CURRENT BID  ·  {len(cur)} BIDDERS", R.font(26, mono=True), (220, 224, 245), tracking=3)
    num = R.text_layer(f"${cur[-1][2]}", R.font(90, 700), WHITE)
    w = max(lab.width, num.width) + 90; h = lab.height + num.height + 44
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    im.alpha_composite(lab, ((w - lab.width) // 2, 18)); im.alpha_composite(num, ((w - num.width) // 2, 20 + lab.height)); return im, 1 + 0.08 * (1 - R.clamp((t - cur[-1][0]) / 0.2))

def frame(t):
    if t >= CLIP: return end_card(t - CLIP)
    im = FR[min(len(FR) - 1, int(t * FPS))].convert("RGBA")
    M.scrim(im, False, 700, 150); M.scrim(im, True, 300, 90)
    # 0. listing card, then message counter
    if t < SWEEP:
        k = (t - 0.05) / 0.3; a = R.clamp(k * 3) * (1 - R.clamp((t - (SWEEP - 0.25)) / 0.25))
        R.paste_center(im, LISTING, 60 + LISTING.width / 2, 250, a, 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    if 1.1 <= t < SWEEP:
        n = int(round(12 * R.clamp((t - 1.1) / 0.6))); offers = 0 if t >= 3.7 else None
        cc = counter_chip(n, offers); k = (t - (3.7 if offers is not None else 1.1)) / 0.25
        R.paste_center(im, cc, 60 + cc.width / 2, 390, 1 - R.clamp((t - (SWEEP - 0.25)) / 0.25), 0.88 + 0.12 * R.stamp(k) if k < 1 else 1.0)
    # 1. the old way: grey bubbles pile up, go grey/dim on "not one real offer", swept left at SWEEP
    for at, b, x, y in OLD:
        if t < at: continue
        k = (t - at) / 0.25; sc = 0.6 + 0.4 * R.stamp(k) if k < 1 else 1.0; a = R.clamp(k * 3)
        dx = 0
        if t >= SWEEP: s = R.clamp((t - SWEEP - (y - 1000) / 2500) / 0.35); dx = -1300 * s ** 2; a *= 1 - s
        if t >= 3.7 and t < SWEEP: a *= 0.55
        R.paste_center(im, b, x + b.width / 2 - 80 + dx, y, a, sc)
    # 2. HyperBidz: violet wipe, bids climbing, ticker
    if SWEEP <= t < SWEEP + 0.35:
        k = (t - SWEEP) / 0.35; x = int(W * (1.2 - 1.4 * R.ease_out(k)))
        band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(band).polygon([(x, 0), (x + 220, 0), (x + 60, H), (x - 160, H)], fill=(124, 92, 255, 150))
        im.alpha_composite(band.filter(ImageFilter.GaussianBlur(25)))
    shown = [r for r in ROWS if t >= r[0]][-4:]
    y = 1340
    for i, (at, row, top) in enumerate(reversed(shown)):
        k = R.clamp((t - at) / 0.28); pop = 0.8 + 0.2 * R.stamp(k) if k < 1 else 1.0
        r = top if i == 0 else row
        R.paste_center(im, r, 60 + r.width / 2, y, R.ease_out(k) * (1 - 0.22 * i), pop); y -= 116
    tk = ticker(t)
    if tk: R.paste_center(im, tk[0], W - 60 - tk[0].width / 2 * tk[1], 330, R.ease_out((t - BIDS[0][0]) / 0.3), tk[1])
    # captions
    for t0, t1, lines in CAPS:
        if t0 <= t < t1:
            k = (t - t0) / 0.18; a = R.clamp(k * 3) * (1 - R.clamp((t - (t1 - 0.1)) / 0.1))
            R.paste_center(im, caption(lines), W / 2, 1560 + (1 - R.ease_out(k)) * 20, a)
    if SWEEP <= t < SWEEP + 0.08: im = M.flash(im, 0.3)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

def end_card(k):
    im = R.GRAD_BG.copy(); s = k / 0.42; sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, R.z_mark(190), W / 2, 500, R.clamp(s * 3), sc)
    for i, line in enumerate(["Don't sell it.", "Let them bid for it."]):
        a = R.ease_out((k - 0.35 - i * 0.3) / 0.3); R.paste_center(im, R.text_layer(line, R.font(96, 700), WHITE), W / 2, 760 + i * 116 + (1 - a) * 20, a)
    b = R.ease_out((k - 1.3) / 0.35)
    hy, bz = R.text_layer("HYPER", R.font(54, 500), (215, 225, 255), tracking=6), R.text_layer("BIDZ", R.font(54, 700), WHITE, tracking=6)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0)); wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    R.paste_center(im, wm, W / 2, 1100, b); R.wrap_center(im, "Live auctions for Lebanon. Coming soon.", R.font(46, 500), WHITE, 1185, alpha=b, max_w=900)
    c = R.ease_out((k - 1.7) / 0.35); R.paste_center(im, R.pill("Follow @hyperbidz", R.font(50, 700), NAVY, WHITE, pad=(52, 28)), W / 2, 1340, c, 0.94 + 0.06 * c)
    out = im.convert("RGB")
    if k > END - 0.5: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), R.clamp((k - (END - 0.5)) / 0.5))
    return out

def build_audio(path):
    n = int(TOTAL * SR); out = np.zeros(n); rng = np.random.default_rng(41)
    tt = lambda d: np.arange(int(d * SR)) / SR
    def add(sig, at, g=1.0):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += sig[: j - i] * g
    def lp(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
    voice = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "src.mp4", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, dtype=np.int16).astype(np.float64) / 32768
    voice = voice / (np.max(np.abs(voice)) + 1e-9) * 0.9
    env = np.convolve(np.abs(voice), np.ones(2400) / 2400, mode="same"); duck = 1 - 0.65 * np.clip(env / (env.max() + 1e-9) * 3, 0, 1)
    # bed: muted, slightly flat pulse for the old way, brighter after the sweep
    bed = np.zeros(len(voice)); x = np.arange(len(voice)) / SR
    bed += (np.sin(2 * np.pi * 98 * x) * 0.4 + np.sin(2 * np.pi * 146.8 * x) * 0.25) * 0.05 * np.minimum(1, x / 0.4)
    post = x >= SWEEP; bed[post] += (np.sin(2 * np.pi * 196 * x[post]) * 0.3 + np.sin(2 * np.pi * 293.7 * x[post]) * 0.25 + np.sin(2 * np.pi * 392 * x[post]) * 0.15) * 0.06
    add(bed * duck, 0)
    main = out; out = np.zeros(n)
    for k in range(16):
        y = tt(0.2); add(np.sin(2 * np.pi * np.cumsum(50 + 40 * np.exp(-y * 30)) / SR) * np.exp(-y * 12) * (0.09 if k * 0.5 < SWEEP else 0.16), k * 0.5)
    def dull_pop(at, g=0.22):  # old-way message sound: flat, dull
        y = tt(0.12); add(np.sin(2 * np.pi * 520 * y) * np.exp(-y * 35), at, g)
    def ding(at, f=(1318.5, 1975.5), g=0.2):
        for f0, dd in zip(f, (0, 0.07)):
            y = tt(0.35); add(np.sin(2 * np.pi * f0 * y) * np.exp(-y * 12), at + dd, g)
    dull_pop(0.05, 0.18)
    dull_pop(1.1, 0.12)
    for at, _, _, _, _ in BUBBLES: dull_pop(at)
    y = tt(0.5); add(lp(rng.normal(0, 1, len(y)), 5) * np.sin(np.pi * y / 0.5) ** 2, SWEEP - 0.1, 0.35)   # sweep whoosh
    for i, (at, _, _) in enumerate(BIDS): ding(at, (1318.5 + 80 * i, 1975.5 + 80 * i), 0.16)
    fx = out; fx[:len(duck)] *= (0.35 + 0.65 * duck); out = main + fx * 0.8; out[:len(voice)] += voice
    x = tt(0.4); add(np.sin(2 * np.pi * 98 * x) * np.exp(-x * 11) * 0.6, CLIP + 0.02)
    x = tt(END); env2 = np.minimum(1, x / 0.3) * np.exp(-np.maximum(0, x - 1.6) * 0.8)
    add(sum(np.sin(2 * np.pi * f * x) * a for f, a in ((196, .5), (246.94, .35), (293.66, .35), (392, .22))) * env2 * 0.3, CLIP + 0.05)
    out[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR)) ** 1.5
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.92
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    if "--stills" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        ims = [frame(t).resize((216, 384)) for t in ts]; s = Image.new("RGB", (216 * len(ims), 384))
        for i, im in enumerate(ims): s.paste(im, (216 * i, 0))
        s.save("stills.jpg", quality=85); print("stills.jpg"); sys.exit()
    build_audio("ep1_audio.wav")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", "ep1_audio.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(round(TOTAL * FPS))): enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT, round(TOTAL, 2))
