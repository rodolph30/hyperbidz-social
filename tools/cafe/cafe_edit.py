"""Composite the Higgsfield cafe scene into a branded Reel.
Usage: python3 cafe_edit.py scene.mp4 out.mp4"""
import subprocess, sys, json, wave
import numpy as np
from PIL import Image, ImageDraw
import render as R   # brand helpers: fonts, pills, end card, easing

SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS = 1080, 1920, 30
probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", SRC]))
SCENE = min(8.0, float(probe["format"]["duration"]))
END = 3.4
DUR = SCENE + END
N = int(round(DUR * FPS))

def glass_chip(text, fg, bg_rgba, border=None, size=40, tracking=6, pad=(40, 20)):
    tl = R.text_layer(text, R.font(size, mono=True), fg, tracking=tracking)
    w, h = tl.width + pad[0] * 2, tl.height + pad[1] * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=bg_rgba, outline=border, width=3 if border else 0)
    im.alpha_composite(tl, (pad[0], pad[1])); return im

def shadow_text(text, size, fill):
    layer = R.text_layer(text, R.font(size, 700), fill)
    sh = R.text_layer(text, R.font(size, 700), (0, 0, 0))
    a = sh.getchannel("A").point(lambda v: int(v * 0.55)); sh.putalpha(a)
    out = Image.new("RGBA", (layer.width + 8, layer.height + 8), (0, 0, 0, 0))
    out.alpha_composite(sh, (4, 5)); out.alpha_composite(layer, (0, 0)); return out

def overlay(base, t):
    im = base.convert("RGBA")
    # top scrim for legibility
    scrim = Image.new("RGBA", (W, 560), (0, 0, 0, 0)); sd = ImageDraw.Draw(scrim)
    for y in range(560):
        sd.line([(0, y), (W, y)], fill=(11, 14, 20, int(150 * (1 - y / 560) ** 1.4)))
    im.alpha_composite(scrim, (0, 0))
    # hook line
    if t < 2.6:
        k = R.ease_out(t / 0.3) * (1 - R.clamp((t - 2.35) / 0.25))
        for i, ln in enumerate(["POV: 3 seconds left", "on the lakta."]):
            R.paste_center(im, shadow_text(ln, 78, (255, 255, 255)), W / 2, 390 + i * 92, k)
    # countdown chip, app styling
    if t < 5.6:
        secs = 3 if t < 2.6 else (2 if t < 4.0 else 1)
        label = "ENDS IN" if t < 2.6 else ("GOING ONCE…" if t < 4.0 else "GOING TWICE…")
        frac = (t if t < 2.6 else (t - 2.6 if t < 4.0 else t - 4.0))
        pulse = 1 + 0.04 * max(0.0, 1 - (frac % 1.0) / 0.3)
        fill = (11, 14, 20, 120) if t < 2.6 else (124, 92, 255, 110)
        border = None if t < 2.6 else (167, 139, 250, 255)
        chip = glass_chip(f"{label}  00:0{secs}", (255, 255, 255), fill, border=border, size=40, tracking=4)
        R.paste_center(im, chip, W / 2, 610 if t >= 2.6 else 640, 1.0, pulse)
        if t >= 2.6:  # breathing final-seconds frame
            a = 0.12 + 0.3 * (0.5 - 0.5 * np.cos(2 * np.pi * (t - 2.6) / 0.9))
            fr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(fr).rectangle((0, 0, W - 1, H - 1), outline=(124, 92, 255, int(255 * a)), width=18)
            im.alpha_composite(fr)
    else:
        chip = glass_chip("HAMMER FALLING", (255, 255, 255), (49, 38, 98, 200), border=(167, 139, 250, 255), size=40, tracking=8)
        R.paste_center(im, chip, W / 2, 610, R.ease_out((t - 5.6) / 0.2))
        s = (t - 5.9) / 0.42
        if s > 0:
            sc = 1.7 - 0.7 * R.stamp(s) if s < 1 else 1.0
            R.paste_center(im, shadow_text("You won it.", 120, (255, 255, 255)), W / 2, 1330, R.clamp(s * 2.5), sc)
    # fade to stage at the end of the scene
    if t > SCENE - 0.35:
        k = R.clamp((t - (SCENE - 0.35)) / 0.35)
        im = Image.blend(im, Image.new("RGBA", (W, H), R.BG + (255,)), k)
    return im.convert("RGB")

def build_audio(path, sr=48000):
    # scene audio
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-t", str(SCENE), "-ac", "1", "-ar", str(sr), "-f", "s16le", "scene.pcm"], check=False)
    try:
        scene = np.frombuffer(open("scene.pcm", "rb").read(), dtype=np.int16).astype(np.float64) / 32768
    except Exception:
        scene = np.zeros(int(SCENE * sr))
    n = int(DUR * sr); out = np.zeros(n)
    out[: min(n, len(scene))] += scene[: n] * 0.9
    out[int((SCENE - 0.35) * sr): int(SCENE * sr)] *= np.linspace(1, 0.1, int(SCENE * sr) - int((SCENE - 0.35) * sr))
    rng = np.random.default_rng(3)
    tt = lambda d: np.arange(int(d * sr)) / sr
    def add(sig, at):
        i = int(at * sr); j = min(n, i + len(sig)); out[i:j] += sig[: j - i]
    for k, at in enumerate([0.0, 1.0, 2.0, 2.6, 3.3, 4.0, 4.5, 5.0]):
        x = tt(0.06)
        add((np.sin(2 * np.pi * 3100 * x) * np.exp(-x * 90) * 0.5 + rng.normal(0, 1, len(x)) * np.exp(-x * 400) * 0.3) * (0.25 + 0.03 * k), at)
    x = tt(0.9)
    add((np.sin(2 * np.pi * 68 * x) * np.exp(-x * 7) + rng.normal(0, 1, len(x)) * np.exp(-x * 120) * 0.4) * 0.6, 5.6)
    x = tt(END)
    env = np.minimum(1, x / 0.35) * np.exp(-np.maximum(0, x - 1.2) * 0.9)
    chord = sum(np.sin(2 * np.pi * f * x) * a for f, a in ((220, .5), (277.18, .35), (329.63, .35), (440, .25)))
    add(chord * env * 0.25, SCENE)
    out[-int(0.25 * sr):] *= np.linspace(1, 0, int(0.25 * sr))
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.8
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(sr); w_.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    if "--still" in sys.argv:
        dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", SRC, "-t", str(SCENE), "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        want = {int(1.2 * FPS), int(3.2 * FPS), int(6.6 * FPS)}
        for i in range(int(SCENE * FPS)):
            raw = dec.stdout.read(W * H * 3)
            if not raw: break
            if i in want:
                overlay(Image.frombytes("RGB", (W, H), raw), i / FPS).save(f"cafe_still_{i}.png")
        R.end_card(11.4 + 2.5).save("cafe_still_end.png"); sys.exit()
    build_audio("cafe_audio.wav")
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", SRC, "-t", str(SCENE), "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "cafe_audio.wav",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    last = None
    for i in range(N):
        t = i / FPS
        if t < SCENE:
            raw = dec.stdout.read(W * H * 3)
            if raw and len(raw) == W * H * 3: last = Image.frombytes("RGB", (W, H), raw)
            frame = overlay(last, t)
        else:
            frame = R.end_card(11.4 + (t - SCENE))
        enc.stdin.write(frame.tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT)
