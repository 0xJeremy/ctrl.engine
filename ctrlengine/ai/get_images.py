import cv2
import argparse
import os

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_CAMERA = 0

def main(args):
	im_counter = 0
	label_counter = 0
	cam = cv2.VideoCapture(args.camera or DEFAULT_CAMERA)
	cam.set(cv2.CAP_PROP_FRAME_WIDTH, args.width or DEFAULT_WIDTH)
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height or DEFAULT_HEIGHT)
	path = args.path
	os.mkdir('{}/label{}'.format(path, label_counter))
	while True:
		ret, frame = cam.read()
		frame = cv2.resize(frame, (224, 224))
		key = cv2.waitKey(10) & 0xFF
		if key == ord('q'):
			cam.release()
			break
		if key == ord('n'):
			label_counter += 1
			os.mkdir('{}/label{}'.format(path, label_counter))
		if key == ord('p'):
			cv2.imwrite(os.path.join(path , 'label{}/IMAGE{}.jpg'.format(label_counter, im_counter)), frame)
			im_counter += 1
		cv2.imshow("Capture Stream", frame)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='A tool for getting images to classify')
	parser.add_argument('-p', '--path', help='Specifies where to save the images captures', required=True)
	parser.add_argument('-c', '--camera', help='Specifies which camera number to use for capturing images', type=int)
	# parser.add_argument('-pi', '--pi', help='Specifies the device being used is a raspberry pi (with pi camera)', action='store_true')
	parser.add_argument('-width', '--width', help='Specifies the width of the image being captured (default 640px)', type=int)
	parser.add_argument('-height', '--height', help='Specifies the height of the image being captured (default 480px)', type=int)
	args = parser.parse_args()
	main(args)