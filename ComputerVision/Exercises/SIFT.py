import cv2
import numpy as np

img1 = cv2.imread("..\datasets\hw2\hw2_book_page_1.jpg")
img2 = cv2.imread("..\datasets\hw2\hw2_book_page_2.jpg")

# Initiate SIFT detector
sift = cv2.ORB_create(100)

# Find keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, np.array([]))
kp2, des2 = sift.detectAndCompute(img2, np.array([]))

print(des1.shape, des1)
print(des2.shape, des2)

# print(des1, des2)

# FLANN
# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(np.float32(des1), np.float32(des2), k=3)

draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   flags=0)

cv2.imwrite("kp1.jpg", cv2.drawKeypoints(image=img1, keypoints=kp1,
                                         outImage=np.array([]), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
cv2.imwrite("kp2.jpg", cv2.drawKeypoints(image=img2, keypoints=kp2,
                                         outImage=np.array([]), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
cv2.imwrite("SIFT_MATCH.jpg", cv2.drawMatchesKnn(
    img1, kp1, img2, kp2, matches, None, **draw_params))
