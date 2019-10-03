import numpy as np
import cv2
import os

def directionalMeanFilter(image, dir=0, size=3):
    if size not in (3, 5, 7):
        raise ValueError("Improper filter size! (must be 3, 5 or 7)")
    if dir not in range(4):
        raise ValueError("Improper direction! (must be in range from 0 to 3)")
    
    kernel = np.zeros((size, size))
    if dir in (0, 2):
        kernel[size//2, :] = np.ones(size)/size
    else:
        kernel = np.diag(np.ones(size))/size
    if dir >= 2:
        kernel = np.rot90(kernel)
    
    return np.uint8(cv2.filter2D(src=image, ddepth=-1, kernel=kernel))

if __name__ == "__main__":
    
    img = cv2.imread("samples\cameraman.tif")

    # Add Gaussian noises:
    noise = np.zeros(img.shape, dtype=np.uint8)
    cv2.randn(noise, mean=np.zeros(3), stddev=np.ones(3)*30)
    img = cv2.add(img, noise)

    # Run the filter:
    outputDir = "DirectionalFilterOutput"
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    cv2.imwrite("%s\cameraman_noise.tif"%(outputDir), img)
    for size in (3, 5, 7):
        for dir in range(4):
            cv2.imwrite("%s\cameraman_o_dir%d_size%d.tif"%(outputDir, dir, size), directionalMeanFilter(image=img, dir=dir, size=size))
