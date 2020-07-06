import argparse

from edgetpu.detection.engine import DetectionEngine
import numpy as np
import cv2
from PIL import Image
from PIL import ImageDraw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', help='Output image path.')
    parser.add_argument(
        '--keep_aspect_ratio',
        action='store_true',
        help=(
            'keep the image aspect ratio when down-sampling the image by adding '
            'black pixel padding (zeros) on bottom or right. '
            'By default the image is resized and reshaped without cropping. This '
            'option should be the same as what is applied on input images during '
            'model training. Otherwise the accuracy may be affected and the '
            'bounding box of detection result may be stretched.'
        ),
    )
    args = parser.parse_args()

    cam = cv2.VideoCapture(2)

    # Initialize engine.
    # engine = DetectionEngine(args.model)
    engine = DetectionEngine('../models/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite')
    # engine = DetectionEngine('models/face_detection_front.tflite')
    # engine = DetectionEngine('models/mobilenet_ssd_v2_coco_quant_postprocess.tflite')
    # engine = DetectionEngine('models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

    while True:
        ret, frame = cam.read()
        frame = cv2.resize(frame, (257, 257))
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            cam.release()
            break
        img = Image.fromarray(frame)
        objs = engine.detect_with_image(
            img, threshold=0.05, keep_aspect_ratio=args.keep_aspect_ratio, relative_coord=False, top_k=10
        )
        for obj in objs:
            box = obj.bounding_box.flatten().tolist()
            print(obj.score)
            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
        cv2.imshow("capture stream", frame)


if __name__ == '__main__':
    main()
