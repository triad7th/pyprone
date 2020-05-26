from typing import Union

from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QPlainTextEdit, QVBoxLayout

from pyprone.core.enums.qt import WnPos, WnStatus
from pyprone.agents import PrWorld, PrAct

from .view import PrView

class PrMonV(PrView):
    """
    monitor view for PrText
    """
    def __init__(self,
        name: str,
        world: PrWorld,
        act: PrAct,
        target_id: int,
        position: Union[WnPos, QPoint] = WnPos.NONE,
        status: WnStatus = WnStatus.NONE):
        """
        name : name of this view
        target_id : PrObj id to show in this iew
        """
        # view
        self.area: QPlainTextEdit = None
        self.layout: QVBoxLayout = None
        super().__init__(name, world, act, target_id, position, status)

    # build
    def build(self):
        """ build Qt Widgets """
        # view
        self.area = QPlainTextEdit(self.obj_to_show.text)
        self.area.setFont(QFont('consolas', 12))
        self.area.setStyleSheet("background-color: black; color: white;")
        self.area.setMaximumBlockCount(128)
        self.area.setFocusPolicy(Qt.NoFocus)
        

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.area)

        # window
        super().build()

        # add layout
        self.window.setLayout(self.layout)
        self.window.setStyleSheet("background-color: black; color: white;")

    # time callback
    def update(self, **kwargs: dict):
        self.area.setPlainText(self.obj_to_show.text)
        self.area.moveCursor(QTextCursor.End)
