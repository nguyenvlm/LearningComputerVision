import numpy as np
from cv2 import warpAffine, imread, imwrite
from math import sin, cos, radians, pi

def translate(image, delta_x=0, delta_y=0):
    T = np.float32(
        [[1, 0, delta_x], 
        [0, 1, delta_y]]
    )
    r, c = image.shape[:2]
    return warpAffine(image, T, (c,r))

def rotate(image, theta=0, clockwise=False):
    theta = radians(theta%360)
    if clockwise:
        theta = 2*pi - theta
    T = np.float32(
        [[cos(theta), sin(theta), 1], 
        [-sin(theta), cos(theta), 1]]
    )
    r, c = image.shape[:2]
    return warpAffine(image, T, (c,r))

def rescale(image, scale_x=1, scale_y=1):
    T = np.float32(
        [[scale_x, 0, 0], 
        [0, scale_y, 0]]
    )
    r, c = image.shape[:2]
    return warpAffine(image, T, (c,r))

def shear(image, shear_x=0, shear_y=0):
    T = np.float32(
        [[1, shear_y, 0], 
        [shear_x, 1, 0]]
    )
    r, c = image.shape[:2]
    return warpAffine(image, T, (c,r))