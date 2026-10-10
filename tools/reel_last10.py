"""Render HyperBidz Reel: "The last 10 seconds" (1080x1920, 30 fps, 15 s, with sound)."""
# Example Reel renderer (post 2). Copy it for new motion Reels; run `python3 tools/slides.py` once first so tools/fonts exists.
import math, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 15.0
N = int(FPS * DUR)
OUT = sys.argv[1] if len(sys.argv) > 1 else "reel.mp4"

BG = (11, 14, 20)
WHITE = (255, 255, 255)
MUTED = (176, 178, 181)          # white at 0.68 over the stage
ACCENT = (167, 139, 250)         # #A78BFA
FEED = (124, 92, 255)            # #7C5CFF
BLUE = (47, 123, 255)            # #2F7BFF
NAVY = (42, 21, 128)             # #2A1580 (text on white CTA)

GROTESK = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "fonts", "SpaceGrotesk-VF.ttf")
MONO = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "fonts", "SpaceMono-Bold.ttf")
_fc = {}

def font(size, weight=700, mono=False):
    size = max(8, int(round(size)))
    key = (size, weight, mono)
    if key not in _fc:
        if mono:
            f = ImageFont.truetype(MONO, size)
        else:
            f = ImageFont.truetype(GROTESK, size)
            f.set_variation_by_axes([weight])
        _fc[key] = f
    return _fc[key]

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3

def bezier(p1x, p1y, p2x, p2y):
    def bx(t): return 3*(1-t)**2*t*p1x + 3*(1-t)*t**2*p2x + t**3
    def by(t): return 3*(1-t)**2*t*p1y + 3*(1-t)*t**2*p2y + t**3
    def f(x):
        x = clamp(x); lo, hi = 0.0, 1.0
        for _ in range(30):
            mid = (lo + hi) / 2
            if bx(mid) < x: lo = mid
            else: hi = mid
        return by((lo + hi) / 2)
    return f

stamp = bezier(0.2, 1.3, 0.35, 1.0)   # motion.easing.stamp from the design system

def mix(c1, c2, k):
    return tuple(int(round(a + (b - a) * k)) for a, b in zip(c1, c2))

# ---------- precomputed art ----------
def diag_gradient(w, h, c1, c2):
    x = np.linspace(0, 1, w)[None, :]; y = np.linspace(0, 1, h)[:, None]
    k = clamp_arr((x * w + y * h * 0.55) / (w + h * 0.55))
    arr = (np.array(c1)[None, None, :] * (1 - k[..., None]) + np.array(c2)[None, None, :] * k[..., None])
    return Image.fromarray(arr.astype(np.uint8), "RGB")

def clamp_arr(a):
    return np.clip(a, 0, 1)

GRAD_BG = diag_gradient(W, H, BLUE, FEED).convert("RGBA")
BAR_GRAD = Image.fromarray(np.array([[mix(BLUE, FEED, i / 499)] for i in range(500)], dtype=np.uint8).repeat(10, axis=1), "RGB").convert("RGBA")

Z_TOP = [(24.75,16),(84.75,16),(81.94,36),(59.69,54.36),(44.98,41.74),(51.94,36),(21.94,36)]
Z_BOT = [(55,58.23),(48.01,64),(78.01,64),(75.2,84),(15.2,84),(18.01,64),(40.28,45.62)]

def z_mark(size, color=WHITE):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    s = size / 100
    for poly in (Z_TOP, Z_BOT):
        d.polygon([(x * s, y * s) for x, y in poly], fill=color + (255,))
    return im

# ---------- drawing helpers ----------
def text_layer(text, f, fill, features=None, tracking=0):
    """Render text tightly on a transparent layer (tracking in px between glyphs)."""
    if tracking:
        widths = [f.getlength(ch) for ch in text]
        tw = int(sum(widths) + tracking * (len(text) - 1)) + 4
    else:
        tw = int(f.getlength(text, features=features)) + 4
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (tw, asc + desc + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if tracking:
        x = 2
        for ch, wch in zip(text, widths):
            d.text((x, 2), ch, font=f, fill=fill + (255,)); x += wch + tracking
    else:
        d.text((2, 2), text, font=f, fill=fill + (255,), features=features)
    return im

def paste_center(base, layer, cx, cy, alpha=1.0, scale=1.0):
    if alpha <= 0.003: return
    if abs(scale - 1) > 0.002:
        layer = layer.resize((max(1, int(layer.width * scale)), max(1, int(layer.height * scale))), Image.LANCZOS)
    if alpha < 0.999:
        a = layer.getchannel("A").point(lambda v: int(v * alpha)); layer = layer.copy(); layer.putalpha(a)
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def pill(text, f, fg, bg, border=None, pad=(44, 22), tracking=0, radius=None, bg_alpha=255):
    tl = text_layer(text, f, fg, tracking=tracking)
    w, h = tl.width + pad[0] * 2, tl.height + pad[1] * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    r = radius if radius is not None else h // 2
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=bg + (bg_alpha,), outline=(border + (255,)) if border else None, width=3 if border else 0)
    im.alpha_composite(tl, (pad[0], pad[1]))
    return im

