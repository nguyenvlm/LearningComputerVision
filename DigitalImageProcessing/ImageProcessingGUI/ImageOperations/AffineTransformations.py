import numpy as np
from cv2 import warpAffine, imread, imwrite
from math import sin, cos, radians, pi, sqrt

def translate(image, delta_x=0, delta_y=0):
    T = np.float32(
        [[1, 0, delta_x], 
        [0, 1, delta_y]]
    )
    r, c = image.shape[:2]
    return warpAffine(image, T, (c,r))

def rotate(image, theta=0, clockwise=False, scale='auto'):
    theta = radians(theta%360)
    if clockwise:
        theta = 2*pi - theta
    if scale == 'auto':
        scale = sin(theta) + cos(theta)
    r, c = image.shape[:2]
    center_x, center_y = c/2, r/2
    a, b = scale*cos(theta), scale*sin(theta)
    T = np.float32(
        [[a, b, (1-a)*center_x-b*center_y], 
        [-b, a, b*center_x+(1-a)*center_y]]
    )
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

# if __name__ == "__main__":
#     org = imread("original.png")
#     imwrite("result.png", rotate(org,45))