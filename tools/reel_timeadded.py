"""Render HyperBidz Reel p006: "The clock saw that." (time added explainer, 1080x1920, 30 fps, 13.5 s, with sound).
Adapted from reel_last10.py (imports its helpers). Run `python3 tools/slides.py` once first so tools/fonts exists.
Usage: python3 tools/reel_timeadded.py out.mp4 [--still]
No amounts are shown: bids appear as pop-ups with a blurred amount; the added time is shown as a refill, never a number."""
import math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_last10 import (W, H, BG, WHITE, MUTED, ACCENT, FEED, BLUE, NAVY, GRAD_BG, font, clamp, ease_out, stamp,
                         mix, z_mark, text_layer, paste_center, pill, wrap_center)

FPS, DUR = 30, 13.5
N = int(FPS * DUR)
GREEN = (0, 163, 100)
END = 10.8

# ---------- timeline ----------
# clock value shown per time window (None = hidden behind TIME ADDED)
CLOCK = [(0.0, 0.9, 3), (0.9, 1.8, 2), (1.8, 2.3, 1), (2.3, 4.0, None), (4.0, 4.9, 2), (4.9, 5.6, 1), (5.6, 6.5, None),
         (6.5, 7.45, 3), (7.45, 8.4, 2), (8.4, 9.35, 1)]
ADDED = [(2.3, 4.0), (5.6, 6.5)]       # windows where the clock refills
BIDS = [(1.95, "YOU", "placed a bid", True), (5.25, "RIVAL", "placed a bid", False)]
HEAD = [(0.0, 2.3, "Last-second bid?", "The clock saw that."), (2.3, 4.0, "A last-second bid", "adds time."),
        (4.0, 6.5, "So everyone gets", "a fair answer."), (6.5, 9.35, "It ends when", "nobody answers.")]

def clock_at(t):
    for a, b, v in CLOCK:
        if a <= t < b: return v, t - a
    return None, 0

def bar_level(t):
    """Fraction of the bar that is full: drains, refills on time added."""
    if t < 2.3: return 0.32 - 0.25 * t / 2.3
    if t < 3.0: return 0.07 + 0.93 * ease_out((t - 2.3) / 0.7)
    if t < 4.0: return 1.0 - 0.06 * (t - 3.0)
    if t < 5.6: return 0.24 - 0.16 * (t - 4.0) / 1.6
    if t < 6.1: return 0.08 + 0.92 * ease_out((t - 5.6) / 0.5)
    if t < 6.5: return 1.0 - 0.05 * (t - 6.1) / 0.4
    if t < 9.35: return 0.3 * (1 - (t - 6.5) / 2.85)
    return 0.0

def bubble(who, what, mine):
    """Bid pop-up: avatar dot, name, action and a blurred amount."""
    w, h = 760, 150
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bg = FEED + (255,) if mine else (22, 26, 36, 235)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=44, fill=bg, outline=(198, 184, 255, 255) if mine else (255, 255, 255, 60), width=3)
    d.ellipse((34, 35, 114, 115), fill=(255, 255, 255, 255) if mine else (60, 66, 82, 255))
    d.text((74, 75), who[0], font=font(40, 700), fill=FEED if mine else WHITE, anchor="mm")
    d.text((140, 30), who, font=font(30, mono=True), fill=WHITE)
    d.text((140, 72), what, font=font(42, 500), fill=WHITE)
    # blurred amount
    amt = Image.new("RGBA", (220, 70), (0, 0, 0, 0)); ad = ImageDraw.Draw(amt)
    ad.text((110, 35), "$ ●●●", font=font(44, 700), fill=WHITE, anchor="mm")
    amt = amt.filter(ImageFilter.GaussianBlur(9))
    im.alpha_composite(amt, (w - 250, 40))
    return im

