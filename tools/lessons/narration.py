"""Narrator voice + timeline + subtitles for the lesson videos (all offline, no paid tools).

Voice: Kokoro-82M (Apache-2.0) through kokoro-onnx. Model files are downloaded from GitHub by setup_tts.sh into
~/.cache/kokoro (or $KOKORO_DIR). The series voice is fixed in VOICE/SPEED so every video sounds like the same narrator.

Usage in a lesson script:
    LINES = [("hook", "Here's a [paradox.]", 0.5), ...]       # key, text ([brackets] = highlighted word in subtitles), pause after
    TL = Timeline(LINES, start=0.4)                            # makes / caches the audio and the timing
    TL.t("hook") -> (start, end) of that line;  TL.at("hook", 0.6) -> time 60% through the line (by characters)
    TL.word("hook", "paradox") -> time the word is spoken (estimated from characters)
    subtitles(im, t, TL) draws the subtitle pill for whatever is being said at t
    TL.voice_track(total) -> numpy float array at 48 kHz
"""
import os, re, json, hashlib, subprocess
import numpy as np

SR = 48000
VOICE, SPEED, LANG = "am_michael", 1.0, "en-us"      # the series narrator (calm, clear, American English)
KDIR = os.environ.get("KOKORO_DIR", os.path.expanduser("~/.cache/kokoro"))
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".voice_cache")
_K = None

def _kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        for d in (KDIR, "/home/claude/tts"):
            if os.path.exists(os.path.join(d, "kokoro-v1.0.onnx")):
                _K = Kokoro(os.path.join(d, "kokoro-v1.0.onnx"), os.path.join(d, "voices-v1.0.bin")); break
        else:
            raise SystemExit("Kokoro model missing: run tools/lessons/setup_tts.sh")
    return _K

def plain(text):
    """what the narrator says: {shown|spoken} -> spoken, [emphasis] -> emphasis"""
    return re.sub(r"[\[\]]", "", re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\2", text))

def shown(text):
    """what the subtitles show: {shown|spoken} -> shown (keeps [emphasis] markup)"""
    return re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\1", text)

def speak(text, voice=VOICE, speed=SPEED):
    """text -> mono float32 at 48 kHz (cached by text+voice+speed)"""
    os.makedirs(CACHE, exist_ok=True)
    say = plain(text).replace("…", ",")
    key = hashlib.sha1(f"{voice}|{speed}|{say}".encode()).hexdigest()[:16]; path = os.path.join(CACHE, key + ".npy")
    if os.path.exists(path): return np.load(path)
    s, sr = _kokoro().create(say, voice=voice, speed=speed, lang=LANG)
    from scipy.signal import resample_poly
    y = resample_poly(np.asarray(s, np.float64), SR // 1000, sr // 1000).astype(np.float32)
    # trim leading/trailing silence so timings are tight
    e = np.abs(y) > 0.004; idx = np.where(e)[0]
    if len(idx): y = y[max(0, idx[0] - int(0.04 * SR)): idx[-1] + int(0.22 * SR)]
    f = int(0.05 * SR); y[-f:] *= np.linspace(1, 0, f)
    np.save(path, y); return y

class Timeline:
    def __init__(self, lines, start=0.4, voice=VOICE, speed=SPEED):
        self.lines, self.start = lines, start; self.audio, self.times, self.text = {}, {}, {}
        t = start
        for key, text, pause in lines:
            y = speak(text, voice, speed); d = len(y) / SR
            self.audio[key] = y; self.times[key] = (t, t + d); self.text[key] = text; t += d + pause
        self.end = t
    def t(self, key): return self.times[key]
    def at(self, key, frac):
        a, b = self.times[key]; return a + (b - a) * frac
    def word(self, key, word):
        """estimated time a spoken word starts, by its character position in the spoken line"""
        s = plain(self.text[key]); i = s.lower().find(word.lower()); a, b = self.times[key]
        if i < 0: raise KeyError(f"{word!r} not in line {key!r}: {s!r}")
        return a + (b - a) * (max(0, i) / max(1, len(s)))
    def voice_track(self, total):
        out = np.zeros(int(total * SR), np.float32)
        for key, y in self.audio.items():
            i = int(self.times[key][0] * SR); j = min(len(out), i + len(y)); out[i:j] += y[: j - i]
        return out
    def speaking(self, total, pad=0.15):
        """0..1 envelope that is 1 while the narrator talks (for ducking the music)"""
        env = np.zeros(int(total * SR), np.float32)
        for a, b in self.times.values():
            env[max(0, int((a - pad) * SR)): int((b + pad) * SR)] = 1
        k = int(0.25 * SR); return np.convolve(env, np.ones(k) / k, "same")
    def chunks(self, key, max_words=6):
        """split a line into subtitle chunks with estimated times"""
        text = re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(" ", "\x01"), self.text[key]); words = text.split(); out, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) >= max_words or re.search(r"[.,:;?!…]\]?$", w) and len(cur) >= 3: out.append(" ".join(cur)); cur = []
        if cur:
            if out and len(cur) < 2: out[-1] += " " + " ".join(cur)
            else: out.append(" ".join(cur))
        out = [c.replace("\x01", " ") for c in out]
        a, b = self.times[key]; total = sum(len(plain(c)) for c in out); res, acc = [], 0
        for c in out:
            c0 = a + (b - a) * acc / total; acc += len(plain(c)); res.append((c0, a + (b - a) * acc / total, shown(c)))
        return res
    def subtitle_at(self, t, hold=0.35):
        best = None
        for key, _, _ in self.lines:
            for c0, c1, c in self.chunks(key):
                if c0 - 0.05 <= t < c1 + hold: best = (c0, c1, c)
        return best

