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

if __name__ == "__main__":
    org = cv2.imread("hello.jpg")
    cv2.imwrite("result.jpg", contrastAutoAdjust(org))