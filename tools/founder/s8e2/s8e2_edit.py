"""Season 8 Ep. 2 'بدّك تشوف شو في بـ HyperBidz؟' — into the phone.
He asks, picks up his phone and turns its black screen to us. The screen wakes (HyperBidz splash, then a live lot),
the camera dives into the phone until the app fills the frame, and a live bidding war plays out on the real listing
screen (rebuilt from the app's C1 flow): Ralph, Abir, Karim and 'You' trade +$23 bids, rows slide in, the current bid
rolls up, the status pill flips between 'X leads' and 'You're leading', the CTA flips between red 'Re-bid' and green
'Raise your max', an outbid push banner drops in, the clock runs down — hammer: 'You won it'. Then a VHS rewind
throws everything back: out of the app, out of the phone, the phone back on the table, the founder looking at us.
Held shot, Arabic end card."""
import sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude"); sys.path.insert(0, "/home/claude/s8e2")
from founder_common import *
import s7_common as Q
import ar_common as A
import app_ui as U
from phone import screen_quad
from s7_common import ease, fade, shield, put

T_UI0, Z0, Z1, HAM, REW0, REW1, CLIP, END = 4.9, 5.6, 6.7, 13.3, 14.6, 16.4, 17.9, 4.4
APP0 = Z1; TOTAL = CLIP + END; HOLD_SRC = 2.45; ZEND = 3.9

def clean_all(frames):
    """the laptop's Apple logo: tracked from frame 0 and inpainted while the laptop is in view"""
    tr = A.track(frames[:150], {"logo": (950, 1225)}, size=72, search=130)["logo"]; out = []
    for i, fr in enumerate(frames):
        if i >= 150: out.append(fr); continue
        a = np.asarray(fr.convert("RGB")).copy(); cx, cy = tr[i]; x0, y0 = int(cx - 70), int(cy - 70); x1, y1 = x0 + 140, y0 + 140
        x0, y0 = max(0, x0), max(0, y0); reg = a[y0:y1, x0:x1].copy(); m = np.zeros(reg.shape[:2], np.uint8)
        cv2.ellipse(m, (int(cx - x0), int(cy - y0)), (34, 40), 0, 0, 360, 255, -1); a[y0:y1, x0:x1] = cv2.inpaint(reg, m, 9, cv2.INPAINT_TELEA); out.append(Image.fromarray(a))
    return out
FR = clean_all(decode())

# phone screen quads, smoothed; expanded a touch to cover the rounded-corner inset
QD = {}
for i in range(int(T_UI0 * FPS) - 3, len(FR)):
    r = screen_quad(FR[i])
    if r is not None and r[1] > 60000: QD[i] = r[0]
_keys = sorted(QD)
def quad(i):
    i = max(_keys[0], min(_keys[-1], i)); ks = [k for k in _keys if abs(k - i) <= 3]
    q = np.mean([QD[k] for k in ks], 0); c = q.mean(0); return (c + (q - c) * 1.02).astype(np.float32)

PHONE_H = 2340
CAPS = [(0.1, 2.45, [("بدّك تشوف", WHITE), ("شو في بـ HyperBidz؟", Q.LAV)])]
LAST = (("قريباً…", False), ("على تلفونك.", True))

# ---------- the bidding war ----------
EVENTS = [(7.25, "You", 838), (7.95, "Abir", 861), (8.45, "Karim", 884), (9.0, "You", 907), (9.55, "Ralph", 930), (10.0, "Abir", 953),
          (10.5, "You", 976), (11.0, "Karim", 999), (11.5, "Ralph", 1022), (12.05, "You", 1045)]
INIT = [("Ralph", 815), ("You", 792), ("Abir", 769)]
def when(age):
    return "now" if age < 6 else (f"{int(age)}s" if age < 60 else f"{int(age // 60)}m")

def state(t):
    hist = [(n, a, -999) for n, a in reversed(INIT)] + [(n, a, et) for et, n, a in EVENTS if t >= et]
    top = hist[-1]; prev = hist[-2] if len(hist) > 1 else top
    nk = (t - top[2]) / 0.35 if top[2] > 0 else 2.0
    rows = []
    for j, (n, a, et) in enumerate(reversed(hist[-3:])):
        age = (t - et) * 6 if et > 0 else (60 if a == 815 else 180 if a == 769 else 70)
        rows.append((n, a, when(age), nk if j == 0 else 2.0))
    left = max(0, 14 - int(max(0, t - APP0) / 0.47))
    nxt = top[1] + 23; you = top[0] == "You"
    press = 0.0
    for et, n, a in EVENTS:
        if n == "You" and -0.18 <= t - et < 0.3: press = max(press, 1 - abs(t - et + 0.05) / 0.25)
    return dict(leader=top[0], cur=top[1], prev_cur=prev[1], roll_k=min(1, (t - top[2]) / 0.3) if top[2] > 0 else 1, timer=f"00:{left:02d}",
                timer_hot=left <= 10 and t >= APP0, rows=rows, nbids=len(hist), recent=len(hist), cta="raise" if you else "rebid", cta_amt=nxt,
                progress=0.55 + 0.45 * ease((t - APP0) / (HAM - APP0)) if t >= APP0 else 0.55, press=max(0, press), flash=max(0, 1 - (t - top[2]) / 0.5) * 0.8 if top[2] > 0 else 0)

