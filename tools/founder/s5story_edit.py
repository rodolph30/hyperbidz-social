"""Season 5 (the Vault) Ep. 4 'How you got it'. 'What makes a watch special?': a minimal dial ticks in the dark at the
top. 'Mmm' (hand on heart): the lit gradient edge beats twice like a heart. 'It's not just what's on your wrist': a spec
card, ON YOUR WRIST: Swiss chronograph · 40 mm · Automatic · leather strap. 'It's how you got it': the card flips into
its provenance, HOW YOU GOT IT: 21:58 · 14 bidders in the Vault / 21:59:56 · your bid $4,250 / 22:00 · hammer fell ·
yours. Last shot held with a slow push-in. Vault end card 'Every watch has a story. Make yours live.'"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s5_common as V

OUT = sys.argv[1]; SHOT = 8.0; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.45; END = 4.1; TOTAL = CLIP + END
FR = decode()
CAPS = [(0.30, 2.10, ["You know what makes", "a watch [special?]"]), (3.75, 5.60, ["It's not just what's", "on your [wrist.]"]), (6.35, 9.20, ["It's [how you got it.]"])]
DIAL0, BEAT, SPEC, FLIP, ROWS = 0.3, (2.75, 3.15), 3.85, 6.3, (6.55, 6.85, 7.15)

def dial(t, size=170):
    im = Image.new("RGBA", (size + 60, size + 60), (0, 0, 0, 0)); c = im.width / 2; r = size / 2
    g = V.glow(im.width, r * 0.9, a=110); im.alpha_composite(g)
    d = ImageDraw.Draw(im); d.ellipse((c - r, c - r, c + r, c + r), fill=(7, 8, 12, 235), outline=V.EDGE + (255,), width=4)
    for i in range(12):
        a = np.radians(i * 30); r0 = r - (18 if i % 3 == 0 else 11)
        d.line([(c + r0 * np.sin(a), c - r0 * np.cos(a)), (c + (r - 6) * np.sin(a), c - (r - 6) * np.cos(a))], fill=V.LAV + (255,), width=4 if i % 3 == 0 else 2)
    for ang, ln, w_, col in ((np.radians(305), r * 0.48, 7, (235, 238, 255)), (np.radians(60), r * 0.72, 5, (235, 238, 255))):
        d.line([(c, c), (c + ln * np.sin(ang), c - ln * np.cos(ang))], fill=col + (255,), width=w_)
    sa = np.radians(int(t * 6) * 6)                                                                      # the seconds hand ticks
    d.line([(c - 18 * np.sin(sa), c + 18 * np.cos(sa)), (c + (r - 14) * np.sin(sa), c - (r - 14) * np.cos(sa))], fill=V.BTN + (255,), width=3)
    d.ellipse((c - 7, c - 7, c + 7, c + 7), fill=V.BTN + (255,)); return im

def spec_card():
    w, h = 900, 300; im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    c = M.glass(w, h, 44, fill=(9, 10, 15, 220), border=(255, 255, 255, 60)); d = ImageDraw.Draw(c)
    c.alpha_composite(V.mono("ON YOUR WRIST", 24, (200, 204, 220), 6), (46, 34))
    for i, (a, b) in enumerate((("Swiss chronograph", "40 mm"), ("Automatic", "leather strap"), ("Condition", "like new"))):
        y = 92 + i * 66; ta = R.text_layer(a, R.font(38, 600), WHITE); tb = R.text_layer(b, R.font(36, 500), (190, 194, 210))
        c.alpha_composite(ta, (46, y)); c.alpha_composite(tb, (w - 46 - tb.width, y + 2))
        if i < 2: d.line([(46, y + 58), (w - 46, y + 58)], fill=(255, 255, 255, 26), width=2)
    im.alpha_composite(c, (40, 40)); return im
SPEC_IM = spec_card()

def prov_card(n):
    w, h = 900, 330; im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((40, 40, w + 40, h + 40), radius=44, fill=(94, 108, 255, 120)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26)))
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=44, fill=(9, 10, 15, 230), outline=V.EDGE + (255,), width=3)
    z = V.zmark(30); c.alpha_composite(z, (46, 34)); c.alpha_composite(V.mono("HOW YOU GOT IT  ·  PROVENANCE", 24, V.LAV, 5), (88, 36))
    rows = (("21:58", "14 bidders in the Vault", False), ("21:59:56", "Your bid · $4,250", False), ("22:00", "Hammer fell · yours", True))
    for i, (tm, tx, last) in enumerate(rows[:n]):
        y = 96 + i * 74
        if last:
            m = Image.new("L", (w - 60, 64), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 61, 63), radius=32, fill=255)
            hl = Image.new("RGBA", (w - 60, 64), (0, 0, 0, 0)); hl.paste(V.lin_grad(w - 60, 64, V.BLUE, V.BTN, 90), (0, 0), m); c.alpha_composite(hl, (30, y - 8))
        c.alpha_composite(V.mono(tm, 26, WHITE if last else V.LAV, 2), (52, y + 6))
        tl = R.text_layer(tx, R.font(36, 700 if last else 600), WHITE); c.alpha_composite(tl, (250, y))
        d.ellipse((222, y + 18, 236, y + 32), fill=(255, 255, 255, 255) if last else V.EDGE + (255,))
        if i < n - 1: d.line([(229, y + 34), (229, y + 74)], fill=V.EDGE + (200,), width=3)
    im.alpha_composite(c, (40, 40)); return im
PROV = [prov_card(n) for n in range(4)]

def frame(t):
    if t >= CLIP: return V.vault_end_card(t - CLIP, ["Every watch", "has a story.", "Make yours live."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = V.vault_grade(fr)
    im = hold_zoom(im, t, SHOT, 7.0, HOLD, 1.07, (540, 640))
    if t >= BEAT[0] - 0.1:                                                                               # the edge beats like a heart, then stays lit
        base = 0.55 * R.ease_out((t - BEAT[0]) / 0.6); beat = sum(np.exp(-((t - b) / 0.09) ** 2) for b in BEAT)
        V.lit_edge(im, min(1.0, base + 0.9 * beat) if t < 4.0 else min(1.0, 0.55 + 0.45 * R.ease_out((t - 4.0) / 1.5)), t)
    if DIAL0 <= t < SPEC + 0.3:                                                                          # what makes a watch special
        R.paste_center(im, dial(t), W / 2, 260, R.clamp((t - DIAL0) / 0.4) * (1 - R.clamp((t - SPEC) / 0.3)), 0.9 + 0.1 * R.ease_out((t - DIAL0) / 0.5))
    if SPEC <= t < FLIP + 0.15:                                                                          # on your wrist
        k = R.ease_out((t - SPEC) / 0.4); sx = 1 - R.clamp((t - FLIP) / 0.15)
        c = SPEC_IM if sx >= 1 else SPEC_IM.resize((max(1, int(SPEC_IM.width * sx)), SPEC_IM.height))
        R.paste_center(im, c, W / 2, 270 + (1 - k) * -40, R.clamp((t - SPEC) / 0.2))
    if t >= FLIP + 0.15:                                                                                 # how you got it
        n = sum(t >= r for r in ROWS); sx = R.ease_out((t - FLIP - 0.15) / 0.2); c = PROV[n]
        c = c if sx >= 1 else c.resize((max(1, int(c.width * sx)), c.height))
        R.paste_center(im, c, W / 2, 285, 1 - R.clamp((t - (CLIP - 0.5)) / 0.3))
        if t >= ROWS[2]: sparkle_burst(im, t, ROWS[2] + 0.05, W / 2 + 330, 420, ((-60, -40, 26), (60, -50, 18), (50, 40, 26)))
    draw_caps(im, t, CAPS, y=1700, size=60)
    if t > CLIP - XF: im = Image.blend(im, Image.new("RGBA", (W, H), V.STAGE + (255,)), R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = V.VaultMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        V.pad(mx, 0.0, CLIP, ((73.4, .3), (110, .2), (146.8, .18), (185, .08)), 0.045, 1.0)
        V.ticks(mx, DIAL0, 2.6, 6, 0.03)
        for b in BEAT: y = mx.tt(0.2); mx.fadd(np.sin(2 * np.pi * 55 * y) * np.exp(-y * 20), b, 0.3)        # heartbeat on 'Mmm'
        V.chime(mx, SPEC - 0.05, 1046.5, 0.04)
        mx.whoosh(FLIP - 0.05, 0.3, 0.14)
        for i, r in enumerate(ROWS[:2]): y = mx.tt(0.04); mx.fadd(np.sin(2 * np.pi * 2400 * y) * np.exp(-y * 90), r, 0.03)
        V.lock(mx, 7.42, 0.28); V.chime(mx, 7.48, 1318.5, 0.08)                                           # after 'got it'
        mx.write("s5story_audio.wav")
    render(frame, TOTAL, "s5story_audio.wav", OUT)
