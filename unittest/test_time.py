from PyQt5.QtWidgets import QApplication

from pyprone.core import PrObjCb
from pyprone.agents import PrClock
class FakeObjCb(PrObjCb):
    def __init__(self, name):
        PrObjCb.__init__(self, name)

    def update(self, number: int, boy: str):
        self.log(f"{self.name}|{number}|{boy} update")


def test_PrObjCb():
    app = QApplication([])
    time = PrClock('1s timer', 1000)
    obj1 = FakeObjCb("obj1")
    obj2 = FakeObjCb("obj2")

    time.register(obj1.update, number=10, boy='a')
    time.register(obj2.update, number=11, boy='b')

    app.exec_()

test_PrObjCb()