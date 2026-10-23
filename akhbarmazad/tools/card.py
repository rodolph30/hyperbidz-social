"""akhbarmazad news card, broadcast style: one story (JSON) -> 1080x1920 PNG -> 12 s image Reel (MP4).

Usage:
  python3 akhbarmazad/tools/card.py akhbarmazad/posts/M001/story.json            # card.png + reel.mp4 next to it
  python3 akhbarmazad/tools/card.py story.json --png-only

Look (owner's reference, 23 Oct 2026: "it should look like news"): a TV "breaking news" frame. Red slanted
عاجل banner, a big white headline with a gold second line, a red rule and a small dateline, a gold-framed panel
with the item, a price bar, a ticker bar with who / which auction / when, the source, and red light streaks.

story.json fields (Arabic, right-to-left; Latin and number runs are isolated automatically):
  banner     default "عاجل"                     (the red banner word)
  headline   white line, e.g. "لوحة سيارة في دبي"    (1 line ideally, 2 max)
  highlight  gold line,  e.g. "بـ 55 مليون درهم"      (1 line)
  dateline   small line under the red rule, e.g. "مزاد الأرقام المميزة · دبي · أبريل 2023"
  visual     {"type": "plate", "style": "dubai"|"abudhabi"|"sharjah"|"ksa"|"generic", "code": "AA", "number": "8"}
             {"type": "phone", "number": "058 7777777", "label": "du"}
             {"type": "emoji", "name": "camel"}       (assets/emoji/<name>.png, Microsoft Fluent Emoji, MIT)
  tag        optional red stamp on the panel, e.g. "رقم قياسي", "مزاد خيري"
  kicker     price label, default "بيعت بـ"
  price      "55,000,000"   currency "درهم"   usd "نحو 15 مليون دولار" (optional)
  winner     ticker 1 (e.g. "مزايد لم يُكشف اسمه")   event  ticker 2 (e.g. "مزادات الإمارات")   date  ticker 3 (e.g. "أبريل 2023")
  source     "المصدر: ..."

Everything that matters sits inside the 3:4 grid crop (y 240..1680); the top and bottom bands are background only.
"""
import html, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # akhbarmazad/
REPO = os.path.dirname(ROOT)
FONTS = os.path.join(REPO, "tools", "lessons", "fonts")
EMOJI = os.path.join(ROOT, "assets", "emoji")

LATIN = re.compile(r"([A-Za-z0-9][A-Za-z0-9 .,+\-/&']*[A-Za-z0-9]|[A-Za-z0-9])")

GAVEL = """<svg viewBox="0 0 64 64" class="ico"><g fill="url(#gold)">
<rect x="5" y="16" width="38" height="16" rx="4" transform="rotate(-45 24 24)"/></g>
<line x1="30" y1="30" x2="55" y2="55" stroke="url(#gold)" stroke-width="7" stroke-linecap="round"/>
<rect x="4" y="54" width="30" height="7" rx="3.5" fill="url(#gold)"/></svg>"""
BARS = """<svg viewBox="0 0 64 64" class="ico"><g fill="url(#gold)"><rect x="8" y="38" width="12" height="20" rx="2"/>
<rect x="26" y="26" width="12" height="32" rx="2"/><rect x="44" y="12" width="12" height="46" rx="2"/></g></svg>"""
PEOPLE = """<svg viewBox="0 0 64 64" class="ico"><g fill="url(#gold)"><circle cx="32" cy="20" r="10"/>
<path d="M14 54c0-11 8-18 18-18s18 7 18 18z"/><circle cx="13" cy="26" r="7"/><path d="M0 54c0-8 5-13 12-13 3 0 5 1 7 2-4 3-7 7-8 11z"/>
<circle cx="51" cy="26" r="7"/><path d="M64 54c0-8-5-13-12-13-3 0-5 1-7 2 4 3 7 7 8 11z"/></g></svg>"""
CAL = """<svg viewBox="0 0 64 64" class="ico"><g fill="url(#gold)"><rect x="8" y="12" width="48" height="44" rx="6"/></g>
<rect x="14" y="26" width="36" height="24" rx="3" fill="#0A1222"/><g fill="url(#gold)"><rect x="18" y="6" width="6" height="12" rx="3"/>
<rect x="40" y="6" width="6" height="12" rx="3"/><rect x="19" y="31" width="8" height="7" rx="1.5"/><rect x="31" y="31" width="8" height="7" rx="1.5"/></g></svg>"""
DEFS = """<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#FFE7A3"/><stop offset=".55" stop-color="#E2AE4A"/><stop offset="1" stop-color="#A9741C"/></linearGradient></defs></svg>"""


