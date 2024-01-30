import cv2
import numpy as np
import math

def sampleImage(arr, idx0, idx1):
    res = np.zeros((4,))
    if idx0 < 0 or idx1 < 0 or idx0 > (arr.shape[0] - 1) or idx1 > (arr.shape[1] - 1):
        return res
    idx0_fl = math.floor(idx0)
    idx0_cl = math.ceil(idx0)
    idx1_fl = math.floor(idx1)
    idx1_cl = math.ceil(idx1)

    s1 = arr[int(idx0_fl), int(idx1_fl)]
    s2 = arr[int(idx0_fl), int(idx1_cl)]
    s3 = arr[int(idx0_cl), int(idx1_cl)]
    s4 = arr[int(idx0_cl), int(idx1_fl)]
    x = idx0 - idx0_fl
    y = idx1 - idx1_fl
    res[0] = s1[0] * (1 - x) * (1 - y) + s2[0] * (1 - x) * y + s3[0] * x * y + s4[0] * x * (1 - y)
    res[1] = s1[1] * (1 - x) * (1 - y) + s2[1] * (1 - x) * y + s3[1] * x * y + s4[1] * x * (1 - y)
    res[2] = s1[2] * (1 - x) * (1 - y) + s2[2] * (1 - x) * y + s3[2] * x * y + s4[2] * x * (1 - y)
    res[3] = s1[3] * (1 - x) * (1 - y) + s2[3] * (1 - x) * y + s3[3] * x * y + s4[3] * x * (1 - y)
    return res

def getRadialX(x, y, cx, cy, k, xscale, xshift):
    x = (x * xscale + xshift)
    y = (y * yscale + yshift)
    res = x + ((x - cx) * k * ((x - cx) * (x - cx) + (y - cy) * (y - cy)))
    return res

def getRadialY(x, y, cx, cy, k, yscale, yshift):
    x = (x * xscale + xshift)
    y = (y * yscale + yshift)
    res = y + ((y - cy) * k * ((x - cx) * (x - cx) + (y - cy) * (y - cy)))
    return res

def calc_shift(x1, x2, cx, k, thresh):
    x3 = x1 + (x2 - x1) * 0.5
    res1 = x1 + ((x1 - cx) * k * ((x1 - cx) * (x1 - cx)))
    res3 = x3 + ((x3 - cx) * k * ((x3 - cx) * (x3 - cx)))

    if res1 > -thresh and res1 < thresh:
        return x1
    if res3 < 0:
        return calc_shift(x3, x2, cx, k, thresh)
    else:
        return calc_shift(x1, x3, cx, k, thresh)

def main():
    src = cv2.imread(argv[1], 1)
    height, width = src.shape[:2]
    dst = np.zeros_like(src)
    K = float(argv[3])
    centerX = int(argv[4])
    centerY = int(argv[5])

    global xscale, yscale, xshift, yshift  # Declaring these as global to use in other functions
    xshift = calc_shift(0, centerX - 1, centerX, K, thresh)
    newcenterX = width - centerX
    xshift_2 = calc_shift(0, newcenterX - 1, newcenterX, K, thresh)

    yshift = calc_shift(0, centerY - 1, centerY, K, thresh)
    newcenterY = height - centerY
    yshift_2 = calc_shift(0, newcenterY - 1, newcenterY, K,
