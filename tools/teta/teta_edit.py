"""Brand edit for the "Teta discovers auctions" Higgsfield clip.
Usage: python3 teta_edit.py scene.mp4 out.mp4 [cues.json] [--still] [--mute-scene]
cues.json (optional): {"q1": [start, end], "q2": [start, end], "freeze": t}
Needs render.py (brand helpers) and fonts/ next to it."""
import json, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw
import render as R

args = [a for a in sys.argv[1:] if not a.startswith("--")]
SRC, OUT = args[0], args[1]
CUES = {"q1": [0.4, 3.2], "q2": [3.6, 6.8], "freeze": 8.4}
if len(args) > 2:
    CUES.update(json.load(open(args[2])))
MUTE = "--mute-scene" in sys.argv
W, H, FPS = 1080, 1920, 30
dur = float(json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", SRC]))["format"]["duration"])
FREEZE_AT = min(CUES["freeze"], dur - 0.1)
FREEZE_LEN = 1.3
END = 3.6
TOTAL = FREEZE_AT + FREEZE_LEN + END
N = int(round(TOTAL * FPS))

def bubble(speaker, line, size=62):
    f = R.font(size, 700)
    lines = []
    cur = ""
    for w in line.split():
        t = (cur + " " + w).strip()
        if f.getlength(t) <= 860: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    lab = R.text_layer(speaker.upper(), R.font(26, mono=True), (167, 139, 250), tracking=4)
    tls = [R.text_layer(l, f, (255, 255, 255)) for l in lines]
    w = max([lab.width] + [t.width for t in tls]) + 72
    h = lab.height + sum(int(size * 1.12) for _ in tls) + 64
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=(11, 14, 20, 205))
    im.alpha_composite(lab, ((w - lab.width) // 2, 26))
    y = 26 + lab.height + 8
    for t in tls:
        im.alpha_composite(t, ((w - t.width) // 2, y)); y += int(size * 1.12)
    return im

B1 = bubble("Auctioneer", "Do I hear higher?")
B2 = bubble("Teta", "Higher? Yalla, I'll go LOWER.")

def shadow_text(text, size, fill, weight=700):
    layer = R.text_layer(text, R.font(size, weight), fill)
    sh = R.text_layer(text, R.font(size, weight), (0, 0, 0))
    sh.putalpha(sh.getchannel("A").point(lambda v: int(v * 0.6)))
    out = Image.new("RGBA", (layer.width + 8, layer.height + 8), (0, 0, 0, 0))
    out.alpha_composite(sh, (4, 5)); out.alpha_composite(layer, (0, 0)); return out

HOOK = [shadow_text("POV: Teta discovers", 76, (255, 255, 255)), shadow_text("auctions", 76, (255, 255, 255))]

def scrim(im, top=True):
    s = Image.new("RGBA", (W, 620), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    for y in range(620):
        a = int(150 * (1 - y / 620) ** 1.5)
        d.line([(0, y), (W, y)], fill=(11, 14, 20, a))
    im.alpha_composite(s if top else s.transpose(Image.FLIP_TOP_BOTTOM), (0, 0 if top else H - 620))

def pop(t, start, end):
    if t < start or t > end: return 0.0, 1.0
    k = (t - start) / 0.28
    sc = 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0
    a = min(1.0, k * 3) * (1 - R.clamp((t - (end - 0.18)) / 0.18))
    return a, sc

def scene_frame(base, t):
    im = base.convert("RGBA")
    scrim(im, True); scrim(im, False)
    if t < 2.8:
        a = R.ease_out(t / 0.3) * (1 - R.clamp((t - 2.55) / 0.25))
        for i, l in enumerate(HOOK):
            R.paste_center(im, l, W / 2, 300 + i * 92, a)
    a, sc = pop(t, *CUES["q1"])
    if a > 0: R.paste_center(im, B1, W / 2, 1420, a, sc)
    a, sc = pop(t, *CUES["q2"])
    if a > 0: R.paste_center(im, B2, W / 2, 1420, a, sc)
    return im

def freeze_frame(base, k):
    # slow push-in on the frozen reaction, desaturate slightly, caption
    z = 1 + 0.06 * R.ease_out(k)
    w, h = int(W * z), int(H * z)
    im = base.resize((w, h), Image.LANCZOS).crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H)).convert("RGBA")
    grey = im.convert("L").convert("RGBA")
    im = Image.blend(im, grey, 0.35)
    scrim(im, False)
    a = R.ease_out(k / 0.25)
    R.paste_center(im, shadow_text("The whole room:", 70, (255, 255, 255)), W / 2, 1460, a)
    return im

def end_card(k):
    im = R.GRAD_BG.copy()
    if k < 0.25:
        im = Image.blend(Image.new("RGBA", (W, H), R.BG + (255,)), im, R.ease_out(k / 0.25))
    s = k / 0.42
    sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, R.text_layer("Sorry, Teta.", R.font(150, 700), (255, 255, 255)), W / 2, 640, R.clamp(s * 3), sc)
    a = R.ease_out((k - 0.5) / 0.35)
    R.wrap_center(im, "At an auction, bids only go up.", R.font(64, 500), (255, 255, 255), 830, alpha=a, max_w=900, line_h=1.15)
    b = R.ease_out((k - 1.1) / 0.35)
    R.paste_center(im, R.z_mark(150), W / 2, 1090, b)
    f1, f2 = R.font(56, 500), R.font(56, 700)
    hy, bz = R.text_layer("HYPER", f1, (215, 225, 255), tracking=6), R.text_layer("BIDZ", f2, (255, 255, 255), tracking=6)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0))
    wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    R.paste_center(im, wm, W / 2, 1230, b)
    R.wrap_center(im, "Live auctions for Lebanon. Coming soon.", R.font(46, 500), (255, 255, 255), 1320, alpha=b, max_w=900)
    c = R.ease_out((k - 1.5) / 0.35)
    R.paste_center(im, R.pill("Follow @hyperbidz", R.font(50, 700), R.NAVY, (255, 255, 255), pad=(52, 28)), W / 2, 1470, c, 0.94 + 0.06 * c)
    return im

