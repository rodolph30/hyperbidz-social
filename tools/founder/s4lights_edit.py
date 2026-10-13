"""Season 4 'Lights on' (warehouse, dark classic coupé). It opens in total darkness; a clack, the headlights flicker
on with anamorphic flares and he walks out of the light. 'The rarest cars in Lebanon never hit the listings': a search
bar types 'rare classic car, Lebanon' and comes back with 0 results. The card flips into a private invitation:
PRIVATE AUCTION · BEIRUT, 'One night only.' with a gold shimmer on the words, Friday 21:00 and a ticking countdown.
'Be there.': the Remind me button is tapped and turns into 'Reminder set'. Last shot held with a slow push-in.
End card 'One night only. Be there.' Grille badge blurred."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s4_common as S

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, RED, GOLD = S.VIOLET, S.RED, (240, 200, 120)
FR = decode()
def KEEP(a):
    lum = a.mean(-1); rg = a[..., 0] - a[..., 1]
    return ((rg > 20) & (rg < 110) & (a[..., 1] > 85)) | ((a[..., 2] > a[..., 0] + 4) & (lum < 120)) | ((lum > 200) & (a[..., 0] - a[..., 2] < 25) & (a[..., 1] > 190))
for fr in FR: S.blur_unless(fr, (685, 1230, 806, 1314), 14, KEEP, clean=5, edge=18)

CAPS = [(0.30, 1.95, ["The [rarest cars]", "in Lebanon…"]), (1.95, 3.50, ["never hit the [listings.]"]), (4.00, 5.00, ["They go [live]…"]),
        (5.00, 6.40, ["for [one night only.]"]), (6.85, 9.20, ["[Be there.]"])]
ON, TYPE0, TYPE1, ZERO, FLIP, NIGHT, TAP = 0.30, 0.85, 1.85, 2.25, 3.62, 5.05, 7.0
QUERY = "rare classic car, Lebanon"
LIGHTS = [(151, 1253), (972, 1253)]
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
FLARE = np.zeros((H, W), np.float32)
for cx, cy in LIGHTS:
    FLARE += np.exp(-((_xx - cx) ** 2 + (_yy - cy) ** 2) / (2 * 70 ** 2)) * 0.9 + np.exp(-((_yy - cy) / 7) ** 2) * np.exp(-np.abs(_xx - cx) / 420) * 0.75
FLARE = FLARE[..., None] * np.array([190, 210, 255], np.float32)

def lit(fr, t):
    """darkness, then the headlights clack on (with a flicker) and flare"""
    if t < ON: k = 0.0
    elif t < ON + 0.07: k = R.ease_out((t - ON) / 0.07)
    elif t < ON + 0.13: k = 0.35
    else: k = R.ease_out((t - ON - 0.13) / 0.12)
    im = S.look(fr, "night"); a = np.asarray(im.convert("RGB"), np.float32)
    a = a * (0.05 + 0.95 * k) + FLARE * (0.35 * k + 0.5 * max(0, 1 - abs(t - ON - 0.2) / 0.25) * (t > ON)) * (0.92 + 0.08 * np.sin(t * 9))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def search(n, results):
    w, h = 780, 100; im = Image.new("RGBA", (w, h + (90 if results else 0)), (0, 0, 0, 0))
    bar = M.glass(w, h, h // 2, fill=(18, 18, 26, 232), border=(255, 255, 255, 70)); d = ImageDraw.Draw(bar)
    d.ellipse((34, 30, 70, 66), outline=(220, 224, 236, 255), width=5); d.line([(64, 60), (80, 76)], fill=(220, 224, 236, 255), width=6)
    q = R.text_layer(QUERY[:n] + ("|" if n < len(QUERY) else ""), R.font(36, 500), WHITE); bar.alpha_composite(q, (102, (h - q.height) // 2 - 2))
    im.alpha_composite(bar, (0, 0))
    if results:
        r = M.glass(w - 80, 74, 22, fill=(18, 18, 26, 215), border=(255, 76, 96, 160)); a = R.text_layer("0 RESULTS", R.font(28, mono=True), (255, 120, 135), tracking=4)
        b = R.text_layer("Never listed.", R.font(30, 500), (205, 208, 222)); r.alpha_composite(a, (28, 18)); r.alpha_composite(b, (r.width - 28 - b.width, 18))
        im.alpha_composite(r, (40, h + 14))
    return im

def invite(t):
    w, h = 800, 236; im = M.glass(w, h, 30, fill=(14, 12, 10, 236), border=GOLD + (230,)); d = ImageDraw.Draw(im)
    hd = R.text_layer("PRIVATE AUCTION  ·  BEIRUT", R.font(24, mono=True), GOLD, tracking=4); im.alpha_composite(hd, (36, 26))
    ti = R.text_layer("One night only.", R.font(62, 700), WHITE)
    if t >= NIGHT:                                                                            # gold shimmer across the words
        k = (t - NIGHT) / 0.7
        if k < 1:
            g = np.asarray(ti, np.float32).copy(); xs = np.arange(ti.width)[None, :]
            band = np.exp(-((xs - (-100 + k * (ti.width + 200))) / 60) ** 2)
            for c, v in enumerate(GOLD): g[..., c] = g[..., c] * (1 - band) + v * band
            ti = Image.fromarray(g.astype(np.uint8))
        else: ti = R.text_layer("One night only.", R.font(62, 700), (255, 232, 180))
    im.alpha_composite(ti, (36, 64))
    left = max(0, 2 * 3600 + 59 * 60 + 59 - int((t - FLIP) * 1))
    cd = R.text_layer(f"Fri 21:00  ·  in {left // 3600:02d}:{left % 3600 // 60:02d}:{left % 60:02d}", R.font(28, 500), (205, 200, 190)); im.alpha_composite(cd, (36, 160))
    done = t >= TAP + 0.18
    lab = R.text_layer("Reminder set" if done else "Remind me", R.font(30, 700), (60, 40, 140) if done else WHITE)
    bw, bh = lab.width + (84 if done else 56), 66; bx, by = w - 36 - bw, 146
    if done:
        b = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); ImageDraw.Draw(b).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=bh // 2, fill=(255, 255, 255, 255))
        db = ImageDraw.Draw(b); db.line([(24, 34), (34, 44), (52, 22)], fill=(124, 92, 255, 255), width=6); b.alpha_composite(lab, (62, (bh - lab.height) // 2 - 2))
    else:
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=bh // 2, fill=255)
        b = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); b.paste(M.grad(bw, bh), (0, 0), m); b.alpha_composite(lab, (28, (bh - lab.height) // 2 - 2))
    sc = 1.0
    if TAP <= t < TAP + 0.35: sc = 1 - 0.08 * np.sin(np.pi * (t - TAP) / 0.35)
    R.paste_center(im, b, bx + bw / 2, by + bh / 2, 1.0, sc)
    return im, (bx + bw / 2, by + bh / 2)

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["One night only.", "Be there."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = lit(fr, min(t, SHOT - 0.01) if t >= ON else 0.0)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 560))
    fade = 1 - R.clamp((t - (CLIP - 0.5)) / 0.3)
    if TYPE0 - 0.2 <= t < FLIP + 0.15:                                                       # nothing listed
        n = int(len(QUERY) * R.clamp((t - TYPE0) / (TYPE1 - TYPE0))); k = R.ease_out((t - TYPE0 + 0.2) / 0.3)
        sx = 1 - R.clamp((t - FLIP) / 0.15)
        s = search(n, t >= ZERO)
        if t >= ZERO and t < ZERO + 0.25: s = s  # results pop below
        s = s.resize((max(1, int(s.width * sx)), s.height)) if sx < 1 else s
        R.paste_center(im, s, W / 2, 150 + s.height / 2 + (1 - k) * -30, R.clamp(k * 2) * (0.6 + 0.4 * sx))
    if t >= FLIP + 0.15:                                                                     # ...it flips into an invitation
        c, (bx, by) = invite(t); sx = R.ease_out((t - FLIP - 0.15) / 0.2)
        c2 = c.resize((max(1, int(c.width * sx)), c.height)) if sx < 1 else c
        cy = 70 + c.height / 2
        R.paste_center(im, c2, W / 2, cy, fade)
        if TAP <= t < TAP + 0.7:
            kk = R.clamp((t - TAP) / 0.6); cx0 = W / 2 - c.width / 2 + bx; cy0 = cy - c.height / 2 + by
            S.ring(im, cx0, cy0, 20 + 160 * R.ease_out(kk), (1 - kk) * 0.9, VIOLET, 6)
            if t < TAP + 0.25: R.paste_center(im, finger(), cx0 + 10, cy0 + 26, 0.85 * (1 - R.clamp((t - TAP - 0.15) / 0.1)))
        if t >= TAP + 0.6: sparkle_burst(im, t, TAP + 0.6, W / 2 + 230, cy + 60, ((-80, -30, 26), (90, -40, 18), (60, 40, 26)))
    draw_caps(im, t, CAPS, y=1700, size=62)
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

def finger():
    im = Image.new("RGBA", (70, 70), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((8, 8, 62, 62), fill=(255, 255, 255, 170), outline=(255, 255, 255, 255), width=3); return im

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, 0.0),))
        S.drone(mx, 0.0, ON + 0.1, 41, 0.12)
        y = mx.tt(0.12); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 45), ON - 0.02, 0.4)    # the clack
        mx.thud(ON, 0.35); y = mx.tt(1.2); mx.fadd(np.sin(2 * np.pi * 60 * y) * np.minimum(1, y / 0.05) * np.exp(-y * 2.5), ON, 0.06)   # electrical hum swell
        S.tone(mx, ON, FLIP, ((98, .3), (146.8, .2), (196, .14), (233.1, .08)), 0.045, 0.8)     # G minor, mysterious
        for i in range(len(QUERY)):
            if i % 2: continue
            y = mx.tt(0.03); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 120), TYPE0 + (TYPE1 - TYPE0) * i / len(QUERY), 0.03)
        S.beep(mx, ZERO, 330, 0.12, 0.04)
        mx.whoosh(FLIP - 0.05, 0.4, 0.3)
        S.tone(mx, FLIP + 0.2, CLIP, ((146.8, .3), (185, .2), (220, .2), (293.7, .1)), 0.05, 0.6)
        mx.shimmer(3.75, 1567.98, 0.05)
        for at in (6.3, 6.62): y = mx.tt(0.04); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 90), at, 0.08)   # countdown ticks, in the gap
        y = mx.tt(0.06); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 3) * np.exp(-y * 80), TAP, 0.05)    # tap
        mx.ping(7.62, 1318.5, 0.1); mx.thud(7.6, 0.3); mx.shimmer(7.65, 1567.98, 0.07)
        mx.write("s4lights_audio.wav")
    render(frame, TOTAL, "s4lights_audio.wav", OUT)
