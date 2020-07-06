from threading import Thread
import cv2


class camera:
    RESOLUTION = (640, 480)

    def __init__(self, cam_src=0, resolution=RESOLUTION):
        self.cam = cv2.VideoCapture(cam_src)
        self.cam.set(3, resolution[0])
        self.cam.set(4, resolution[1])
        self.ret = None
        self.frame = None
        self.stopped = False
        Thread(target=self.run, args=()).start()

    def get_frame(self):
        return self.frame

    def read(self):
        return self.ret, self.frame

    def run(self):
        while True:
            if self.stopped:
                self.cam.release()
                return
            self.ret, self.frame = self.cam.read()

    def stop(self):
        self.stopped = True
