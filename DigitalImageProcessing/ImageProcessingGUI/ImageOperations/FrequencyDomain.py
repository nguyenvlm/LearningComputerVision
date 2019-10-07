import numpy as np
import cv2
import math

def discreteFourierTransform(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    dft = cv2.dft(np.float32(gray), flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

    return magnitude_spectrum

def butterworthLowPassMask(width,height,dinit = 20,n = 1):
    width = width / 2
    height = height / 2

    hw = np.arange(-width, width)
    hh = np.arange(-height, height)

    x, y = np.meshgrid(hh, hw)
    mg = np.sqrt(x**2 + y**2)
    return 1 / (1 + (mg/dinit)**(2*n))
    
def butterworthHighPassMask(width,height,dinit = 20,n = 1):
    width = width / 2
    height = height / 2

    hw = np.arange(-width, width)
    hh = np.arange(-height, height)

    x, y = np.meshgrid(hh, hw)
    mg = np.sqrt(x**2 + y**2)
    return 1 / (1 + (dinit/mg)**(2*n))

def butterworthFilter(image, d=20, n=1, filter_type="low"):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    width, height = gray.shape

    mask = ""
    if filter_type == "low":
        mask = butterworthLowPassMask(width, height, d, n) 
    elif filter_type == "high":
        mask = butterworthHighPassMask(width, height, d, n)

    fft = np.fft.fftshift(np.fft.fft2(np.float32(gray)))

    img_pass = mask * fft
    result = np.abs(np.fft.ifft2(np.fft.ifftshift(img_pass)))

    return result

def notchFilter(image):
    pass


if __name__ == "__main__":
    img = cv2.imread("../sample/hw4_radiograph_1.jpg")
    cv2.imwrite("../sample/output/output.jpg", butterworthFilter(img, 20, 1, "high"))