def app_screen(t, H):
    im = U.listing(state(t), H)
    if 7.95 <= t < 9.35:                                                                                 # outbid push
        k = min(ease((t - 7.95) / 0.3), 1 - ease((t - 9.05) / 0.3)); b = U.banner(1)
        im.alpha_composite(b, (U.p(10), int(-b.height + (b.height + U.p(52)) * k)))
    return im

def splash(H):
    im = U.won(0, H=H) if False else Image.new("RGBA", (1080, H), (0, 0, 0, 0))
    g = np.linspace(0, 1, H)[:, None]; arr = np.array([47, 123, 255.]) * (1 - g) + np.array([124, 92, 255.]) * g
    im = Image.fromarray(np.repeat(arr[:, None, :], 1080, 1).astype(np.uint8)).convert("RGBA"); R.paste_center(im, Q.V.zflat(300, WHITE), 540, H / 2); return im

def screen_content(t, H):
    if t < T_UI0 + 0.35: return splash(H)
    if t < T_UI0 + 0.55: return Image.blend(splash(H), app_screen(t, H), (t - T_UI0 - 0.35) / 0.2)
    if t >= HAM: return U.won(t - HAM, H=H)
    return app_screen(t, H)

_MASK = {}
def phone_mask(H):
    if H not in _MASK:
        m = Image.new("L", (1080, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 1079, H - 1), radius=110, fill=255); _MASK[H] = np.asarray(m)
    return _MASK[H]

def warp_onto(base, ui, q, alpha=1.0):
    """perspective-warp the UI canvas into quad q (TL, TR, BR, BL) on base, as a lit screen"""
    H = ui.height; src = np.float32([[0, 0], [1079, 0], [1079, H - 1], [0, H - 1]]); M = cv2.getPerspectiveTransform(src, q)
    rgba = np.asarray(ui.convert("RGB")).astype(np.float32); a = phone_mask(H).astype(np.float32) / 255 * alpha
    sheen = np.linspace(0.07, 0, H)[:, None] * np.linspace(1, 0.2, 1080)[None, :]; rgba = np.clip(rgba * 0.97 + 255 * sheen[..., None], 0, 255)
    wr = cv2.warpPerspective(rgba, M, (W, H_FR), flags=cv2.INTER_LINEAR); wa = cv2.warpPerspective(a, M, (W, H_FR), flags=cv2.INTER_LINEAR)[..., None]
    b = np.asarray(base.convert("RGB")).astype(np.float32); out = b * (1 - wa) + wr * wa
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")
H_FR = H

def zoom_params(t, i):
    q = quad(i); c = q.mean(0); k = Q.ease_in((t - Z0) / (Z1 - Z0)); z = 1 + (ZEND - 1) * k
    w, h = W / z, H / z; l = min(max(c[0] - w / 2, 0), W - w); tp = min(max(c[1] - h / 2, 0), H - h); return z, l, tp, q, k

