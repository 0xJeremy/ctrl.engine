import cv2
from pose_detection import pose_detection

engine = pose_detection()
cam = cv2.VideoCapture(2)
ret, frame = cam.read()
print(engine.detect(frame))