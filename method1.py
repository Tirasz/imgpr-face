import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
from itertools import chain

def morph(img, size = 7, shape = cv2.MORPH_RECT, dil_iters = 1, er_iters = 2):
    struct = cv2.getStructuringElement(shape, (size, size))
    dilated = cv2.dilate(img, struct, iterations=dil_iters)
    eroded = cv2.erode(dilated, struct, iterations=er_iters)
    return cv2.dilate(eroded, struct)

def preprocess(img, filename='', testMode = False):
    # nomralize +median blur + morphing for noise
    tr_img = np.zeros((img.shape))
    tr_img = cv2.normalize(img, tr_img, 0,255, cv2.NORM_MINMAX)
    tr_img = morph(cv2.medianBlur(tr_img, 7), dil_iters=2, er_iters=1, size=3)
    return tr_img


def detectAndDisplay(img):
    img = preprocess(img)
    rows, cols, channels = img.shape
    # RGB Szinmodell 2D normalizált színtérbe (+1 h ne baszodjon el)
    B,G,R = np.array(cv2.split(img), dtype=np.float32)
    r = R / (R+G+B+1)
    g = G / (R+G+B+1)

    # Normalizált csatornák oszlopvektorokká alakítása cv.kmeans miatt
    r_flat = r.reshape((-1, 1))
    g_flat = g.reshape((-1, 1))
    b_zeros = np.float32(np.zeros((rows, cols)).reshape((-1,1)))

    # KMEANS setup, futtatás
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 20, 1.0) # Megállási feltétel(ek): max iterációk: 10, minimum pontosság: 1
    K = 6 # HÁNY KLASZTER
    k_means_data = np.column_stack((b_zeros, r_flat, g_flat)) # Kmeans adata: a jellemzok oszlopok
    ret,label,center=cv2.kmeans(k_means_data,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Eredmények
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    res3 = np.uint8(res2 * 255)
    return res3