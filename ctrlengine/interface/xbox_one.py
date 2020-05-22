import pygame
from pygame.locals import *
from threading import Thread
import time

"""
NOTES - pygame events and values
JOYAXISMOTION
event.axis			  event.value
0 - x axis left thumb   (+1 is right, -1 is left)
1 - y axis left thumb   (+1 is down, -1 is up)
2 - x axis right thumb  (+1 is right, -1 is left)
3 - y axis right thumb  (+1 is down, -1 is up)
4 - right trigger
5 - left trigger
JOYBUTTONDOWN | JOYBUTTONUP
event.button
A = 0
B = 1
X = 2
Y = 3
LB = 4
RB = 5
BACK = 6
START = 7
XBOX = 8
LEFTTHUMB = 9
RIGHTTHUMB = 10
JOYHATMOTION
event.value
[0] - horizontal
[1] - vertival
[0].0 - middle
[0].-1 - left
[0].+1 - right
[1].0 - middle
[1].-1 - bottom
[1].+1 - top
"""
class xbox_one():

	class ctrls():
		LTHUMBX = 0
		LTHUMBY = 1
		RTHUMBX = 2
		RTHUMBY = 3
		RTRIGGER = 4
		LTRIGGER = 5
		A = 6
		B = 7
		X = 8
		Y = 9
		LB = 10
		RB = 11
		BACK = 12
		START = 13
		XBOX = 14
		LEFTTHUMB = 15
		RIGHTTHUMB = 16
		DPAD = 17

	class PyGameAxis():
		LTHUMBX = 0
		LTHUMBY = 1
		RTHUMBX = 2
		RTHUMBY = 3
		RTRIGGER = 4
		LTRIGGER = 5

	class PyGameButtons():
		A = 0
		B = 1
		X = 2
		Y = 3
		LB = 4
		RB = 5
		BACK = 6
		START = 7
		XBOX = 8
		LEFTTHUMB = 9
		RIGHTTHUMB = 10

	AXISCONTROLMAP = {PyGameAxis.LTHUMBX: ctrls.LTHUMBX,
					  PyGameAxis.LTHUMBY: ctrls.LTHUMBY,
					  PyGameAxis.RTHUMBX: ctrls.RTHUMBX,
					  PyGameAxis.RTHUMBY: ctrls.RTHUMBY}
	
	TRIGGERCONTROLMAP = {PyGameAxis.RTRIGGER: ctrls.RTRIGGER,
						 PyGameAxis.LTRIGGER: ctrls.LTRIGGER}

	BUTTONCONTROLMAP = {PyGameButtons.A: ctrls.A,
						PyGameButtons.B: ctrls.B,
						PyGameButtons.X: ctrls.X,
						PyGameButtons.Y: ctrls.Y,
						PyGameButtons.LB: ctrls.LB,
						PyGameButtons.RB: ctrls.RB,
						PyGameButtons.BACK: ctrls.BACK,
						PyGameButtons.START: ctrls.START,
						PyGameButtons.XBOX: ctrls.XBOX,
						PyGameButtons.LEFTTHUMB: ctrls.LEFTTHUMB,
						PyGameButtons.RIGHTTHUMB: ctrls.RIGHTTHUMB}
						
	def __init__(self, controllerCallBack=None, joystickNo=0, deadzone=0.1, scale=1, invertYAxis=False):		
		self.controllerCallBack = controllerCallBack
		self.joystickNo = joystickNo
		self.deadzone = [deadzone*-1, deadzone]
		self.scale = scale
		self.invertYAxis = invertYAxis
		self.controlCallbacks = {}

		self.stopped = False

		self._cVs = {self.ctrls.LTHUMBX:0,
					 self.ctrls.LTHUMBY:0,
					 self.ctrls.RTHUMBX:0,
					 self.ctrls.RTHUMBY:0,
					 self.ctrls.RTRIGGER:0,
					 self.ctrls.LTRIGGER:0,
					 self.ctrls.A:0,
					 self.ctrls.B:0,
					 self.ctrls.X:0,
					 self.ctrls.Y:0,
					 self.ctrls.LB:0,
					 self.ctrls.RB:0,
					 self.ctrls.BACK:0,
					 self.ctrls.START:0,
					 self.ctrls.XBOX:0,
					 self.ctrls.LEFTTHUMB:0,
					 self.ctrls.RIGHTTHUMB:0,
					 self.ctrls.DPAD:(0,0)}

		pygame.init()
		pygame.joystick.init()
		joy = pygame.joystick.Joystick(self.joystickNo)
		joy.init()
		Thread(target=self._start, args=()).start()

	def _start(self):
		while not self.stopped:
			for event in pygame.event.get():
				if event.type == JOYAXISMOTION:
					if event.axis in self.AXISCONTROLMAP:
						yAxis = True if (event.axis == self.PyGameAxis.LTHUMBY or event.axis == self.PyGameAxis.RTHUMBY) else False
						self.updateControlValue(self.AXISCONTROLMAP[event.axis], self._sortOutAxisValue(event.value, yAxis))
					if event.axis in self.TRIGGERCONTROLMAP:
						self.updateControlValue(self.TRIGGERCONTROLMAP[event.axis], self._sortOutTriggerValue(event.value))		
				elif event.type == JOYHATMOTION:
					self.updateControlValue(self.ctrls.DPAD, event.value)

				elif event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:
					if event.button in self.BUTTONCONTROLMAP:
						self.updateControlValue(self.BUTTONCONTROLMAP[event.button], self._sortOutButtonValue(event.type))
		
	def stop(self):
		self.stopped = True

	def updateControlValue(self, control, value):
		if self._cVs[control] != value:
			self._cVs[control] = value
			self.doCallBacks(control, value)
	
	def doCallBacks(self, control, value):
		if self.controllerCallBack != None:
			self.controllerCallBack(control, value)
		if control in self.controlCallbacks:
			self.controlCallbacks[control](value)
			
	def setupControlCallback(self, control, callbackFunction):
		self.controlCallbacks[control] = callbackFunction

	def _sortOutAxisValue(self, value, yAxis = False):
		if yAxis and self.invertYAxis:
			value = value * -1
		value = value * self.scale
		if value < self.deadzone[1] and value > self.deadzone[0]:
			value = 0
		return value

	def _sortOutTriggerValue(self, value):
		return max(0,(value + 1) / 2) * self.scale

	def _sortOutButtonValue(self, eventType):
		return 1 if eventType == JOYBUTTONDOWN else 0

	##################
	### PROPERTIES ###
	##################

	@property
	def LTHUMBX(self): return self._cVs[self.ctrls.LTHUMBX]

	@property
	def LTHUMBY(self): return self._cVs[self.ctrls.LTHUMBY]

	@property
	def RTHUMBX(self): return self._cVs[self.ctrls.RTHUMBX]

	@property
	def RTHUMBY(self): return self._cVs[self.ctrls.RTHUMBY]

	@property
	def RTRIGGER(self): return self._cVs[self.ctrls.RTRIGGER]

	@property
	def LTRIGGER(self): return self._cVs[self.ctrls.LTRIGGER]

	@property
	def A(self): return self._cVs[self.ctrls.A]

	@property
	def B(self): return self._cVs[self.ctrls.B]

	@property
	def X(self): return self._cVs[self.ctrls.X]

	@property
	def Y(self): return self._cVs[self.ctrls.Y]

	@property
	def LB(self): return self._cVs[self.ctrls.LB]

	@property
	def RB(self): return self._cVs[self.ctrls.RB]

	@property
	def BACK(self): return self._cVs[self.ctrls.BACK]

	@property
	def START(self): return self._cVs[self.ctrls.START]

	@property
	def XBOX(self): return self._cVs[self.ctrls.XBOX]

	@property
	def LEFTTHUMB(self): return self._cVs[self.ctrls.LEFTTHUMB]

	@property
	def RIGHTTHUMB(self): return self._cVs[self.ctrls.RIGHTTHUMB]

	@property
	def DPAD(self): return self._cVs[self.ctrls.DPAD]
