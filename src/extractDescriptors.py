"""
Description:  Calculates the keypoints and descriptors for a set of BGR images.
Inputs:       List of BGR images to calculate keypoints and descriptors for
Returns:     "kps" which is a list of keypoints for each image. "descs" which is a list of descriptors for each keypoint.
"""

import cv2
import numpy as np

def extract_descriptors(imgs):
    kps = []
    descs = []

    sift = cv2.xfeatures2d.SIFT_create()

    for img in imgs:
        
        # use gaussian blur to remove some noise and convert to grayscale
        img = cv2.GaussianBlur(img,(5,5),0)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # kp - a set of keypoint objects (pt,size,angle,response,octave) https://docs.opencv.org/3.4/d2/d29/classcv_1_1KeyPoint.html
        # des - a set of descriptors for each keypoint. 128 bin values per keypoint
        kp, des = sift.detectAndCompute(gray_img, None)

        kps.append(kp)
        descs.append(des)

        # Leaving this for now. uncomment to see the keypoints on the image.
        # kp_img = cv2.drawKeypoints(img, kp, None, color=(0, 255, 0),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # cv2.imshow('SIFT', kp_img)
        # cv2.waitKey()

    return kps, descs
