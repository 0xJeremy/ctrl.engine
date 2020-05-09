import cv2

base = 'haar/haarcascade_'

class haar_cascade():
	EYE = base+'eye.xml'
	EYE_GLASSES = base+'eye_tree_eyeglasses.xml'
	CAT = base+'frontalcatface.xml'
	CAT_EXTENDED = base+'frontalcatface_extended.xml'
	FACE = base+'frontalface_default.xml'
	FACE_ALT = base+'frontalface_alt.xml'
	FACE_ALT2 = base+'frontalface_alt2.xml'
	FACE_ALT_TREE = base+'frontalface_alt_tree.xml'
	BODY = base+'fullbody.xml'
	LEFT_EYE = base+'lefteye_2splits.xml'
	RIGHT_EYE = base+'righteye_2splits.xml'
	RUS_LICENSE = base+'russian_plate_number.xml'
	RUS_LICENSE_16STAGES = base+'license_plate_rus_16.stages.xml'
	LOWER_BODY = base+'lowerbody.xml'
	PROFILE_FACE = base+'profileface.xml'
	SMILE = base+'smile.xml'
	UPPER_BODY = base+'upperbody.xml'
	def __init__(self, model=FACE, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20)):
		self.classifier = cv2.CascadeClassifier(model)
		self.scaleFactor = scaleFactor
		self.minNeighbors = minNeighbors
		self.minSize = minSize
		self.results = None

	def setScaleFactor(self, scaleFactor):
		self.scaleFactor = scaleFactor

	def setMinNeighbors(self, minNeighbors):
		self.minNeighbors = minNeighbors

	def setMinSize(self, minSize):
		self.minSize = minSize

	def detect(self, img):
		self.results = self.classifier.detectMultiScale(
				img,
				scaleFactor=self.scaleFactor,
				minNeighbors=self.minNeighbors,
				minSize=self.minSize
			)
		return self.results

	def get_results(self):
		return self.results
