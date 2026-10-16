"""Shared pieces for founder-series edits: decode, captions, stars, end card, audio base."""
import subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/manouche")
import render as R
import mhelpers as M
W, H, FPS, SR = 1080, 1920, 30, 48000
WHITE, BG, NAVY = R.WHITE, R.BG, R.NAVY

def decode(src="src.mp4"):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3); return [Image.frombytes("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]

def caption(lines, size=72):
    f = R.font(size, 700); out = []
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

def draw_caps(im, t, caps, y=1560, size=72):
    for t0, t1, lines in caps:
        if t0 <= t < t1:
            k = (t - t0) / 0.18; a = R.clamp(k * 3) * (1 - R.clamp((t - (t1 - 0.1)) / 0.1))
            R.paste_center(im, caption(lines, size), W / 2, y + (1 - R.ease_out(k)) * 20, a)

def star(sz):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = sz / 2
    d.polygon([(c, 0), (c + sz * .12, c - sz * .12), (sz, c), (c + sz * .12, c + sz * .12), (c, sz), (c - sz * .12, c + sz * .12), (0, c), (c - sz * .12, c - sz * .12)], fill=(255, 255, 255, 255))
    return im
STARS = {s: star(s) for s in (14, 18, 26, 34)}

def sparkle_burst(im, t, t0, cx, cy, spots=((-90, -60, 26), (95, -40, 18), (60, 70, 34), (-70, 60, 18))):
    for j, (ox, oy, sz) in enumerate(spots):
        tw = (t - t0 - 0.05 * j) * 3.5
        if 0 < tw < np.pi: R.paste_center(im, STARS[sz], cx + ox, cy + oy, np.sin(tw), 0.6 + 0.4 * np.sin(tw))

def end_card(k, lines, END):
    im = R.GRAD_BG.copy(); s = k / 0.42; sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, R.z_mark(190), W / 2, 500, R.clamp(s * 3), sc)
    for i, line in enumerate(lines):
        a = R.ease_out((k - 0.35 - i * 0.3) / 0.3); R.paste_center(im, R.text_layer(line, R.font(100, 700), WHITE), W / 2, 760 + i * 118 + (1 - a) * 20, a)
    b = R.ease_out((k - 1.3) / 0.35)
    hy, bz = R.text_layer("HYPER", R.font(54, 500), (215, 225, 255), tracking=6), R.text_layer("BIDZ", R.font(54, 700), WHITE, tracking=6)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0)); wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    R.paste_center(im, wm, W / 2, 1100, b); R.wrap_center(im, "Live auctions for Lebanon. Coming soon.", R.font(46, 500), WHITE, 1185, alpha=b, max_w=900)
    c = R.ease_out((k - 1.7) / 0.35); R.paste_center(im, R.pill("Follow @hyperbidz", R.font(50, 700), NAVY, WHITE, pad=(52, 28)), W / 2, 1340, c, 0.94 + 0.06 * c)
    out = im.convert("RGB")
    if k > END - 0.5: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), R.clamp((k - (END - 0.5)) / 0.5))
    return out

