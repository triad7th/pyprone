from PyQt5.QtCore import QTimer, QElapsedTimer
from PyQt5.QtWidgets import QApplication

etimer = QElapsedTimer()

def cb():    
    global etimer
    print(etimer.elapsed())

app = QApplication([])

timer = QTimer()
timer.timeout.connect(cb)
timer.start(1000)
etimer.start()

app.exec_()

    