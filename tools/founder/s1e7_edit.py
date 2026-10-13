"""Season 1 Ep. 7 'Two prices' (Veo, modern apartment) — same design as the first 'Two prices' presenter Reel: kinetic captions, price-tag elements, bid flood, sound bed, end card.
Usage: python3 intro_edit.py out.mp4 [--stills t,...]"""
import subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/manouche")
import render as R
import mhelpers as M

W, H, FPS, SR = 1080, 1920, 30, 48000
WHITE, BG, NAVY, ACCENT = R.WHITE, R.BG, R.NAVY, R.ACCENT
OUT = sys.argv[1]
CLIP = 8.0; HOLD = 0.35; END = 3.6
T_END = CLIP + HOLD; TOTAL = T_END + END
# phrases (from the transcript), highlighted words in violet
CAPS = [(0.25, 2.60, ["Everything you own", "has [two prices.]"]),
        (2.90, 4.70, ["The one you'd", "sell it for…"]),
        (5.00, 7.75, ["…and the one someone", "would [fight for.]"])]
TAGS_IN, LEFT_ON, RIGHT_ON, MYSTERY = 0.8, 3.0, 5.2, 7.05
RISE = [20, 35, 60, 95, 140, 210, 340]; RISE_T0, RISE_DT = 5.3, 0.2
PUNCH = 6.45

def decode():
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "src.mp4", "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3); return [Image.frombytes("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]
FR = decode()

def base(t):
    fr = FR[min(len(FR) - 1, int(t * FPS))]
    z = 1.02 + (0.05 * R.ease_out((t - PUNCH) / 0.25) if PUNCH <= t < 7.3 else 0) + 0.02 * t / CLIP  # slow push, punch-in on "fight"
    return M.zoom(fr, z, 0.5, 0.45)