def iso(text):
    """escape, then isolate Latin/number runs so they don't scramble the RTL line"""
    return LATIN.sub(lambda m: '<bdi dir="ltr">' + m.group(1) + "</bdi>", html.escape(text))


def font_faces():
    faces = []
    for fam, files in (("Cairo", {600: "Cairo-600", 700: "Cairo-700", 800: "Cairo-800", 900: "Cairo-900"}),
                       ("Readex", {500: "Readex-500", 600: "Readex-600", 700: "Readex-700"})):
        for w, f in files.items():
            faces.append("@font-face{font-family:'%s';font-weight:%d;src:url('file://%s/%s.ttf');}" % (fam, w, FONTS, f))
    return "\n".join(faces)


def plate(v):
    style, code, num = v.get("style", "generic"), html.escape(v.get("code", "")), html.escape(v.get("number", ""))
    label = {"dubai": ("دبي", "DUBAI"), "abudhabi": ("أبوظبي", "ABU DHABI"), "sharjah": ("الشارقة", "SHARJAH"),
             "ksa": ("السعودية", "KSA")}.get(style, (v.get("label", ""), ""))
    if style == "ksa":
        ar_l, ar_n = html.escape(v.get("ar_code", "")), html.escape(v.get("ar_number", ""))
        return f"""<div class="plate ksa"><div class="strip"><span>السعودية</span><b>KSA</b></div>
          <div class="half"><div class="ar">{ar_n}</div><div class="la">{num}</div></div><div class="sep"></div>
          <div class="half"><div class="ar">{ar_l}</div><div class="la">{code}</div></div></div>"""
    codebox = f'<div class="code {style}">{code}</div>' if code else ""
    return f"""<div class="plate {style}">{codebox}<div class="mid"><span>{label[0]}</span><span>{label[1]}</span></div>
      <div class="num">{num}</div></div>"""


def phone(v):
    return f"""<div class="phone"><div class="op">{html.escape(v.get('label', ''))}</div>
      <div class="pnum" dir="ltr">{html.escape(v['number'])}</div><div class="bars"><i></i><i></i><i></i><i></i></div></div>"""


