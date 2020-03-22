import math

# Rotates a point around an origin
# Origin is the new (0, 0) point
# Point is a tuple (x, y) that will be rotated
# Angle is the angle (in degrees) to rotate
def rotate(origin, point, angle):
	ox, oy = origin
	px, py = point
	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return qx, qy

from .logger import logger
logger = logger

from .reporter import reporter
reporter = reporter
