"""peek.py <script> <out.png> t1,t2,...  -> full-res frames side by side at half size"""
import sys
script, out, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
sys.argv = [script, "x.mp4", "--stills", "0"]
src = open(script).read().split('if __name__ == "__main__":')[0]
import os; g = {"__name__": "peek", "__file__": os.path.abspath(script)}; exec(compile(src, script, "exec"), g)
from PIL import Image
ims = [g["frame"](t).resize((540, 960)) for t in ts]; s = Image.new("RGB", (540 * len(ims), 960))
for i, im in enumerate(ims): s.paste(im, (540 * i, 0))
s.save(out)
