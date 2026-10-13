"""Put the owner's voice (Higgsfield voice change of the raw Veo clip) back on a finished episode.
Runs in the Higgsfield sandbox, where the voice-changed clip can be downloaded.

Usage: python3 mix_voice.py <final.mp4> <bed.wav> <meta.json> <raw_veo.mp4> <voice_changed.mp4> <out.mp4>
- aligns the new voice to the raw clip (envelope cross-correlation, normally 0 lag),
- matches its loudness to the original voice over the speech parts, applies the episode's voice gain,
- adds it to the voice-free bed (music, effects, end card) and muxes it under the untouched video."""
import json, subprocess, sys, wave
import numpy as np
SR = 48000

def dec(path):
    out = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(out, dtype=np.float32).astype(np.float64)

def env(x, win=480):
    return np.convolve(np.abs(x), np.ones(win) / win, mode="same")

def lag_of(a, b, maxlag=14400):
    ea, eb = env(a)[::48], env(b)[::48]; n = min(len(ea), len(eb)); ea, eb = ea[:n] - ea[:n].mean(), eb[:n] - eb[:n].mean()
    m = maxlag // 48; best, bl = -1e18, 0
    for l in range(-m, m + 1):
        s = np.dot(ea[max(0, l):n + min(0, l)], eb[max(0, -l):n - max(0, l)])
        if s > best: best, bl = s, l
    return bl * 48

if __name__ == "__main__":
    final, bedp, metap, rawp, vcp, out = sys.argv[1:7]
    meta = json.load(open(metap)); bed = dec(bedp); raw = dec(rawp); vc = dec(vcp)
    lag = lag_of(raw, vc)                       # >0: vc must be delayed
    al = np.zeros(len(bed))
    src = vc[max(0, -lag):]; i0 = max(0, lag); al[i0:i0 + len(src)] = src[: len(bed) - i0]
    mask = env(raw) > 0.02 * env(raw).max() * 3
    mask = np.pad(mask, (0, max(0, len(al) - len(mask))))[: len(al)]
    rms_new = np.sqrt(np.mean(al[mask] ** 2)) + 1e-9; rms_old = np.sqrt(np.mean(raw[mask[: len(raw)]] ** 2)) + 1e-9
    voice = al * (rms_old / rms_new) * meta["gain"]
    mix = bed + voice; pk = np.max(np.abs(mix))
    if pk > 0.97: mix *= 0.97 / pk
    with wave.open("mix.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-i", "mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(json.dumps({"out": out, "lag_samples": int(lag), "loudness_match": round(float(rms_old / rms_new), 3), "peak": round(float(pk), 3)}))
