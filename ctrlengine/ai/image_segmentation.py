from edgetpu.basic.basic_engine import BasicEngine
from edgetpu.utils import image_processing
import numpy as np
from PIL import Image
import cv2


class image_segmentation:
    MODEL_PASCAL = 'models/deeplabv3_mnv2_pascal_quant_edgetpu.tflite'
    MODEL_DM05 = 'models/deeplabv3_mnv2_dm05_pascal_quant_edgetpu.tflite'

    def __init__(self, model=MODEL_PASCAL):
        self.engine = BasicEngine(model)
        _, self.width, self.height, _ = self.engine.get_input_tensor_shape()

    def segment(self, img):
        self.input_image = cv2.resize(img, (self.width, self.height))
        _, raw_result = self.engine.run_inference(self.input_image.flatten())
        result = np.reshape(raw_result, (self.height, self.width))
        self.segmented_img = self.label_to_color_image(result.astype(int)).astype(np.uint8)

    def get_original_image(self):
        return self.input_image

    def get_segmented_image(self):
        return self.segmented_img

    def label_to_color_image(self, label):
        colormap = np.zeros((256, 3), dtype=int)
        indices = np.arange(256, dtype=int)
        for shift in reversed(range(8)):
            for channel in range(3):
                colormap[:, channel] |= ((indices >> channel) & 1) << shift
            indices >>= 3
        return colormap[label]

    def write_image_to_file(self, filename):
        orig = Image.fromarray(self.input_image)
        segm = Image.fromarray(self.segmented_img)
        concated_image = Image.new('RGB', (self.width * 2, self.height))
        concated_image.paste(orig, (0, 0))
        concated_image.paste(segm, (self.width, 0))
        concated_image.save(filename)