def stage(t):
    im = Image.new("RGBA", (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    v, dt = clock_at(t)
    added = any(a <= t < b for a, b in ADDED)
    final = v is not None
    # breathing violet frame in the final seconds, green flash on time added
    if final:
        a = 0.10 + 0.28 * (0.5 - 0.5 * math.cos(2 * math.pi * t / 0.9))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((0, 0, W - 1, H - 1), outline=FEED + (int(255 * a),), width=18)
        im.alpha_composite(ov)
    for a0, b0 in ADDED:
        if a0 <= t < a0 + 0.6:
            k = (t - a0) / 0.6
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((0, 0, W - 1, H - 1), outline=GREEN + (int(220 * (1 - k)),), width=18)
            im.alpha_composite(ov)
    # label + clock
    if final:
        label = "GOING ONCE…" if v == 3 else "GOING TWICE…"
        pulse = 1 + 0.04 * max(0.0, 1 - dt / 0.3)
        paste_center(im, text_layer(label, font(40, mono=True), ACCENT, tracking=8), W / 2, 520, 1.0, pulse)
        paste_center(im, text_layer(f"00:{v:02d}", font(250, 700), ACCENT, features=["tnum"]), W / 2, 720, 1.0, pulse)
    elif added:
        a0 = max(a for a, b in ADDED if a <= t)
        s = (t - a0) / 0.42
        sc = 1.6 - 0.6 * stamp(s) if s < 1 else 1.0
        chip = pill("+ TIME ADDED", font(64, mono=True), WHITE, GREEN, pad=(60, 34), tracking=8)
        paste_center(im, chip, W / 2, 700, clamp(s * 3), sc)
    # bar
    x0, x1, y = 140, 940, 920
    d.rounded_rectangle((x0, y, x1, y + 10), radius=5, fill=(35, 38, 47))
    fw = int((x1 - x0) * clamp(bar_level(t)))
    if fw > 10:
        cols = [mix(GREEN, (0, 200, 130), i / max(1, fw - 1)) for i in range(fw)] if added else [mix(BLUE, FEED, i / max(1, fw - 1)) for i in range(fw)]
        gh = Image.fromarray(np.array([cols] * 10, dtype=np.uint8), "RGB").convert("RGBA")
        m = Image.new("L", (fw, 10), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw - 1, 9), radius=5, fill=255)
        im.paste(gh, (x0, y), m)
    # headline: first line white, second violet
    for a0, a1, l1, l2 in HEAD:
        if a0 <= t < a1:
            k_in = 1.0 if a0 == 0.0 else ease_out((t - a0) / 0.25); k_out = 1 - clamp((t - (a1 - 0.15)) / 0.15)
            wrap_center(im, l1, font(92, 700), WHITE, 1080, alpha=k_in * k_out, dy=(1 - k_in) * 30, max_w=1010)
            k2 = ease_out((t - a0 - 0.5) / 0.25) if a0 == 0.0 else k_in
            wrap_center(im, l2, font(92, 700), ACCENT, 1185, alpha=k2 * k_out, dy=(1 - k2) * 30, max_w=1010)
    # bid pop-ups
    for tb, who, what, mine in BIDS:
        if tb <= t < tb + 1.6:
            k = (t - tb) / 0.35
            sc = stamp(k) if k < 1 else 1.0
            out = clamp((t - (tb + 1.35)) / 0.25)
            paste_center(im, bubble(who, what, mine), W / 2, 1420, clamp(k * 3) * (1 - out), max(0.01, sc))
    return im

def hammer(t):
    im = Image.new("RGBA", (W, H), BG + (255,))
    k = t - 9.35
    chip = pill("HAMMER FALLING", font(52, mono=True), WHITE, (49, 38, 98), border=ACCENT, tracking=10, pad=(56, 30))
    paste_center(im, chip, W / 2, 700, ease_out(k / 0.2))
    wrap_center(im, "Nobody answered.", font(96, 700), WHITE, 950, max_w=1010, alpha=ease_out((k - 0.1) / 0.25))
    if t >= 9.85:
        s = (t - 9.85) / 0.42
        sc = 1.7 - 0.7 * stamp(s) if s < 1 else 1.0
        paste_center(im, text_layer("Highest bid wins.", font(96, 700), ACCENT), W / 2, 1075, clamp(s * 2.5), sc)
    return im

def end_card(t):
    k = t - END
    im = GRAD_BG.copy()
    if k < 0.3:
        im = Image.blend(Image.new("RGBA", (W, H), BG + (255,)), im, ease_out(k / 0.3))
    s = k / 0.42
    sc = 1.6 - 0.6 * stamp(s) if s < 1 else 1.0
    paste_center(im, z_mark(280), W / 2, 560, clamp(s * 3), sc)
    a = ease_out((k - 0.35) / 0.3)
    hy, bz = text_layer("HYPER", font(78, 500), (215, 225, 255), tracking=8), text_layer("BIDZ", font(78, 700), WHITE, tracking=8)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0))
    wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    paste_center(im, wm, W / 2, 790, a, 1 + (1 - a) * 0.04)
    wrap_center(im, "The clock plays fair.", font(84, 700), WHITE, 960, alpha=ease_out((k - 0.6) / 0.3), max_w=900)
    wrap_center(im, "Live auctions for Lebanon. Coming soon.", font(54, 500), (235, 238, 255), 1090, alpha=ease_out((k - 0.9) / 0.3), max_w=860, line_h=1.15)
    b = ease_out((k - 1.2) / 0.3)
    paste_center(im, pill("Follow @hyperbidz", font(54, 700), NAVY, WHITE, pad=(56, 30)), W / 2, 1290, b, 0.94 + 0.06 * b)
    return im

