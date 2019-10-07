import numpy as np
import cv2
import math

def toGrayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.stack((gray,)*3, axis=-1)


def invert(image):
    return np.uint8(255-image)


def logTransform(image, c=2):
    return np.uint8(c*np.log1p(image+1))


def expoTransform(image, gamma=0.8, c=1):  # gamma correction
    return np.uint8(c*(image+1)**gamma)


def contrastAutoAdjust(image):
    for c in range(image.shape[-1]):
        gmax, gmin = np.amax(image[:, :, c]), np.amin(image[:, :, c])
        image[:, :, c] = np.uint8(255/(gmax-gmin) * (image[:, :, c]-gmin))
    return image


def histogramEqualize(image, stride=2, adaptive_size='full'):
    result_image = np.copy(image)
    r, c, channel = image.shape
    if adaptive_size == 'full':
        adaptive_size = (r, c)
    h, w = adaptive_size
    for x in range(0, r-h+1, stride):
        for y in range(0, c-w+1, stride):
            for i in range(channel):
                single_channel = image[x:min(x+h, r), y:min(y+w, c), i]
                hist = np.histogram(
                    single_channel, range=(0, 256), bins=256)[0]
                hist = np.cumsum(hist)
                hist = np.uint8(hist/np.amax(hist)*255)
                result_image[x:min(x+h, r), y:min(y+w, c),
                             i] = np.vectorize(lambda p: hist[int(p)])(single_channel)
                             
    return result_image


if __name__ == "__main__":
    img = cv2.imread("../sample/hello.jpg")
    cv2.imwrite("../sample/output/output.jpg", histogramEqualize(img, (2, 1)))
