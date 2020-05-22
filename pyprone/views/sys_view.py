from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QPlainTextEdit, QLineEdit, QVBoxLayout, QWidget

from pyprone.objects import PrSys
import pyprone.helpers as PrHelper

class PrSysView():
    def __init__(self, syscon, syscon_cmd=None, add_input=False, title='PsSysView', pos=None):
        # object
        self.syscon = syscon

        # command
        self.syscon_cmd = syscon_cmd

        # view
        self.area = QPlainTextEdit(self.syscon.text)
        self.area.setFixedSize(600, 400)
        self.area.setFocusPolicy(Qt.NoFocus)

        # input
        if add_input: self.line = QLineEdit()

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.area)
        if add_input: self.layout.addWidget(self.line)

        # window
        self.window = QWidget()
        self.window.setWindowTitle(title)
        self.window.setLayout(self.layout)
        if pos:
            p = QPoint(*PrHelper.qt.bottom_right(self.window))
            self.window.move(p + pos)
        else:
            self.window.move(QPoint(*PrHelper.qt.bottom_right(self.window)))
        self.window.show()

        # connect
        if add_input: self.line.returnPressed.connect(self.return_pressed)

    def return_pressed(self):
        text = self.line.text()        
        self.syscon_cmd.command(text)        
        self.line.clear()

    def update(self):
        self.area.setPlainText(self.syscon.text)
