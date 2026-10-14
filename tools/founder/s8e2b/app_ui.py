"""HyperBidz listing screen, rebuilt from the app's own screens (flows doc, C1 'Bidding, outbid, strike back, hammer')
at 1080 px wide: status bar, hero photo with back / seller / wallet chips, the white sheet with title, meta, the live
bid card (status pill, LIVE, CURRENT BID, ENDS IN, progress, bids-in-the-last-5-min, bid rows with TOP BID, All N bids),
description, and the bottom bar (Watch, Ask, primary CTA: red Re-bid / green Raise your max). Plus the hammer screen
'You won it'. Fonts: Space Grotesk + Space Mono, as in the app."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R

S = 1080 / 420                                     # screenshot points → pixels
INK = (11, 14, 20); MUTED = (95, 102, 115); LINE = (227, 229, 234); BRAND = (109, 77, 255); WHITE = (255, 255, 255)
SHEET = (241, 241, 244); CARD = (250, 250, 251); CARD_EDGE = (228, 229, 234)
G_BG = (219, 244, 231); G = (0, 157, 98); G_TX = (0, 122, 78)
L_BG = (237, 233, 254); L_TX = (98, 72, 234)
LIVE = (236, 64, 86); RED = (226, 50, 70); TAG_BG = (234, 230, 253); TAG_TX = (112, 92, 224)
AV = {"You": (103, 72, 254), "Ralph": (167, 150, 240), "Abir": (40, 168, 110), "Karim": (240, 150, 60), "Nadine": (221, 92, 140), "Tarek": (240, 150, 60), "Maya": (40, 168, 110)}
HERO = None

def p(v): return int(round(v * S))
def gt(t, size, w=700, col=INK): return R.text_layer(t, R.font(p(size), w), col)
def mt(t, size, col=MUTED, tr=None): return R.text_layer(t, R.font(p(size), mono=True), col, tracking=tr if tr is not None else max(2, p(size) // 5))
def rr(d, box, r, fill=None, outline=None, width=1): d.rounded_rectangle([int(v) for v in box], radius=int(r), fill=fill, outline=outline, width=width)

def money(v): return f"${v:,}"

def status_bar(im, y=0, t="14:04"):
    d = ImageDraw.Draw(im); im.alpha_composite(gt(t, 15, 600, WHITE), (p(26), y + p(12)))
    x = im.width - p(28); d.rounded_rectangle((x - p(24), y + p(17), x, y + p(28)), radius=p(3), fill=WHITE)     # battery
    for i in range(3): r = p(4 + i * 3.2); cx, cy = x - p(40), y + p(29); d.arc((cx - r, cy - r, cx + r, cy + r), 225, 315, fill=WHITE, width=p(1.8))
    for i in range(4): d.ellipse((x - p(76) + i * p(5.5), y + p(21), x - p(73) + i * p(5.5), y + p(24)), fill=(150, 150, 150))
    d.ellipse((im.width / 2 - p(6), y + p(15), im.width / 2 + p(6), y + p(27)), fill=(0, 0, 0))                          # the phone's punch-hole camera

def chip(text, icon=None, h=36):
    tl = gt(text, 13.5, 600, WHITE); w = tl.width + p(26) + (p(26) if icon else 0)
    im = Image.new("RGBA", (w, p(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rr(d, (0, 0, w - 1, p(h) - 1), p(h) / 2, fill=(20, 22, 28, 200), outline=(255, 255, 255, 40), width=2)
    x = p(10)
    if icon is not None: im.alpha_composite(icon, (x, (p(h) - icon.height) // 2)); x += icon.width + p(6)
    im.alpha_composite(tl, (x, (p(h) - tl.height) // 2 - 2)); return im

def disc(letter, col, s, txt=WHITE):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((0, 0, s - 1, s - 1), fill=col + (255,))
    tl = R.text_layer(letter, R.font(int(s * 0.38), 600), txt); im.alpha_composite(tl, ((s - tl.width) // 2, (s - tl.height) // 2 - 2)); return im

def zcoin(s):
    import s5_common as V
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((0, 0, s - 1, s - 1), fill=BRAND + (255,))
    z = V.zflat(int(s * 0.6), WHITE); im.alpha_composite(z, ((s - z.width) // 2, (s - z.height) // 2)); return im

def hero(im, top_h, wallet=706.19):
    global HERO
    if HERO is None: HERO = Image.open("hero.png").convert("RGBA")
    h = HERO.resize((im.width, int(HERO.height * im.width / HERO.width)))
    off = max(0, h.height - top_h - p(10)) // 2
    im.alpha_composite(h.crop((0, off, im.width, off + top_h + p(30))), (0, 0))
    sb = Image.new("RGBA", (im.width, p(60)), (0, 0, 0, 0)); sb.putalpha(Image.linear_gradient("L").rotate(180).resize((im.width, p(60))).point(lambda v: int(v * 0.45)))
    im.alpha_composite(Image.new("RGBA", (im.width, p(60)), (0, 0, 0, 255)).copy() if False else sb)
    status_bar(im)
    d = ImageDraw.Draw(im); y = p(70)
    d.ellipse((p(14), y, p(14) + p(36), y + p(36)), fill=(20, 22, 28, 200)); d.line([(p(35), y + p(11)), (p(28), y + p(18)), (p(35), y + p(25))], fill=WHITE, width=p(2.2), joint="curve")
    im.alpha_composite(chip("Rodolph", disc("R", (16, 16, 20), p(24))), (p(56), y))
    w = chip(f"${wallet:,.2f}", zcoin(p(24))); im.alpha_composite(w, (im.width - w.width - p(14), y))
    pill = Image.new("RGBA", (p(150), p(36)), (0, 0, 0, 0)); dp = ImageDraw.Draw(pill); rr(dp, (0, 0, pill.width - 1, pill.height - 1), p(18), fill=(20, 22, 28, 170), outline=(255, 255, 255, 40), width=2)
    for i in range(4):                                                                                 # expand · sound · share · flag
        cx, cy = p(22) + i * p(36), p(18); c = (235, 235, 240)
        if i == 0: dp.line([(cx - p(6), cy + p(6)), (cx + p(6), cy - p(6))], fill=c, width=p(1.5)); dp.line([(cx + p(1), cy - p(6)), (cx + p(6), cy - p(6)), (cx + p(6), cy - p(1))], fill=c, width=p(1.5))
        if i == 1: dp.polygon([(cx - p(6), cy - p(3)), (cx - p(2), cy - p(3)), (cx + p(3), cy - p(7)), (cx + p(3), cy + p(7)), (cx - p(2), cy + p(3)), (cx - p(6), cy + p(3))], outline=c, width=p(1.4))
        if i == 2:
            for (a, b) in ((-6, 0), (5, -6), (5, 6)): dp.ellipse((cx + p(a) - p(2.5), cy + p(b) - p(2.5), cx + p(a) + p(2.5), cy + p(b) + p(2.5)), outline=c, width=p(1.3))
            dp.line([(cx - p(4), cy - p(1)), (cx + p(3), cy - p(5))], fill=c, width=p(1.2)); dp.line([(cx - p(4), cy + p(1)), (cx + p(3), cy + p(5))], fill=c, width=p(1.2))
        if i == 3: dp.line([(cx - p(5), cy - p(7)), (cx - p(5), cy + p(8))], fill=c, width=p(1.5)); dp.polygon([(cx - p(5), cy - p(7)), (cx + p(6), cy - p(4)), (cx - p(5), cy)], outline=c, width=p(1.4))
    im.alpha_composite(pill, (im.width - pill.width - p(14), top_h - p(48)))

def roll_number(old, new, k, size, col):
    """the current bid rolling up inside a tight window: old slides up and out, new slides in from below"""
    a = gt(old, size, 700, col); b = gt(new, size, 700, col); bb = b.getchannel("A").getbbox() or (0, 0, b.width, b.height)
    top, bot = bb[1] - 6, bb[3] + 6; vh = bot - top; w = max(a.width, b.width)
    im = Image.new("RGBA", (w + 4, b.height), (0, 0, 0, 0)); e = 1 - (1 - min(1, max(0, k))) ** 3
    view = Image.new("RGBA", (w + 4, vh), (0, 0, 0, 0))
    if e < 1: view.alpha_composite(a, (0, int(-top - vh * e)))
    if e > 0: view.alpha_composite(b, (0, int(-top + vh * (1 - e))))
    im.alpha_composite(view, (0, top)); return im

def listing(st, H=1920, top_h=None):
    """st: dict with leader, cur, prev_cur, roll_k, timer, timer_hot, rows [(name, amount, when, new_k)], nbids, recent,
    cta ('rebid'|'raise'), cta_amt, press, flash (0..1 card glow), time_added (0..1)"""
    im = Image.new("RGBA", (1080, H), SHEET + (255,)); top_h = top_h or (p(270) if H > 2100 else p(205))
    hero(im, top_h)
    sh = Image.new("RGBA", (1080, H - top_h), (0, 0, 0, 0)); rr(ImageDraw.Draw(sh), (0, 0, 1079, H - top_h + p(30)), p(20), fill=SHEET + (255,)); im.alpha_composite(sh, (0, top_h))
    y0 = top_h; d = ImageDraw.Draw(im)
    im.alpha_composite(gt("Camera Lens Kit with Prime Lenses", 16.5, 700), (p(16), y0 + p(17)))
    dt = gt("Details  ›", 12, 600, L_TX); im.alpha_composite(dt, (1080 - dt.width - p(16), y0 + p(21)))
    im.alpha_composite(mt("#5599  ·  NEW  ·  NO RESERVE", 9.5, (150, 152, 160)), (p(16), y0 + p(44)))
    # the bid card
    rows = st["rows"]; nrows = len(rows); cy0 = y0 + p(70); ch = p(168) + p(46) * nrows + p(34)
    card = Image.new("RGBA", (p(380) + 40, ch + 40), (0, 0, 0, 0)); dc = ImageDraw.Draw(card)
    if st.get("flash", 0) > 0.01:
        gl = Image.new("RGBA", card.size, (0, 0, 0, 0)); rr(ImageDraw.Draw(gl), (14, 14, card.width - 14, card.height - 14), p(18), fill=BRAND + (int(150 * st["flash"]),)); card.alpha_composite(gl.filter(ImageFilter.GaussianBlur(12)))
    rr(dc, (20, 20, 20 + p(380), 20 + ch), p(18), fill=CARD + (255,), outline=CARD_EDGE + (255,), width=3)
    ox, oy = 20 + p(14), 20
    you = st["leader"] == "You"
    ptxt = "You're leading" if you else f"{st['leader']} leads"; pbg, pfg = (G_BG, G_TX) if you else (L_BG, L_TX)
    pt = gt(ptxt, 12.5, 600, pfg); pw = pt.width + p(34); rr(dc, (ox, oy + p(14), ox + pw, oy + p(40)), p(13), fill=pbg + (255,))
    dc.ellipse((ox + p(11), oy + p(24), ox + p(17), oy + p(30)), fill=(G if you else L_TX) + (255,)); card.alpha_composite(pt, (ox + p(24), oy + p(27) - pt.height // 2 - 2))
    lv = mt("LIVE", 10.5, LIVE, 4); card.alpha_composite(lv, (ox + p(352) - lv.width, oy + p(21))); dc.ellipse((ox + p(352) - lv.width - p(11), oy + p(25), ox + p(352) - lv.width - p(5), oy + p(31)), fill=LIVE + (255,))
    card.alpha_composite(mt("CURRENT BID", 9, (130, 132, 140), 4), (ox, oy + p(53)))
    num = roll_number(money(st["prev_cur"]), money(st["cur"]), st["roll_k"], 27, INK); card.alpha_composite(num, (ox - 4, oy + p(64)))
    el = mt("ENDS IN", 9, (130, 132, 140), 4); card.alpha_composite(el, (ox + p(352) - el.width, oy + p(62)))
    tm = gt(st["timer"], 21, 700, (L_TX if st.get("timer_hot") else INK)); card.alpha_composite(tm, (ox + p(352) - tm.width, oy + p(74)))
    by = oy + p(112); rr(dc, (ox, by, ox + p(352), by + p(4)), p(2), fill=(231, 232, 236, 255))
    rr(dc, (ox, by, ox + p(352) * st.get("progress", 0.05), by + p(4)), p(2), fill=BRAND + (255,))
    bolt = Image.new("RGBA", (p(12), p(14)), (0, 0, 0, 0)); ImageDraw.Draw(bolt).polygon([(p(7), 0), (0, p(8)), (p(5), p(8)), (p(4), p(14)), (p(12), p(5)), (p(7), p(5))], fill=(250, 176, 40, 255))
    card.alpha_composite(bolt, (ox, oy + p(124))); card.alpha_composite(gt(f"{st['recent']} bids in the last 5 min", 11.5, 500, MUTED), (ox + p(18), oy + p(121)))
    dc.line([(ox, oy + p(146)), (ox + p(352), oy + p(146))], fill=LINE + (255,), width=2)
    for i, (name, amt, when, nk) in enumerate(rows):                                                   # bid rows (newest on top)
        ry = oy + p(152) + i * p(46) - int((1 - min(1, nk)) * p(46)) * (1 if i > 0 else 0)
        a = min(1, nk * 1.6) if i == 0 else 1
        rowl = Image.new("RGBA", (p(372), p(44)), (0, 0, 0, 0)); dr = ImageDraw.Draw(rowl)
        if i == 0 and nk < 1.6: rr(dr, (0, p(2), p(372), p(42)), p(10), fill=BRAND + (int(40 * max(0, 1 - (nk - 0.4))),))
        av = disc(name[0], AV[name], p(30)); rowl.alpha_composite(av, (p(4), p(7)))
        nm = gt(name, 14.5, 600, L_TX if name == "You" else INK); rowl.alpha_composite(nm, (p(44), p(22) - nm.height // 2 - 2)); x = p(44) + nm.width + p(8)
        if i == 0:
            tg = mt("TOP BID", 9, TAG_TX, 3); tw = tg.width + p(14); rr(dr, (x, p(13), x + tw, p(31)), p(5), fill=TAG_BG + (255,)); rowl.alpha_composite(tg, (x + p(7), p(15))); x += tw + p(8)
        rowl.alpha_composite(gt(when, 11, 500, (130, 132, 140)), (x, p(15)))
        am = gt(money(amt), 14.5, 700, G if (name == "You" and i == 0) else INK); rowl.alpha_composite(am, (p(362) - am.width, p(22) - am.height // 2 - 2))
        if a < 1: rowl.putalpha(rowl.getchannel("A").point(lambda v: int(v * a)))
        card.alpha_composite(rowl, (ox - p(4), ry))
    ay = oy + p(152) + nrows * p(46) + p(4); rr(dc, (ox, ay, ox + p(352), ay + p(36)), p(12), fill=(234, 235, 239, 255))
    card.alpha_composite(gt(f"All {st['nbids']} bids", 12, 600, INK), (ox + p(12), ay + p(9))); op = mt("OPENED  $769", 9.5, (130, 132, 140), 3); card.alpha_composite(op, (ox + p(326) - op.width, ay + p(12))); vx, vy = ox + p(338), ay + p(16); dc.line([(vx - p(4), vy), (vx, vy + p(4)), (vx + p(4), vy)], fill=(130, 132, 140, 255), width=p(1.5), joint="curve")
    im.alpha_composite(card, (p(20) - 20, cy0 - 20))
    if st.get("time_added", 0) > 0.01:                                                                  # anti-snipe
        k = st["time_added"]; ta = mt("TIME ADDED!", 11, WHITE, 4); w = ta.width + p(26); t2 = Image.new("RGBA", (w, p(26)), (0, 0, 0, 0)); rr(ImageDraw.Draw(t2), (0, 0, w - 1, p(26) - 1), p(13), fill=G + (255,)); t2.alpha_composite(ta, (p(13), p(5)))
        R.paste_center(im, t2, 1080 / 2, cy0 - p(2), min(1, k * 3) * (1 - max(0, k - 0.8) * 5), 0.9 + 0.1 * min(1, k * 3))
    # description
    dy = cy0 + ch + p(26); im.alpha_composite(gt("Description", 14, 700), (p(16), dy))
    for i, ln in enumerate(("Photography kit for a hobbyist stepping up: a", "mirrorless body with prime lenses, including a", "50mm f1.8 and an 85mm portrait prime. Glass is", "clean with no fungus, haze or scratches.")):
        im.alpha_composite(gt(ln, 12.5, 400, (125, 128, 136)), (p(16), dy + p(26) + i * p(19)))
    # bottom bar
    bb = H - p(96); fd = Image.new("RGBA", (1080, p(30)), SHEET + (0,)); fd.putalpha(Image.linear_gradient("L").resize((1080, p(30)))); im.alpha_composite(fd, (0, bb - p(30)))
    bar = Image.new("RGBA", (1080, H - bb), SHEET + (255,)); im.alpha_composite(bar, (0, bb))
    for i, (lab, kind) in enumerate((("Watch", "heart"), ("Ask", "q"))):
        x = p(16) + i * p(66); rr(d, (x, bb + p(10), x + p(56), bb + p(66)), p(14), fill=WHITE + (255,), outline=(226, 227, 231, 255), width=2); cx = x + p(28)
        if kind == "heart":
            hp = [(cx, bb + p(36)), (cx - p(9), bb + p(27)), (cx - p(7), bb + p(21)), (cx - p(2), bb + p(21)), (cx, bb + p(24)), (cx + p(2), bb + p(21)), (cx + p(7), bb + p(21)), (cx + p(9), bb + p(27))]
            d.line(hp + [hp[0]], fill=INK + (255,), width=p(1.6), joint="curve")
        else:
            d.ellipse((cx - p(9), bb + p(19), cx + p(9), bb + p(37)), outline=INK + (255,), width=p(1.6)); qt = gt("?", 12, 700); im.alpha_composite(qt, (cx - qt.width // 2, bb + p(20)))
            d.ellipse((x + p(46), bb + p(6), x + p(58), bb + p(18)), fill=TAG_BG + (255,)); one = gt("1", 8, 700, TAG_TX); im.alpha_composite(one, (x + p(52) - one.width // 2, bb + p(6)))
        lb = gt(lab, 10, 600, MUTED); im.alpha_composite(lb, (cx - lb.width // 2, bb + p(44)))
    cx0, cx1 = p(148), p(404); cta = st["cta"]; pr = st.get("press", 0)
    btn = Image.new("RGBA", (cx1 - cx0, p(56)), (0, 0, 0, 0)); db = ImageDraw.Draw(btn)
    if cta == "rebid":
        rr(db, (0, 0, btn.width - 1, btn.height - 1), p(14), fill=RED + (255,)); l1 = gt(f"Re-bid {money(st['cta_amt'])} now", 14.5, 700, WHITE)
        l2 = gt(f"+$23 · holds ${st['cta_amt'] * 0.025:,.2f}, back if outbid", 10, 500, (255, 225, 230))
    else:
        rr(db, (0, 0, btn.width - 1, btn.height - 1), p(14), fill=(222, 246, 236, 255), outline=(52, 168, 120, 255), width=3); l1 = gt("Raise your max", 14.5, 700, G_TX)
        l2 = gt(f"You're top bidder · ${st['cur'] * 0.025:,.2f} held", 10, 500, G_TX)
    btn.alpha_composite(l1, ((btn.width - l1.width) // 2, p(8))); btn.alpha_composite(l2, ((btn.width - l2.width) // 2, p(31)))
    R.paste_center(im, btn, (cx0 + cx1) / 2, bb + p(38), 1.0, 1 - 0.05 * pr)
    if pr > 0.01:                                                                                        # tap ring
        rg = Image.new("RGBA", (p(120), p(120)), (0, 0, 0, 0)); r = p(20) + p(30) * pr; c = p(60)
        ImageDraw.Draw(rg).ellipse((c - r, c - r, c + r, c + r), outline=(255, 255, 255, int(220 * (1 - pr))), width=p(2.5)); R.paste_center(im, rg, (cx0 + cx1) / 2, bb + p(38))
    d.rounded_rectangle((1080 / 2 - p(68), H - p(10), 1080 / 2 + p(68), H - p(6)), radius=p(2), fill=INK + (255,))     # home indicator
    return im

def won(k, amount=1045, H=1920):
    """the hammer screen, 'You won it' (C1 step 9)"""
    im = Image.new("RGBA", (1080, H), (0, 0, 0, 0)); g = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([78, 50, 222.]), np.array([108, 80, 250.]); arr = top * (1 - g) + bot * g
    im = Image.fromarray(np.repeat(arr[:, None, :], 1080, 1).reshape(H, 1080, 3).astype(np.uint8)).convert("RGBA")
    status_bar(im)
    def put(layer, x, y, a):
        if a <= 0.01: return
        l = layer.copy(); l.putalpha(l.getchannel("A").point(lambda v: int(v * min(1, a)))); im.alpha_composite(l, (int(x), int(y)))
    e = lambda t0: max(0.0, min(1.0, (k - t0) / 0.35))
    put(mt("HAMMER FELL  2:10:14 PM", 9.5, (225, 220, 255), 4), p(20), p(70), e(0))
    cl = Image.new("RGBA", (1080, p(100)), (0, 0, 0, 0)); ImageDraw.Draw(cl).ellipse((1080 - p(46), p(60), 1080 - p(16), p(90)), fill=(255, 255, 255, 60)); im.alpha_composite(cl); d = ImageDraw.Draw(im); d.line([(1080 - p(36), p(70)), (1080 - p(26), p(80))], fill=WHITE, width=p(1.6)); d.line([(1080 - p(26), p(70)), (1080 - p(36), p(80))], fill=WHITE, width=p(1.6))
    yy = H * 0.36
    for i, w in enumerate(("You", "won it")): put(gt(w, 46, 700, WHITE), p(20), yy + i * p(50) + (1 - e(0.05 + 0.1 * i)) * 30, e(0.05 + 0.1 * i))
    put(mt("CAMERA LENS KIT WITH PRIME LENSES  #5599", 9, (225, 220, 255), 3), p(20), yy + p(118), e(0.3))
    put(gt(money(amount), 27, 700, WHITE), p(20), yy + p(134), e(0.35))
    put(gt(f"Winner fee ${amount * 0.025:,.2f} paid · {money(amount)} due in 71:59:59", 11, 500, (225, 220, 255)), p(20), yy + p(172), e(0.4))
    by = H - p(190)
    b1 = Image.new("RGBA", (p(380), p(48)), (0, 0, 0, 0)); rr(ImageDraw.Draw(b1), (0, 0, b1.width - 1, b1.height - 1), p(14), fill=WHITE + (255,)); t1 = gt("Complete your win", 15, 700, (40, 24, 140)); b1.alpha_composite(t1, ((b1.width - t1.width) // 2, (b1.height - t1.height) // 2 - 3)); put(b1, p(20), by, e(0.5))
    for i, s in enumerate(("Message Rodolph", "View lot")):
        b = Image.new("RGBA", (p(185), p(44)), (0, 0, 0, 0)); rr(ImageDraw.Draw(b), (0, 0, b.width - 1, b.height - 1), p(12), fill=(60, 36, 170, 255)); t = gt(s, 13, 600, WHITE); b.alpha_composite(t, ((b.width - t.width) // 2, (b.height - t.height) // 2 - 3)); put(b, p(20) + i * p(195), by + p(58), e(0.55))
    pk = gt("Pickup in person · arrange details with the seller", 10.5, 500, (225, 220, 255)); put(pk, (1080 - pk.width) / 2, by + p(116), e(0.6))
    d.rounded_rectangle((1080 / 2 - p(68), H - p(10), 1080 / 2 + p(68), H - p(6)), radius=p(2), fill=(255, 255, 255, 230))
    return im

def banner(k, title="You've been outbid", body="Abir bid $861 on Camera Lens Kit · Re-bid $884"):
    """iOS-style push notification from HyperBidz"""
    w, h = 1080 - 2 * p(10), p(70); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); rr(ImageDraw.Draw(im), (0, 0, w - 1, h - 1), p(20), fill=(246, 246, 248, 245))
    ic = Image.new("RGBA", (p(38), p(38)), (0, 0, 0, 0)); rr(ImageDraw.Draw(ic), (0, 0, p(38) - 1, p(38) - 1), p(9), fill=BRAND + (255,))
    import s5_common as V; z = V.zflat(p(24), WHITE); ic.alpha_composite(z, ((ic.width - z.width) // 2, (ic.height - z.height) // 2)); im.alpha_composite(ic, (p(14), p(16)))
    im.alpha_composite(gt("HYPERBIDZ", 9.5, 600, (120, 122, 130)), (p(62), p(10))); nw = gt("now", 10, 500, (120, 122, 130)); im.alpha_composite(nw, (w - nw.width - p(14), p(10)))
    im.alpha_composite(gt(title, 13, 700, INK), (p(62), p(25))); im.alpha_composite(gt(body, 11.5, 500, (60, 62, 70)), (p(62), p(45)))
    return im
