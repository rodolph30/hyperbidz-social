#!/usr/bin/env bash
# One-time setup in a fresh session: the narrator voice (Kokoro-82M via kokoro-onnx) and the offline speech checker
# (sherpa-onnx whisper base.en). Everything downloads from PyPI and GitHub releases (both reachable from the workspace).
set -e
pip install -q --break-system-packages kokoro-onnx soundfile scipy sherpa-onnx numpy pillow 2>&1 | grep -v "WARNING: Running pip" || true
K=${KOKORO_DIR:-$HOME/.cache/kokoro}; mkdir -p "$K"
[ -s "$K/kokoro-v1.0.onnx" ] || curl -sSL -o "$K/kokoro-v1.0.onnx" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s "$K/voices-v1.0.bin" ] || curl -sSL -o "$K/voices-v1.0.bin" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
A=${ASR_DIR:-$HOME/.cache/asr}; mkdir -p "$A"
if [ ! -s "$A/sherpa-onnx-whisper-base.en/base.en-encoder.int8.onnx" ]; then
  curl -sSL -o "$A/w.tar.bz2" https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2
  tar -xjf "$A/w.tar.bz2" -C "$A" && rm "$A/w.tar.bz2"
fi
command -v ffmpeg >/dev/null || (apt-get install -y -qq ffmpeg >/dev/null 2>&1 || echo "ffmpeg missing: install it")
echo "voice: $K  asr: $A  ready"