def forward(t):
    """the picture before the rewind, at output time t (< REW0)"""
    if t >= APP0 + 0.12:
        im = screen_content(t, H).convert("RGBA")
        if t < APP0 + 0.4: Q.flash(im, (1 - (t - APP0 - 0.12) / 0.28) * 0.5, (235, 228, 255))
        if t >= HAM: Q.flash(im, max(0, 1 - (t - HAM) / 0.25) * 0.8, (255, 255, 255))
        return im
    i = min(len(FR) - 1, int(t * FPS)); fr = FR[i]; im = Q.hq_grade(fr, 0.2)
    has_screen = t >= T_UI0 - 0.03 and i in QD or (t >= T_UI0 and _keys and i >= _keys[0])
    if t < Z0:
        if has_screen:
            ui = screen_content(t, PHONE_H); im = warp_onto(im, ui, quad(i), min(1, (t - T_UI0 + 0.03) / 0.2))
            glow = ease((t - T_UI0) / 0.4) * 0.5; c = quad(i).mean(0); R.paste_center(im, Q.V.glow(900, 260, (110, 90, 255), int(90 * glow)), c[0], c[1])
        return im
    z, l, tp, q, k = zoom_params(t, i)                                                                  # the dive
    zi = im.crop((int(l), int(tp), int(l + W / z), int(tp + H / z))).resize((W, H), Image.BICUBIC)
    if k > 0.55:
        acc = np.asarray(zi, np.float32); n = 1
        for s in (1.025, 1.05, 1.08):
            ww, hh = W / s, H / s; c2 = zi.crop((int((W - ww) / 2), int((H - hh) / 2), int((W + ww) / 2), int((H + hh) / 2))).resize((W, H), Image.BILINEAR)
            acc += np.asarray(c2, np.float32) * (k - 0.55) * 2; n += (k - 0.55) * 2
        zi = Image.fromarray(np.clip(acc / n, 0, 255).astype(np.uint8))
    qz = ((q - np.float32([l, tp])) * np.float32([W / (W / z), H / (H / z)])).astype(np.float32)
    out = warp_onto(zi, screen_content(t, PHONE_H), qz)
    if t > APP0 - 0.05: out = Image.blend(out.convert("RGB"), screen_content(t, H).convert("RGB"), (t - APP0 + 0.05) / 0.17).convert("RGBA")
    Q.flash(out, max(0, (t - (Z1 - 0.2)) / 0.2) * 0.45, (235, 228, 255))
    return out

def rew_src(t):
    r = (t - REW0) / (REW1 - REW0); f = 0.5 - 0.5 * np.cos(np.pi * min(1, max(0, r)))
    return REW0 - 0.02 - (REW0 - 0.02 - HOLD_SRC) * f