def visual(v):
    t = v.get("type")
    if t == "plate":
        return plate(v)
    if t == "phone":
        return phone(v)
    if t == "emoji":
        return f'<img class="emoji" src="file://{os.path.join(EMOJI, v["name"] + ".png")}">'
    return ""


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:#060B16;overflow:hidden}
body{font-family:'Cairo';color:#fff;position:relative}
.bg{position:absolute;inset:0;background:
  radial-gradient(ellipse 700px 600px at 85% 380px, rgba(46,92,170,.45), rgba(0,0,0,0) 70%),
  radial-gradient(ellipse 800px 500px at 10% 1500px, rgba(200,24,36,.28), rgba(0,0,0,0) 70%),
  linear-gradient(165deg,#0E1A33 0%,#08101F 45%,#050A14 100%)}
.slab{position:absolute;background:linear-gradient(120deg,rgba(255,255,255,.05),rgba(255,255,255,0));transform:skewX(-24deg)}
.streak{position:absolute;height:6px;border-radius:6px;background:linear-gradient(90deg,rgba(255,40,50,0),#FF2B36 45%,#ff8c8c 50%,#FF2B36 55%,rgba(255,40,50,0));
  box-shadow:0 0 24px 6px rgba(255,30,40,.55);transform-origin:center}
.handle{position:absolute;top:150px;left:0;right:0;text-align:center;font-family:'Readex';font-weight:600;font-size:30px;color:rgba(255,255,255,.55);letter-spacing:1px}

/* breaking banner */
.banner{position:absolute;top:250px;right:-40px;width:600px;height:124px;transform:skewX(-14deg);
  background:linear-gradient(180deg,#FF3B42 0%,#D3121C 60%,#A80A14 100%);box-shadow:0 18px 40px rgba(210,20,30,.45), inset 0 3px 0 rgba(255,255,255,.35)}
.banner:after{content:"";position:absolute;left:-46px;top:0;width:22px;height:100%;background:#D3121C}
.banner:before{content:"";position:absolute;left:-84px;top:0;width:12px;height:100%;background:#D3121C;opacity:.75}
.banner span{position:absolute;inset:0;display:flex;align-items:center;justify-content:flex-end;padding-right:110px;transform:skewX(14deg);
  font-weight:900;font-size:92px;line-height:1;text-shadow:0 4px 0 rgba(0,0,0,.25);direction:rtl}
.banner small{font-weight:800;font-size:40px;margin-right:22px;opacity:.95}
.brand{position:absolute;top:283px;left:70px;display:flex;align-items:center;gap:12px;font-weight:900;font-size:40px;direction:rtl}
.brand .ico{width:54px;height:54px}
.brand b{background:linear-gradient(180deg,#FFE7A3,#E2AE4A 55%,#A9741C);-webkit-background-clip:text;background-clip:text;color:transparent}

/* headline */
.hl{position:absolute;top:400px;left:64px;right:64px;direction:rtl;text-align:right}
.hl h1{font-weight:900;font-size:96px;line-height:1.12;text-shadow:0 6px 24px rgba(0,0,0,.45)}
.hl h2{font-weight:900;font-size:104px;line-height:1.15;margin-top:4px;
  background:linear-gradient(180deg,#FFF0C2 0%,#F4C65A 45%,#C28A28 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 6px 18px rgba(0,0,0,.45))}
.rule{width:300px;height:7px;background:#E3202B;margin:22px 0 14px auto;border-radius:3px}
.dateline{font-family:'Readex';font-weight:600;font-size:32px;color:rgba(255,255,255,.82);word-spacing:6px}

/* panel */
.panel{position:absolute;top:960px;left:60px;right:60px;height:410px;border-radius:30px;padding:5px;
  background:linear-gradient(135deg,#FFE7A3,#C9922E 40%,#FFE7A3 60%,#9E6A17);box-shadow:0 30px 60px rgba(0,0,0,.55)}
.panel .in{width:100%;height:100%;border-radius:26px;overflow:hidden;position:relative;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(ellipse 60% 70% at 50% 45%, #1E2E52 0%, #0C1529 70%, #08101F 100%)}
.panel .in:after{content:"";position:absolute;left:0;right:0;top:0;height:45%;background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,0))}
.emoji{width:330px;height:330px;object-fit:contain;filter:drop-shadow(0 26px 40px rgba(0,0,0,.6));position:relative;z-index:1}
.stamp{position:absolute;top:26px;right:28px;z-index:2;background:#E3202B;color:#fff;font-weight:900;font-size:36px;padding:2px 26px 8px;border-radius:12px;
  transform:rotate(4deg);box-shadow:0 10px 26px rgba(227,32,43,.45);border:3px solid rgba(255,255,255,.85)}

/* price bar */
.price{position:absolute;top:770px;left:60px;right:60px;height:160px;border-radius:24px;direction:rtl;display:flex;align-items:center;justify-content:space-between;padding:0 44px;
  background:linear-gradient(90deg,#B90E18,#E3202B 50%,#B90E18);box-shadow:0 20px 40px rgba(200,20,30,.35), inset 0 3px 0 rgba(255,255,255,.25)}
.price .k{font-weight:800;font-size:44px;line-height:1.15;white-space:nowrap}
.price .vv{display:flex;flex-direction:column;align-items:flex-start}
.price .vv small{font-family:'Readex';font-weight:500;font-size:26px;opacity:.92;direction:rtl;margin-top:4px}
.price .v{direction:ltr;font-weight:900;font-size:108px;line-height:1;letter-spacing:-1px;text-shadow:0 4px 0 rgba(0,0,0,.2)}
.price .v span{font-size:48px;font-weight:800;margin-left:14px;letter-spacing:0}

/* ticker */
.ticker{position:absolute;top:1400px;left:0;right:0;height:112px;direction:rtl;display:flex;align-items:center;padding:0 110px 0 30px;
  background:linear-gradient(180deg,rgba(9,16,32,.95),rgba(5,10,20,.95));border-top:2px solid rgba(255,255,255,.12);border-bottom:4px solid #E3202B}
.ticker div{flex:1;display:flex;align-items:center;gap:14px;padding:0 26px;min-width:0}
.ticker div+div{border-right:2px solid rgba(226,174,74,.45)}
.ticker .ico{width:50px;height:50px;flex:none}
.ticker p{font-family:'Readex';font-weight:500;font-size:22px;color:rgba(255,255,255,.6);line-height:1.2}
.ticker p b{display:block;font-family:'Cairo';font-weight:800;font-size:29px;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.source{position:absolute;top:1532px;left:60px;right:60px;direction:rtl;text-align:center;font-family:'Readex';font-weight:500;font-size:22px;color:rgba(255,255,255,.5)}

/* plates */
.plate{display:flex;align-items:center;background:linear-gradient(180deg,#FFFFFF,#ECECE6);border:7px solid #111;border-radius:22px;height:200px;padding:0 34px;gap:26px;
  box-shadow:0 30px 60px rgba(0,0,0,.6), inset 0 0 0 4px #F7F7F4, inset 0 0 0 7px #c9c9c4;position:relative;z-index:1}
.plate .code{font-weight:900;font-size:146px;color:#111;direction:ltr;line-height:1}
.plate .code.abudhabi{background:#C8102E;color:#fff;border-radius:10px;padding:0 22px;font-size:116px}
.plate .code.sharjah{color:#d4a017}
.plate .mid{display:flex;flex-direction:column;align-items:center;color:#111;font-weight:800;line-height:1.05}
.plate .mid span:first-child{font-size:40px}
.plate .mid span:last-child{font-size:28px;letter-spacing:4px;font-family:'Readex';font-weight:700}
.plate .num{font-weight:900;font-size:166px;color:#111;direction:ltr;line-height:1;letter-spacing:4px}
.plate.ksa{gap:0;padding:0 26px 0 0;height:230px}
.plate.ksa .strip{width:84px;height:100%;background:#0b5ea8;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:14px 0 0 14px;margin-right:24px}
.plate.ksa .strip span{font-size:15px;font-weight:700}.plate.ksa .strip b{font-size:26px;font-family:'Readex'}
.plate.ksa .half{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 22px}
.plate.ksa .ar{font-size:92px;font-weight:900;color:#111;line-height:1.05}
.plate.ksa .la{font-size:76px;font-weight:900;color:#111;direction:ltr;letter-spacing:10px;line-height:1}
.plate.ksa .sep{width:6px;height:78%;background:#111}
/* phone number: a SIM-style card */
.phone{width:760px;height:300px;border-radius:36px;background:linear-gradient(140deg,#FFE7A3,#D9A441 45%,#A9741C);position:relative;z-index:1;
  box-shadow:0 30px 60px rgba(0,0,0,.6);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:#1B1204}
.phone .op{font-family:'Readex';font-weight:700;font-size:34px;opacity:.8}
.phone .pnum{font-weight:900;font-size:104px;letter-spacing:4px;line-height:1.05}
.phone .bars{display:flex;gap:8px;align-items:flex-end}.phone .bars i{display:block;width:12px;background:#1B1204;border-radius:3px;opacity:.75}
.phone .bars i:nth-child(1){height:12px}.phone .bars i:nth-child(2){height:20px}.phone .bars i:nth-child(3){height:28px}.phone .bars i:nth-child(4){height:36px}
"""


def page(s):
    stamp = f'<div class="stamp">{html.escape(s["tag"])}</div>' if s.get("tag") else ""
    usd = f'<small>{iso(s["usd"])}</small>' if s.get("usd") else ""
    pfs = 108 if len(s['price']) <= 9 else 96 if len(s['price']) <= 11 else 84
    if s.get("usd"):
        pfs -= 14
    tick = []
    for icon, label, key in ((PEOPLE, "الفائز", "winner"), (GAVEL, "المزاد", "event"), (CAL, "التاريخ", "date")):
        if s.get(key):
            tick.append(f'<div>{icon}<p>{label}<b>{iso(s[key])}</b></p></div>')
    streaks = "".join(f'<div class="streak" style="width:{w}px;top:{t}px;left:{l}px;transform:rotate({r}deg);opacity:{o}"></div>'
                      for w, t, l, r, o in ((1300, 1640, -260, -16, .9), (900, 1720, 300, -16, .55), (700, 190, 520, -16, .45), (1100, 745, -500, -16, .22)))
    slabs = "".join(f'<div class="slab" style="width:{w}px;height:1920px;top:0;left:{l}px"></div>' for w, l in ((220, 120), (120, 520), (300, 860)))
    return f"""<!doctype html><html lang="ar"><head><meta charset="utf-8"><style>{font_faces()}{CSS}</style></head>
<body>{DEFS}<div class="bg"></div>{slabs}{streaks}
<div class="handle">@akhbarmazad</div>
<div class="banner"><span>{html.escape(s.get('banner', 'عاجل'))}</span></div>
<div class="brand">{GAVEL}<span>أخبار <b>مزاد</b></span></div>
<div class="hl"><h1>{iso(s['headline'])}</h1>{f'<h2>{iso(s["highlight"])}</h2>' if s.get('highlight') else ''}
  <div class="rule"></div><div class="dateline">{iso(s.get('dateline', ''))}</div></div>
<div class="panel"><div class="in">{stamp}{visual(s['visual'])}</div></div>
<div class="price"><div class="k">{iso(s.get('kicker', 'بيعت بـ'))}</div>
  <div class="vv"><div class="v" style="font-size:{pfs}px">{html.escape(s['price'])}<span>{html.escape(s['currency'])}</span></div>{usd}</div></div>
<div class="ticker">{''.join(tick)}</div>
<div class="source">{iso(s.get('source', ''))}</div>
</body></html>"""


def render_png(story, out_png):
    from playwright.sync_api import sync_playwright
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page(story))
        tmp = f.name
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + tmp)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(250)
        pg.screenshot(path=out_png)
        b.close()
    os.unlink(tmp)


def render_reel(png, out_mp4, seconds=12):
    """static image Reel with a silent track (Instagram's song is attached at posting time)"""
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", png,
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(seconds),
                    "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-r", "30",
                    "-c:a", "aac", "-b:a", "64k", "-shortest", "-movflags", "+faststart", out_mp4], check=True)


if __name__ == "__main__":
    src = sys.argv[1]
    story = json.load(open(src, encoding="utf-8"))
    d = os.path.dirname(os.path.abspath(src))
    png = os.path.join(d, "card.png")
    render_png(story, png)
    if "--png-only" not in sys.argv:
        render_reel(png, os.path.join(d, "reel.mp4"))
    print("done", png)
