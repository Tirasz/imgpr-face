import cv2

def detectAndDisplay(img):
    rows, cols, channels = img.shape
    return cv2.rectangle(img, (0, 0), (rows, cols), (255,0,0), 2)