import cv2
from pose_detection import pose_detection
from face_detection import face_detection
from image_segmentation import image_segmentation

engine = image_segmentation()
cam = cv2.VideoCapture(2)

import time

ret, frame = cam.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
engine.segment(frame)
engine.write_image_to_file('test.jpg')
# img = engine.get_segmented_image()

# while True:
# 	ret, frame = cam.read()
# 	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
# 	key = cv2.waitKey(10) & 0xFF
# 	if key == ord('q'):
# 		cam.release()
# 		break
# 	# start = time.time()
# 	engine.segment(frame)
# 	# print("{:.2f} ms".format((time.time()-start)*1000))
# 	# boxes = engine.get_bounding_boxes()
# 	# for box in boxes:
# 	# 	cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255,0,0), 2)
# 	cv2.imshow("frame", engine.get_segmented_image())

