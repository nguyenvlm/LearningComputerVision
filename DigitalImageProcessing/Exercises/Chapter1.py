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


print(len(images))
