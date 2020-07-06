import tensorflow as tf
import cv2
import argparse
import numpy as np

DEFAULT_CAMERA = 0
INPUT_DETAILS = None
OUTPUT_DETAILS = None
FLOATING_MODEL = None
MEAN = 0.0
STD = 255.0


def load_interpreter(path):
    global INPUT_DETAILS, OUTPUT_DETAILS, FLOATING_MODEL
    interp = tf.lite.Interpreter(model_path=path)
    interp.allocate_tensors()
    INPUT_DETAILS, OUTPUT_DETAILS = interp.get_input_details(), interp.get_output_details()
    FLOATING_MODEL = INPUT_DETAILS[0]['dtype'] == np.float32
    return interp, INPUT_DETAILS[0]['shape'][2], INPUT_DETAILS[0]['shape'][1]


def run_model(interpreter, frame, labels):
    global INPUT_DETAILS, OUTPUT_DETAILS
    interpreter.set_tensor(INPUT_DETAILS[0]['index'], frame)
    interpreter.invoke()
    results = np.squeeze(interpreter.get_tensor(OUTPUT_DETAILS[0]['index']))
    top_k = results.argsort()[-5:][::-1]
    return [(labels[i], float(results[i])) for i in top_k]


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def transform_image(frame, width, height):
    global FLOATING_MODEL, MEAN, STD
    # frame = cv2.resize(frame, (width, height))
    frame = np.expand_dims(frame, axis=0)
    if FLOATING_MODEL:
        frame = (np.float32(frame) - MEAN) / STD
    return frame


def print_results(results):
    for item in results:
        print("{}: {:08.6f}".format(item[0], item[1]))
    print()


def main(args):
    labels = load_labels(args.labels)
    interpreter, width, height = load_interpreter(args.path)
    cam = cv2.VideoCapture(args.camera or DEFAULT_CAMERA)

    while True:
        ret, frame = cam.read()
        frame = cv2.resize(frame, (width, height))
        img = transform_image(frame, width, height)
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            cam.release()
            break
        results = run_model(interpreter, img, labels)
        print_results(results)
        cv2.imshow("Capture Stream", ((np.float32(frame) - 0) / 255))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool for testing a trained model')
    parser.add_argument('-p', '--path', help='Specifies where the saved model lives', required=True)
    parser.add_argument('-c', '--camera', help='Specifies which camera number to use for capturing images', type=int)
    parser.add_argument('-l', '--labels', help='Get labels from file', required=True)
    args = parser.parse_args()
    main(args)
