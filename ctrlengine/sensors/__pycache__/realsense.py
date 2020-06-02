import pyrealsense2 as rs
import numpy as np
import cv2

class realsense_camera():
	RESOLUTION = (640, 480)
	FPS = 30
	def __init__(self, resolution=RESOLUTION, fps=FPS):
		self.color_frame = None
		self.depth_frame = None
		self.frames = None
		self.pipe = rs.pipeline()
		self.config = rs.config()
		self.resolution = resolution
		self.fps = fps
		self.config.enable_stream(rs.stream.depth, resolution[0], resolution[1], rs.format.z16, fps)
		self.config.enable_stream(rs.stream.color, resolution[0], resolution[1], rs.format.bgr8, fps)
		self.pipe.start(self.config)

	def get_color_frame(self):
		frames = self.pipeline.wait_for_frames()
		self.color_frame = frames.get_color_frame()
		return np.asanyarray(self.color_frame.get_data())

	def get_depth_frame(self):
		frames = self.pipeline.wait_for_frames()
		self.depth_frame = frames.get_depth_frame()
		return np.asanyarray(self.depth_frame.get_data())

	def get_colormap(self, alpha=0.03, colormap=cv2.COLORMAP_JET):
		return cv2.applyColorMap(cv2.convertScaleAbs(self.get_depth_frame(), alpha=alpha), colormap)

	def update(self):
		frames = self.pipeline.wait_for_frames()
		self.color_frame = frames.get_color_frame()
		self.depth_frame = frames.get_depth_frame()
		return [self.color_frame, self.depth_frame]

	def stop(self):
		self.pipe.stop()
