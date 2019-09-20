import cv2

# Initiate SIFT detector
img1 = np.zeros((640, 480, 3))
img2 = np.zeros((640, 480, 3))
orb = cv2.ORB_create()

# Find keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
