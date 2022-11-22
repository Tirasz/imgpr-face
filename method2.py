import cv2
import numpy as np
from scipy.signal import medfilt2d

def L(M):
    # L(x) = 105*logbaseten(x+1+n)
    # The constant 105 simply scales the output of the log function into the range [0,254].
    # n is a random noise value, generated from a distribution uniform over the range [0,1).
    # The random noise is added to prevent banding artifacts in dark areas of the image.
    # The constant 1 added before the log transformation prevents excessive inflation of color distinctions in very dark regions.
    return (105 * np.log10(M + np.random.random(M.shape)+ 1))

def getKernel(size):
    size = int(size)
    if size%2:
        return size
    return size + 1

def get_contour_areas(contours):
    all_areas= []
    for cnt in contours:
        area= cv2.contourArea(cnt)
        all_areas.append(area)

    return all_areas


def detectAndDisplay(img):
    rows, cols, channels = img.shape

    # https://www.cs.hmc.edu/~fleck/naked-skin.html
    # The zero-response of the camera is estimated as the smallest value in any of the three color planes,
    #  omitting locations within 10 pixels of the image edges.
    #  This value is subtracted from each R, G, and B value.
    #  This avoids potentially significant desaturation of opponent color values if the zero-response is far from zero.

    with_border = cv2.rectangle(img, (0,0), (cols, rows), (255,255,255), 10)
    zero_response = np.amin(with_border)

    B, G, R = cv2.split(img)
    R = R - zero_response
    G = G - zero_response
    B = B - zero_response

    # The RGB values are then transformed into log-opponent values I, Rg, and By as follows:
        #L(x) = 105*logbaseten(x+1+n)
        #I = L(G)
        #Rg = L(R) - L(G)
        #By = L(B) - (L(G) + L(R))/2
    # The green channel is used to represent intensity because the red and blue channels from some cameras have poor spatial resolution.
    # The log transformation makes the Rg and By values, as well as differences between I values (e.g. texture amplitude), independent of illumination level.
    # return 105 * math.log10(x+1+n)
    # I = np.float64(CALC_L(G))

    LG = np.float32(L(G))
    LR = np.float32(L(R))
    I = np.float32(LG) 
    Rg = LR - LG 
    By = L(B) - (LG + LR)/2

    # The algorithm computes a scaling factor SCALE, which measures the size of the image.
    # SCALE is the sum of the height and the width of the image (in pixels), divided by 320.
    # Spatial constants used in the skin filter are functions of SCALE, so that their output does not depend on the resolution of the input image.
    SCALE = (rows + cols) / 320

    # The Rg and By arrays are smoothed with a median filter of radius 2*SCALE, to reduce noise.

    # Rg = medfilt2d(Rg, getKernel(SCALE*2))
    # By = medfilt2d(By, getKernel(SCALE*2))
    Rg = medfilt2d(Rg, getKernel(SCALE*2))
    By = medfilt2d(By, getKernel(SCALE*2))


    # To compute texture amplitude, the intensity image was smoothed with a median filter of radius 4*SCALE. 
    # The result was subtracted from the original image.
    # The absolute values of these differences are then run through a second median filter of radius 6*SCALE. 
    #SMOOTH_I = medfilt2d(I, getKernel(SCALE*4))
    #DIFF = np.abs(I - SMOOTH_I)
    #TEXTURE = medfilt2d(DIFF, getKernel(SCALE*6))


    # For convenience, define the hue at a pixel to be atan(Rg,By), where Rg and By are the smoothed values computed as in the previous section.
    HUE = np.degrees(np.arctan2(Rg, By))

    # The saturation at the pixel is sqrt(Rg^2 + By^2). 
    SAT = np.sqrt(np.square(Rg) + np.square(By))

    # The first (tightly-tuned) stage of the skin filter marks all pixels whose texture amplitude is no larger than 5,
    # and (a) whose hue is between 110 and 150 and whose saturation is between 20 and 60 
    # or (b) whose hue is between 130 and 170 and whose saturation is between 30 and 130.
    mask = np.zeros((rows, cols), dtype=np.uint8)
    
    mask[ (HUE > 110) & (HUE < 150) & (SAT > 20) & (SAT < 60)] = 255
    mask[ (HUE > 130) & (HUE < 170) & (SAT > 30) & (SAT < 130)] = 255
    # The skin regions are cleaned up and enlarged slightly, to accomodate possible desaturated regions adjacent to the marked regions.
    #  Specifically, a pixel is marked in the final map if at least one eighth of the pixels in a circular neighborhood of radius
    #  24*SCALE pixels are marked in the original map. This is done quickly (though only approximately) by slightly modifying the fast median filter.
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(SCALE*6), int(SCALE*6))))
    
    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    largest = 0
    largestIndex = -1
    # loop over the number of unique connected component labels
    for i in range(0, numLabels):
        # if this is the first component then we examine the
        # *background* (typically we would just ignore this
        # component in our loop)
        if(i == 0):
            continue
        # extract the connected component area
        area = stats[i, cv2.CC_STAT_AREA]
        if(area > largest):
            largest = area
            largestIndex = i
    i = largestIndex
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    (cX, cY) = centroids[i]
    output = img.copy()
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)

    return output
