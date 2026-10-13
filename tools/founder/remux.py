"""remux.py <script> <video_in.mp4> <video_out.mp4>: rebuild only the script's audio and swap it into an existing render"""
import sys, subprocess, re
script, vin, vout = sys.argv[1:4]
src = open(script).read(); pre, main = src.split('if __name__ == "__main__":')
pre = pre.replace("FR = decode()", "FR = []")
sys.argv = [script, "x.mp4"]; g = {"__name__": "remux"}; exec(compile(pre, script, "exec"), g)
body = main.split("render(frame")[0]
lines = [l[8:] if l.startswith("        ") else l.strip() for l in body.splitlines() if l.strip() and not l.strip().startswith("if ")]
exec("\n".join(lines), g)
wav = re.search(r'mx\.write\("([^"]+)"\)', body).group(1)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vin, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", vout], check=True)
print("remuxed", vout)
