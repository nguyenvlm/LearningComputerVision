import numpy as np
import cv2
import math

def meanFilter(image):
    meanMatrix = np.ones((3,3), np.float32)/9
    return np.uint8(cv2.filter2D(src=image, ddepth=-1, kernel=meanMatrix))

def medianFilter(image):
    return np.uint8(cv2.medianBlur(src=image, ksize=3))

def gaussianFilter(image, sigma=1):
    gaussianMatrix = cv2.getGaussianKernel(ksize=3, sigma=sigma)
    return np.uint8(cv2.filter2D(src=image, ddepth=-1, kernel=gaussianMatrix))

if __name__ == "__main__":
    img = cv2.imread("hello.jpg")
    cv2.imwrite("output.jpg", gaussianFilter(img))