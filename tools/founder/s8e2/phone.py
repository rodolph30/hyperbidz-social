"""Find the phone's black screen in each frame: the biggest very dark blob, fitted with a 4-corner quad."""
import numpy as np, cv2
def screen_quad(fr):
    a = np.asarray(fr.convert("RGB")); g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    m = (g < 5).astype(np.uint8) * 255; m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2: return None
    cands = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 40000 and 150 < cen[i][0] < 930 and 400 < cen[i][1] < 1600]
    if not cands: return None
    i = max(cands, key=lambda i: st[i, cv2.CC_STAT_AREA])
    cnt, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); c = max(cnt, key=cv2.contourArea)
    hull = cv2.convexHull(c).reshape(-1, 2).astype(np.float32)
    s = hull.sum(1); d = hull[:, 0] - hull[:, 1]
    tl, br, tr, bl = hull[np.argmin(s)], hull[np.argmax(s)], hull[np.argmax(d)], hull[np.argmin(d)]
    return np.array([tl, tr, br, bl], np.float32), st[i, cv2.CC_STAT_AREA]
