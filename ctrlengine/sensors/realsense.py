import pyrealsense2 as rs
import numpy as np
import cv2


class realsense_camera:
    RESOLUTION = (640, 480)
    FPS = 30

    def __init__(self, resolution=RESOLUTION, fps=FPS):
        self.resolution = resolution
        self.fps = fps
        self.color_frame = None
        self.depth_frame = None
        self.color_image = None
        self.depth_image = None
        self.frames = None
        self.pipe = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, resolution[0], resolution[1], rs.format.z16, fps)
        self.config.enable_stream(rs.stream.color, resolution[0], resolution[1], rs.format.bgr8, fps)
        self.pipe.start(self.config)

    def _update(self):
        while True:
            frames = self.pipe.wait_for_frames()
            self.color_frame = frames.get_color_frame()
            self.depth_frame = frames.get_depth_frame()
            if not self.color_frame or not self.depth_frame:
                continue
            return

    def get_color_frame(self):
        self._update()
        return self.color_frame

    def get_color_image(self):
        self.color_image = np.asanyarray(self.get_color_frame().get_data())
        return self.color_image

    def get_depth_frame(self):
        self._update()
        return depth_frame

    def get_depth_image(self):
        self.depth_image = np.asanyarray(self.get_depth_frame().get_data())
        return self.depth_image

    def get_colormap(self, alpha=0.03, colormap=cv2.COLORMAP_JET):
        return cv2.applyColorMap(cv2.convertScaleAbs(self.get_depth_image(), alpha=alpha), colormap)

    def apply_colormap(self, image, alpha=0.03, colormap=cv2.COLORMAP_JET):
        return cv2.applyColorMap(cv2.convertScaleAbs(image, alpha=alpha), colormap)

    def get_combined_image(self):
        self._update()
        return np.hstack((np.asanyarray(self.color_frame.get_data()), np.asanyarray(self.depth_frame.get_data())))

    def stop(self):
        self.pipe.stop()
