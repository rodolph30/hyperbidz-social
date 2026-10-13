"""HyperBidz 'The phone that couldn't stay still' — 16:9 Arena clip framed into a 9:16 Reel.
Layout: hook + notifications in the top band, footage in the middle, live bid ticker in the bottom band.
Usage: python3 buzz_edit.py out.mp4 [--stills t,...]"""
import subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/manouche")
import render as R
import mhelpers as M

W, H, FPS, SR = 1080, 1920, 30, 48000
WHITE, BG, NAVY = R.WHITE, R.BG, R.NAVY
OUT = sys.argv[1]
VY0, VH = 340, 1100                      # video band
# output timeline
T = dict(slow=8.3, real=10.1, freeze=10.95, end=12.65)
END = 3.4; TOTAL = T["end"] + END
BIDS = [(5.0, 25), (5.6, 40), (6.2, 55), (6.7, 70), (7.2, 90), (7.6, 110), (8.0, 125), (8.6, 140)]
SHUTTER, TAP, PUTDOWN = 2.2, 2.6, 3.6
ONCE, TWICE, SOLD = 9.0, 9.8, 10.6

def decode(t0, t1):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-i", "src.mp4", "-t", str(t1 - t0), "-vf",
                          "scale=-2:1100:flags=lanczos,crop=1080:1100:(iw*0.45-540):0,fps=30", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    n = len(raw) // (1080 * 1100 * 3); return [Image.frombytes("RGB", (1080, 1100), raw[i * 1080 * 1100 * 3:(i + 1) * 1080 * 1100 * 3]) for i in range(n)]
FR = decode(0, 10.1)                      # source frames at 30 fps
def src_frame(s): return FR[min(len(FR) - 1, max(0, int(round(s * 30))))]

def src_time(t):
    if t < T["slow"]: return t
    if t < T["real"]: return 8.3 + (t - T["slow"]) * 0.5          # slow motion on the catch
    if t < T["freeze"]: return 9.2 + (t - T["real"])
    return 10.05

# ---------- stage ----------
def stage():
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(0, 1, W)[None, :]
    g1 = np.exp(-(((x - 0.5) / 0.6) ** 2 + ((y - 0.02) / 0.12) ** 2)); g2 = np.exp(-(((x - 0.5) / 0.6) ** 2 + ((y - 0.98) / 0.14) ** 2))
    a = np.array(BG)[None, None, :] + np.array([124, 92, 255])[None, None, :] * (0.28 * g1 + 0.22 * g2)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
STAGE = stage()

def shadow(text, size, weight=700, fill=WHITE):
    layer = R.text_layer(text, R.font(size, weight), fill)
    a = layer.getchannel("A").point(lambda v: int(v * 0.6))
    sh = Image.merge("RGBA", (*[Image.new("L", layer.size, 0)] * 3, a)).filter(ImageFilter.GaussianBlur(7))
    out = Image.new("RGBA", (layer.width + 24, layer.height + 24), (0, 0, 0, 0)); out.alpha_composite(sh, (12, 16)); out.alpha_composite(layer, (12, 12)); return out

