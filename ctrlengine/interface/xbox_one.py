import pygame
from pygame.locals import JOYAXISMOTION, JOYHATMOTION
from pygame.locals import JOYBUTTONUP, JOYBUTTONDOWN
from threading import Thread

### MAPPING
# Left  Joystick X: 0
# Left  Joystick Y: 1
# Right Joystick X: 2
# Right Joystick Y: 3
#
# Left  Trigger: 4
# Right Trigger: 5
#
# A: 6
# B: 7
# X: 8
# Y: 9
#
# Right Bumper: 10
# Left  Bumper: 11
#
# Back: 12
# Start: 13
#
# Left  Joystick Press: 14
# Right Joystick Press: 15
#
# D-Pad: 16
###


class xbox_one:
    class ctrls:
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
        LEFTTHUMB = 14
        RIGHTTHUMB = 15
        DPAD = 16

    AXISMAP = {0: ctrls.LTHUMBX, 1: ctrls.LTHUMBY, 3: ctrls.RTHUMBX, 4: ctrls.RTHUMBY}

    TRIGGERMAP = {2: ctrls.RTRIGGER, 5: ctrls.LTRIGGER}

    BUTTONMAP = {
        0: ctrls.A,
        1: ctrls.B,
        2: ctrls.X,
        3: ctrls.Y,
        4: ctrls.LB,
        5: ctrls.RB,
        6: ctrls.BACK,
        7: ctrls.START,
        8: ctrls.LEFTTHUMB,
        9: ctrls.RIGHTTHUMB,
    }

    def __init__(self, controllerCallBack=None, joystickNo=0, deadzone=0.1, scale=1, invertYAxis=False):
        self.controllerCallBack = controllerCallBack
        self.joystickNo = joystickNo
        self.deadzone = [deadzone * -1, deadzone]
        self.scale = scale
        self.invertYAxis = invertYAxis
        self.controlCallbacks = {}

        self.stopped = False
        self._cVs = {i: 0 for i in range(16)}
        self._cVs[16] = (0, 0)

        pygame.init()
        pygame.joystick.init()
        joy = pygame.joystick.Joystick(self.joystickNo)
        joy.init()
        Thread(target=self._start, args=()).start()

    def _start(self):
        while not self.stopped:
            for event in pygame.event.get():
                if event.type == JOYAXISMOTION:
                    if event.axis in self.AXISMAP:
                        yAxis = True if (event.axis == self.LTHUMBY or event.axis == self.RTHUMBY) else False
                        self.updateControlValue(self.AXISMAP[event.axis], self._sortOutAxisValue(event.value, yAxis))
                    elif event.axis in self.TRIGGERMAP:
                        self.updateControlValue(self.TRIGGERMAP[event.axis], self._sortOutTriggerValue(event.value))
                elif event.type == JOYHATMOTION:
                    self.updateControlValue(self.ctrls.DPAD, event.value)

                elif event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:
                    if event.button in self.BUTTONMAP:
                        self.updateControlValue(self.BUTTONMAP[event.button], self._sortOutButtonValue(event.type))

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

    def _sortOutAxisValue(self, value, yAxis=False):
        if yAxis and self.invertYAxis:
            value = value * -1
        value = value * self.scale
        if value < self.deadzone[1] and value > self.deadzone[0]:
            value = 0
        return value

    def _sortOutTriggerValue(self, value):
        return max(0, (value + 1) / 2) * self.scale

    def _sortOutButtonValue(self, eventType):
        return 1 if eventType == JOYBUTTONDOWN else 0

    ##################
    ### PROPERTIES ###
    ##################

    @property
    def LTHUMBX(self):
        return self._cVs[self.ctrls.LTHUMBX]

    @property
    def LTHUMBY(self):
        return self._cVs[self.ctrls.LTHUMBY]

    @property
    def RTHUMBX(self):
        return self._cVs[self.ctrls.RTHUMBX]

    @property
    def RTHUMBY(self):
        return self._cVs[self.ctrls.RTHUMBY]

    @property
    def RTRIGGER(self):
        return self._cVs[self.ctrls.RTRIGGER]

    @property
    def LTRIGGER(self):
        return self._cVs[self.ctrls.LTRIGGER]

    @property
    def A(self):
        return self._cVs[self.ctrls.A]

    @property
    def B(self):
        return self._cVs[self.ctrls.B]

    @property
    def X(self):
        return self._cVs[self.ctrls.X]

    @property
    def Y(self):
        return self._cVs[self.ctrls.Y]

    @property
    def LB(self):
        return self._cVs[self.ctrls.LB]

    @property
    def RB(self):
        return self._cVs[self.ctrls.RB]

    @property
    def BACK(self):
        return self._cVs[self.ctrls.BACK]

    @property
    def START(self):
        return self._cVs[self.ctrls.START]

    @property
    def LEFTTHUMB(self):
        return self._cVs[self.ctrls.LEFTTHUMB]

    @property
    def RIGHTTHUMB(self):
        return self._cVs[self.ctrls.RIGHTTHUMB]

    @property
    def DPAD(self):
        return self._cVs[self.ctrls.DPAD]