# ---------- elements ----------
def caption(lines, k):
    """two-line caption, words in [brackets] in violet; k = 0..1 reveal."""
    f = R.font(74, 700); out = []
    for ln in lines:
        parts, hi = [], False
        for chunk in ln.replace("[", "|[").replace("]", "]|").split("|"):
            if not chunk: continue
            if chunk.startswith("["): parts.append((chunk[1:-1], True))
            else: parts.append((chunk, False))
        layers = [R.text_layer(p, f, (167, 139, 250) if h else WHITE) for p, h in parts]
        w = sum(l.width for l in layers) - 4 * (len(layers) - 1); im = Image.new("RGBA", (w, max(l.height for l in layers)), (0, 0, 0, 0)); x = 0
        for l in layers: im.alpha_composite(l, (x, 0)); x += l.width - 4
        out.append(im)
    w = max(o.width for o in out) + 80; h = sum(o.height for o in out) + 50
    box = M.glass(w, h, 30, fill=(11, 14, 20, 190), border=(255, 255, 255, 30))
    y = 25
    for o in out: box.alpha_composite(o, ((w - o.width) // 2, y)); y += o.height - 6
    return box

def tag(label, value, hot=False, glow=0.0, w=430):
    lab = R.text_layer(label, R.font(24, mono=True), (200, 205, 230), tracking=3)
    num = R.text_layer(value, R.font(96, 700), WHITE)
    h = lab.height + num.height + 60
    pad = 30; im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    if hot and glow > 0:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((pad - 6, pad - 6, pad + w + 6, pad + h + 6), radius=40, fill=(124, 92, 255, int(200 * glow)))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(18)))
    if hot:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=255)
        card = Image.new("RGBA", (w, h), (0, 0, 0, 0)); card.paste(M.grad(w, h), (0, 0), m)
    else:
        card = M.glass(w, h, 34, fill=(20, 22, 32, 225), border=(255, 255, 255, 40))
    card.alpha_composite(lab, ((w - lab.width) // 2, 24)); card.alpha_composite(num, ((w - num.width) // 2, 30 + lab.height))
    im.alpha_composite(card, (pad, pad)); return im

def ping(text):
    tl = R.text_layer(text, R.font(34, 700), WHITE); w, h = tl.width + 40, tl.height + 22
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m); im.alpha_composite(tl, (20, 11)); return im
PINGS = [(RISE_T0 + i * RISE_DT, ping(f"+${RISE[i + 1] - RISE[i]}"), (-1) ** i) for i in range(len(RISE) - 1)]

def right_value(t):
    if t < RISE_T0: return "$ ???"
    if t >= MYSTERY: return "$ ???"
    i = min(len(RISE) - 1, int((t - RISE_T0) / RISE_DT)); return f"${RISE[i]}"

def overlay(im, t):
    im = im.convert("RGBA"); M.scrim(im, False, 620, 150); M.scrim(im, True, 380, 110)
    # price tags
    if t >= TAGS_IN:
        k = (t - TAGS_IN) / 0.35; a = R.clamp(k * 3) * (1 - R.clamp((t - (CLIP - 0.1)) / 0.3))
        sc_in = 0.6 + 0.4 * R.stamp(k) if k < 1 else 1.0
        left_focus = LEFT_ON <= t < RIGHT_ON; right_focus = t >= RIGHT_ON
        lt = tag("YOUR PRICE", "$20", hot=False)
        rv = right_value(t); glow = 0.5 + 0.5 * np.sin(t * 9) if RIGHT_ON <= t < MYSTERY else (0.35 if t >= MYSTERY else 0)
        rt = tag("THEIR PRICE", rv, hot=right_focus, glow=glow)
        la = a * (1.0 if not right_focus else 0.55); ra = a * (1.0 if not left_focus else 0.55)
        ls = sc_in * (1.08 if left_focus else 1.0); rs = sc_in * (1.08 if right_focus else 1.0)
        if RISE_T0 <= t < MYSTERY:  # bump on each new bid
            ph = ((t - RISE_T0) % RISE_DT) / RISE_DT; rs *= 1 + 0.05 * (1 - ph)
        R.paste_center(im, lt, 215, 255, la, ls * 0.8); R.paste_center(im, rt, W - 215, 255, ra, rs * 0.8)
        for at, p, side in PINGS:  # little "+$" chips flying into the right tag
            k2 = (t - at) / 0.55
            if 0 <= k2 < 1:
                x = W - 215 + side * 130 * (1 - k2); y = 640 - 210 * R.ease_out(k2)
                R.paste_center(im, p, x, y, (1 - k2) ** 0.7)
        if t >= MYSTERY:  # the second price stays a mystery: a question mark pulse
            pass
    # captions
    for t0, t1, lines in CAPS:
        if t0 <= t < t1 + 0.12:
            k = (t - t0) / 0.22; a = R.clamp(k * 3) * (1 - R.clamp((t - t1) / 0.12))
            R.paste_center(im, caption(lines, k), W / 2, 1450 + (1 - R.ease_out(k)) * 30, a)
    if PUNCH <= t < PUNCH + 0.1: im = M.flash(im, 0.25)
    if t >= CLIP: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - CLIP) / HOLD))
    return im

def end_card(k):
    im = R.GRAD_BG.copy(); s = k / 0.42; sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, R.z_mark(190), W / 2, 500, R.clamp(s * 3), sc)
    for i, line in enumerate(["Find out", "the second price."]):
        a = R.ease_out((k - 0.35 - i * 0.25) / 0.3); R.paste_center(im, R.text_layer(line, R.font(100, 700), WHITE), W / 2, 760 + i * 118 + (1 - a) * 20, a)
    b = R.ease_out((k - 1.3) / 0.35)
    hy, bz = R.text_layer("HYPER", R.font(54, 500), (215, 225, 255), tracking=6), R.text_layer("BIDZ", R.font(54, 700), WHITE, tracking=6)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0)); wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    R.paste_center(im, wm, W / 2, 1100, b); R.wrap_center(im, "Live auctions for Lebanon. Coming soon.", R.font(46, 500), WHITE, 1185, alpha=b, max_w=900)
    c = R.ease_out((k - 1.7) / 0.35); R.paste_center(im, R.pill("Follow @hyperbidz", R.font(50, 700), NAVY, WHITE, pad=(52, 28)), W / 2, 1340, c, 0.94 + 0.06 * c)
    out = im.convert("RGB")
    if k > END - 0.5: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), R.clamp((k - (END - 0.5)) / 0.5))
    return out

