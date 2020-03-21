import subprocess
import select
import time

DEADZONE = 4000
RAW_MAX = 32768.0
RAW_MIN = 32767.0
RESPONSE_LENGTH = 140

MAPPING = {"leftX":           (3, 9),
           "leftY":           (13, 19),
           "rightX":          (24, 30),
           "rightY":          (34, 40),
           "dpadUp":          (45, 46),
           "dpadDown":        (50, 51),
           "dpadLeft":        (55, 56),
           "dpadRight":       (60, 61),
           "Back":            (68, 69),
           "Guide":           (76, 77),
           "Start":           (84, 85),
           "leftThumbstick":  (90, 91),
           "rightThumbstick": (95, 96),
           "A":               (100, 101),
           "B":               (104, 105),
           "X":               (108, 109),
           "Y":               (112, 113),
           "leftBumper":      (118, 119),
           "rightBumper":     (123, 124),
           "leftTrigger":     (129, 132),
           "rightTrigger":    (136, 139)}

class xbox_ctrl:

    def __init__(self,refreshRate=30, timeout=2):
        self.proc = subprocess.Popen(['xboxdrv','--no-uinput','--detach-kernel-driver'], stdout=subprocess.PIPE, bufsize=0)
        self.pipe = self.proc.stdout

        self.connectStatus = False
        self.reading = '0' * RESPONSE_LENGTH

        self._refreshTime = 0
        self._refreshDelay = 1.0 / refreshRate

        found = False
        waitTime = time.time() + timeout
        while waitTime > time.time() and not found:
            if self._readable():
                response = self.pipe.readline()
                if response[0:7] == b'No Xbox':
                    raise IOError('No Xbox controller/receiver found')
                found = response[0:12].lower() == b'press ctrl-c'
                if len(response) == RESPONSE_LENGTH:
                    found = True
                    self.connectStatus = True
                    self.reading = response
        if not found:
            self.close()
            raise IOError('Unable to detect Xbox controller/receiver - Run python as sudo')

    #######################
    ### Private Methods ###
    #######################

    def _readable(self):
        readable, writeable, exception = select.select([self.pipe],[],[],0)
        return readable

    def _refresh(self):
        if self._refreshTime < time.time():
            self._refreshTime = time.time() + self._refreshDelay
            if self._readable():
                while self._readable():
                    response = self.pipe.readline()
                    if len(response) == 0:
                        raise IOError('Xbox controller disconnected from USB')
                self.connectStatus = len(response) == RESPONSE_LENGTH
                if self.connectStatus:
                    self.reading = response

    def _axisScale(self, raw, deadzone):
        if abs(raw) < deadzone:
            return 0.0
        if raw < 0:
            return (raw + deadzone) / (RAW_MIN - deadzone)
        return (raw - deadzone) / (RAW_MAX - deadzone)

    def _getValue(self, key, r=True):
        if r:
            self._refresh()
        (start, end) = MAPPING[key]
        return int(self.reading[start:end])

    #######################
    ### Input Functions ###
    #######################

    def leftX(self, deadzone=DEADZONE, r=True):
        return self._axisScale(self._getValue("leftX", r=r), deadzone)

    def leftY(self, deadzone=DEADZONE, r=True):
        return self._axisScale(self._getValue("leftY", r=r), deadzone)

    def rightX(self, deadzone=DEADZONE, r=True):
        return self._axisScale(self._getValue("rightX", r=r), deadzone)

    def rightY(self, deadzone=DEADZONE, r=True):
        return self._axisScale(self._getValue("rightY", r=r), deadzone)

    def dpadUp(self): return self._getValue("dpadUp")
        
    def dpadDown(self): return self._getValue("dpadDown")
        
    def dpadLeft(self): return self._getValue("dpadLeft")
        
    def dpadRight(self): return self._getValue("dpadRight")
        
    def Back(self): return self._getValue("Back")

    def Guide(self): return self._getValue("Guide")

    def Start(self): return self._getValue("Start")

    def leftThumbstick(self): return self._getValue("leftThumbstick")

    def rightThumbstick(self): return self._getValue("rightThumbstick")

    def A(self): return self._getValue("A")
        
    def B(self): return self._getValue("B")

    def X(self): return self._getValue("X")

    def Y(self): return self._getValue("Y")

    def leftBumper(self): return self._getValue("leftBumper")

    def rightBumper(self): return self._getValue("rightBumper")

    def leftTrigger(self): return self._getValue("leftTrigger")
        
    def rightTrigger(self): return self._getValue("rightTrigger")

    def leftStick(self, deadzone=DEADZONE):
        return (self.leftX(deadzone),self.leftY(deadzone, r=False))

    def rightStick(self, deadzone=DEADZONE):
        return (self.rightX(deadzone),self.rightY(deadzone, r=False))

    #########################
    ### Utility Functions ###
    #########################

    def connected(self):
        self._refresh()
        return self.connectStatus

    def close(self): self.proc.kill()
