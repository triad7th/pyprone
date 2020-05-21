from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Text
TEXT = ""

# GUI:
app = QApplication([])
text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.NoFocus)
message = QLineEdit()
layout = QVBoxLayout()
layout.addWidget(text_area)
layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.show()


# Event handlers:
def display_new_messages():
    global TEXT
    new_message = TEXT
    if new_message:
        text_area.appendPlainText(new_message)
        TEXT = ""
        

def send_message():
    global TEXT
    TEXT = message.text()
    message.clear()

# Signals:
message.returnPressed.connect(send_message)
timer = QTimer()
timer.timeout.connect(display_new_messages)
timer.start(100)

app.exec_()
