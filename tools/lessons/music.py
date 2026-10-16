"""Background music for the lessons, synthesised in code (no samples, no licences). The owner wants a different bed every
video and it must stay quietly under the narrator, so: pick a STYLE per lesson (rotate) and a seed (key + progression).

    bed = music.make(total, style="keys", seed=1)        # float array at 48 kHz, peak ~1
    mix it ~ -24 dB under the voice and duck it while the narrator speaks (see mix() below).

Styles: keys (soft electric piano), marimba (light mallet arpeggios), pluck (warm plucked arpeggio), ambient (pad and
bell, no drums), lofi (keys + dusty drums + vinyl crackle). Lesson N uses STYLES[(N-1) % 5] with seed N unless noted."""
import numpy as np

SR = 48000
STYLES = ["keys", "marimba", "ambient", "pluck", "lofi"]
PROGS = [  # chord roots and voicings (MIDI), all gentle and resolved
    [(0, [0, 4, 7, 11]), (9, [9, 12, 16, 19]), (5, [5, 9, 12, 16]), (7, [7, 11, 14, 17])],       # I vi IV V (maj7 colours)
    [(5, [5, 9, 12, 16]), (7, [7, 11, 14, 19]), (4, [4, 7, 11, 14]), (9, [9, 12, 16, 19])],      # IV V iii vi
    [(0, [0, 4, 7, 14]), (7, [7, 11, 14, 19]), (9, [9, 12, 16, 19]), (5, [5, 9, 12, 17])],       # I V vi IV
    [(2, [2, 5, 9, 12]), (7, [7, 11, 14, 17]), (0, [0, 4, 7, 11]), (9, [9, 12, 16, 19])],        # ii V I vi
]
KEYS = [53, 55, 57, 50, 52, 48]   # F, G, A, D, E, C (base octave for chords)

def note(m): return 440.0 * 2 ** ((m - 69) / 12)

def _env(n, a=0.005, d=1.0):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(d, 1e-3))

def _ep(f, dur, vel=1.0):          # soft electric piano: sine + bell partial + slow tremolo
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3) + 0.08 * np.sin(2 * np.pi * 7 * f * t) * np.exp(-t * 14)
    return s * _env(n, 0.008, dur * 0.45) * (1 + 0.12 * np.sin(2 * np.pi * 4.5 * t)) * vel

def _mallet(f, dur=0.6, vel=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 7) + 0.35 * np.sin(2 * np.pi * 3.98 * f * t) * np.exp(-t * 22) + 0.1 * np.sin(2 * np.pi * 9.1 * f * t) * np.exp(-t * 40)) * vel

def _pluck(f, dur, rng, bright=0.35):
    n = int(dur * SR); p = max(2, int(SR / f)); out = np.zeros(n + p)
    buf = rng.uniform(-1, 1, p); buf = np.convolve(buf, np.ones(3) / 3, "same") * (1 - bright) + buf * bright; out[:p] = buf
    for i in range(p, n + p, p):
        prev = out[i - p:i]; nxt = 0.5 * (prev + np.roll(prev, 1)) * 0.996; j = min(n + p, i + p); out[i:j] = nxt[: j - i]
    return out[p:p + n] * np.exp(-np.arange(n) / SR * 5)

def _pad(fs, dur):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for i, f in enumerate(fs):
        for det in (-0.12, 0.12): s += np.sin(2 * np.pi * (f + det) * t + i)
    att = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.8).clip(0, 1)
    return s / (2 * len(fs)) * att

def _kick(rng, g=1.0):
    t = np.arange(int(0.3 * SR)) / SR; return np.sin(2 * np.pi * np.cumsum(48 + 70 * np.exp(-t * 30)) / SR) * np.exp(-t * 13) * g
def _hat(rng, g=1.0):
    n = int(0.05 * SR); return np.convolve(rng.normal(0, 1, n), [1, -0.97], "same") * np.exp(-np.arange(n) / SR * 90) * g
def _snare(rng, g=1.0):
    n = int(0.22 * SR); t = np.arange(n) / SR
    return (rng.normal(0, 1, n) * np.exp(-t * 22) * 0.6 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5) * g

