"""Season 5 (the Vault) finale 'You know what to do', outside a hotel at night. 'Good taste gets you noticed': his Vault
profile card (seal ring, VAULT MEMBER) and notifications pop: Karim started following you, Maya saved your profile.
'Good timing gets you the watch': a live lot's clock runs down 0:03 → 0:00, he takes the lead at the last second and
the hammer falls: You won it. 'HyperBidz': the members' seal stamps in, the lit edge glows. 'You know what to do':
5 VAULT LOTS LIVE NOW and a Join the Vault button that gets tapped. Last shot held with a slow push-in.
Vault end card 'You know what to do.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s5_common as V

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.45; END = 3.9; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.35, 2.15, ["Good taste gets you [noticed.]"]), (2.55, 4.60, ["Good timing gets you", "[the watch.]"]),
        (5.20, 6.30, ["[HyperBidz.]"]), (6.60, 9.20, ["You know [what to do.]"])]
PROF, NOTES, CLOCK, LEAD, ZERO, WON, BRAND, JOIN, TAP = 0.45, (1.15, 1.7), 2.6, 3.55, 4.12, 4.4, 5.3, 6.6, 7.62

def profile():
    w, h = 760, 200; im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((40, 40, w + 40, h + 40), radius=40, fill=(94, 108, 255, 100)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(24)))
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=40, fill=(9, 10, 15, 225), outline=(255, 255, 255, 50), width=2)
    d.ellipse((30, 26, 130, 126), fill=(11, 14, 20, 255), outline=V.EDGE + (255,), width=5)
    r = R.text_layer("R", R.font(48, 700), WHITE); c.alpha_composite(r, (80 - r.width // 2, 76 - r.height // 2 - 4))
    n = R.text_layer("Rodolph", R.font(44, 700), WHITE); c.alpha_composite(n, (160, 30))
    ck = 160 + n.width + 18; d.ellipse((ck, 42, ck + 34, 76), fill=(52, 199, 123, 255)); d.line([(ck + 8, 59), (ck + 15, 66), (ck + 27, 50)], fill=WHITE + (255,), width=4)
    s = R.text_layer("Trusted  ·  640 trust score", R.font(26, 500), (190, 194, 210)); c.alpha_composite(s, (160, 88))
    strip = Image.new("RGBA", (w - 60, 46), (0, 0, 0, 0)); ImageDraw.Draw(strip).rounded_rectangle((0, 0, w - 61, 45), radius=14, fill=(6, 7, 11, 255))
    strip.alpha_composite(V.zflat(24, V.ICON), (14, 11)); strip.alpha_composite(V.mono("VAULT MEMBER", 20, V.LAV, 4), (50, 12))
    sn = V.mono("SINCE OCT 2026", 20, (190, 194, 210), 2); strip.alpha_composite(sn, (strip.width - sn.width - 16, 12)); c.alpha_composite(strip, (30, 140))
    im.alpha_composite(c, (40, 40)); return im
PROF_IM = profile()

def note(initial, text, col):
    tx = R.text_layer(text, R.font(30, 600), WHITE); w, h = tx.width + 120, 74
    im = M.glass(w, h, h // 2, fill=(9, 10, 15, 220), border=(255, 255, 255, 60)); d = ImageDraw.Draw(im)
    d.ellipse((14, 12, 64, 62), fill=col + (255,)); i = R.text_layer(initial, R.font(26, 700), WHITE); im.alpha_composite(i, (39 - i.width // 2, 37 - i.height // 2 - 2))
    im.alpha_composite(tx, (82, (h - tx.height) // 2 - 3)); return im
NOTE_IM = [note("K", "Karim started following you", (109, 77, 255)), note("M", "Maya saved your profile", (221, 92, 140))]
YOU = V.bid_chip("R", "You lead at $5,200", "you", (109, 77, 255))
WON_IM = V.won_panel("10:02 PM", "Chronograph on steel bracelet", "$5,200", 820)
LIVE = None

def frame(t):
    if t >= CLIP: return V.vault_end_card(t - CLIP, ["You know", "what to do."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = V.vault_grade(fr)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 700))
    if t >= WON: V.lit_edge(im, R.ease_out((t - WON) / 0.5), t)
    fade = 1 - R.clamp((t - (CLIP - 0.5)) / 0.3)
    if PROF <= t < CLOCK + 0.3:                                                                          # good taste gets you noticed
        k = R.ease_out((t - PROF) / 0.4); out = R.clamp((t - CLOCK) / 0.3)
        R.paste_center(im, PROF_IM, W / 2, 190 + (1 - k) * -60 - out * 80, R.clamp((t - PROF) / 0.2) * (1 - out))
        for j, at in enumerate(NOTES):
            if t < at: continue
            nxt = NOTES[j + 1] if j + 1 < len(NOTES) else CLOCK; s = (t - at) / 0.3
            R.paste_center(im, NOTE_IM[j], W / 2, 375, R.clamp(s * 3) * (1 - R.clamp((t - nxt + 0.1) / 0.15)), 0.85 + 0.15 * R.stamp(s) if s < 1 else 1.0)
    if CLOCK <= t < WON + 0.3:                                                                           # good timing
        left = max(0, int(np.ceil((ZERO - t) * 2.0))); out = R.clamp((t - WON) / 0.3)
        R.paste_center(im, V.timer_chip(f"0:{left:02d}", hot=True), 900, 160, R.clamp((t - CLOCK) / 0.2) * (1 - out), 1 + 0.06 * (1 - ((t - CLOCK) * 2.0) % 1) * (t < ZERO))
    if LEAD <= t < WON + 0.3:
        s = (t - LEAD) / 0.3; R.paste_center(im, YOU, 40 + YOU.width / 2, 160, R.clamp(s * 3) * (1 - R.clamp((t - WON) / 0.3)), 0.85 + 0.15 * R.stamp(s) if s < 1 else 1.0)
    if WON <= t < BRAND + 0.3:                                                                           # gets you the watch
        s = (t - WON) / 0.34; out = R.clamp((t - BRAND) / 0.3)
        R.paste_center(im, WON_IM, W / 2, 245, R.clamp(s * 3) * (1 - out), (1.25 - 0.25 * R.stamp(s) if s < 1 else 1.0) * 0.82 * (1 - 0.1 * out))
        sparkle_burst(im, t, WON + 0.1, W / 2 + 280, 160, ((-80, -40, 26), (80, -50, 18), (60, 40, 26)))
    if t >= BRAND:                                                                                       # HyperBidz
        s = (t - BRAND) / 0.34; a = R.clamp(s * 3) * fade
        R.paste_center(im, V.seal(130), W / 2, 200, a, 1.5 - 0.5 * R.stamp(s) if s < 1 else 1.0)
        R.paste_center(im, V.mono_pill("HYPERBIDZ VAULT", 26), W / 2, 345, R.clamp((t - BRAND - 0.2) / 0.3) * a)
        sparkle_burst(im, t, BRAND, W / 2, 200, ((-110, -40, 26), (110, -50, 18), (90, 50, 26)))
    if t >= JOIN:                                                                                        # you know what to do
        k = R.ease_out((t - JOIN) / 0.45); pressed = np.exp(-((t - TAP) / 0.12) ** 2) if t >= TAP - 0.3 else 0
        R.paste_center(im, V.live_line("5 VAULT LOTS LIVE NOW", t), W / 2, 1385 + (1 - k) * 60, R.clamp((t - JOIN - 0.1) / 0.3) * fade)
        R.paste_center(im, V.join_button("Join the Vault", 820, pressed), W / 2, 1520 + (1 - k) * 160, R.clamp((t - JOIN) / 0.2) * fade, (1 - 0.05 * pressed) * (1 + 0.015 * np.sin((t - JOIN) * 5)))
        if TAP <= t < TAP + 0.7:
            kk = R.clamp((t - TAP) / 0.6); lay = Image.new("RGBA", (900, 900), (0, 0, 0, 0)); rr = 40 + 380 * R.ease_out(kk)
            ImageDraw.Draw(lay).ellipse((450 - rr, 450 - rr, 450 + rr, 450 + rr), outline=(167, 139, 250, int(230 * (1 - kk))), width=8); R.paste_center(im, lay, W / 2, 1520)
        if t >= TAP + 0.1: sparkle_burst(im, t, TAP + 0.1, W / 2, 1520, ((-380, -40, 34), (380, -50, 26), (330, 50, 18), (-320, 60, 26)))
    draw_caps(im, t, CAPS, y=1845 if t >= JOIN else 1700, size=58)
    if t > CLIP - XF: im = Image.blend(im, Image.new("RGBA", (W, H), V.STAGE + (255,)), R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = V.VaultMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        V.pad(mx, 0.0, WON, ((73.4, .3), (110, .22), (146.8, .16)), 0.045, 0.8)
        for at in NOTES: mx.ping(at + 0.02, 1567.98, 0.035)
        V.ticks(mx, CLOCK, ZERO, 8, 0.035)                                                                # faster: the last seconds
        V.lock(mx, WON - 0.02, 0.35); V.chime(mx, WON + 0.05, 1318.5, 0.08)                               # after 'watch'
        V.pad(mx, WON, CLIP, ((146.8, .3), (185, .22), (220, .2), (277.2, .1), (329.6, .05)), 0.055, 0.4)
        V.chime(mx, 6.05, 1567.98, 0.05)                                                                  # after 'HyperBidz'
        y = mx.tt(0.05); mx.fadd(mx.lp(mx.rng.normal(0, 1, len(y)), 2) * np.exp(-y * 90), TAP, 0.07)
        mx.shimmer(TAP + 0.05, 1318.5, 0.08); mx.thud(TAP + 0.02, 0.3)
        mx.write("s5timing_audio.wav")
    render(frame, TOTAL, "s5timing_audio.wav", OUT)
