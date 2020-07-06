import cv2
from realsense import realsense_camera

cam = realsense_camera()

while True:

    image = cam.get_combined_image()

    cv2.imshow('RealSense', image)
    cv2.waitKey(1)