def make(total, style="keys", seed=1):
    rng = np.random.default_rng(seed); n = int(total * SR) + SR; out = np.zeros(n)
    key = KEYS[seed % len(KEYS)]; prog = PROGS[(seed // len(KEYS) + seed) % len(PROGS)]
    def add(sig, at, g=1.0):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n and j > i: out[i:j] += sig[: j - i] * g
    bpm = {"keys": 78, "marimba": 96, "pluck": 90, "ambient": 64, "lofi": 82}[style]; beat = 60 / bpm; bar = beat * 4
    nb = int(total / bar) + 2
    for b in range(nb):
        t0 = b * bar; root, ch = prog[b % 4]; chord = [key + c for c in ch]; bass = key + root - 12
        if style == "keys":
            for i, m in enumerate(chord): add(_ep(note(m), bar * 1.05, 0.22), t0 + i * 0.012)
            add(_ep(note(chord[-1] + 12), beat * 1.5, 0.08), t0 + beat * 2.5)
            add(np.sin(2 * np.pi * note(bass) * np.arange(int(bar * SR)) / SR) * _env(int(bar * SR), 0.02, bar * 0.6), t0, 0.22)
            for k in range(8): add(_hat(rng), t0 + k * beat / 2, 0.025 if k % 2 else 0.012)
        elif style == "marimba":
            pat = [0, 2, 1, 3, 2, 1, 3, 2]
            for k in range(8): add(_mallet(note(chord[pat[k]] + 12), 0.6, 0.18 if k % 2 == 0 else 0.12), t0 + k * beat / 2)
            add(_mallet(note(bass), 1.2, 0.3), t0); add(_mallet(note(bass + 7), 0.8, 0.18), t0 + beat * 2)
            for k in range(8): add(_hat(rng), t0 + k * beat / 2 + 0.01, 0.018)
            add(_kick(rng), t0, 0.18); add(_kick(rng), t0 + beat * 2, 0.12)
        elif style == "pluck":
            pat = [0, 2, 1, 3, 2, 1, 3, 2]
            for k in range(8): add(_pluck(note(chord[pat[k]] + 12), 0.5, rng), t0 + k * beat / 2, 0.14)
            add(_pluck(note(bass), 1.4, rng, 0.25), t0, 0.35)
            add(_kick(rng), t0, 0.22); add(_kick(rng), t0 + beat * 2, 0.16)
            for k in range(8): add(_hat(rng), t0 + k * beat / 2, 0.02)
        elif style == "ambient":
            add(_pad([note(m) for m in chord], bar * 1.1), t0, 0.16)
            for k in (0, 3, 5):
                if rng.random() < 0.8: add(_mallet(note(chord[rng.integers(0, 4)] + 24), 1.8, 0.07), t0 + k * beat * 0.75)
            add(np.sin(2 * np.pi * note(bass) * np.arange(int(bar * SR)) / SR) * _env(int(bar * SR), 0.3, bar * 0.8), t0, 0.14)
        elif style == "lofi":
            for i, m in enumerate(chord): add(_ep(note(m), bar * 1.02, 0.18), t0 + i * 0.02 + 0.03)
            add(_kick(rng), t0, 0.3); add(_kick(rng), t0 + beat * 1.5, 0.18); add(_snare(rng), t0 + beat, 0.12); add(_snare(rng), t0 + beat * 3, 0.12)
            for k in range(8): add(_hat(rng), t0 + k * beat / 2 + (0.03 if k % 2 else 0), 0.02)
            add(np.sin(2 * np.pi * note(bass) * np.arange(int(bar * SR)) / SR) * _env(int(bar * SR), 0.02, bar * 0.5), t0, 0.25)
    if style == "lofi":                                                                         # vinyl crackle
        cr = np.zeros(n); idx = rng.integers(0, n, int(total * 25)); cr[idx] = rng.normal(0, 1, len(idx)); out += np.convolve(cr, [1, -0.6], "same") * 0.05
    out = out[: int(total * SR)]
    fi, fo = int(1.5 * SR), int(2.5 * SR); out[:fi] *= np.linspace(0, 1, fi); out[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    return out / (np.max(np.abs(out)) + 1e-9)

def mix(voice, bed, speaking, sfx=None, bed_db=-22.0, duck_db=-8.0):
    """voice ~ full level; the bed sits bed_db under it and drops a further duck_db while the narrator talks"""
    n = len(voice); bed = np.pad(bed, (0, max(0, n - len(bed))))[:n]; speaking = np.pad(speaking, (0, max(0, n - len(speaking))))[:n]
    vr = np.sqrt(np.mean(voice[np.abs(voice) > 0.01] ** 2)) if np.any(np.abs(voice) > 0.01) else 0.1
    br = np.sqrt(np.mean(bed ** 2)) + 1e-9
    g = vr / br * 10 ** (bed_db / 20) * (1 - speaking * (1 - 10 ** (duck_db / 20)))
    out = voice + bed * g
    if sfx is not None: out = out + np.pad(sfx, (0, max(0, n - len(sfx))))[:n]
    return out / (np.max(np.abs(out)) + 1e-9) * 0.89
