from socketengine import client
from threading import Thread

import psutil
import socket
import time


def getHostIP():
    host = socket.gethostname()
    return host, socket.gethostbyname(host)


class reporter:
    def __init__(self, address='127.0.0.1', port=8080, start=True, pi=True, channel='reporter', updateTime=1):
        self.socket = None
        self.address = address
        self.port = port
        self.usingPi = pi
        self.channel = channel
        self.updateTime = updateTime
        if self.usingPi:
            from gpiozero import CPUTemperature

            self.getTemp = lambda: CPUTemperature()
        self.stopped = False
        if start:
            self.start()

    def start(self):
        self.startTime = time.time()
        self.socket = client(self.address, self.port).start()
        self.socket.write("connected", True)
        Thread(target=self._update, args=()).start()
        return self

    def _update(self):
        while True:
            if self.stopped:
                self.socket.close()
                return
            data = {}
            hostname, ip = getHostIP()
            cpu = psutil.cpu_percent()
            ram = dict(psutil.virtual_memory()._asdict())['percent']

            data = {
                'hostname': hostname,
                'ip': ip,
                'cpu': cpu,
                'ram': ram,
                'time': time.time(),
                'runtime': (time.time() - self.startTime),
            }
            if self.usingPi:
                data['cpu_temp'] = self.getTemp()
            self.socket.write(self.channel, data)
            time.sleep(self.updateTime)

    def close(self):
        self.stopped = True
