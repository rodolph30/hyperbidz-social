"""Story frames for the campaign survey (baseline before Lesson 01, endline after the last lesson).
The owner adds the Instagram sticker (poll / quiz / slider) in the dashed zone. Usage: python3 survey_frames.py <outdir> [baseline|endline]"""
import sys, os
OUT = os.path.abspath(sys.argv[1]); MODE = sys.argv[2] if len(sys.argv) > 2 else "baseline"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cast import *

def dashed(im, box, col=(167, 139, 250), a=140):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x0, y0, x1, y1 = box; L = 22
    d.rounded_rectangle(box, radius=34, fill=(12, 10, 20, 90))
    for x in range(x0 + 30, x1 - 30, L * 2): d.line([(x, y0), (x + L, y0)], fill=col + (a,), width=4); d.line([(x, y1), (x + L, y1)], fill=col + (a,), width=4)
    for y in range(y0 + 30, y1 - 30, L * 2): d.line([(x0, y), (x0, y + L)], fill=col + (a,), width=4); d.line([(x1, y), (x1, y + L)], fill=col + (a,), width=4)
    im.alpha_composite(lay)
    t = tl("sticker goes here", mono(24), col); put(im, t, (x0 + x1) / 2, (y0 + y1) / 2, 0.55)

def frame(n, total, kind, question, note=None, emoji_hint=None):
    im = app_stage(spot=(540, 820, 560, 640), spot_a=0.22)
    lt = tl("AUCTION CHECK", mono(24), MUTED_APP); put(im, lt, 540, 300)
    dots = Image.new("RGBA", (total * 34, 20), (0, 0, 0, 0)); d = ImageDraw.Draw(dots)
    for i in range(total): d.ellipse((i * 34 + 3, 3, i * 34 + 17, 17), fill=(VIOLET if i < n else (90, 80, 110)) + (255,))
    put(im, dots, 540, 352)
    chip_t = tl(kind.upper(), mono(24), LILAC); w, h = chip_t.width + 40, chip_t.height + 20
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, outline=LILAC + (150,), width=2); c.alpha_composite(chip_t, (20, 10))
    put(im, c, 540, 500)
    q = rich(question, 84, "serif", WHITE, LILAC, 900); put(im, q, 540, 550 + q.height / 2 + 40)
    if note: put(im, rich(note, 40, "sans", MUTE, LILAC, 880), 540, 470 + q.height + 140)
    dashed(im, (150, 1120, 930, 1500))
    return im.convert("RGB")

def cover(title, sub, foot):
    im = app_stage(spot=(540, 860, 560, 640), spot_a=0.3)
    for i, (x, n) in enumerate(((400, 14), (540, 27), (680, 8))): put(im, paddle(n, [BLUE, VIOLET, GREEN_APP][i], 110), x, 540)
    put(im, rich(title, 96, "serif", WHITE, LILAC, 920), 540, 820)
    put(im, rich(sub, 44, "sans", MUTE, LILAC, 860), 540, 1040)
    put(im, rich(foot, 40, "serif", LILAC, LILAC, 860), 540, 1500)
    return im.convert("RGB")

QS = [
    ("poll", "Have you ever bid in an [auction?]", "Yes / Never"),
    ("quiz", "In an auction, who decides the [final price?]", None),
    ("quiz", "In Lebanon, courts sell seized property at [public auction.] True or false?", None),
    ("quiz", "When you buy a share on a stock exchange, the price comes from…", None),
    ("slider", "How comfortable would you be [buying] something at an auction?", None),
    ("poll", "Would you use a live auction app [made for Lebanon?]", "Yes / Maybe / No"),
]
if MODE == "endline": QS.append(("poll", "Did you watch our [auction lessons?]", "Most of them / A few / No"))
os.makedirs(OUT, exist_ok=True)
if MODE == "baseline":
    cover("Quick [auction] check", f"{len(QS)} questions · 30 seconds · no googling", "Daily auction lessons start [tomorrow.]").save(f"{OUT}/{MODE}-00.jpg", quality=92)
else:
    cover("The [auction] check, again", f"{len(QS)} questions · let's see what changed", "Thank you for [learning with us.]").save(f"{OUT}/{MODE}-00.jpg", quality=92)
for i, (k, q, note) in enumerate(QS, 1):
    frame(i, len(QS), k, q, None).save(f"{OUT}/{MODE}-{i:02d}.jpg", quality=92)
print(OUT)
