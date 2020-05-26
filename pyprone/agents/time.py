from typing import List

from PyQt5.QtCore import QTimer
from pyprone.core import PrObj

class PrCallback():
    def __init__(self, func: callable, **kwargs: dict):
        self.func = func
        self.kwargs = kwargs

    def call(self):
        self.func(**self.kwargs)

class PrTime(PrObj):
    """
    just bunch of time callback calls
    """
    def __init__(self, name: str, interval: int):
        self.cbs: List[PrCallback] = []
        self._interval = interval

        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(self._interval)
        PrObj.__init__(self, name)

    def register(self, func: callable, **kwargs: dict):
        self.cbs.append(PrCallback(func, **kwargs))
        self.log(f'register : {kwargs.get("pid")}({kwargs.get("name")}) as interval {self._interval}')

    def run(self):
        for callback in self.cbs:
            if isinstance(callback, PrCallback):
                callback.call()
            elif callable(callback):
                callback()
