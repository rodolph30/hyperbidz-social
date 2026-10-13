"""cover.py <script> <out.jpg> <t>  -> full-res frame of an edit as the cover"""
import sys
script, out, t = sys.argv[1], sys.argv[2], float(sys.argv[3])
sys.argv = [script, "x.mp4", "--stills", "0"]
src = open(script).read().split('if __name__ == "__main__":')[0]
g = {"__name__": "peek"}; exec(compile(src, script, "exec"), g)
g["frame"](t).save(out, quality=90)
