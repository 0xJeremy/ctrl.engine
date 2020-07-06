from datetime import datetime
from inspect import getframeinfo, stack

DEPTH = 2
TRACEBACK = -2


def generateHeader(logType):
    t = datetime.now()
    return '|{}{}Z| [{}] '.format(t.strftime('%Y-%m-%dT%H:%M:%S.'), t.strftime('%f')[0:3], logType)


class logger:
    def __init__(self, path="robot.log", keepOpen=False):
        self.path = path
        self.keepOpen = keepOpen
        if self.keepOpen:
            self.f = open(self.path, 'a+')
        else:
            self.f = None

    def log(self, msg):
        self._writeLog(msg, 'LOG')

    def debug(self, msg):
        self._writeLog(msg, 'DBG')

    def warning(self, msg):
        self._writeLog(msg, 'WRN')

    def error(self, msg):
        self._writeLog(msg, 'ERR')
        fileinfo = getframeinfo(stack()[DEPTH][0])
        raise Exception('ERROR: {} at <{}:{}>'.format(msg, fileinfo.filename, fileinfo.lineno))

    def _writeLog(self, msg, logType):
        header = generateHeader(logType)
        fileinfo = getframeinfo(stack()[DEPTH][0])
        filepath = ''.join(fileinfo.filename.split('/')[TRACEBACK:])
        logString = '{}{} <{}:{}>\n'.format(header, msg, fileinfo.filename, fileinfo.lineno)
        if self.keepOpen:
            if self.f is None:
                self.f = open(self.path, 'a+')
            self.f.write(logString)
        else:
            with open(self.path, 'a+') as f:
                f.write(logString)

    def close(self):
        if self.keepOpen and self.f is not None:
            self.f.close()
            self.f = None
