"""Founder series Ep. 2 'Worthless': the raised-hand moment is replaced by a magical cutaway
(old camera card, WORTHLESS? stamp, three bidders popping in on "three people"), then live price race and SOLD.
Usage: python3 ep2_edit.py out.mp4 [--stills t,...]"""
import subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, "/home/claude/manouche")
import render as R
import mhelpers as M

W, H, FPS, SR = 1080, 1920, 30, 48000
WHITE, BG, NAVY = R.WHITE, R.BG, R.NAVY
OUT = sys.argv[1]
CLIP = 8.0; XF = 0.35; END = 3.6; TOTAL = CLIP + END
CUT_IN, CUT_OUT = 1.70, 4.00                 # cutaway hides the early, oversized three-finger gesture
STAMP = 2.15                                  # "worthless"
BIDDERS = [(3.20, "M", 150, 720), (3.45, "K", 930, 640), (3.70, "R", 540, 345)]   # absolute positions around the card   # on "three people"
CAPS = [(0.45, 1.66, ["Everyone thinks", "their old stuff"]), (1.70, 2.90, ["is [worthless]…"]), (2.95, 3.98, ["until [three people]"]),
        (4.00, 5.40, ["want it [at the same time.]"]), (6.55, 7.70, ["[That's an auction.]"])]
RACE = [(4.05, 180), (4.35, 205), (4.65, 230), (4.95, 245), (5.2, 260)]
SOLD = 6.65

def decode():
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "src.mp4", "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3); return [Image.frombytes("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]
FR = decode()

# ---------- assets ----------
def stage():
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(0, 1, W)[None, :]
    g = np.exp(-(((x - 0.5) / 0.55) ** 2 + ((y - 0.42) / 0.3) ** 2))
    a = np.array(BG)[None, None, :] * (1 - 0.0 * g[..., None]) + np.array([124, 92, 255])[None, None, :] * (0.38 * g)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
STAGE = stage()

def item_card():
    ph = Image.open("camera_hq.png").convert("RGB").resize((620, 620), Image.LANCZOS)
    w, h = 660, 740; card = M.glass(w, h, 40, fill=(20, 22, 32, 240), border=(255, 255, 255, 60))
    m = Image.new("L", ph.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), radius=28, fill=255)
    card.paste(ph, (20, 20), m)
    t = R.text_layer("Old film camera", R.font(40, 700), WHITE); card.alpha_composite(t, (36, 660)); return card
CARD = item_card()

def price_pill(v, hot=False):
    tl = R.text_layer(f"${v}", R.font(64, 700), WHITE); w, h = tl.width + 70, tl.height + 30
    if hot:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    else:
        im = M.glass(w, h, h // 2, fill=(40, 42, 52, 235), border=(255, 255, 255, 60))
    im.alpha_composite(tl, (35, 13)); return im

def stamp_worthless():
    tl = R.text_layer("WORTHLESS?", R.font(78, 700), WHITE); w, h = tl.width + 70, tl.height + 36
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 20 + w, 20 + h), radius=18, fill=(11, 14, 20, 230), outline=(255, 255, 255, 230), width=5)
    im.alpha_composite(tl, (55, 36)); return im.rotate(-8, resample=Image.BICUBIC, expand=True)
WORTHLESS = stamp_worthless()

