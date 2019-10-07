import numpy as np
import cv2
import math

def medianFilter(image, size=3):
    return np.uint8(cv2.medianBlur(src=image, ksize=size))

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

def imsave(num, algo, img):
    imname = "radiograph_{}_{}.jpg".format(num, algo)
    cv2.imwrite("./output/" + imname, img)

if __name__ == "__main__":
    img_1 = cv2.imread("./samples/radiograph_1.jpg")
    img_2 = cv2.imread("./samples/radiograph_2.jpg")

    # Apply Median Filter with Adjusted Kernel's Size
    imsave(1, "median_filter", medianFilter(img_1, 15))
    imsave(2, "median_filter", medianFilter(img_2, 11))

    # Apply Discrete Fourier Transform
    imsave(1, "dft", discreteFourierTransform(img_1))
    imsave(2, "dft", discreteFourierTransform(img_2))

    # Apply Butterworth Lowpass Filter
    imsave(1, "butterworth_lowpass", butterworthFilter(img_1, 20, 2, "low"))
    imsave(2, "butterworth_lowpass", butterworthFilter(img_2, 20, 3, "low"))

    # Apply Butterworth Highpass Filter
    imsave(1, "butterworth_highpass", butterworthFilter(img_1, 100, 1, "high"))
    imsave(2, "butterworth_highpass", butterworthFilter(img_2, 40, 1, "high"))
