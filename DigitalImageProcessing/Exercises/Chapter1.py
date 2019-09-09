import cv2
import matplotlib.pyplot as plt
import glob
import os

# Datasets path definition
os.chdir(os.path.dirname(os.path.realpath(__file__)))
dataset_path = os.path.join(r"..\datasets\Chapter.1")

# Images read
images = []

for t in ("*.jpg", "*.png", "*.tif"):
    for f in glob.glob1(dataset_path, t):
        img = os.path.join(dataset_path, f)
        if (os.path.isfile(img)):
            images.append(cv2.imread(img))

print("Number of Images: {}".format(len(images)))

# Plot Images
plt.figure("Images Gallery", (13, 6))
for i in range(1, 15):
    plt.subplot(3, 5, i)
    plt.imshow(images[i-1], interpolation="nearest")
    plt.axis('off')

plt.tight_layout(pad=0.5, h_pad=0, w_pad=0)
plt.show()
