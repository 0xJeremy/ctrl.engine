import cv2

class tracker():
	OPENCV_OBJECT_TRACKERS = {
		'csrt': cv2.TrackerCSRT_create,
		'kcf': cv2.TrackerKCF_create,
		'boosting': cv2.TrackerBoosting_create,
		'mil': cv2.TrackerMIL_create,
		'tld': cv2.TrackerTLD_create,
		'medianflow': cv2.TrackerMedianFlow_create,
		'mosse': cv2.TrackerMOSSE_create
	}
	def __init__(self, type='kcf'):
		self.tracker = tracker.OPENCV_OBJECT_TRACKERS[type]()
		self.box = None
		self.ref = None

	def init_from_reference(self, img, ref):
		self.ref = ref
		self.tracker.init(img, ref)

	def init_from_selection(self, window_name, img):
		self.ref = cv2.selectROI(window_name, img, fromCenter=False, showCrosshair=True)
		self.tracker.init(img, self.ref)
		return self.ref

	def update(self, img):
		ret, self.box = self.tracker.update(img)
		if ret:
			return self.box
		return None

	def get_box(self):
		return self.box
