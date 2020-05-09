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