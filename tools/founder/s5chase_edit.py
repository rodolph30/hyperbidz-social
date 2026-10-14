"""Season 5 (the Vault) Ep. 1 'Worth the chase'. Two of the owner's clips cut together: at the boutique counter, chin
on hand, as the camera starts to push in; then behind the glass case, dissolving to his close-up for the line.
Black-stage Vault grade. Cold open: the members' seal and 'SEASON 5 · THE VAULT'. A Vault lot is live: the timer races
down in the corner and TOP BID chips chase each other (Nadim, Karim, Rita…). On the close-up the lit gradient edge
ignites and the lot card rises. On 'worth the chase' he takes the lead (YOU · $4,000, the card turns green), the timer
runs out and the hammer falls: 'You won it'. Last shot held with a slow push-in. Vault end card."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from founder_common import *
import s5_common as V

OUT = sys.argv[1]; SHOT = 9.7; HOLD = 1.4; CLIP = SHOT + HOLD; XF = 0.45; END = 3.9; TOTAL = CLIP + END
FR = decode()
CUT, CLOSE, LEAD, HAMMER = 2.6, 5.45, 7.85, 9.12
CAPS = [(6.45, 7.80, ["Some things are…"]), (7.80, 10.95, ["worth the [chase.]"])]
BIDS = [(1.0, "N", "Nadim", 3598, (53, 126, 221)), (2.1, "K", "Karim", 3698, (109, 77, 255)), (3.3, "R", "Rita", 3800, (221, 92, 140)), (4.45, "N", "Nadim", 3900, (53, 126, 221))]
CHIPS = [V.bid_chip(i, f"{n} bid ${a:,}", "top", c) for _, i, n, a, c in BIDS]
YOU_CHIP = V.bid_chip("R", "You lead at $4,000", "you", (109, 77, 255))
SEAL = V.seal(120); SEASON = V.mono_pill("SEASON 5  ·  THE VAULT", 30); PILL = V.vault_pill()
WON = V.won_strip("9:41 PM", "$4,000")

def secs(t): return max(0, int(np.ceil((HAMMER - t) * 3.1)))
def card(t):
    nb = sum(t >= b[0] for b in BIDS); lead = t >= LEAD
    price = 4000 if lead else BIDS[nb - 1][3]; n = 9 + nb + (1 if lead else 0)
    return V.lot_card("Swiss Chronograph on Leather Strap", f"${price:,}", f"YOUR BID · {n} BIDS" if lead else f"CURRENT BID · {n} BIDS",
                      None, border=(52, 199, 123) if lead else V.EDGE, label_col=V.GREEN if lead else (255, 255, 255))

def frame(t):
    if t >= CLIP: return V.vault_end_card(t - CLIP, ["Some things are", "worth the chase."], END)
    fr = FR[min(len(FR) - 1, int(min(t, SHOT - 0.01) * FPS))]
    im = V.vault_grade(fr)
    if t < 0.5: im = Image.blend(Image.new("RGBA", (W, H), V.STAGE + (255,)), im, R.ease_out(t / 0.5))       # cold open from the black stage
    im = hold_zoom(im, t, SHOT, 8.7, HOLD, 1.07, (540, 760))
    if t >= 5.0: V.lit_edge(im, R.ease_out((t - 5.0) / 0.5), t)                                          # the Vault lights up
    if t < 2.5:                                                                                          # cold open: the seal
        a = R.clamp((t - 0.2) / 0.35) * (1 - R.clamp((t - 2.1) / 0.35))
        R.paste_center(im, SEAL, W / 2, 250, a, 1.25 - 0.25 * R.ease_out((t - 0.2) / 0.5))
        R.paste_center(im, SEASON, W / 2, 400, R.clamp((t - 0.55) / 0.35) * (1 - R.clamp((t - 2.1) / 0.35)))
    if 2.35 <= t < CLOSE + 0.3:
        R.paste_center(im, PILL, 290, 150, R.clamp((t - 2.35) / 0.3) * (1 - R.clamp((t - CLOSE) / 0.3)))
    if 0.9 <= t < SHOT + 0.2:                                                                            # the clock
        s = secs(t); R.paste_center(im, V.timer_chip(f"0:{s:02d}", hot=s <= 10), 900, 150, R.clamp((t - 0.9) / 0.25) * (1 - R.clamp((t - HAMMER - 0.4) / 0.3)))
    if t < CLOSE + 0.3:                                                                                  # bids chasing each other
        shown = [(b[0], c) for b, c in zip(BIDS, CHIPS) if t >= b[0]][-3:]
        for j, (at, ch) in enumerate(reversed(shown)):
            k = R.ease_out((t - at) / 0.3); x = W - 40 - ch.width / 2 + (1 - k) * 200
            R.paste_center(im, ch, x, 270 + j * 84, R.clamp((t - at) / 0.15) * (1 - 0.3 * j) * (1 - R.clamp((t - CLOSE) / 0.3)), 1 + 0.06 * (1 - R.clamp((t - at - 0.3) / 0.2)) if j == 0 else 1.0)
    if CLOSE <= t < HAMMER + 0.35:                                                                       # the lot card rises
        k = R.ease_out((t - CLOSE) / 0.45); c = card(t); out = R.clamp((t - HAMMER) / 0.3)
        pop = 1 + 0.04 * (1 - R.clamp((t - LEAD) / 0.25)) if t >= LEAD else 1.0
        R.paste_center(im, c, W / 2, 1560 + (1 - k) * 160, R.clamp((t - CLOSE) / 0.2) * (1 - out), pop * (1 - 0.06 * out))
    if LEAD <= t < CLIP:
        s = (t - LEAD) / 0.3; R.paste_center(im, YOU_CHIP, 40 + YOU_CHIP.width / 2, 150, R.clamp(s * 3) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), 0.85 + 0.15 * R.stamp(s) if s < 1 else 1.0)
    if t >= HAMMER:                                                                                      # the hammer falls
        s = (t - HAMMER) / 0.32; R.paste_center(im, WON, W / 2, 1560, R.clamp(s * 3) * (1 - R.clamp((t - (CLIP - 0.5)) / 0.3)), 1.3 - 0.3 * R.stamp(s) if s < 1 else 1.0)
        sparkle_burst(im, t, HAMMER + 0.1, W / 2 + 330, 1470, ((-80, -40, 26), (80, -50, 18), (60, 40, 26)))
    draw_caps(im, t, CAPS, y=1810 if t >= CLOSE else 1700, size=58)
    if HAMMER <= t < HAMMER + 0.08: im = M.flash(im, 0.22, (220, 210, 255))
    if t > CLIP - XF: im = Image.blend(im, Image.new("RGBA", (W, H), V.STAGE + (255,)), R.ease_out((t - (CLIP - XF)) / XF))
    return im.convert("RGB")

if __name__ == "__main__":
    if "--stills" not in sys.argv:
        mx = V.VaultMix(CLIP, END, pad_freqs=((146.8, 0.0),))
        V.pad(mx, 0.0, CLIP, ((73.4, .35), (110, .25), (146.8, .2), (174.6, .1)), 0.05, 1.2)              # D minor, deep and slow
        V.ticks(mx, 0.0, HAMMER, 6, 0.03)
        V.chime(mx, 0.25, 1174.7, 0.05)
        for i, (at, *_ ) in enumerate(BIDS): mx.ping(at + 0.03, 880 * 2 ** (i * 2 / 12), 0.04)
        mx.whoosh(4.85, 0.6, 0.18); V.chime(mx, 5.05, 1567.98, 0.04)
        V.lock(mx, HAMMER + 0.02, 0.4); V.chime(mx, HAMMER + 0.1, 1318.5, 0.08); V.pad(mx, HAMMER, CLIP, ((146.8, .3), (185, .22), (220, .2), (277.2, .1)), 0.05, 0.3)
        mx.write("s5chase_audio.wav")
    render(frame, TOTAL, "s5chase_audio.wav", OUT)