def vhs(im, t):
    a = np.asarray(im.convert("RGB")).astype(np.int16); rng = np.random.default_rng(int(t * 97))
    out = a.copy(); out[..., 0] = np.roll(a[..., 0], 7, 1); out[..., 2] = np.roll(a[..., 2], -7, 1)
    for _ in range(7):
        y0 = int(rng.integers(0, H - 40)); hh = int(rng.integers(6, 40)); out[y0:y0 + hh] = np.roll(out[y0:y0 + hh], int(rng.integers(-40, 40)), 1)
    yb = int((t * 1900) % (H + 200)) - 100; band = slice(max(0, yb), min(H, yb + 60))
    out[band] = np.clip(out[band] * 0.6 + rng.integers(60, 200, out[band].shape[:2])[..., None] * 0.4, 0, 255)
    out[::4] = (out[::4] * 0.82).astype(np.int16)
    l = out.mean(-1, keepdims=True); out = l + (out - l) * 0.75
    im2 = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")
    if int(t * 4) % 2 == 0:
        tag = Image.new("RGBA", (420, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(tag)
        for x0 in (0, 34): d.polygon([(x0 + 34, 14), (x0 + 34, 74), (x0, 44)], fill=(255, 255, 255, 235))
        tag.alpha_composite(R.text_layer("REWIND", R.font(48, mono=True), WHITE, tracking=6), (96, 16)); im2.alpha_composite(tag, (60, 230))
    return im2

def part_tag():
    tl = A.atext("الموسم ٨  ·  الحلقة ٢", 30, 700, Q.LAV); w, h = tl.width + 44, tl.height + 2
    im = Q.glass_layer(w, h, h // 2, fill=(12, 14, 26, 190), edge=(255, 255, 255, 90)); im.alpha_composite(tl, (22, 0)); return im
PART = part_tag()

_CAP = {}
def caps(im, t, y=1730):
    for t0, t1, lines in CAPS:
        if not (t0 <= t < t1): continue
        a = fade(t, t0, t1, 0.3, 0.3); key = tuple(lines)
        if key not in _CAP: _CAP[key] = [A.atext(s, 60, 700, c) for s, c in lines]
        ls = _CAP[key]; w = max(l.width for l in ls) + 76; h = sum(l.height for l in ls) - 14 * (len(ls) - 1) + 30
        yy = y + (1 - a) * 12; shield(im, (W / 2 - w / 2, yy - h / 2, W / 2 + w / 2, yy + h / 2), a, 28, dark=0.58); cy = yy - h / 2 + 12
        for l in ls: put(im, l, W / 2 - l.width / 2, cy, a); cy += l.height - 14

def scene(t):
    if t < REW0:
        im = forward(t)
        if t < T_UI0: R.paste_center(im, PART, W / 2, 215, fade(t, 0.0, T_UI0, 0.3, 0.3)); caps(im, t)
        return im
    if t < REW1: return vhs(forward(rew_src(t)), t)
    fr = FR[int(HOLD_SRC * FPS)]; im = Q.hq_grade(fr, 0.2)                                              # back in the office
    im = hold_zoom(im, t - REW1 + 0.0, 0.0, 0.0, CLIP - REW1, 1.06, (560, 820))
    if t < REW1 + 0.25: im = Image.blend(im.convert("RGB"), vhs(im, t).convert("RGB"), 1 - (t - REW1) / 0.25).convert("RGBA")
    a = ease((t - REW1 - 0.35) / 0.5)
    if a > 0:
        gr = Image.new("RGBA", (W, 700), (8, 8, 18, 0)); gr.putalpha(Image.linear_gradient("L").resize((W, 700)).point(lambda v: int(v * 0.75 * a))); im.alpha_composite(gr, (0, H - 700))
    for i, (s, hl) in enumerate(LAST): Q.place(im, A.atext(s, 76, 800, Q.LAV if hl else WHITE), W / 2, 1560 + i * 100, ease((t - REW1 - 0.35 - 0.2 * i) / 0.5), 14)
    return im

_LAST = {}
def frame(t):
    if t < CLIP: return scene(t).convert("RGB")
    ec = A.end_card(t - CLIP, END, (("بدّك تشوف أكتر؟", False), ("تابعنا.", True))); k = (t - CLIP) / 0.45
    if k >= 1: return ec
    if "f" not in _LAST: _LAST["f"] = scene(CLIP - 0.01).convert("RGB")
    return Image.blend(_LAST["f"], ec, ease(k))

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = Q.HQMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        g = A.darbuka_groove(TOTAL, 1.0, bpm=96, seed=9); x = np.arange(len(g)) / SR
        env = np.minimum(1, x / 0.4) * (0.6 + 0.4 * np.clip((x - 2.2) / 0.6, 0, 1)) * (0.85 + 0.15 * np.clip((x - APP0) / 0.2, 0, 1)) * np.where((x > REW0) & (x < REW1 + 0.15), 0.0, 1.0) * np.where(x > HAM, np.clip((HAM + 0.05 - x) / 0.08, 0, 1) + np.clip((x - REW1 - 0.2) / 0.4, 0, 1) * 0.45, 1.0)
        env *= np.clip((CLIP + 0.05 - x) / 0.15, 0, 1); env = np.convolve(env, np.ones(240) / 240, "same"); mx.fadd(g * env, 0.0, 0.5)
        mx.shimmer(T_UI0, 1568, 0.03); Q.riser(mx, Z0 - 0.3, Z1, 0.12, 180, 2400); mx.whoosh(Z1 - 0.35, 0.45, 0.25); Q.impact(mx, Z1, 0.18)
        y = mx.tt(0.5); pulse = np.sin(2 * np.pi * 55 * y) * np.exp(-y * 7)                                     # tension pulse under the war
        tt = APP0
        while tt < HAM: mx.fadd(pulse, tt, 0.18 + 0.12 * (tt - APP0) / (HAM - APP0)); tt += 0.47
        for s in range(15): Q.V.ticks(mx, APP0 + s * 0.47, APP0 + s * 0.47 + 0.01, rate=1, g=0.06)
        for et, n, a in [e for e in EVENTS if e[1] == "You"]: Q.key_click(mx, et - 0.05, 0.06); Q.V.chime(mx, et + 0.02, 1568, 0.04)
        for et, n, a in [e for e in EVENTS if e[1] != "You"]: Q.coin(mx, et, 0.05); Q.coin(mx, et + 0.06, 0.03)
        Q.bubble_pop(mx, 7.95, 0.06); Q.ding(mx, 7.97, 1318.5, 0.04)
        Q.gavel(mx, HAM, 0.16); Q.impact(mx, HAM, 0.12)
        for i, m in enumerate((62, 66, 69, 74, 78)):
            p_ = Q.pluck(Q.note(m), 0.9, 0.55) * np.exp(-np.arange(int(0.9 * SR)) / SR * 4); mx.fadd(p_, HAM + 0.15 + i * 0.08, 0.16)
        mx.shimmer(HAM + 0.5, 1568, 0.035)
        D = REW1 - REW0; y = mx.tt(D); f = 2600 - 1800 * (y / D) + 300 * np.sin(2 * np.pi * 9 * y)                # tape rewind squeal
        sq = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35 + mx.lp(mx.rng.normal(0, 1, len(y)), 2) * 0.5; sq *= np.minimum(1, y / 0.1) * np.clip((D - y) / 0.1, 0, 1)
        mx.fadd(sq, REW0, 0.12); mx.whoosh(REW0, 0.5, 0.18); Q.impact(mx, REW1, 0.2)
        mx.write("s8e2_audio.wav")
    render(frame, TOTAL, "s8e2_audio.wav", sys.argv[1])
