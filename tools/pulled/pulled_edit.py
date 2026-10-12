"""HyperBidz "Pulled In" Reel editor (Karim series).
Usage: python3 pulled_edit.py cfg.json out.mp4 [--stills]
Timeline: A = shot 1 (notification, double-take, pulled into the phone)
          B = shot 2 (auction hall: live bids, Going once/twice, gavel)
          C = end of shot 1 (portal clears, he's back on the couch, "You won it." notification, hold)
          then the HyperBidz end card.
All cue times in cfg are seconds inside each segment (0 = segment start).
Needs render.py (brand helpers) and fonts/ next to it."""
import json, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R

W, H, FPS, SR = 1080, 1920, 30, 48000
cfg = json.load(open(sys.argv[1])); OUT = sys.argv[2]
STILLS = "--stills" in sys.argv
SEG = cfg["segments"]
for s in SEG:
    s["len"] = s["out"] - s["in"] + s.get("hold", 0)
END = cfg.get("end_len", 3.6)
starts, t = [], 0.0
for s in SEG:
    starts.append(t); t += s["len"]
END_AT = t; TOTAL = t + END
N = int(round(TOTAL * FPS))
WHITE, BG, BLUE, FEED, ACCENT, NAVY = R.WHITE, R.BG, R.BLUE, R.FEED, R.ACCENT, R.NAVY

# ---------- overlay pieces ----------
def grad(w, h):
    return R.diag_gradient(w, h, BLUE, FEED).convert("RGBA")

