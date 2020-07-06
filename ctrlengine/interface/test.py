import time
from xbox_one import xbox_one


def controlCallBack(controllerID, value):
    print("Control Id = {}, Value = {}".format(controllerID, value))


def leftThumbX(xValue):
    print("LX {}".format(xValue))


def leftThumbY(yValue):
    print("LY {}".format(yValue))


ctrl = xbox_one(controlCallBack, deadzone=30, scale=100, invertYAxis=True)

ctrl.setupControlCallback(ctrl.ctrls.LTHUMBX, leftThumbX)
ctrl.setupControlCallback(ctrl.ctrls.LTHUMBY, leftThumbY)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("User cancelled")

except:
    print("Unexpected error")
    raise

finally:
    ctrl.stop()
