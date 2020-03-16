from threading import Thread

###############################################################

####################
### CAMERA CLASS ###
####################

class camera:
	PI_CAMERA = 1
	USB_CAMERA = 2
	def __init__(self, resolution=(640, 480), framerate=30, camera_type=PI_CAMERA, cam_src=0):
		self.camera_type = camera_type
		if self.camera_type == camera.PI_CAMERA:
			from picamera.array import PIRGBArray
			from picamera import PiCamera
			self.camera = PiCamera()
			self.camera.resolution = resolution
			self.camera.framerate = framerate
			self.rawCapture = PIRGBArray(self.camera, size=resolution)
			self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True)
			self.frame = []
		elif self.camera_type == camera.USB_CAMERA:
			import cv2
			self.stream = cv2.VideoCapture(cam_src)
			ret = self.stream.set(3, resolution[0])
			ret = self.stream.set(4, resolution[1])
			(self.grabbed, self.frame) = self.stream.read()
		else:
			raise RuntimeError("Camera type is not supported.")

		self.stopped = False

	def start(self):
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		if self.camera_type == camera.PI_CAMERA:
			for f in self.stream:
				self.frame = f.array
				self.rawCapture.truncate(0)
				if self.stopped:
					self.stream.close()
					self.rawCapture.close()
					self.camera.close()
		elif self.camera_type == camera.USB_CAMERA:
			while True:
				if self.stopped:
					self.stream.release()
					return
				(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		return self.frame

	def stop(self):
		self.stopped = True

###############################################################