def decoder():
    return subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", SRC, "-t", str(FREEZE_AT + 0.05), "-vf",
                             f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)

def build_audio(path, sr=48000):
    n = int(TOTAL * sr); out = np.zeros(n)
    tt = lambda d: np.arange(int(d * sr)) / sr
    def add(sig, at):
        i = int(at * sr); j = min(n, i + len(sig)); out[i:j] += sig[: j - i]
    rng = np.random.default_rng(5)
    if not MUTE:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-t", str(FREEZE_AT), "-ac", "1", "-ar", str(sr), "-f", "s16le", "scene.pcm"], check=False)
        try:
            sc = np.frombuffer(open("scene.pcm", "rb").read(), dtype=np.int16).astype(np.float64) / 32768
            out[: min(n, len(sc))] += sc[:n] * 0.85
        except Exception:
            pass
    else:
        x = tt(FREEZE_AT)  # soft room tone
        out[: len(x)] += np.convolve(rng.normal(0, 1, len(x)), np.ones(200) / 200, mode="same") * 0.6
    # record scratch at the freeze
    x = tt(0.45)
    f = 900 * np.exp(-x * 6) + 120
    scratch = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-x * 4) * 0.5 + rng.normal(0, 1, len(x)) * np.exp(-x * 9) * 0.35
    add(scratch, FREEZE_AT)
    out[int((FREEZE_AT + 0.45) * sr): int((FREEZE_AT + FREEZE_LEN) * sr)] *= 0.0
    # cricket-quiet beat, then end card stamp + chord
    e = FREEZE_AT + FREEZE_LEN
    x = tt(0.4); add(np.sin(2 * np.pi * 110 * x) * np.exp(-x * 12) * 0.6, e)
    x = tt(END)
    env = np.minimum(1, x / 0.3) * np.exp(-np.maximum(0, x - 1.4) * 0.9)
    add(sum(np.sin(2 * np.pi * fr * x) * am for fr, am in ((261.63, .5), (329.63, .35), (392, .35), (523.25, .2))) * env * 0.28, e)
    out[-int(0.25 * sr):] *= np.linspace(1, 0, int(0.25 * sr))
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.85
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(sr); w_.writeframes((out * 32767).astype(np.int16).tobytes())

def render_full():
    build_audio("teta_audio.wav")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "teta_audio.wav",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    dec = decoder(); last = None
    n_scene = int(FREEZE_AT * FPS)
    for k in range(N):
        t = k / FPS
        if k < n_scene:
            raw = dec.stdout.read(W * H * 3)
            if raw and len(raw) == W * H * 3: last = Image.frombytes("RGB", (W, H), raw)
            fr = scene_frame(last, t)
        elif t < FREEZE_AT + FREEZE_LEN:
            fr = freeze_frame(last, (t - FREEZE_AT) / FREEZE_LEN)
        else:
            fr = end_card(t - FREEZE_AT - FREEZE_LEN)
        enc.stdin.write(fr.convert("RGB").tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT)

if __name__ == "__main__" and "--still" not in sys.argv:
    render_full(); sys.exit()

if __name__ == "__main__":
    dec = decoder(); frames = []
    last = None
    i = 0
    while True:
        raw = dec.stdout.read(W * H * 3)
        if not raw or len(raw) < W * H * 3: break
        last = Image.frombytes("RGB", (W, H), raw)
        if "--still" in sys.argv and i % 15 == 0: frames.append((i / FPS, last))
        if "--still" not in sys.argv: frames.append(last)
        i += 1
    if "--still" in sys.argv:
        picks = [t for t, _ in frames]
        for t, fr in frames:
            scene_frame(fr, t).convert("RGB").resize((270, 480)).save(f"st_{t:04.1f}.jpg", quality=80)
        freeze_frame(last, 0.6).convert("RGB").resize((270, 480)).save("st_freeze.jpg", quality=80)
        end_card(2.5).convert("RGB").resize((270, 480)).save("st_end.jpg", quality=80)
        sys.exit()
    print("unused")
