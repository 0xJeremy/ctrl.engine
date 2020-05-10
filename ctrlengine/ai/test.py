###############################
### TESTING USB ACCELERATOR ###
###############################

# import cv2
# from face_detection import face_detection
# import time

# engine = face_detection()
# cam = cv2.VideoCapture(2)

# while True:
# 	start = time.time()
# 	ret, frame = cam.read()
# 	key = cv2.waitKey(10)
# 	if key == ord('q'):
# 		cam.release()
# 		break
# 	start = time.time()
# 	engine.detect(frame)
# 	boxes = engine.get_bounding_boxes()
# 	for box in boxes:
# 		cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255,0,0), 2)
# 	cv2.imshow("frame", frame)
# 	print("{:.2f} ms".format((time.time()-start)*1000))

###############################################################

############################
### TESTING GOOGLE CLOUD ###
############################

# from cloud_vision import cloud_vision
# import cv2
# import time

# engine = cloud_vision()
# cam = cv2.VideoCapture(2)

# ret, frame = cam.read()

# start = time.time()
# print(engine.detect_faces(frame))
# print("{:.2f} ms".format((time.time()-start)*1000))

###############################################################

###########################
### TESTING AZURE CLOUD ###
###########################

# from azure_vision import azure_vision
# import cv2
# import time

# engine = azure_vision()
# cam = cv2.VideoCapture(2)

# ret, frame = cam.read()

# start = time.time()
# print(engine.detect_faces(frame))
# print("{:.2f} ms".format((time.time()-start)*1000))

###############################################################

############################
### TESTING HAAR CASCADE ###
############################

# import cv2
# from haar_cascade import haar_cascade
# import time

# engine = haar_cascade(model=haar_cascade.FACE)

# cam = cv2.VideoCapture(2)

# while True:
# 	start = time.time()
# 	ret, frame = cam.read()
# 	faces = engine.detect(frame)
# 	k = cv2.waitKey(10)
# 	if k == ord('q'):
# 		cam.release()
# 		break
# 	for (x,y,w,h) in faces:
# 		cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
# 	cv2.imshow('frame', frame)
# 	print("{:.2f} ms".format((time.time()-start)*1000))

###############################################################

####################
### TEST TRACKER ###
####################

from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import cv2
from tracker import tracker

TRACK_TYPE = 'mosse'

track_obj = tracker(type=TRACK_TYPE)
ref = None

cam = cv2.VideoCapture(2)
fps = None

while True:
	ret, frame = cam.read()
	frame = imutils.resize(frame, width=600)
	(H, W) = frame.shape[:2]

	if ref is not None:
		box = track_obj.update(frame)
		if box is not None:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		fps.update()
		fps.stop()
		info = [
			("Tracker", TRACK_TYPE),
			("Success", "Yes" if box != None else "No"),
			("FPS", "{:.2f}".format(fps.fps())),
		]
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(10)
	if key == ord("q"):
		cam.release()
		cv2.destroyAllWindows()
		break

	elif key == ord("s"):
		ref = track_obj.init_from_selection("Frame", frame)
		fps = FPS().start()
