from edgetpu.detection.engine import DetectionEngine
import numpy as np
from PIL import Image

class face_detection():
	MODEL = 'models/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite'
	def __init__(self, threshold=0.5, num_results=10):
		self.engine = DetectionEngine(face_detection.MODEL)
		self.objs = None
		self.boxes = None
		self.scores = None
		self.threshold = threshold
		self.num_results = num_results

	def set_threshold(self, num):
		self.threshold = num

	def set_max_results(self, num):
		self.num_results = num

	def detect(self, img):
		img = Image.fromarray(img)
		self.objs = self.engine.detect_with_image(img,
												  threshold=self.threshold,
												  keep_aspect_ratio=True,
												  relative_coord=False,
												  top_k=self.num_results)
		self.boxes = [obj.bounding_box.flatten().tolist() for obj in self.objs]
		self.scores = [obj.score for obj in self.objs]
		return self.objs

	def get_bounding_boxes(self):
		return self.boxes

	def get_scores(self):
		return self.scores
