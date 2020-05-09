from edgetpu.classification.engine import ClassificationEngine
from edgetpu.utils.dataset_utils import read_label_file
import numpy as np
from PIL import Image

class image_classification():
	MODEL_EFFICIENT_S  = 'models/efficientnet-edgetpu-S_quant_edgetpu.tflite'
	MODEL_EFFICIENT_M  = 'models/efficientnet-edgetpu-M_quant_edgetpu.tflite'
	MODEL_EFFICIENT_L  = 'models/efficientnet-edgetpu-L_quant_edgetpu.tflite'

	MODEL_MOBILENET_V1 = 'models/mobilenet_v1_1.0_224_quant_edgetpu.tflite'
	MODEL_MOBILENET_V2 = 'models/mobilenet_v2_1.0_224_quant_edgetpu.tflite'

	MODEL_INCEPTION_V1 = 'models/inception_v1_224_quant_edgetpu.tflite'
	MODEL_INCEPTION_V2 = 'models/inception_v2_224_quant_edgetpu.tflite'
	MODEL_INCEPTION_V3 = 'models/inception_v3_299_quant_edgetpu.tflite'
	MODEL_INCEPTION_V4 = 'models/inception_v4_299_quant_edgetpu.tflite'

	LABELS = 'models/imagenet_labels.txt'

	def __init__(self, threshold=0.5, num_results=10, model=MODEL_EFFICIENT_S, labels=LABELS):
		self.engine = ClassificationEngine(model)
		self.model_labels = read_label_file(labels)
		self.objs = None
		self.scores = None
		self.labels = None
		self.threshold = threshold
		self.num_results = num_results

	def set_threshold(self, num):
		self.threshold = num

	def set_max_results(self, num):
		self.num_results = num

	def classify(self, img):
		img = Image.fromarray(img)
		self.objs = self.engine.classify_with_image(img,
												    threshold=self.threshold,
												    top_k=self.num_results)
		self.scores = [obj[1] for obj in self.objs]
		self.labels = [self.model_labels[obj[0]] for obj in self.objs]
		return self.objs

	def get_scores(self):
		return self.scores

	def get_labels(self):
		return self.labels
