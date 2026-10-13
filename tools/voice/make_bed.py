"""Split a finished founder episode into a 'bed' (music + effects + end card sound, no voice) so the voice can be
swapped for the owner's own (Higgsfield voice change on the raw Veo clip), keeping every effect and its timing.

Usage: python3 make_bed.py <final.mp4> <raw_veo.mp4> <out_prefix>
Writes <out_prefix>.bed.wav (48 kHz mono, float32) and <out_prefix>.json {gain, lag, voice_rms}.
The episode's voice is the raw clip's audio times one gain, so a least-squares fit finds that gain and the bed is
what is left after subtracting it."""
import json, subprocess, sys, wave
import numpy as np
SR = 48000

def dec(path, t=None):
    cmd = ["ffmpeg", "-loglevel", "error", "-i", path] + (["-t", str(t)] if t else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, dtype=np.float32).astype(np.float64)

def best_lag(a, v, maxlag=4000):
    n = min(len(a), len(v)); a, v = a[:n], v[:n]
    F = np.fft.rfft(a, 2 * n); G = np.fft.rfft(v, 2 * n); c = np.fft.irfft(F * np.conj(G))
    cand = np.concatenate([c[:maxlag], c[-maxlag:]]); i = int(np.argmax(np.abs(cand)))
    return i if i < maxlag else i - 2 * maxlag

def shift(v, lag, n):
    out = np.zeros(n)
    if lag >= 0: out[lag:lag + len(v)] = v[: max(0, n - lag)][: n - lag]
    else: out[: len(v) + lag] = v[-lag:][:n]
    return out

if __name__ == "__main__":
    final, raw, pre = sys.argv[1:4]
    mix = dec(final); v = dec(raw)
    lag = best_lag(mix, v); vs = shift(v, lag, len(mix))
    g = float(np.dot(mix, vs) / np.dot(vs, vs))
    # the effective gain drifts by about 1% across the clip (AAC); fit it per 0.5 s window where the voice is present
    win = SR // 2; gs = np.full(len(mix), g)
    centers, vals = [], []
    for i0 in range(0, len(mix) - win, win // 2):
        seg = vs[i0:i0 + win]; e = np.dot(seg, seg)
        if e > win * 0.01 ** 2 * 50: centers.append(i0 + win // 2); vals.append(np.dot(mix[i0:i0 + win], seg) / e)
    if len(vals) >= 2: gs = np.interp(np.arange(len(mix)), centers, vals)
    bed = mix - gs * vs
    speech = np.abs(vs) > 0.02
    leak = float(np.sqrt(np.mean((bed[speech]) ** 2)) / np.sqrt(np.mean((g * vs[speech]) ** 2)))
    with wave.open(pre + ".bed.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(bed, -1, 1) * 32767).astype(np.int16).tobytes())
    meta = {"gain": g, "lag": lag, "voice_rms": float(np.sqrt(np.mean(v[np.abs(v) > 0.02] ** 2))), "bed_to_voice_rms_in_speech": leak}
    json.dump(meta, open(pre + ".json", "w")); print(pre, json.dumps(meta))
