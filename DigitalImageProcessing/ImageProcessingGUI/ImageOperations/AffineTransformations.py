import numpy as np
import cv2
import math

def translate(image, delta_x=0, delta_y=0):
    T = np.float32(
        [[1, 0, delta_x], 
        [0, 1, delta_y]]
    )
    r, c = image.shape[:2]
    return cv2.warpAffine(image, T, (c,r))

def rotate(image, theta=0, clockwise=False, scale='auto'):
    theta = math.radians(theta%360)
    if clockwise:
        theta = 2*math.pi - theta
    if scale == 'auto':
        scale = math.sin(theta) + math.cos(theta)
    r, c = image.shape[:2]
    center_x, center_y = c/2, r/2
    a, b = scale*math.cos(theta), scale*math.sin(theta)
    T = np.float32(
        [[a, b, (1-a)*center_x-b*center_y], 
        [-b, a, b*center_x+(1-a)*center_y]]
    )
    return cv2.warpAffine(image, T, (c,r))

def rescale(image, scale_x=1, scale_y=1):
    T = np.float32(
        [[scale_x, 0, 0], 
        [0, scale_y, 0]]
    )
    r, c = image.shape[:2]
    return cv2.warpAffine(image, T, (c,r))

def shear(image, shear_x=0, shear_y=0):
    T = np.float32(
        [[1, shear_y, 0], 
        [shear_x, 1, 0]]
    )
    r, c = image.shape[:2]
    return cv2.warpAffine(image, T, (c,r))

def resize(image, new_x, new_y, interpolation='NEAREST'):
    inter_map = {
        'NEAREST': cv2.INTER_NEAREST,
        'BILINEAR': cv2.INTER_LINEAR,
        'CUBIC': cv2.INTER_CUBIC
    }
    return cv2.resize(image, (new_x, new_y), interpolation=inter_map[interpolation])