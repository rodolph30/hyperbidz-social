"""Offline transcription with word-ish timing: python3 transcribe.py media.mp4 [chunk_s]
Splits audio into short windows on silences and transcribes each (sherpa-onnx whisper base.en)."""
import sys, subprocess, numpy as np, sherpa_onnx
M = "/home/claude/asr/sherpa-onnx-whisper-base.en/base.en-"
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M + "encoder.int8.onnx", decoder=M + "decoder.int8.onnx", tokens=M + "tokens.txt", num_threads=4)
sr = 16000
a = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout, dtype=np.int16).astype(np.float32) / 32768
# segment on silence
win = int(0.05 * sr); e = np.array([np.sqrt(np.mean(a[i:i + win] ** 2)) for i in range(0, len(a) - win, win)])
th = max(0.01, np.percentile(e, 30) * 2.5); speech = e > th
segs, cur = [], None
for i, s in enumerate(speech):
    t = i * 0.05
    if s and cur is None: cur = [t, t]
    if s: cur[1] = t + 0.05
    if not s and cur is not None and t - cur[1] > 0.35: segs.append(cur); cur = None
if cur: segs.append(cur)
for t0, t1 in segs:
    s0, s1 = max(0, int((t0 - 0.1) * sr)), min(len(a), int((t1 + 0.1) * sr))
    st = rec.create_stream(); st.accept_waveform(sr, a[s0:s1]); rec.decode_stream(st)
    print(f"{t0:5.2f}-{t1:5.2f}  {st.result.text.strip()}")
