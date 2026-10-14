"""s6_reend.py <ep> : rebuild Season 6 episode <ep>'s ending with the crisp end card. Frames before the cross-fade are
taken from the v1 render as they are; the last 0.5 s of the held shot cross-fades into end_card2; the v1 audio track is
kept untouched (so the owner's voice mix only needs the new picture)."""
import sys, subprocess
sys.path.insert(0, "/home/claude")
from founder_common import *
import s6_common as K
ep = int(sys.argv[1]); d = f"/home/claude/s6e{ep}"
LINES = {1: ["The one", "that got away", "comes back."], 2: ["Your closet.", "Their wishlist."], 3: ["One of one.", "For less."],
         4: ["Best friends.", "Fierce bidders."], 5: ["Every bag", "has a next story."], 6: ["Bid like", "you mean it."]}[ep]
v1 = f"{d}/hyperbidz-founder-s6e{ep}-v1.mp4"; out = f"{d}/hyperbidz-founder-s6e{ep}-v2.mp4"
SHOT, HOLD = 8.0, 1.4; CLIP = SHOT + HOLD; XF = 0.5
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v1], capture_output=True, text=True).stdout)
END = round(dur - CLIP, 1); TOTAL = CLIP + END
FR = decode(v1)
print("ep", ep, "dur", dur, "END", END, "frames", len(FR))
def frame(t):
    i = int(round(t * FPS))
    if t < CLIP - XF: return FR[min(len(FR) - 1, i)]
    if t < CLIP:
        a = K.ease((t - (CLIP - XF)) / XF); return Image.blend(FR[min(len(FR) - 1, i)], K.end_card2(0.0, LINES, END), a)
    return K.end_card2(t - CLIP, LINES, END)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", v1, "-vn", "-c:a", "copy", f"{d}/v1audio.m4a"], check=True)
enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-i", f"{d}/v1audio.m4a", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                        "-c:a", "copy", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(len(FR)): enc.stdin.write(frame(i / FPS).convert("RGB").tobytes())
enc.stdin.close(); enc.wait(); print("done", out)
