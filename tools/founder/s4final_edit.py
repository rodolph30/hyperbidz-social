"""Season 4 finale 'You just won' (Raouché at golden hour, red convertible). Live auction countdown: giant 3 · 2 · 1
slam in over the sky with 'GOING ONCE · $46,000', 'GOING TWICE', 'FINAL CALL' and a rising tension bed. A gavel winds up
and strikes on 'Sold.': shockwave, screen shake, flash, a huge SOLD stamp and golden confetti raining down. On
'Congratulations' a HyperBidz notification drops in: 'You won your first car. Red convertible · $46,000 · 31 bidders'.
He points at the camera on 'you just won your first car on HyperBidz'. Last shot held with a slow push-in.
End card 'Your first car is waiting.' Hubcap emblem blurred (tracked)."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s4_common as S

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.4; END = 3.8; TOTAL = CLIP + END
VIOLET, RED, GOLD = S.VIOLET, S.RED, (255, 206, 92)
FR = decode()
TRACK = [(0.0, 152, 1572), (0.1, 148, 1578), (0.2, 140, 1590), (0.3, 136, 1596), (0.4, 132, 1604), (0.5, 126, 1616), (0.6, 120, 1624), (0.7, 112, 1636),
         (0.8, 106, 1644), (0.9, 100, 1652), (1.0, 92, 1662), (1.1, 84, 1670), (1.2, 70, 1690), (1.3, 62, 1700), (1.4, 56, 1710), (1.5, 42, 1728), (1.6, 32, 1740), (2.8, -90, 1900)]
for i, fr in enumerate(FR):                                                                   # hubcap emblem, tracked until it leaves frame
    t = i / FPS
    if t > 2.8: break
    x = np.interp(t, [p[0] for p in TRACK], [p[1] for p in TRACK]); y = np.interp(t, [p[0] for p in TRACK], [p[2] for p in TRACK]); r = 36 + 10 * t
    box = (int(max(0, x - r)), int(max(0, y - r)), int(min(W, x + r)), int(min(H, y + r)))
    if box[2] - box[0] > 12 and box[3] - box[1] > 12: S.blur_unless(fr, box, 10, lambda a: np.zeros(a.shape[:2], bool), edge=10)

NUMS = [(0.18, "3", "GOING ONCE  ·  $46,000"), (1.12, "2", "GOING TWICE  ·  $46,000"), (1.97, "1", "FINAL CALL")]
WIND, STRIKE, NOTE, POINT, BRAND = 2.45, 2.90, 3.62, 5.4, 7.62
CAPS = [(3.90, 5.05, ["[Congratulations.]"]), (5.10, 9.20, ["You just won your [first car]", "on HyperBidz."])]
rng = np.random.default_rng(13)

def big_num(ch):
    f = R.font(330, 700); tl = R.text_layer(ch, f, WHITE); w, h = tl.width + 40, tl.height + 40
    m = Image.new("L", (w, h), 0); m.paste(tl.getchannel("A"), (20, 20))
    g = M.grad(w, h); out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); out.paste(g, (0, 0), m)
    edge = m.filter(ImageFilter.MaxFilter(9)); ol = Image.new("RGBA", (w, h), (255, 255, 255, 0)); ol.putalpha(edge)
    sh = Image.new("RGBA", (w, h), (20, 10, 60, 0)); sh.putalpha(edge.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.5)))
    res = Image.new("RGBA", (w + 20, h + 30), (0, 0, 0, 0)); res.alpha_composite(sh, (10, 22)); res.alpha_composite(ol, (10, 10)); res.alpha_composite(out, (10, 10)); return res
NUM_IM = [big_num(n) for _, n, _ in NUMS]
SUB_IM = [M.chip(s, (14, 12, 24, 225), VIOLET, 28, 4) for _, _, s in NUMS]

def gavel():
    s = 1000; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s // 2
    d.rounded_rectangle((c, c - 17, c + 410, c + 17), radius=16, fill=(120, 72, 38, 255), outline=(70, 40, 20, 255), width=3)         # handle
    d.rounded_rectangle((c + 380, c - 112, c + 500, c + 112), radius=24, fill=(150, 92, 48, 255), outline=(80, 46, 22, 255), width=4)  # head
    for yy in (c - 74, c + 62): d.rectangle((c + 380, yy, c + 500, yy + 12), fill=(220, 180, 90, 255))                              # brass bands
    d.rounded_rectangle((c + 394, c - 100, c + 410, c + 100), radius=6, fill=(190, 130, 80, 140))
    return im
GAVEL = gavel()
PIVOT, RAD = (1100, 300), 440

def gavel_angle(t):
    if t < WIND + 0.3: return 214 + 18 * R.ease_out((t - WIND) / 0.3)                         # raised at the top, winding up
    if t < STRIKE: k = R.clamp((t - WIND - 0.3) / (STRIKE - WIND - 0.3)); return 232 - 34 * k ** 2.2   # the strike
    k = t - STRIKE; return 198 + 9 * np.sin(k * 26) * np.exp(-k * 9)                           # bounce

def sold_stamp():
    tl = R.text_layer("SOLD", R.font(150, 700), WHITE, tracking=10); w, h = tl.width + 120, tl.height + 50
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=40, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.paste(M.grad(w, h), (0, 0), m)
    ImageDraw.Draw(im).rounded_rectangle((14, 14, w - 15, h - 15), radius=30, outline=(255, 255, 255, 200), width=5)
    im.alpha_composite(tl, (60, 14)); return im.rotate(-7, resample=Image.BICUBIC, expand=True)
SOLD_IM = sold_stamp()
IMPACT = (PIVOT[0] + RAD * np.cos(np.radians(198)), PIVOT[1] + RAD * np.sin(np.radians(198)))

N = 190                                                                                         # confetti
CF = dict(x=np.where(rng.random(N) < 0.55, rng.uniform(0, W, N), IMPACT[0] + rng.normal(0, 40, N)),
          y=np.where(rng.random(N) < 0.55, rng.uniform(-400, -20, N), IMPACT[1] + rng.normal(0, 30, N)))
burst = CF["y"] > 0
CF["vx"] = np.where(burst, rng.normal(0, 520, N), rng.normal(0, 40, N)); CF["vy"] = np.where(burst, rng.uniform(-1700, -700, N), rng.uniform(120, 320, N))
CF["rot"] = rng.uniform(0, np.pi, N); CF["spin"] = rng.normal(0, 9, N); CF["sz"] = rng.uniform(10, 22, N); CF["ph"] = rng.uniform(0, 6.28, N)
CF["col"] = [[GOLD, (255, 236, 170), VIOLET, (124, 92, 255), WHITE, (255, 150, 170)][j] for j in rng.choice(6, N, p=[.32, .18, .16, .12, .14, .08])]
CF["delay"] = np.where(burst, 0.0, rng.uniform(0, 0.9, N))

def confetti(im, t):
    if t < STRIKE: return
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(N):
        k = t - STRIKE - CF["delay"][i]
        if k <= 0: continue
        vy = CF["vy"][i]; g = 1400 if burst[i] else 0
        drag = np.exp(-k * 1.6) if burst[i] else 1.0
        x = CF["x"][i] + CF["vx"][i] * (1 - np.exp(-k * 1.6)) / 1.6 + 30 * np.sin(k * 3 + CF["ph"][i])
        y = CF["y"][i] + (vy * (1 - np.exp(-k * 1.6)) / 1.6 + 0.5 * g * k * k * 0.25 + (240 * k if burst[i] else 0)) if burst[i] else CF["y"][i] + vy * k
        if y > H + 40: continue
        a = CF["rot"][i] + CF["spin"][i] * k; s = CF["sz"][i]; fl = abs(np.cos(k * 6 + CF["ph"][i]))      # flutter
        dx, dy = np.cos(a) * s, np.sin(a) * s; ex, ey = -np.sin(a) * s * 0.45 * fl, np.cos(a) * s * 0.45 * fl
        al = int(240 * min(1, (CLIP - 0.3 - t) / 0.4)) if t > CLIP - 0.7 else 240
        d.polygon([(x - dx - ex, y - dy - ey), (x + dx - ex, y + dy - ey), (x + dx + ex, y + dy + ey), (x - dx + ex, y - dy + ey)], fill=CF["col"][i] + (max(0, al),))

def notification():
    w, h = 900, 176; im = M.glass(w, h, 34, fill=(248, 248, 252, 242), border=(255, 255, 255, 255))
    ic = Image.new("RGBA", (104, 104), (0, 0, 0, 0)); m = Image.new("L", (104, 104), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 103, 103), radius=26, fill=255)
    ic.paste(M.grad(104, 104), (0, 0), m); R.paste_center(ic, R.z_mark(62), 52, 52); im.alpha_composite(ic, (30, 36))
    a = R.text_layer("HYPERBIDZ  ·  NOW", R.font(22, mono=True), (110, 110, 130), tracking=3); im.alpha_composite(a, (158, 30))
    b = R.text_layer("You won your first car.", R.font(44, 700), (20, 18, 40)); im.alpha_composite(b, (158, 62))
    c = R.text_layer("Red convertible  ·  $46,000  ·  31 bidders", R.font(28, 500), (90, 80, 140)); im.alpha_composite(c, (158, 120))
    return im
NOTE_IM = notification()

def frame(t):
    if t >= CLIP: return end_card(t - CLIP, ["Your first car", "is waiting."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = S.look(fr, "dusk")
    if STRIKE <= t < STRIKE + 0.35:                                                          # impact shake
        k = (t - STRIKE) / 0.35; amp = 22 * (1 - k) ** 2
        im = S.zcrop(im, 1.04, (540 + amp * np.sin(t * 90), 900 + amp * np.cos(t * 70)))
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.08, (560, 560))
    if t < STRIKE:                                                                            # 3 · 2 · 1
        for j, (at, n, s) in enumerate(NUMS):
            nxt = NUMS[j + 1][0] if j + 1 < len(NUMS) else STRIKE
            if not (at <= t < nxt): continue
            k = (t - at) / 0.28; out = R.clamp((t - (nxt - 0.12)) / 0.12)
            R.paste_center(im, NUM_IM[j], W / 2, 238, R.clamp(k * 3) * (1 - out), (2.2 - 1.2 * R.stamp(k) if k < 1 else 1.0 + 0.04 * (t - at)) * (1 + 0.3 * out))
            R.paste_center(im, SUB_IM[j], W / 2, 52, R.clamp((t - at - 0.1) / 0.15) * (1 - out))
            for r in range(2): kk = R.clamp((t - at - 0.06 * r) / 0.5); S.ring(im, W / 2, 238, 90 + 230 * R.ease_out(kk), (1 - kk) * 0.7, VIOLET, 8)
    if WIND <= t < STRIKE + 0.7:                                                             # the gavel
        a = gavel_angle(t); al = R.clamp((t - WIND) / 0.12) * (1 - R.clamp((t - STRIKE - 0.45) / 0.25))
        g = GAVEL.rotate(-a, resample=Image.BICUBIC); R.paste_center(im, g, PIVOT[0], PIVOT[1], al)
    if t >= STRIKE:
        for r in range(3): kk = R.clamp((t - STRIKE - 0.07 * r) / 0.7); S.ring(im, IMPACT[0], IMPACT[1], 40 + 520 * R.ease_out(kk), (1 - kk) * 0.9, GOLD if r == 1 else VIOLET, 10)
    if STRIKE <= t < NOTE + 0.5:
        s = (t - STRIKE - 0.02) / 0.3; out = R.clamp((t - NOTE) / 0.4)
        R.paste_center(im, SOLD_IM, 470, 190 - 40 * out, R.clamp(s * 3) * (1 - out), (2.0 - 1.0 * R.stamp(s) if s < 1 else 1.0) * (1 + 0.15 * out))
    confetti(im, t)
    if t >= NOTE:                                                                            # the notification
        k = R.ease_out((t - NOTE) / 0.45)
        R.paste_center(im, NOTE_IM, W / 2, 118 - (1 - k) * 260, R.clamp((t - NOTE) / 0.2) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), 1.0 + 0.04 * (1 - R.clamp((t - NOTE - 0.45) / 0.2)) if t > NOTE + 0.45 else 1.0)
    if t >= BRAND: sparkle_burst(im, t, BRAND, W / 2 - 330, 118, ((-60, -50, 26), (60, -60, 18), (50, 50, 26)))
    draw_caps(im, t, CAPS, y=1700, size=62)
    if STRIKE <= t < STRIKE + 0.09: im = M.flash(im, 0.55 * (1 - (t - STRIKE) / 0.09), (255, 240, 210))
    if t > CLIP - XF: im = Image.blend(im, R.GRAD_BG, R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Mix(CLIP, END, pad_freqs=((146.8, 0.0),))
        y = mx.tt(STRIKE - 0.05); rise = mx.lp(mx.rng.normal(0, 1, len(y)), 8) * (y / y[-1]) ** 2.2                          # tension riser
        tone_ = np.sin(2 * np.pi * np.cumsum(70 + 90 * (y / y[-1]) ** 2) / SR) * (0.3 + 0.7 * y / y[-1])
        mx.fadd((rise * 0.5 + tone_ * 0.6) * np.minimum(1, (y[-1] - y) / 0.03), 0.0, 0.07)
        for at, *_ in NUMS: mx.thud(at - 0.03, 0.5); S.beep(mx, at + 0.45, 1760, 0.05, 0.04)                                     # boom + tick per number
        y = mx.tt(0.06); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 1) * np.exp(-y * 70), STRIKE - 0.03, 0.75)                   # the gavel crack
        mx.thud(STRIKE - 0.02, 0.7)
        for j in range(5): y = mx.tt(0.08); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 50), 3.52 + j * 0.05, 0.12)   # confetti pops, after 'Sold'
        y = mx.tt(2.0); cheer = mx.lp(mx.rng.normal(0, 1, len(y)), 4) * (0.7 + 0.3 * np.sin(2 * np.pi * 5.3 * y) * np.sin(2 * np.pi * 3.1 * y))
        mx.fadd(cheer * np.minimum(1, y / 0.15) * np.exp(-y * 1.3), 3.52, 0.12)                                                  # a crowd's cheer
        S.tone(mx, 3.5, CLIP, ((146.8, .3), (185, .22), (220, .2), (293.7, .12), (370, .06)), 0.06, 0.4)                       # D major, triumphant
        mx.ping(NOTE - 0.02, 1318.5, 0.1); mx.ping(NOTE + 0.1, 1760, 0.06)
        mx.shimmer(BRAND + 0.1, 1567.98, 0.09); mx.thud(7.75, 0.35)
        mx.write("s4final_audio.wav")
    render(frame, TOTAL, "s4final_audio.wav", OUT)