class Mix:
    """voice + ducked pad + ducked effects + end chord."""
    def __init__(self, clip, end, src="src.mp4", pad_freqs=((146.8, .35), (220, .25), (293.7, .2), (440, .08))):
        self.n = int((clip + end) * SR); self.clip, self.end = clip, end; self.rng = np.random.default_rng(7)
        v = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, dtype=np.int16).astype(np.float64) / 32768
        self.voice = v / (np.max(np.abs(v)) + 1e-9) * 0.9
        if len(self.voice) < int(clip * SR): self.voice = np.concatenate([self.voice, np.zeros(int(clip * SR) - len(self.voice))])   # held last shot
        env = np.convolve(np.abs(self.voice), np.ones(2400) / 2400, mode="same"); self.duck = 1 - 0.65 * np.clip(env / (env.max() + 1e-9) * 3, 0, 1)
        x = np.arange(len(self.voice)) / SR
        pad = sum(np.sin(2 * np.pi * f * x + i) * a for i, (f, a) in enumerate(pad_freqs)) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.5 * x)) * 0.06 * np.minimum(1, x / 0.5)
        self.main = np.zeros(self.n); self.main[:len(pad)] += pad * self.duck; self.fx = np.zeros(self.n)
    def tt(self, d): return np.arange(int(d * SR)) / SR
    def fadd(self, sig, at, g=1.0):
        i = int(at * SR); j = min(self.n, i + len(sig))
        if 0 <= i < self.n: self.fx[i:j] += sig[: j - i] * g
    def lp(self, x, k): return np.convolve(x, np.ones(k) / k, mode="same")
    def shimmer(self, at, base=1318.5, g=0.1):
        for i, m in enumerate((1, 1.25, 1.5, 2)):
            y = self.tt(0.9); self.fadd(np.sin(2 * np.pi * base * m * y) * np.exp(-y * 5), at + 0.05 * i, g)
    def whoosh(self, at, d=0.35, g=0.4):
        y = self.tt(d); self.fadd(self.lp(self.rng.normal(0, 1, len(y)), 5) * np.sin(np.pi * y / d) ** 2, at, g)
    def thud(self, at, g=0.5):
        y = self.tt(0.35); self.fadd(np.sin(2 * np.pi * np.cumsum(60 + 50 * np.exp(-y * 20)) / SR) * np.exp(-y * 12), at, g)
    def ping(self, at, f0, g=0.18):
        y = self.tt(0.4); self.fadd((np.sin(2 * np.pi * f0 * y) + 0.3 * np.sin(4 * np.pi * f0 * y)) * np.exp(-y * 9), at, g)
    def write(self, path):
        fx = self.fx.copy(); fx[:len(self.duck)] *= (0.4 + 0.6 * self.duck)
        out = self.main + fx; out[:len(self.voice)] += self.voice
        x = self.tt(0.4); i = int((self.clip + 0.02) * SR); out[i:i + len(x)] += np.sin(2 * np.pi * 98 * x) * np.exp(-x * 11) * 0.6
        x = self.tt(self.end); env2 = np.minimum(1, x / 0.3) * np.exp(-np.maximum(0, x - 1.6) * 0.8); i = int((self.clip + 0.05) * SR)
        chord = sum(np.sin(2 * np.pi * f * x) * a for f, a in ((196, .5), (246.94, .35), (293.66, .35), (392, .22))) * env2 * 0.3
        out[i:i + len(chord)] += chord[: self.n - i]
        out[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR)) ** 1.5
        out = out / (np.max(np.abs(out)) + 1e-9) * 0.92
        with wave.open(path, "wb") as w_:
            w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

def hold_zoom(im, t, shot=8.0, start=7.0, hold=1.4, z1=1.08, focus=(540, 700)):
    """owner's rule (14 Oct): let the last shot breathe. From `start` to the end of the hold, push in slowly toward
    `focus`; the video itself is frozen on its last frame after `shot`."""
    if t < start: return im
    k = R.clamp((t - start) / (shot + hold - start)); z = 1 + (z1 - 1) * (k * k * (3 - 2 * k))
    w, h = W / z, H / z; cx, cy = focus; l = min(max(cx - w / 2, 0), W - w); tp = min(max(cy - h / 2, 0), H - h)
    return im.crop((int(l), int(tp), int(l + w), int(tp + h))).resize((W, H), Image.BICUBIC)

def render(frame, total, audio_path, out):
    if "--stills" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        ims = [frame(t).resize((216, 384)) for t in ts]; s = Image.new("RGB", (216 * len(ims), 384))
        for i, im in enumerate(ims): s.paste(im, (216 * i, 0))
        s.save("stills.jpg", quality=85); print("stills.jpg"); return False
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", audio_path, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(round(total * FPS))): enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait(); print("done", out, round(total, 2)); return True
