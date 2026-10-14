"""Remove the floating HyperBidz watermark in the ceiling and the laptop's Apple logo (cv2 inpaint on crops)."""
import numpy as np, cv2
from PIL import Image
WM = (30, 50, 350, 270); AP = (880, 1130, 1000, 1255)
def clean(fr):
    a = np.asarray(fr.convert("RGB")).copy()
    x0, y0, x1, y1 = WM; reg = a[y0:y1, x0:x1]; hsv = cv2.cvtColor(reg, cv2.COLOR_RGB2HSV)
    m = ((reg.mean(-1) > 150) | ((hsv[..., 1] > 90) & (reg[..., 2] > 120))).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    a[y0:y1, x0:x1] = cv2.inpaint(reg, m, 11, cv2.INPAINT_TELEA)
    x0, y0, x1, y1 = AP; reg = a[y0:y1, x0:x1]; m = np.zeros(reg.shape[:2], np.uint8)
    cv2.ellipse(m, (62, 63), (30, 36), 0, 0, 360, 255, -1)
    a[y0:y1, x0:x1] = cv2.inpaint(reg, m, 9, cv2.INPAINT_TELEA)
    return Image.fromarray(a)