def frame(t):
    if t >= T_END: return end_card(t - T_END)
    return overlay(base(min(t, CLIP - 0.01)), t).convert("RGB")

# ---------- sound ----------
def build_audio(path):
    n = int(TOTAL * SR); out = np.zeros(n); rng = np.random.default_rng(31)
    tt = lambda d: np.arange(int(d * SR)) / SR
    def add(sig, at, g=1.0):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += sig[: j - i] * g
    def lp(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
    voice = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "src.mp4", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, dtype=np.int16).astype(np.float64) / 32768
    voice = voice / (np.max(np.abs(voice)) + 1e-9) * 0.9
    # music bed: soft pad + gentle pulse, ducked under the voice
    bed = np.zeros(int(CLIP * SR)); x = tt(CLIP)
    for f, a in ((110, .5), (164.8, .3), (220, .25), (329.6, .12)): bed += np.sin(2 * np.pi * f * x) * a
    bed *= 0.05 * np.minimum(1, x / 0.6)
    for k in range(int(CLIP / 0.5)):
        y = tt(0.25); add(np.sin(2 * np.pi * np.cumsum(50 + 40 * np.exp(-y * 30)) / SR) * np.exp(-y * 12) * 0.12, k * 0.5)
    env = np.convolve(np.abs(voice[:len(bed)]), np.ones(2400) / 2400, mode="same"); duck = 1 - 0.6 * np.clip(env / (env.max() + 1e-9) * 3, 0, 1)
    add(bed * duck, 0); add(voice, 0)
    def pop(at, f0=880, g=0.18):
        y = tt(0.25); add(np.sin(2 * np.pi * f0 * y) * np.exp(-y * 18) + lp(rng.normal(0, 1, len(y)), 4) * np.exp(-y * 60) * 0.3, at, g)
    pop(TAGS_IN, 660); pop(TAGS_IN + 0.12, 990)
    for at, _, _ in PINGS: pop(at, 1568 + 120 * ((at - RISE_T0) / RISE_DT), 0.13)
    y = tt(0.5); add(lp(rng.normal(0, 1, len(y)), 6) * np.sin(np.pi * y / 0.5) ** 2, PUNCH - 0.2, 0.25)   # whoosh into "fight"
    y = tt(0.35); add(np.sin(2 * np.pi * 70 * y) * np.exp(-y * 9), PUNCH + 0.03, 0.35)                     # punch on "fight"
    y = tt(1.6); add(np.sin(2 * np.pi * 587.3 * y) * np.exp(-y * 2.5) * 0.5 + np.sin(2 * np.pi * 880 * y) * np.exp(-y * 3) * 0.3, MYSTERY + 0.05, 0.12)  # mystery tone
    x = tt(0.4); add(np.sin(2 * np.pi * 98 * x) * np.exp(-x * 11) * 0.6, T_END + 0.02)
    x = tt(END); env2 = np.minimum(1, x / 0.3) * np.exp(-np.maximum(0, x - 1.6) * 0.8)
    add(sum(np.sin(2 * np.pi * f * x) * a for f, a in ((196, .5), (246.94, .35), (293.66, .35), (392, .22))) * env2 * 0.3, T_END + 0.05)
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
    build_audio("s1e7_audio.wav")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", "s1e7_audio.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(round(TOTAL * FPS))): enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT, round(TOTAL, 2))