def wrap_center(base, text, f, fill, cy, alpha=1.0, max_w=900, line_h=1.08, dy=0):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if f.getlength(t) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    lines.append(cur)
    lh = f.size * line_h
    top = cy - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        paste_center(base, text_layer(ln, f, fill), W / 2, top + i * lh + dy, alpha)

# ---------- scene ----------
HEADLINES = [(0.0, 3.0, "You have 10 seconds."), (3.0, 6.0, "The price keeps climbing."),
             (6.0, 8.5, "Someone just bid."), (8.5, 10.0, "Your move.")]

def frame(t):
    if t >= 11.4:
        return end_card(t)
    im = Image.new("RGBA", (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    if t < 10.0:
        secs = 10 - int(math.floor(t)); frac = t - math.floor(t)
        final = secs <= 7
        # final-seconds frame, breathing 0.10 <-> 0.38 every 0.9 s
        if final:
            a = 0.10 + 0.28 * (0.5 - 0.5 * math.cos(2 * math.pi * (t - 3.0) / 0.9))
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rectangle((0, 0, W - 1, H - 1), outline=FEED + (int(255 * a),), width=18)
            im.alpha_composite(ov)
        # label above the clock
        label = "ENDS IN" if not final else ("GOING ONCE…" if secs > 3 else "GOING TWICE…")
        lab_col = MUTED if not final else ACCENT
        pulse = 1 + 0.04 * max(0.0, 1 - frac / 0.3)
        paste_center(im, text_layer(label, font(40, mono=True), lab_col, tracking=8), W / 2, 520, 1.0, pulse if final else 1.0)
        # the clock
        col = WHITE if not final else ACCENT
        clock = text_layer(f"00:{secs:02d}", font(250, 700), col, features=["tnum"])
        paste_center(im, clock, W / 2, 720, 1.0, pulse)
        # strike-flash ring when the bid lands (6.0 s)
        if 6.0 <= t < 6.75:
            k = (t - 6.0) / 0.75; ra = 0.9 * (k / 0.15 if k < 0.15 else (1 - k) / 0.85)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rounded_rectangle((110, 560, 970, 880), radius=60, outline=FEED + (int(255 * ra),), width=6)
            im.alpha_composite(ov)
        # draining progress bar
        x0, x1, y = 140, 940, 920
        d.rounded_rectangle((x0, y, x1, y + 10), radius=5, fill=(35, 38, 47))
        fill_w = int((x1 - x0) * clamp(1 - t / 10.0))
        if fill_w > 10:
            g = BAR_GRAD.resize((fill_w, 10)).rotate(0)
            gh = Image.fromarray(np.array([[mix(BLUE, FEED, i / max(1, fill_w - 1)) for i in range(fill_w)]] * 10, dtype=np.uint8), "RGB").convert("RGBA")
            m = Image.new("L", (fill_w, 10), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fill_w - 1, 9), radius=5, fill=255)
            im.paste(gh, (x0, y), m)
        # headline
        for a0, a1, txt in HEADLINES:
            if a0 <= t < a1:
                k_in = ease_out((t - a0) / 0.3); k_out = 1 - clamp((t - (a1 - 0.2)) / 0.2)
                wrap_center(im, txt, font(96, 700), WHITE, 1100, alpha=k_in * k_out, dy=(1 - k_in) * 30)
        # rising bars (3.0 - 6.0 s, stay faint after)
        if t >= 3.0:
            heights = [70, 110, 150, 190, 230]
            base_y, bw, gap = 1560, 110, 26
            x = (W - (5 * bw + 4 * gap)) / 2
            fade = 1.0 if t < 6.0 else max(0.25, 1 - (t - 6.0) / 0.6)
            for i, hgt in enumerate(heights):
                k = ease_out((t - 3.0 - i * 0.45) / 0.5)
                if k <= 0: continue
                hh = int(hgt * k)
                bar = BAR_GRAD.resize((bw, hh)) if hh > 0 else None
                if bar is None: continue
                m = Image.new("L", (bw, hh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, hh - 1), radius=26, fill=int(255 * fade * (0.35 + 0.65 * (i + 1) / 5)))
                im.paste(bar, (int(x + i * (bw + gap)), base_y - hh), m)
        # NEW HIGH BID bubble pops at 6.2 s
        if t >= 6.2:
            k = (t - 6.2) / 0.35
            sc = stamp(k) if k < 1 else 1.0
            bub = pill("NEW HIGH BID", font(40, mono=True), WHITE, FEED, border=(198, 184, 255), tracking=6)
            paste_center(im, bub, W / 2, 1265, clamp(k * 3), max(0.01, sc))
    else:
        # 10.0 - 11.4: hammer falling
        k = (t - 10.0)
        chip = pill("HAMMER FALLING", font(52, mono=True), WHITE, (49, 38, 98), border=ACCENT, tracking=10, pad=(56, 30))
        paste_center(im, chip, W / 2, 700, ease_out(k / 0.2))
        wrap_center(im, "Clock hits zero.", font(104, 700), WHITE, 950, alpha=ease_out((k - 0.1) / 0.25))
        if t >= 10.6:
            s = (t - 10.6) / 0.42
            sc = 1.7 - 0.7 * stamp(s) if s < 1 else 1.0
            layer = text_layer("Highest bid wins.", font(104, 700), ACCENT)
            paste_center(im, layer, W / 2, 1090, clamp(s * 2.5), sc)
    return im.convert("RGB")

def end_card(t):
    k = t - 11.4
    im = GRAD_BG.copy()
    if k < 0.3:   # crossfade from the stage
        stage = Image.new("RGBA", (W, H), BG + (255,))
        im = Image.blend(stage, im, ease_out(k / 0.3))
    s = k / 0.42
    sc = 1.6 - 0.6 * stamp(s) if s < 1 else 1.0
    paste_center(im, z_mark(300), W / 2, 640, clamp(s * 3), sc)
    a = ease_out((k - 0.45) / 0.35)
    wm_f1, wm_f2 = font(78, 500), font(78, 700)
    hy, bz = text_layer("HYPER", wm_f1, (215, 225, 255), tracking=8), text_layer("BIDZ", wm_f2, WHITE, tracking=8)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0))
    wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    paste_center(im, wm, W / 2, 880, a, 1 + (1 - a) * 0.04)
    paste_center(im, text_layer("MA FI EKHER SE3ER. FI EKHER SENYE.", font(34, mono=True), (235, 238, 255), tracking=5), W / 2, 1010, ease_out((k - 0.9) / 0.35))
    wrap_center(im, "Live auctions for Lebanon. Coming soon.", font(58, 500), WHITE, 1130, alpha=ease_out((k - 1.2) / 0.35), max_w=860, line_h=1.15)
    b = ease_out((k - 1.6) / 0.35)
    paste_center(im, pill("Follow @hyperbidz", font(54, 700), NAVY, WHITE, pad=(56, 30)), W / 2, 1330, b, 0.94 + 0.06 * b)
    return im.convert("RGB")

