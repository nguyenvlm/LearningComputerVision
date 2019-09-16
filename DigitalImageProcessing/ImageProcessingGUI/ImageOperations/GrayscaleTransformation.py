import numpy as np
import cv2
import math

def toGrayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.stack((gray,)*3, axis=-1)

def invert(image):
    return ~image

def logTransform(image, c=2):
    return np.float32(c*np.log1p(image+1))

def expoTransform(image, gamma=0.8, c=2): # gamma correction
    return c*image**gamma

def contrastAutoAdjust(image):
    gray_image = toGrayscale(image)
    gmax, gmin = np.amax(gray_image), np.amin(gray_image)
    return 255/(gmax-gmin) * (image-gmin)

def histogramEqualize(image, adaptive_size='full'):
    r,c,channel = image.shape
    if adaptive_size == 'full':
        adaptive_size = (r,c)
    h, w = adaptive_size
    for x in range(0,r-h+1):
        for y in range(0,c-w+1):
            for i in range(channel):
                single_channel = image[x:x+h, y:y+w, i]
                hist = np.histogram(single_channel, range=(0, 256), bins=256)[0]
                hist = np.cumsum(hist)
                hist = np.int32(hist/np.amax(hist)*255)
                image[x:x+h, y:y+w, i] = (np.vectorize(lambda p: hist[p])(single_channel))
                print(image[x:x+h, y:y+w, i].shape, x, y)
    return image