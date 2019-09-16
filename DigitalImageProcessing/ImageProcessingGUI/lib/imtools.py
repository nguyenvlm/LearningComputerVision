import cv2
import numpy as np


def to_grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = np.zeros_like(img)
    result[:, :, 0] = gray
    result[:, :, 1] = gray
    result[:, :, 2] = gray

    return result