def app_icon(size):
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.24), fill=255)
    ic = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ic.paste(grad(size, size), (0, 0), m)
    z = R.z_mark(int(size * 0.78)); ic.alpha_composite(z, ((size - z.width) // 2, (size - z.height) // 2))
    return ic

def glass(w, h, r, fill=(20, 22, 32, 222), border=(255, 255, 255, 34)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=fill, outline=border, width=2)
    return im

def notification(title, body):
    w, h = 960, 196
    im = glass(w, h, 46)
    im.alpha_composite(app_icon(104), (36, (h - 104) // 2))
    x = 164
    im.alpha_composite(R.text_layer("HYPERBIDZ", R.font(26, mono=True), (200, 205, 225), tracking=3), (x, 34))
    now = R.text_layer("now", R.font(28, 500), (176, 178, 181)); im.alpha_composite(now, (w - 40 - now.width, 32))
    im.alpha_composite(R.text_layer(title, R.font(42, 700), WHITE), (x, 74))
    im.alpha_composite(R.text_layer(body, R.font(34, 500), (205, 208, 220)), (x, 128))
    return im

def bid_row(handle, amount, mine=False):
    f1, f2 = R.font(36, 500), R.font(42, 700)
    hl = R.text_layer(handle, f1, WHITE if mine else (200, 204, 218))
    am = R.text_layer(f"${amount:,}", f2, WHITE)
    w = 40 + 64 + 22 + hl.width + 26 + am.width + 40; h = 100
    if mine:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=50, fill=255)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(grad(w, h), (0, 0), m)
    else:
        im = glass(w, h, 50, fill=(11, 14, 20, 175))
    d = ImageDraw.Draw(im)
    av = (24, 18, 24 + 64, 18 + 64)
    d.ellipse(av, fill=(255, 255, 255, 255) if mine else (124, 92, 255, 255))
    ini = R.text_layer(handle[0].upper(), R.font(34, 700), NAVY if mine else WHITE)
    im.alpha_composite(ini, (24 + 32 - ini.width // 2, 18 + 32 - ini.height // 2 - 2))
    im.alpha_composite(hl, (24 + 64 + 22, (h - hl.height) // 2))
    im.alpha_composite(am, (24 + 64 + 22 + hl.width + 26, (h - am.height) // 2 - 1))
    return im

def chip(text, fill, border=None, size=38, tracking=5):
    tl = R.text_layer(text, R.font(size, mono=True), WHITE, tracking=tracking)
    w, h = tl.width + 76, tl.height + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=fill, outline=border, width=3 if border else 0)
    im.alpha_composite(tl, (38, 20)); return im

def live_chip(viewers, t):
    tl = R.text_layer(f"LIVE  ·  {viewers} watching", R.font(28, mono=True), WHITE, tracking=2)
    w, h = tl.width + 86, tl.height + 30
    im = glass(w, h, h // 2, fill=(11, 14, 20, 170))
    d = ImageDraw.Draw(im); a = int(160 + 95 * (0.5 + 0.5 * np.sin(t * 6)))
    d.ellipse((26, h // 2 - 10, 46, h // 2 + 10), fill=(167, 139, 250, a))
    im.alpha_composite(tl, (60, 15)); return im

def stamp_text(text, size):
    layer = R.text_layer(text, R.font(size, 700), WHITE)
    sh = layer.copy(); sh.putalpha(sh.getchannel("A").point(lambda v: int(v * 0.55)))
    sh = Image.merge("RGBA", (*[Image.new("L", sh.size, 0)] * 3, sh.getchannel("A"))).filter(ImageFilter.GaussianBlur(8))
    out = Image.new("RGBA", (layer.width + 30, layer.height + 30), (0, 0, 0, 0))
    out.alpha_composite(sh, (15, 20)); out.alpha_composite(layer, (15, 15)); return out

def scrim(im, top=True, hgt=520, a0=140):
    s = Image.new("RGBA", (W, hgt), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    for y in range(hgt):
        d.line([(0, y), (W, y)], fill=(11, 14, 20, int(a0 * (1 - y / hgt) ** 1.6)))
    im.alpha_composite(s if top else s.transpose(Image.FLIP_TOP_BOTTOM), (0, 0 if top else H - hgt))

def flash(im, k, color=(220, 225, 255)):
    if k <= 0: return im
    return Image.blend(im, Image.new("RGBA", (W, H), color + (255,)), R.clamp(k))

def blur_box(im, x0, y0, x1, y1, dark=0.35, r=26):
    bx = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
    pad = 40; ex = (max(0, bx[0] - pad), max(0, bx[1] - pad), min(W, bx[2] + pad), min(H, bx[3] + pad))
    reg = im.crop(ex); bl = reg.filter(ImageFilter.GaussianBlur(r))
    if dark: bl = Image.blend(bl, Image.new("RGBA", bl.size, BG + (255,)), dark)
    m = Image.new("L", reg.size, 0)
    ImageDraw.Draw(m).rectangle((bx[0] - ex[0], bx[1] - ex[1], bx[2] - ex[0], bx[3] - ex[1]), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(14))
    reg.paste(bl, (0, 0), m); im.paste(reg, ex[:2]); return im

def zoom(img, s, cx, cy):
    if s <= 1.001: return img
    w, h = W / s, H / s
    l = cx - cx / s; tp = cy - cy / s
    return img.crop((int(l), int(tp), int(l + w), int(tp + h))).resize((W, H), Image.BILINEAR)

def slide_in(t, at, dur=0.38):
    """y-offset factor (1 = hidden above, 0 = in place) with a soft overshoot."""
    k = (t - at) / dur
    if k <= 0: return 1.0
    return 1 - R.stamp(k) if k < 1 else 0.0

NOTIF1 = notification(cfg["notif1"]["title"], cfg["notif1"]["body"])
NOTIF2 = notification(cfg["notif2"]["title"], cfg["notif2"]["body"])
B = cfg["B"]
BIDS = [(b[0], bid_row(b[1], b[2], b[1] == B.get("hero", "Karim"))) for b in B["bids"]]

# ---------- per-segment overlays ----------
def seg_A(base, t, s):
    c = s["cues"]; im = base.convert("RGBA")
    z0, z1 = c["zoom"]
    if t > z0:  # pulled toward the phone: accelerating zoom + radial smear + light
        k = R.clamp((t - z0) / (z1 - z0)); e = k ** 2.2
        sc = 1 + 2.6 * e
        path = c["zoom_path"]; ts = [p[0] for p in path]
        cx, cy = np.interp(t, ts, [p[1] for p in path]) * W, np.interp(t, ts, [p[2] for p in path]) * H
        if k > 0.05:  # radial smear: average of slightly smaller zooms
            acc = np.zeros((H, W, 3))
            for f in (1.0, 0.975, 0.95, 0.925):
                acc += np.asarray(zoom(im, max(1.0, sc * f), cx, cy).convert("RGB"), dtype=np.float64)
            im = Image.fromarray((acc / 4).astype(np.uint8)).convert("RGBA")
        else:
            im = zoom(im, sc, cx, cy)
        im = flash(im, (k - 0.6) / 0.4 * 0.97, (238, 240, 255))
    scrim(im, True, 460, 120)
    n = c["notif"]; out_t = z0 + 0.05
    if n <= t < out_t + 0.3:
        y = 230 - slide_in(t, n) * 330
        a = 1.0 if t < out_t else 1 - R.clamp((t - out_t) / 0.25)
        sc = 1.0 if t < out_t else 1 - 0.3 * R.clamp((t - out_t) / 0.25)
        R.paste_center(im, NOTIF1, W / 2, y + NOTIF1.height / 2, a, sc)
    return im

def seg_B(base, t, s):
    c = s["cues"]; im = base.convert("RGBA")
    for mk in B.get("masks", []):  # hide AI-garbled screen text
        if mk[0] <= t < mk[1]: im = blur_box(im, *mk[2:])
    scrim(im, True, 420, 110); scrim(im, False, 700, 170)
    c0_ = c.get("countdown", c["going_once"] - 1.4)
    if t > 0.3:
        la = R.ease_out((t - 0.3) / 0.3) * (1 - R.clamp((t - c0_ + 0.2) / 0.2))
        lc = live_chip(B.get("viewers", 214), t); R.paste_center(im, lc, 80 + lc.width / 2, 260, la)
    # bid feed, bottom-left, newest at the bottom, max 4 visible
    shown = [(at, row) for at, row in BIDS if t >= at][-B.get("feed_rows", 4):]
    y = B.get("feed_y", 1460)
    for i, (at, row) in enumerate(reversed(shown)):
        k = R.clamp((t - at) / 0.32); pop = 0.8 + 0.2 * R.stamp(k) if k < 1 else 1.0
        a = R.ease_out(k) * (1 - 0.28 * i)
        R.paste_center(im, row, 60 + row.width / 2, y, a, pop)
        y -= 118
    # countdown chip, top centre
    g1, g2, gv = c["going_once"], c["going_twice"], c["gavel"]
    hm = c.get("hammer", gv - 0.25); c0 = c.get("countdown", g1 - 1.4)
    if c0 <= t < gv + 0.2:
        if t < g1: lab, fill, br = f"ENDS IN  00:0{max(1, int(np.ceil(gv - t)))}", (11, 14, 20, 175), None
        elif t < g2: lab, fill, br = "GOING ONCE…", (124, 92, 255, 120), (167, 139, 250, 255)
        elif t < hm: lab, fill, br = "GOING TWICE…", (124, 92, 255, 150), (167, 139, 250, 255)
        else: lab, fill, br = "HAMMER FALLING", (49, 38, 98, 215), (167, 139, 250, 255)
        last = max(x for x in (c0, g1, g2, hm) if x <= t)
        k = (t - last) / 0.3; sc = 0.9 + 0.1 * R.stamp(k) if k < 1 else 1.0
        a = R.ease_out((t - c0) / 0.25) * (1 - R.clamp((t - gv) / 0.12))
        R.paste_center(im, chip(lab, fill, br), c.get("chip_x", W / 2), 262, a, sc)
        if g1 <= t:  # breathing final-seconds frame
            a = 0.15 + 0.35 * (0.5 - 0.5 * np.cos(2 * np.pi * (t - g1) / 0.8))
            fr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(fr).rectangle((0, 0, W - 1, H - 1), outline=(124, 92, 255, int(255 * a)), width=16)
            im.alpha_composite(fr)
    if t >= gv:  # SOLD stamp
        k = (t - gv) / 0.4; sc = 1.7 - 0.7 * R.stamp(k) if k < 1 else 1.0
        R.paste_center(im, stamp_text("SOLD.", 150), W / 2, c.get("sold_y", 440), R.clamp(k * 3), sc)
    fi = c.get("flash_in", 0.4)
    if t < fi: im = flash(im, 1 - t / fi)            # arriving out of the light
    tail = s["len"] - t
    if tail < 0.25: im = flash(im, 1 - tail / 0.25)  # leaving into the light
    return im

def seg_C(base, t, s):
    c = s["cues"]; im = base.convert("RGBA")
    hold_from = s["out"] - s["in"]
    if t > hold_from:  # frozen frame, slow push-in
        im = zoom(im, 1 + 0.05 * R.ease_out((t - hold_from) / s.get("hold", 1)), W * 0.5, H * 0.45)
    scrim(im, True, 460, 120)
    n = c["notif"]
    if t >= n:
        y = 230 - slide_in(t, n) * 330
        R.paste_center(im, NOTIF2, W / 2, y + NOTIF2.height / 2, 1.0)
    if t < 0.2: im = flash(im, 1 - t / 0.2)
    tail = s["len"] - t
    if tail < 0.3: im = Image.blend(im, Image.new("RGBA", (W, H), BG + (255,)), 1 - tail / 0.3)
    return im

FN = {"A": seg_A, "B": seg_B, "C": seg_C}

def end_card(k):
    im = R.GRAD_BG.copy(); s = k / 0.42
    sc = 1.6 - 0.6 * R.stamp(s) if s < 1 else 1.0
    R.paste_center(im, R.z_mark(190), W / 2, 500, R.clamp(s * 3), sc)
    fs = 104
    while max(R.font(fs, 700).getlength(l) for l in cfg["end_lines"]) > 930: fs -= 2
    for i, line in enumerate(cfg["end_lines"]):
        a = R.ease_out((k - 0.35 - i * 0.22) / 0.3)
        R.paste_center(im, R.text_layer(line, R.font(fs, 700), WHITE), W / 2, 760 + i * int(fs * 1.18) + (1 - a) * 20, a)
    b = R.ease_out((k - 1.25) / 0.35)
    hy, bz = R.text_layer("HYPER", R.font(54, 500), (215, 225, 255), tracking=6), R.text_layer("BIDZ", R.font(54, 700), WHITE, tracking=6)
    wm = Image.new("RGBA", (hy.width + bz.width, max(hy.height, bz.height)), (0, 0, 0, 0))
    wm.alpha_composite(hy, (0, 0)); wm.alpha_composite(bz, (hy.width, 0))
    R.paste_center(im, wm, W / 2, 1110, b)
    R.wrap_center(im, "Live auctions for Lebanon. Coming soon.", R.font(46, 500), WHITE, 1195, alpha=b, max_w=900)
    cc = R.ease_out((k - 1.65) / 0.35)
    R.paste_center(im, R.pill("Follow @hyperbidz", R.font(50, 700), NAVY, WHITE, pad=(52, 28)), W / 2, 1350, cc, 0.94 + 0.06 * cc)
    return im

# ---------- video ----------
def decode(s):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(s["in"]), "-i", s["src"], "-t", str(s["out"] - s["in"]), "-vf",
                          f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    return p

def frames():
    for s, st in zip(SEG, starts):
        dec = decode(s); last = None; n = int(round(s["len"] * FPS))
        for i in range(n):
            raw = dec.stdout.read(W * H * 3) if i < int((s["out"] - s["in"]) * FPS) else None
            if raw and len(raw) == W * H * 3: last = Image.frombytes("RGB", (W, H), raw)
            yield st + i / FPS, FN[s["tag"]](last, i / FPS, s).convert("RGB")
        dec.kill()
    for i in range(int(round(END * FPS))):
        yield END_AT + i / FPS, end_card(i / FPS).convert("RGB")

# ---------- audio ----------
def build_audio(path):
    n = int(TOTAL * SR); out = np.zeros(n); rng = np.random.default_rng(7)
    tt = lambda d: np.arange(int(d * SR)) / SR
    def add(sig, at, g=1.0):
        i = int(at * SR); j = min(n, i + len(sig)); out[i:j] += sig[: j - i] * g
    def lp(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
    for s, st in zip(SEG, starts):  # scene audio from the clips
        r = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(s["in"]), "-i", s["src"], "-t", str(s["out"] - s["in"]), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True)
        a = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float64) / 32768
        if len(a):
            a = a * np.minimum(1, np.arange(len(a)) / (0.03 * SR))
            mu = s.get("mute_until")
            if mu:
                i = int(mu * SR); a[:i] = 0; f = min(len(a) - i, int(0.08 * SR)); a[i:i + f] *= np.linspace(0, 1, f)
            add(a, st, s.get("gain", 0.8))
    def ding(at, g=0.35):  # notification: two soft bell tones
        for f0, d in ((1318.5, 0), (1975.5, 0.11)):
            x = tt(0.5); add((np.sin(2 * np.pi * f0 * x) + 0.3 * np.sin(4 * np.pi * f0 * x)) * np.exp(-x * 9), at + d, g)
    def whoosh(at, dur, g=0.8, up=True):
        x = tt(dur); k = x / dur
        env = (k ** 2 if up else (1 - k) ** 2) * np.minimum(1, (1 - k) * 12 if up else k * 12)
        add(lp(rng.normal(0, 1, len(x)), 6) * env, at, g)
    def tick(at, g=0.18, f0=2600):
        x = tt(0.05); add(np.sin(2 * np.pi * f0 * x) * np.exp(-x * 120), at, g)
    def boom(at, g=0.7):
        x = tt(0.7); add(np.sin(2 * np.pi * 52 * x) * np.exp(-x * 6) + lp(rng.normal(0, 1, len(x)), 30) * np.exp(-x * 9) * 0.6, at, g)
    A, Bs, C = SEG[0], SEG[1], SEG[2]; a0, b0, c0 = starts
    def bandnoise(d, lo, hi):
        x = rng.normal(0, 1, int(d * SR)); F = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
        F[(fr < lo) | (fr > hi)] = 0; return np.fft.irfft(F, len(x))
    mu = Bs.get("mute_until")
    if mu:  # crowd murmur: many band-limited "voices" with syllable-rate envelopes, no words
        d = mu + 0.3; m = np.zeros(int(d * SR))
        for v in range(14):
            env = lp(np.abs(rng.normal(0, 1, len(m))), int(SR / rng.uniform(3.5, 7))) ** 1.5
            m += bandnoise(d, rng.uniform(250, 450), rng.uniform(1800, 3200)) * env * rng.uniform(0.5, 1.0)
        m = m / (np.max(np.abs(m)) + 1e-9)
        k = np.arange(len(m)) / SR; m *= np.minimum(1, k / 0.4) * (1 - np.clip((k - mu) / 0.3, 0, 1))
        add(lp(m, 3) * (0.11 + 0.07 * k / d), b0, 1.0)
        # tension pulse that speeds up toward the gavel
        gv = Bs["cues"]["gavel"]; tp = Bs["cues"].get("countdown", 4.0)
        while tp < gv - 0.1:
            x = tt(0.18); add(np.sin(2 * np.pi * 58 * x) * np.exp(-x * 22), b0 + tp, 0.55)
            tp += max(0.22, 0.55 * (gv - tp) / 2.2)
    ding(a0 + A["cues"]["notif"])
    z0, z1 = A["cues"]["zoom"]; whoosh(a0 + z0 - 0.2, z1 - z0 + 0.25, 1.0); boom(b0 - 0.02, 0.6)
    for at, _, _ in B["bids"]: tick(b0 + at)
    hero = [b for b in B["bids"] if b[1] == B.get("hero", "Karim")]
    if hero: tick(b0 + hero[0][0], 0.3, 3300)
    for k in ("going_once", "going_twice"): tick(b0 + Bs["cues"][k], 0.25, 1900)
    boom(b0 + Bs["cues"]["gavel"], 0.5)
    whoosh(c0 - 0.35, 0.6, 0.7); whoosh(c0, 0.8, 0.5, up=False)
    ding(c0 + C["cues"]["notif"], 0.45)
    out[int((END_AT - 0.05) * SR):] *= 0.0
    x = tt(0.4); add(np.sin(2 * np.pi * 98 * x) * np.exp(-x * 11) * 0.6, END_AT + 0.02)
    x = tt(END); env = np.minimum(1, x / 0.3) * np.exp(-np.maximum(0, x - 1.6) * 0.8)
    add(sum(np.sin(2 * np.pi * f * x) * a for f, a in ((196, .5), (246.94, .35), (293.66, .35), (392, .22))) * env * 0.3, END_AT + 0.05)
    out[-int(0.25 * SR):] *= np.linspace(1, 0, int(0.25 * SR))
    out = np.tanh(out * 1.4) / np.tanh(1.4); out = out / (np.max(np.abs(out)) + 1e-9) * 0.89
    with wave.open(path, "wb") as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    if STILLS:
        want = cfg.get("still_times", [])
        got = []
        for t, fr in frames():
            if any(abs(t - w) < 0.5 / FPS for w in want): got.append(fr.resize(tuple(cfg.get("still_size", [270, 480]))))
            if len(got) == len(want): break
        sheet = Image.new("RGB", (got[0].width * len(got) + 0, got[0].height))
        for i, g in enumerate(got): sheet.paste(g, (g.width * i, 0))
        sheet.save("stills.jpg", quality=85); print("stills.jpg", len(got)); sys.exit()
    build_audio("pulled_audio.wav")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", "pulled_audio.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for t, fr in frames(): enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait(); print("done", OUT, round(TOTAL, 2), "s")