def app_icon(size):
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.24), fill=255)
    ic = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ic.paste(M.grad(size, size), (0, 0), m)
    z = R.z_mark(int(size * 0.78)); ic.alpha_composite(z, ((size - z.width) // 2, (size - z.height) // 2)); return ic
ICON = app_icon(84)

def notif(title, body):
    w, h = 980, 148; im = M.glass(w, h, 38, fill=(20, 22, 32, 235))
    im.alpha_composite(ICON, (30, (h - 84) // 2))
    im.alpha_composite(R.text_layer("HYPERBIDZ", R.font(24, mono=True), (200, 205, 225), tracking=3), (136, 22))
    now = R.text_layer("now", R.font(26, 500), (176, 178, 181)); im.alpha_composite(now, (w - 36 - now.width, 20))
    im.alpha_composite(R.text_layer(title, R.font(40, 700), WHITE), (136, 54))
    im.alpha_composite(R.text_layer(body, R.font(30, 500), (205, 208, 220)), (136, 102)); return im
NOTIFS = [(at, notif(f"New bid · ${v}", f"Vintage film camera · {i + 2} bidders")) for i, (at, v) in enumerate(BIDS)]

def listed_pill():
    tl = R.text_layer("LISTED  ·  STARTING BID $20", R.font(32, mono=True), WHITE, tracking=3)
    w, h = tl.width + 120, tl.height + 44; im = M.glass(w, h, h // 2, fill=(49, 38, 98, 230), border=(167, 139, 250, 255))
    d = ImageDraw.Draw(im); cx, cy = 44, h // 2
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(167, 139, 250, 255)); d.line([(cx - 8, cy), (cx - 2, cy + 7), (cx + 9, cy - 7)], fill=(255, 255, 255, 255), width=4)
    im.alpha_composite(tl, (80, 22)); return im
LISTED = listed_pill()

def ticker(t):
    cur = [b for b in BIDS if t >= b[0]]
    val = cur[-1][1] if cur else 20; prev = cur[-2][1] if len(cur) > 1 else 20; at = cur[-1][0] if cur else 0
    k = R.ease_out((t - at) / 0.25) if cur else 1; v = int(round(prev + (val - prev) * k))
    lab = R.text_layer(("SOLD FOR" if t >= SOLD else "CURRENT BID") + f"  ·  {len(cur) + 1 if cur else 0} BIDDERS" if t < SOLD else "SOLD FOR", R.font(28, mono=True), (200, 205, 230), tracking=4)
    num = R.text_layer(f"${v}", R.font(112, 700), WHITE)
    pop = 1.0 + 0.1 * (1 - R.clamp((t - at) / 0.2)) if cur else 1.0
    return lab, num, pop

def chip(text, fill, border=None):
    return M.chip(text, fill, border, size=40)

def frame(t):
    if t >= T["end"]: return end_card(t - T["end"])
    im = STAGE.copy()
    fr = src_frame(src_time(t))
    if t >= T["freeze"]:
        k = (t - T["freeze"]) / (T["end"] - T["freeze"]); z = 1.0 + 0.08 * R.ease_out(k)
        w, h = int(1080 / z), int(1100 / z); fr = fr.crop(((1080 - w) // 2, int((1100 - h) * 0.35), (1080 - w) // 2 + w, int((1100 - h) * 0.35) + h)).resize((1080, 1100), Image.BICUBIC)
    im.paste(fr, (0, VY0))
    d = ImageDraw.Draw(im); d.line([(0, VY0), (W, VY0)], fill=(124, 92, 255), width=3); d.line([(0, VY0 + VH), (W, VY0 + VH)], fill=(124, 92, 255), width=3)
    if T["slow"] <= t < T["real"]:  # slow-motion tint + vignette pulse
        ov = Image.new("RGBA", (W, VH), (124, 92, 255, int(28 + 18 * np.sin((t - T["slow"]) * 8)))); im.alpha_composite(ov, (0, VY0))
    # top band: hook lines, then the notification flood, then SOLD
    if t < 3.9:
        a = R.ease_out((t - 0.2) / 0.3) * (1 - R.clamp((t - 3.6) / 0.3))
        R.paste_center(im, shadow("POV: listing your dad's", 60), W / 2, 130, a); R.paste_center(im, shadow("old camera for $20", 60), W / 2, 210, a)
    if 3.9 <= t < 5.0:
        a = R.ease_out((t - 3.9) / 0.3) * (1 - R.clamp((t - 4.75) / 0.25))
        R.paste_center(im, shadow("…then forgetting about it.", 60), W / 2, 170, a)
    if TAP <= t < 4.9:
        k = (t - TAP) / 0.3; R.paste_center(im, LISTED, W / 2, VY0 + 70, R.clamp(k * 3) * (1 - R.clamp((t - 4.6) / 0.3)), 0.85 + 0.15 * R.stamp(k) if k < 1 else 1.0)
    if 5.0 <= t < SOLD:
        shown = [(at, n) for at, n in NOTIFS if t >= at][-2:]
        for i, (at, n) in enumerate(reversed(shown)):
            k = R.clamp((t - at) / 0.28); y = 95 + i * 160 - (1 - R.stamp(k)) * 120 * (1 if i == 0 else 0)
            R.paste_center(im, n, W / 2, y, (R.clamp(k * 2.5) if i == 0 else 0.75))
    if t >= SOLD:
        k = (t - SOLD) / 0.35; sc = 1.8 - 0.8 * R.stamp(k) if k < 1 else 1.0
        R.paste_center(im, M.stamp_text("SOLD.", 150), W / 2, 175, R.clamp(k * 3), sc)
    # bottom band: live bid ticker + countdown chip on the video edge
    if t >= 4.9:
        lab, num, pop = ticker(t); a = R.ease_out((t - 4.9) / 0.3)
        R.paste_center(im, lab, W / 2, VY0 + VH + 70, a); R.paste_center(im, num, W / 2, VY0 + VH + 160, a, pop)
        if t >= SOLD:
            R.paste_center(im, R.text_layer("Started at $20.", R.font(40, 500), (205, 208, 222)), W / 2, VY0 + VH + 255, R.ease_out((t - SOLD - 0.3) / 0.3))
    if 6.2 <= t < SOLD + 0.1:
        if t < ONCE: lab, fill, br = f"ENDS IN  00:0{max(1, int(np.ceil((ONCE - t) / 0.55)))}", (11, 14, 20, 210), (124, 92, 255, 255)
        elif t < TWICE: lab, fill, br = "GOING ONCE…", (124, 92, 255, 170), (167, 139, 250, 255)
        else: lab, fill, br = "GOING TWICE…", (124, 92, 255, 200), (167, 139, 250, 255)
        last = max(x for x in (6.2, ONCE, TWICE) if x <= t); k = (t - last) / 0.25
        R.paste_center(im, chip(lab, fill, br), W / 2, VY0 + VH, R.ease_out((t - 6.2) / 0.25) * (1 - R.clamp((t - SOLD) / 0.1)), 0.88 + 0.12 * R.stamp(k) if k < 1 else 1.0)
    if SOLD <= t < SOLD + 0.1: im = M.flash(im, 0.6 * (1 - (t - SOLD) / 0.1))
    if t > T["end"] - 0.35: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (T["end"] - 0.35)) / 0.35))
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

# ---------- sound ----------
def build_audio(path):
    n = int(TOTAL * SR); out = np.zeros(n); rng = np.random.default_rng(21)
    tt = lambda d: np.arange(int(d * SR)) / SR
    def add(sig, at, g=1.0):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += sig[: j - i] * g
    def lp(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
    def hp(x): return x - lp(x, 10)
    x = tt(T["end"]); add(lp(rng.normal(0, 1, len(x)), 300) * 0.8, 0)                    # room tone
    # calm intro bed (0-5 s): soft plucked arpeggio + pad, so the first seconds aren't silent
    arp = [329.6, 392.0, 493.9, 587.3, 493.9, 392.0]
    for i in range(15):
        at = 0.05 + i * 0.333; f0 = arp[i % 6]; x = tt(0.6)
        add((np.sin(2 * np.pi * f0 * x) + 0.3 * np.sin(4 * np.pi * f0 * x)) * np.exp(-x * 6) * np.minimum(1, x / 0.005), at, 0.32 * (1 - max(0, at - 4.2) / 0.8))
    x = tt(5.0); env = np.minimum(1, x / 0.8) * np.minimum(1, (5.0 - x) / 0.5)
    add(sum(np.sin(2 * np.pi * f * x) for f in (164.8, 196.0, 246.9)) * env * 0.12, 0)
    for dd in (0, 0.07):                                                                    # shutter
        x = tt(0.05); add(hp(rng.normal(0, 1, len(x))) * np.exp(-x * 90), SHUTTER + dd, 0.5)
    x = tt(0.04); add(np.sin(2 * np.pi * 2400 * x) * np.exp(-x * 140), TAP, 0.25)          # tap
    x = tt(0.25); add((np.sin(2 * np.pi * 380 * x) * np.exp(-x * 40) + hp(rng.normal(0, 1, len(x))) * np.exp(-x * 80) * 0.6), PUTDOWN, 0.55)  # phone on table
    def buzz(at, d, g=0.5):  # phone vibrating against wood
        x = tt(d); motor = np.sign(np.sin(2 * np.pi * 165 * x)) * 0.5 + np.sin(2 * np.pi * 165 * x) * 0.5
        rattle = hp(rng.normal(0, 1, len(x))) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 41 * x)))
        env = np.minimum(1, x / 0.02) * np.minimum(1, (d - x) / 0.03)
        add(lp(motor * 0.6 + rattle * 0.35, 3) * env, at, g)
    def ding(at, g=0.18):
        for f0, dd in ((1568, 0), (2093, 0.07)):
            x = tt(0.3); add(np.sin(2 * np.pi * f0 * x) * np.exp(-x * 14), at + dd, g)
    for i, (at, v) in enumerate(BIDS):
        if at < T["slow"]: buzz(at, 0.22 + 0.06 * i, 0.45 + 0.04 * i); ding(at + 0.05)
    buzz(6.75, T["slow"] - 6.75, 0.45)                                                      # continuous rattle as it slides
    # music: pulsing bass that speeds up with the bids
    t0 = 5.0; step = 0.5
    while t0 < T["slow"]:
        x = tt(0.22); add(np.sin(2 * np.pi * np.cumsum(55 + 40 * np.exp(-x * 25)) / SR) * np.exp(-x * 9), t0, 0.55)
        t0 += step; step = max(0.18, step * 0.86)
    # slow motion: low drone + whoosh + heartbeat, then the calls
    x = tt(T["real"] - T["slow"]); add(np.sin(2 * np.pi * 49 * x) * np.minimum(1, x / 0.2) * 0.4 + lp(rng.normal(0, 1, len(x)), 40) * 0.6, T["slow"], 0.6)
    i0 = int(T["slow"] * SR); out[i0:i0 + int(0.06 * SR)] *= 0.3
    for hb in (T["slow"] + 0.2, T["slow"] + 1.0):
        for dd, a in ((0, 1), (0.17, 0.7)):
            x = tt(0.2); add(np.sin(2 * np.pi * 52 * x) * np.exp(-x * 20) * a, hb + dd, 0.7)
    for c in (ONCE, TWICE):
        x = tt(0.08); add(np.sin(2 * np.pi * 1900 * x) * np.exp(-x * 60), c, 0.35)
    ding(8.6, 0.25)
    # SOLD hit
    x = tt(0.9); add(np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-x * 8)) / SR) * np.exp(-x * 4), SOLD, 0.9)
    for i, f0 in enumerate((1318.5, 1661.2, 1975.5, 2637.0)):
        x = tt(1.0); add(np.sin(2 * np.pi * f0 * x) * np.exp(-x * 4), SOLD + 0.05 + 0.06 * i, 0.12)
    x = tt(0.4); add(np.sin(2 * np.pi * 98 * x) * np.exp(-x * 11) * 0.6, T["end"] + 0.02)
    x = tt(END); env = np.minimum(1, x / 0.3) * np.exp(-np.maximum(0, x - 1.6) * 0.8)
    add(sum(np.sin(2 * np.pi * f * x) * a for f, a in ((196, .5), (246.94, .35), (293.66, .35), (392, .22))) * env * 0.3, T["end"] + 0.05)
    out[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR)) ** 1.5
    out = np.tanh(out * 1.3) / np.tanh(1.3); out = out / (np.max(np.abs(out)) + 1e-9) * 0.89
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    if "--stills" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        ims = [frame(t).resize((216, 384)) for t in ts]; s = Image.new("RGB", (216 * len(ims), 384))
        for i, im in enumerate(ims): s.paste(im, (216 * i, 0))
        s.save("stills.jpg", quality=85); print("stills.jpg"); sys.exit()
    build_audio("buzz_audio.wav")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", "buzz_audio.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(round(TOTAL * FPS))): enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT, round(TOTAL, 2))
