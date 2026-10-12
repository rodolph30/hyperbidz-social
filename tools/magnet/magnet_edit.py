"""Edit for the silent "magnet" Reel: keep the footage untouched (genuine phone look), add sound design
and the HyperBidz end card.
Usage: python3 magnet_edit.py scene.mp4 out.mp4 cues.json [--still]
cues.json: {"press": 4.6, "slide": 5.6, "cut": 9.9}
  press = moment the remote button is pressed (click + hum start)
  slide = moment people start sliding in (whooshes + scrapes)
  cut   = where the footage ends and the end card begins
Needs render.py (brand helpers) and fonts/ next to it."""
import json, subprocess, sys, wave
import numpy as np
from PIL import Image
import render as R

args = [a for a in sys.argv[1:] if not a.startswith("--")]
SRC, OUT = args[0], args[1]
C = json.load(open(args[2]))
W, H, FPS, SR = 1080, 1920, 30, 48000
CUT = C["cut"]
END = 3.8
TOTAL = CUT + END
N = int(round(TOTAL * FPS))

TITLE = ["List it.", "Watch buyers", "get pulled in."]

def end_card(k):
    im = R.GRAD_BG.copy()
    s = k / 0.42
    sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, R.z_mark(190), W / 2, 470, R.clamp(s * 3), sc)
    for i, line in enumerate(TITLE):
        a = R.ease_out((k - 0.35 - i * 0.18) / 0.3)
        R.paste_center(im, R.text_layer(line, R.font(112, 700), (255, 255, 255)), W / 2, 720 + i * 122 + (1 - a) * 20, a)
    b = R.ease_out((k - 1.2) / 0.35)
    f1, f2 = R.font(54, 500), R.font(54, 700)
    hy, bz = R.text_layer("HYPER", f1, (215, 225, 255), tracking=6), R.text_layer("BIDZ", f2, (255, 255, 255), tracking=6)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0))
    wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    R.paste_center(im, wm, W / 2, 1150, b)
    R.wrap_center(im, "Live auctions for Lebanon. Coming soon.", R.font(46, 500), (255, 255, 255), 1235, alpha=b, max_w=900)
    c = R.ease_out((k - 1.6) / 0.35)
    R.paste_center(im, R.pill("Follow @hyperbidz", R.font(50, 700), R.NAVY, (255, 255, 255), pad=(52, 28)), W / 2, 1390, c, 0.94 + 0.06 * c)
    return im

def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")

def build_audio(path):
    n = int(TOTAL * SR); out = np.zeros(n); rng = np.random.default_rng(11)
    tt = lambda d: np.arange(int(d * SR)) / SR
    def add(sig, at):
        i = int(at * SR); j = min(n, i + len(sig)); out[i:j] += sig[: j - i]
    # garage room tone
    x = tt(CUT)
    add(lowpass(rng.normal(0, 1, len(x)), 300) * 2.2, 0)
    # remote click
    x = tt(0.03); add((rng.normal(0, 1, len(x)) * np.exp(-x * 300)) * 0.5, C["press"])
    x = tt(0.02); add((rng.normal(0, 1, len(x)) * np.exp(-x * 400)) * 0.35, C["press"] + 0.07)
    # magnet hum: swells in, steady with slight wobble, until the cut
    d = CUT - C["press"] - 0.1
    x = tt(d)
    swell = np.minimum(1, x / 0.6) ** 1.5
    wob = 1 + 0.06 * np.sin(2 * np.pi * 3.1 * x)
    hum = (np.sin(2 * np.pi * 55 * x) * 1.0 + np.sin(2 * np.pi * 110 * x) * 0.55 + np.sin(2 * np.pi * 165 * x) * 0.3 + np.sin(2 * np.pi * 220 * x) * 0.12)
    buzz = np.sign(np.sin(2 * np.pi * 110 * x)) * 0.05
    add((hum + buzz) * swell * wob * 0.32, C["press"] + 0.1)
    # three bodies sliding in: whoosh + concrete scrape, staggered
    for i in range(3):
        at = C["slide"] + i * 0.35
        x = tt(1.1)
        env = np.sin(np.pi * np.minimum(1, x / 1.1)) ** 2
        whoosh = lowpass(rng.normal(0, 1, len(x)), 18) * env * 1.6
        scrape = lowpass(rng.normal(0, 1, len(x)), 4) * env * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * x)) * 0.9
        add((whoosh + scrape) * 0.55, at)
        x = tt(0.25); add(np.sin(2 * np.pi * 80 * x) * np.exp(-x * 25) * 0.6, at + 1.0)  # bump into the bike
    # hard cut to silence, then end-card stamp + warm chord
    out[int(CUT * SR):] = 0
    x = tt(0.4); add(np.sin(2 * np.pi * 98 * x) * np.exp(-x * 11) * 0.7, CUT + 0.02)
    x = tt(END)
    env = np.minimum(1, x / 0.3) * np.exp(-np.maximum(0, x - 1.6) * 0.8)
    add(sum(np.sin(2 * np.pi * f * x) * a for f, a in ((196, .5), (246.94, .35), (293.66, .35), (392, .22))) * env * 0.3, CUT + 0.05)
    out[-int(0.25 * SR):] *= np.linspace(1, 0, int(0.25 * SR))
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.85
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    if "--still" in sys.argv:
        end_card(2.6).convert("RGB").resize((360, 640)).save("end_still.jpg", quality=85); sys.exit()
    build_audio("magnet_audio.wav")
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", SRC, "-t", str(CUT), "-vf",
                            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", "magnet_audio.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    last = None
    for k in range(N):
        t = k / FPS
        if t < CUT:
            raw = dec.stdout.read(W * H * 3)
            if raw and len(raw) == W * H * 3: last = raw
            enc.stdin.write(last)
        else:
            enc.stdin.write(end_card(t - CUT).convert("RGB").tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT)
