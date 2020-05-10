import cv2

class tracker():
	# Most Accurate, Slowest: CSRT
	# Middle of the road: KCF
	# Fastest: Mosse
	OPENCV_OBJECT_TRACKERS = {
		'csrt': cv2.TrackerCSRT_create, # More accurate than KCF, but slightly slower
		'kcf': cv2.TrackerKCF_create, # Fast, doesn't do well with occlusion
		'boosting': cv2.TrackerBoosting_create, # Slow, outdated
		'mil': cv2.TrackerMIL_create, # Better accuraccy than Boosting
		'tld': cv2.TrackerTLD_create, # Prone to false-positives (do not use)
		'medianflow': cv2.TrackerMedianFlow_create, # Doesn't do well with fast moving targets
		'mosse': cv2.TrackerMOSSE_create # *Extremely* fast, less accurate than KCF
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
