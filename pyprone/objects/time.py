from PyQt5.QtCore import QTimer

class PrTime():
    def __init__(self, interval):
        self.callbacks = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(interval)

    def register(self, callback):
        self.callbacks.append(callback)

    def run(self):
        for callback in self.callbacks:
            callback()

