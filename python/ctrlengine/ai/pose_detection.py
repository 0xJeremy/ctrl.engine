from PoseEngine import PoseEngine
import numpy as np
from PIL import Image

class pose_detection():
  MODEL_S = 'models/posenet_mobilenet_v1_075_353_481_quant_decoder_edgetpu.tflite'
  MODEL_M = 'models/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite'
  MODEL_L = 'models/posenet_mobilenet_v1_075_721_1281_quant_decoder_edgetpu.tflite'

  def __init__(self, mirror=False, model=MODEL_S):
    self.engine = PoseEngine(model, mirror)
    self.resize = {
      pose_detection.MODEL_S: (481, 353),
      pose_detection.MODEL_M: (641, 481),
      pose_detection.MODEL_L: (1281, 721),
    }[model]
    self.poses = None

  def detect(self, img):
    img = Image.fromarray(img)
    img.resize(self.resize, Image.NEAREST)
    self.poses, _ = self.engine.DetectPosesInImage(np.uint8(img))
    return self.poses

  def get_poses(self):
    return self.poses
