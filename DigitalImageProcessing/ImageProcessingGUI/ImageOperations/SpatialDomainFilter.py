import numpy as np
import cv2
import math

def meanFilter(image):
    meanMatrix = np.ones((3,3), np.float32)/9
    return np.uint8(cv2.filter2D(src=image, ddepth=-1, kernel=meanMatrix))

def medianFilter(image, size=3):
    return np.uint8(cv2.medianBlur(src=image, ksize=size))

def gaussianFilter(image, sigma=0.5):
    gaussianMatrix = cv2.getGaussianKernel(ksize=3, sigma=sigma)
    gaussianMatrix = gaussianMatrix*np.transpose(gaussianMatrix)
    return np.uint8(cv2.filter2D(src=image, ddepth=-1, kernel=gaussianMatrix))

def laplacianFilter(image, connectivity=4):
    laplacianMatrix = None
    if connectivity==8:
        laplacianMatrix = np.array([
            [1, 1, 1],
            [1, -8, 1],
            [1, 1, 1]
        ])
    else:
        laplacianMatrix = np.array([
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ])
    return np.uint8(cv2.filter2D(src=image, ddepth=-1, kernel=laplacianMatrix))

def LoGFilter(image, sigma=0.5, connectivity=4):
    return laplacianFilter(gaussianFilter(image,sigma), connectivity)

def highboostFilter(image, A=8):
    boostMatrix = np.ones((3,3))*-1
    boostMatrix[1,1] = max(A, 8)
    return np.uint8(cv2.filter2D(src=image, ddepth=-1, kernel=boostMatrix))

def unsharpMaskFilter(image, mask='gaussian'):
    mask_dict = {
        'gaussian': gaussianFilter,
        'laplacian': laplacianFilter,
        'log': LoGFilter,
        'highboost': highboostFilter
    }
    alpha = 1
    if mask=='gaussian': alpha = 2
    return np.uint8(cv2.addWeighted(image, alpha, mask_dict[mask](image), -1, 0))

if __name__ == "__main__":
    img = cv2.imread("../sample/hw4_radiograph_2.jpg")
    cv2.imwrite("../output/output.jpg", medianFilter(img, 19))