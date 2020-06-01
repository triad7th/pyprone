from typing import List

from PyQt5.QtCore import QTimer
from pyprone.core import PrObj

class PrCallback():
    def __init__(self, func: callable, **kwargs: dict):
        self.func = func
        self.kwargs = kwargs

    def call(self):
        self.func(**self.kwargs)

class PrClock(PrObj):
    """
    set of callback calls for one interval
    """
    def __init__(self, name: str, interval: int):
        self.cbs: List[PrCallback] = []
        self._interval = interval

        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(self._interval)
        super().__init__(name)

    def register(self, func: callable, **kwargs: dict):
        self.cbs.append(PrCallback(func, **kwargs))
        self.log(f'register : {kwargs.get("pid")}({kwargs.get("name")}) as interval {self._interval}')

    def run(self):
        for callback in self.cbs:
            if isinstance(callback, PrCallback):
                callback.call()
            elif callable(callback):
                callback()

class PrTime(PrObj):
    """
    set of PrTime with different interval with preset
    register() makes life easier for adding any PrObj to this
    """
    def __init__(self, name: str):
        self.clocks: List[PrClock] = []

        self.default: PrClock = PrClock('default_clock', 1000)
        self.clocks.append(PrClock('text_clock', 50))
        self.clocks.append(PrClock('midifile_clock', 10))
        super().__init__(name)

    def find(self, name: str):
        clocks = [clock for clock in self.clocks if clock.name == name]
        return clocks[0] if clocks else self.default

    def register(self, obj: any, **kwargs: dict):
        if isinstance(obj, PrObj):
            if obj.tag in ['PrConV', 'PrMonV']:
                self.find('text_clock').register(func=obj.update, name=obj.name, pid=obj.id)
        else:
            self.log(f"couldn't figure out the PrObj type of {str(obj)}")
