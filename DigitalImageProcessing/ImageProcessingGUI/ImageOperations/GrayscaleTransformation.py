import numpy as np
import cv2
import math

def toGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def invert(image):
    return ~image

def logTransform(image, c=2):
    return np.float32(c*np.log1p(image+1))

def expoTransform(image, gamma=0.8, c=2): # gamma correction
    return c*image**gamma