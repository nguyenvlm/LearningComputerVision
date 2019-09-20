# Digital Image Processing

**Teacher:**  [**Ph.D.** Ngo Quoc Viet](https://sites.google.com/site/ngoquviet/)

**Students:**
- Vuong Le Minh Nguyen - 43.01.104.117
- Luong Cong Tam - 43.01.104.117

**Google Classroom:** 

--------------------------

- __<u>Day 1</u>__
    - Generative model
    - Discriminative model
    - K Nearest Neighbor
- __<u>Day 2</u>__
    - Point features
        - Feature detector (based on high-variant patch): 
            1. Auto-correlation: using harris detector [-2 -1 0 1 2] or convolve the image with Gaussian gradient (var = 1)
            2. Estimate patch's importance based on eigenvector and eigenvalue of the auto-correlation matrix
        - Adaptive non-maximal suppression:
            1. To avoid choosing many patchs from the same area, consider choosing a local maxima of which response value is greater than 10% of the other neighbors
            2. Suppress non-maximal features based on Hessian.
        - Feature descriptors:
            - MOPS, SIFT (SUFT, ORB), PCA-SIFT, GLOH
            - GLOH and SIFT are recommended in practice.
    - SIFT:
        1. Scale-space extrema detection
        2. Keypoint localization
        3. Orientation assignment
        4. Generation of keypoint descriptors
        - **Algorithm details:**
            Construct Scale Space -> Take Difference of Gaussians -> Locate DoG Extrema -> Sub Pixel Locate Potential Feature Points -> Filter Edge and Low Contrast Responses -> Assign Keypoints Orientations -> Build Keypoint Descriptors