def avatar(letter, amt):
    s = 120; im = Image.new("RGBA", (s + 160, s + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0)); m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    g.paste(M.grad(s, s), (0, 0), m); im.alpha_composite(g, (80, 0))
    d.ellipse((80, 0, 80 + s - 1, s - 1), outline=(255, 255, 255, 255), width=4)
    l = R.text_layer(letter, R.font(56, 700), WHITE); im.alpha_composite(l, (80 + (s - l.width) // 2, (s - l.height) // 2 - 4))
    tag = R.pill(f"BID ${amt}", R.font(30, mono=True), NAVY, WHITE, pad=(20, 10)); im.alpha_composite(tag, ((im.width - tag.width) // 2, s + 8)); return im
AVS = [(at, avatar(l, a), dx, dy) for (at, l, dx, dy), a in zip(BIDDERS, (60, 120, 180))]

def star(sz):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = sz / 2
    d.polygon([(c, 0), (c + sz * .12, c - sz * .12), (sz, c), (c + sz * .12, c + sz * .12), (c, sz), (c - sz * .12, c + sz * .12), (0, c), (c - sz * .12, c - sz * .12)], fill=(255, 255, 255, 255))
    return im
STARS = {s: star(s) for s in (18, 26, 34)}
rng0 = np.random.default_rng(3)
DUST = [(rng0.uniform(0, W), rng0.uniform(0, H), rng0.uniform(20, 70), rng0.uniform(2, 6), rng0.uniform(0, 6)) for _ in range(70)]

def dust(im, t, strength=1.0):
    d = ImageDraw.Draw(im)
    for x, y, sp, r, ph in DUST:
        yy = (y - sp * t * 3) % H; a = int(70 * strength * (0.5 + 0.5 * np.sin(t * 3 + ph))); r = r * 0.6
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(200, 190, 255, a))

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

def live_bar(t, val):
    tl = R.text_layer(f"LIVE  ·  3 BIDDERS", R.font(28, mono=True), WHITE, tracking=3)
    w, h = tl.width + 90, tl.height + 30; im = M.glass(w, h, h // 2, fill=(11, 14, 20, 200), border=(167, 139, 250, 200))
    a = int(160 + 95 * (0.5 + 0.5 * np.sin(t * 7))); ImageDraw.Draw(im).ellipse((26, h // 2 - 10, 46, h // 2 + 10), fill=(167, 139, 250, a))
    im.alpha_composite(tl, (62, 15)); return im

# ---------- frames ----------
def cutaway(t):
    k = t - CUT_IN; im = STAGE.copy(); dust(im, t, 1.0)
    cx, cy = W / 2, 820
    sc = 0.55 + 0.45 * R.stamp(k / 0.35) if k < 0.35 else 1.0 + 0.02 * (k - 0.35)
    R.paste_center(im, CARD, cx, cy, R.clamp(k / 0.15), sc)
    # price under the card: $20, then bids lift it
    v = 20; hot = False
    for at, _, _, _ in BIDDERS:
        if t >= at: hot = True
    vals = [20] + [a for a in (60, 120, 180)]; n_b = sum(1 for at, _, _, _ in BIDDERS if t >= at); v = vals[n_b]
    pp = price_pill(v, hot); bump = 1 + 0.12 * (1 - R.clamp((t - BIDDERS[n_b - 1][0]) / 0.2)) if n_b else 1
    R.paste_center(im, pp, cx, cy + 440, R.clamp((k - 0.2) / 0.2), bump)
    # WORTHLESS? stamp, cracks away on "until"
    if t >= STAMP:
        s = (t - STAMP) / 0.3; sc2 = 1.7 - 0.7 * R.stamp(s) if s < 1 else 1.0
        a = R.clamp(s * 3) * (1 - R.clamp((t - 3.0) / 0.25))
        R.paste_center(im, WORTHLESS, cx + 60, cy - 40 + 60 * R.clamp((t - 3.0) / 0.25) ** 2, a, sc2)
    # three bidders pop in with sparkles
    for at, av, dx, dy in AVS:
        if t >= at:
            s = (t - at) / 0.3; sc3 = 0.3 + 0.7 * R.stamp(s) if s < 1 else 1.0
            R.paste_center(im, av, dx, dy + 6 * np.sin((t - at) * 5), R.clamp(s * 3), sc3)
            for j, (ox, oy, sz) in enumerate(((-90, -60, 26), (95, -40, 18), (60, 70, 34))):
                tw = (t - at - 0.05 * j) * 4
                if 0 < tw < np.pi: R.paste_center(im, STARS[sz], dx + ox, dy + oy, np.sin(tw), 0.6 + 0.4 * np.sin(tw))
    # zoom-through transitions
    if k < 0.18: im = Image.blend(im, Image.new("RGBA", (W, H), (210, 200, 255, 255)), 0.7 * (1 - k / 0.18))
    return im

def frame(t):
    if t >= CLIP: return end_card(t - CLIP)
    if CUT_IN <= t < CUT_OUT:
        im = cutaway(t)
    else:
        fr = FR[min(len(FR) - 1, int(t * FPS))]
        if t >= CUT_OUT and t < CUT_OUT + 0.25:  # land back on him with a little push
            z = 1.06 - 0.06 * R.ease_out((t - CUT_OUT) / 0.25); fr = M.zoom(fr, z, 0.5, 0.35)
        im = fr.convert("RGBA"); M.scrim(im, False, 700, 150); M.scrim(im, True, 300, 90)
        if t < CUT_IN and t > CUT_IN - 0.15:  # whoosh into the cutaway
            im = Image.blend(im, Image.new("RGBA", (W, H), (210, 200, 255, 255)), 0.7 * (t - (CUT_IN - 0.15)) / 0.15)
        if t >= CUT_OUT:
            cur = [v for at, v in RACE if t >= at]; val = cur[-1] if cur else 180
            lb = live_bar(t, val); R.paste_center(im, lb, W / 2, 205, R.ease_out((t - CUT_OUT) / 0.25))
            last = max([at for at, v in RACE if t >= at] or [CUT_OUT])
            if t < SOLD:
                pp = price_pill(val, True); R.paste_center(im, pp, W / 2, 330, R.ease_out((t - CUT_OUT) / 0.25), 1 + 0.12 * (1 - R.clamp((t - last) / 0.2)))
            else:
                s = (t - SOLD) / 0.35; sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
                sold = R.pill("SOLD  ·  $260", R.font(60, 700), NAVY, WHITE, pad=(46, 24)); R.paste_center(im, sold, W / 2, 330, R.clamp(s * 3), sc)
                for j, (ox, oy, sz) in enumerate(((-260, -50, 34), (250, -70, 26), (-200, 60, 18), (230, 55, 34), (0, -110, 26))):
                    tw = (t - SOLD - 0.06 * j) * 3.5
                    if 0 < tw < np.pi: R.paste_center(im, STARS[sz], W / 2 + ox, 330 + oy, np.sin(tw))
    for t0, t1, lines in CAPS:
        if t0 <= t < t1:
            k = (t - t0) / 0.18; a = R.clamp(k * 3) * (1 - R.clamp((t - (t1 - 0.1)) / 0.1))
            R.paste_center(im, caption(lines), W / 2, 1560 + (1 - R.ease_out(k)) * 20, a)
    if SOLD <= t < SOLD + 0.1: im = M.flash(im, 0.35 * (1 - (t - SOLD) / 0.1))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

def end_card(k):
    im = R.GRAD_BG.copy(); s = k / 0.42; sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, R.z_mark(190), W / 2, 500, R.clamp(s * 3), sc)
    for i, line in enumerate(["Find out what", "it's really worth."]):
        a = R.ease_out((k - 0.35 - i * 0.3) / 0.3); R.paste_center(im, R.text_layer(line, R.font(100, 700), WHITE), W / 2, 760 + i * 118 + (1 - a) * 20, a)
    b = R.ease_out((k - 1.3) / 0.35)
    hy, bz = R.text_layer("HYPER", R.font(54, 500), (215, 225, 255), tracking=6), R.text_layer("BIDZ", R.font(54, 700), WHITE, tracking=6)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0)); wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    R.paste_center(im, wm, W / 2, 1100, b); R.wrap_center(im, "Live auctions for Lebanon. Coming soon.", R.font(46, 500), WHITE, 1185, alpha=b, max_w=900)
    c = R.ease_out((k - 1.7) / 0.35); R.paste_center(im, R.pill("Follow @hyperbidz", R.font(50, 700), NAVY, WHITE, pad=(52, 28)), W / 2, 1340, c, 0.94 + 0.06 * c)
    out = im.convert("RGB")
    if k > END - 0.5: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), R.clamp((k - (END - 0.5)) / 0.5))
    return out

# ---------- sound ----------
def build_audio(path):
    n = int(TOTAL * SR); out = np.zeros(n); rng = np.random.default_rng(51)
    tt = lambda d: np.arange(int(d * SR)) / SR
    def add(sig, at, g=1.0):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += sig[: j - i] * g
    def lp(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
    voice = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "src.mp4", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, dtype=np.int16).astype(np.float64) / 32768
    voice = voice / (np.max(np.abs(voice)) + 1e-9) * 0.9
    env = np.convolve(np.abs(voice), np.ones(2400) / 2400, mode="same"); duck = 1 - 0.65 * np.clip(env / (env.max() + 1e-9) * 3, 0, 1)
    x = np.arange(len(voice)) / SR
    pad = sum(np.sin(2 * np.pi * f * x + p) * a for f, a, p in ((146.8, .35, 0), (220, .25, 1), (293.7, .2, 2), (440, .08, 3))) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.5 * x))
    pad *= 0.06 * np.minimum(1, x / 0.5)
    main = np.zeros(n); main[:len(pad)] += pad * duck
    fx = np.zeros(n)
    def fadd(sig, at, g=1.0):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: fx[i:j] += sig[: j - i] * g
    def shimmer(at, base=1318.5, g=0.1):
        for i, m in enumerate((1, 1.25, 1.5, 2)):
            y = tt(0.9); fadd(np.sin(2 * np.pi * base * m * y) * np.exp(-y * 5), at + 0.05 * i, g)
    def whoosh(at, d=0.35, g=0.4):
        y = tt(d); fadd(lp(rng.normal(0, 1, len(y)), 5) * np.sin(np.pi * y / d) ** 2, at, g)
    def thud(at, g=0.5):
        y = tt(0.35); fadd(np.sin(2 * np.pi * np.cumsum(60 + 50 * np.exp(-y * 20)) / SR) * np.exp(-y * 12), at, g)
    def ping(at, f0, g=0.18):
        y = tt(0.4); fadd((np.sin(2 * np.pi * f0 * y) + 0.3 * np.sin(4 * np.pi * f0 * y)) * np.exp(-y * 9), at, g)
    whoosh(CUT_IN - 0.2); shimmer(CUT_IN, 1046.5, 0.08)
    thud(STAMP, 0.55)
    for i, (at, _, _, _) in enumerate(BIDDERS): ping(at, (1318.5, 1568, 1975.5)[i], 0.2); shimmer(at + 0.02, 2093, 0.035)
    whoosh(CUT_OUT - 0.2, 0.3, 0.3)
    for i, (at, _) in enumerate(RACE): ping(at, 1760 + 110 * i, 0.09)
    thud(SOLD, 0.45); shimmer(SOLD + 0.02, 1318.5, 0.12)
    fx[:len(duck)] *= (0.4 + 0.6 * duck)
    out = main + fx; out[:len(voice)] += voice
    x2 = tt(0.4); add(np.sin(2 * np.pi * 98 * x2) * np.exp(-x2 * 11) * 0.6, CLIP + 0.02)
    x2 = tt(END); env2 = np.minimum(1, x2 / 0.3) * np.exp(-np.maximum(0, x2 - 1.6) * 0.8)
    add(sum(np.sin(2 * np.pi * f * x2) * a for f, a in ((196, .5), (246.94, .35), (293.66, .35), (392, .22))) * env2 * 0.3, CLIP + 0.05)
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
    build_audio("ep2_audio.wav")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", "ep2_audio.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(round(TOTAL * FPS))): enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT, round(TOTAL, 2))