def frame(t):
    if t >= END: return end_card(t).convert("RGB")
    if t >= 9.35: return hammer(t).convert("RGB")
    return stage(t).convert("RGB")

# ---------- audio ----------
def audio(path, sr=48000):
    n = int(sr * DUR); out = np.zeros(n); rng = np.random.default_rng(11)
    def add(sig, at):
        i = int(at * sr); j = min(n, i + len(sig)); out[i:j] += sig[: j - i]
    tt = lambda dur: np.arange(int(dur * sr)) / sr
    def tick(vol, hz=3300):
        x = tt(0.06); return (np.sin(2 * np.pi * hz * x) * np.exp(-x * 90) * 0.6 + rng.normal(0, 1, len(x)) * np.exp(-x * 400) * 0.4) * vol
    # ticks on every clock change and half-tocks
    for a, b, v in CLOCK:
        if v is not None:
            add(tick(0.5), a); add(tick(0.22, 2900), a + 0.45)
    # bid pops: short bright blip
    for tb, *_ in BIDS:
        x = tt(0.18); add(np.sin(2 * np.pi * (880 + 600 * x / 0.18) * x) * np.exp(-x * 18) * 0.45, tb)
    # time added: rising sweep + chime
    for a0, b0 in ADDED:
        x = tt(0.5); sweep = np.sin(2 * np.pi * (300 * x + 900 * x * x)) * np.minimum(1, x / 0.05) * np.exp(-x * 4) * 0.35
        add(sweep, a0)
        x = tt(0.9); add(sum(np.sin(2 * np.pi * f_ * x) * a_ for f_, a_ in ((659.25, .4), (987.77, .3), (1318.5, .15))) * np.exp(-x * 4) * 0.35, a0 + 0.12)
    # heartbeat through the final run 6.5 -> 9.35
    tb = 6.5
    while tb < 9.3:
        bpm = 100 + 50 * (tb - 6.5) / 2.85
        for off, amp in ((0, 0.9), (0.15, 0.6)):
            x = tt(0.18); add(np.sin(2 * np.pi * (52 + 30 * np.exp(-x * 30)) * x) * np.exp(-x * 22) * amp * 0.55, tb + off)
        tb += 60 / bpm
    x = tt(2.8); noise = np.convolve(rng.normal(0, 1, len(x)), np.ones(40) / 40, mode="same")
    add(noise * (x / 2.8) ** 2.2 * 0.5, 6.55)
    out[int(9.35 * sr):] = 0
    x = tt(0.9)
    add(np.sin(2 * np.pi * 68 * x) * np.exp(-x * 7) + np.sin(2 * np.pi * 180 * x) * np.exp(-x * 25) * 0.4 + rng.normal(0, 1, len(x)) * np.exp(-x * 120) * 0.5, 9.85)
    x = tt(0.4); add(np.sin(2 * np.pi * 110 * x) * np.exp(-x * 12) * 0.5, END)
    x = tt(2.7); env = np.minimum(1, x / 0.35) * np.exp(-np.maximum(0, x - 1.2) * 0.9)
    add(sum(np.sin(2 * np.pi * f_ * x) * a_ for f_, a_ in ((220, .5), (277.18, .35), (329.63, .35), (440, .25), (554.37, .12))) * env * 0.3, END)
    out[-int(0.25 * sr):] *= np.linspace(1, 0, int(0.25 * sr))
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.7
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(sr); w_.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    OUT = [a for a in sys.argv[1:] if not a.startswith("--")][0] if len(sys.argv) > 1 else "reel.mp4"
    if "--still" in sys.argv:
        for ts in (1.2, 2.2, 2.8, 5.4, 6.0, 7.0, 8.6, 10.2, 12.8):
            frame(ts).save(os.path.join(os.path.dirname(OUT) or ".", f"still_{ts:04.1f}.png"))
        sys.exit()
    wav = OUT + ".wav"; audio(wav)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(N):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", OUT)
