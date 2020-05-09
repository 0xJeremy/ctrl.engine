from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils.dataset_utils import read_label_file
import numpy as np
from PIL import Image

class object_detection():
	MODEL_V1 = 'models/ssd_mobilenet_v1_coco_quant_postprocess_edgetpu.tflite'
	MODEL_V2 = 'models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite'
	LABELS   = 'models/coco_labels.txt'
	def __init__(self, threshold=0.5, num_results=10, model=MODEL_V2, labels=LABELS):
		self.engine = DetectionEngine(model)
		self.model_labels = read_label_file(labels)
		self.objs = None
		self.boxes = None
		self.scores = None
		self.labels = None
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
		self.labels = [self.model_labels[obj.label_id] for obj in self.objs]
		return self.objs

	def get_bounding_boxes(self):
		return self.boxes

	def get_scores(self):
		return self.scores

	def get_labels(self):
		return self.labels