# ---------- audio ----------
def audio(path, sr=48000):
    n = int(sr * DUR); out = np.zeros(n)
    rng = np.random.default_rng(7)
    def add(sig, at):
        i = int(at * sr); j = min(n, i + len(sig)); out[i:j] += sig[: j - i]
    tt = lambda dur: np.arange(int(dur * sr)) / sr
    # clock ticks each second, a touch louder in the final seconds
    for s in range(10):
        x = tt(0.06); vol = 0.35 + 0.04 * s
        tick = (np.sin(2 * np.pi * (2900 if s < 3 else 3300) * x) * np.exp(-x * 90) * 0.6 + rng.normal(0, 1, len(x)) * np.exp(-x * 400) * 0.4) * vol
        add(tick, s + 0.0)
        add(tick * 0.45, s + 0.5)               # tock
    # heartbeat speeding up 70 -> 150 bpm
    tb = 0.15
    while tb < 9.9:
        bpm = 70 + 80 * (tb / 10)
        for off, amp in ((0, 0.9), (0.16, 0.6)):
            x = tt(0.18); thump = np.sin(2 * np.pi * (52 + 30 * np.exp(-x * 30)) * x) * np.exp(-x * 22) * amp * (0.35 + 0.25 * tb / 10)
            add(thump, tb + off)
        tb += 60 / bpm
    # tension riser 5.5 -> 10.0 s
    x = tt(4.5); noise = rng.normal(0, 1, len(x))
    smooth = np.convolve(noise, np.ones(40) / 40, mode="same")
    add(smooth * (x / 4.5) ** 2.2 * 0.5, 5.5)
    # hard cut to silence at 10.0, gavel at 10.6
    out[int(10.0 * sr):] = 0
    x = tt(0.9)
    gavel = (np.sin(2 * np.pi * 68 * x) * np.exp(-x * 7) * 1.0 + np.sin(2 * np.pi * 180 * x) * np.exp(-x * 25) * 0.4 + rng.normal(0, 1, len(x)) * np.exp(-x * 120) * 0.5)
    add(gavel, 10.6)
    # end card: stamp hit + warm chord
    x = tt(0.4); add(np.sin(2 * np.pi * 110 * x) * np.exp(-x * 12) * 0.5, 11.4)
    x = tt(3.6)
    env = np.minimum(1, x / 0.35) * np.exp(-np.maximum(0, x - 1.2) * 0.9)
    chord = sum(np.sin(2 * np.pi * f_ * x) * a_ for f_, a_ in ((220, .5), (277.18, .35), (329.63, .35), (440, .25), (554.37, .12)))
    add(chord * env * 0.3, 11.4)
    out[-int(0.25 * sr):] *= np.linspace(1, 0, int(0.25 * sr))
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.7
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(sr); w_.writeframes(pcm.tobytes())

if __name__ == "__main__":
    if "--still" in sys.argv:
        for ts in (1.5, 4.8, 7.5, 9.2, 10.9, 14.0):
            frame(ts).save(f"still_{ts:.1f}.png")
        sys.exit()
    audio("audio.wav")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", "audio.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(N):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    print("done", OUT)