def asr_check(wav_path):
    """transcribe the narration offline (sherpa-onnx whisper base.en) to catch mispronunciations; returns text"""
    tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "asr_transcribe.py")
    return subprocess.run(["python3", tool, wav_path], capture_output=True, text=True).stdout

# ---------- exact word timing (for word-by-word kinetic captions) ----------
_REC = None
def _recognizer():
    """sherpa-onnx zipformer (small, English): gives token timestamps, so we know when each word is spoken"""
    global _REC
    if _REC is None:
        import sherpa_onnx
        for d in (os.environ.get("ASR_DIR", os.path.expanduser("~/.cache/asr")), "/root/.cache/asr", "/home/claude/asr"):
            D = os.path.join(d, "sherpa-onnx-zipformer-small-en-2023-06-26")
            if os.path.exists(D): break
        else:
            return None
        _REC = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=os.path.join(D, "encoder-epoch-99-avg-1.int8.onnx"),
            decoder=os.path.join(D, "decoder-epoch-99-avg-1.onnx"), joiner=os.path.join(D, "joiner-epoch-99-avg-1.int8.onnx"),
            tokens=os.path.join(D, "tokens.txt"), num_threads=2)
    return _REC

def _norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())

def units(text):
    """split a line into display units: ([shown text], emphasis?, [spoken words]); {shown|spoken} stays one unit"""
    prot = re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(" ", "\x01"), text)
    out, emph = [], False
    for tok in prot.split():
        tok = tok.replace("\x01", " "); start_emph = emph or tok.startswith("[") or tok.startswith("{[") or "[" in tok[:2]
        e = emph or "[" in tok
        if "[" in tok: emph = True
        if "]" in tok: emph = False
        m = re.search(r"\{([^|}]*)\|([^}]*)\}", tok)
        if m:
            show = tok.replace(m.group(0), m.group(1)); say = tok.replace(m.group(0), m.group(2))
        else:
            show = say = tok
        show = show.replace("[", "").replace("]", ""); say = say.replace("[", "").replace("]", "")
        out.append((show, e, [w for w in say.split() if _norm(w)]))
    return out

def align(y, text):
    """start time (s, from the start of y) of every display unit of `text`; falls back to character spacing"""
    us = units(text); spoken = [w for _, _, ws in us for w in ws]; n = len(spoken); dur = len(y) / SR
    times = [None] * n
    rec = _recognizer()
    if rec is not None and n:
        from scipy.signal import resample_poly
        a = resample_poly(np.asarray(y, np.float64), 1, 3).astype(np.float32)
        st = rec.create_stream(); st.accept_waveform(16000, a); rec.decode_stream(st)
        words, starts = [], []
        for tok, ts in zip(st.result.tokens, st.result.timestamps):
            if tok.startswith(" ") or not words: words.append(tok.strip()); starts.append(ts)
            else: words[-1] += tok
        import difflib
        sm = difflib.SequenceMatcher(a=[_norm(w) for w in spoken], b=[_norm(w) for w in words], autojunk=False)
        for blk in sm.get_matching_blocks():
            for k in range(blk.size): times[blk.a + k] = starts[blk.b + k]
    # fill gaps by character position
    total = sum(len(w) + 1 for w in spoken) or 1; acc = 0; est = []
    for w in spoken: est.append(dur * acc / total); acc += len(w) + 1
    known = [(i, times[i]) for i in range(n) if times[i] is not None]
    for i in range(n):
        if times[i] is None:
            prev = max([k for k in known if k[0] < i], default=None, key=lambda k: k[0]); nxt = min([k for k in known if k[0] > i], default=None, key=lambda k: k[0])
            if prev and nxt: times[i] = prev[1] + (nxt[1] - prev[1]) * (est[i] - est[prev[0]]) / max(1e-6, est[nxt[0]] - est[prev[0]])
            elif prev: times[i] = prev[1] + (est[i] - est[prev[0]])
            elif nxt: times[i] = max(0, nxt[1] - (est[nxt[0]] - est[i]))
            else: times[i] = est[i]
    res, k = [], 0
    for show, e, ws in us:
        res.append((show, e, times[k] if ws and k < n else (res[-1][2] if res else 0.0))); k += len(ws)
    return res

def _timeline_words(self, key):
    """[(shown word, emphasis, absolute start time)] for one line, cached on disk"""
    if not hasattr(self, "_words"): self._words = {}
    if key not in self._words:
        y = self.audio[key]; h = hashlib.sha1((self.text[key] + str(len(y))).encode()).hexdigest()[:16]
        path = os.path.join(CACHE, "w_" + h + ".json")
        if os.path.exists(path): rel = json.load(open(path))
        else: rel = align(y, self.text[key]); json.dump(rel, open(path, "w"))
        a = self.times[key][0]; self._words[key] = [(s, e, a + float(t)) for s, e, t in rel]
    return self._words[key]
Timeline.words = _timeline_words

def _timeline_wordtime(self, key, word):
    """exact time a shown word starts (first match, case-insensitive); falls back to the estimate"""
    for s, e, t in self.words(key):
        if word.lower() in s.lower(): return t
    return self.word(key, word)
Timeline.wt = _timeline_wordtime
