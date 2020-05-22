from PyQt5.QtWidgets import QApplication
from pyprone.objects import PrTime

class FakeSysconView():
    def __init__(self, name):
        self.name = name

    def update(self):
        print(f"{self.name} update")

app = QApplication([])
time = PrTime(1000)
syscon1 = FakeSysconView("syscon1")
syscon2 = FakeSysconView("syscon2")
syscon3 = FakeSysconView("syscon3")
syscon4 = FakeSysconView("syscon4")

time.register(syscon1.update)
time.register(syscon2.update)
time.register(syscon3.update)
time.register(syscon4.update)

app.exec_()
