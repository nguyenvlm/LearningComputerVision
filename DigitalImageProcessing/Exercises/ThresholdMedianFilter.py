import numpy as np
import cv2
import os


def thresholdMedianFilter(image, threshold=5, size=3):
    if size not in (3, 5, 7):
        raise ValueError("Improper filter size! (must be 3, 5 or 7)")
    if threshold not in range(256):
        raise ValueError(
            "Improper threshold value! (must be in range [0, 256])")

    blur = cv2.medianBlur(image, size)
    mask = np.abs(blur-image) > threshold
    filtered = image
    filtered[mask] = blur[mask]

    return np.uint8(filtered)


if __name__ == "__main__":

    img = cv2.imread("samples\lena_color_256.tif")

    # Add salt and pepper noises:
    s_vs_p = 0.5
    amount = 0.1
    num_salt = np.ceil(amount * img.size * s_vs_p)
    num_pepper = np.ceil(amount * img.size * (1. - s_vs_p))
    noise = np.copy(img)
    noise[[np.random.randint(0, i - 1, int(num_salt)) for i in img.shape]] = 1
    noise[[np.random.randint(0, i - 1, int(num_pepper))
           for i in img.shape]] = 0
    img = noise

    # Run the filter
    outputDir = "ThresholdMedianFilterOutput"
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    cv2.imwrite("%s\lena_color_256_noise.tif" % (outputDir), img)
    for size in (3, 5, 7):
        for t in range(5, 31, 2):
            cv2.imwrite("%s\lena_color_256_thres%d_size%d.tif" % (
                outputDir, t, size), thresholdMedianFilter(image=img, threshold=t, size=size))
