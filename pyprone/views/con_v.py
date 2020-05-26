from typing import Union

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QPlainTextEdit, QLineEdit, QVBoxLayout, QWidget

from pyprone.enums.qt import Position
from pyprone.enums.act import Commands
from pyprone.core import PrObj, PrObjCb
from pyprone.entities import PrText, PrTextFactory
from pyprone.agents import PrWorld, PrAct
import pyprone.helpers as PrHelper

Mapping: dict = {
    # entity based command
    "cls": Commands.PRTEXT_CLEAR,
    "clear": Commands.PRTEXT_CLEAR,

    # cross entity command
    "append": Commands.BROADCAST_TEXT,

    # system command
    "exit": Commands.SYSTEM_EXIT
}

class PrConV(PrObjCb):
    """
    viwe for PrText
    """
    def __init__(self, name: str, world: PrWorld, act: PrAct, target_id: int, position: Union[Position, QPoint]):
        """
        name : name of this view
        target_id : PrObj id to show in this iew
        """
        super().__init__(name)

        # agents 
        self.world = world
        self.act = act

        # entities
        self.id_to_show = target_id

        # view
        self.position: Position = position
        self.area: QPlainTextEdit = None
        self.line: QLineEdit = None
        self.layout: QVBoxLayout = None
        self.window: QWidget = None

        # build
        self.build()

        # connect
        self.line.returnPressed.connect(self.on_return_pressed)

    @property
    def id_to_show(self):
        """ PrObj id to show """
        return self._id_to_show

    @id_to_show.setter
    def id_to_show(self, target_id: int):
        """ PrObj is automatcially assigned/created when id_to_show is changed """
        self._id_to_show = target_id
        self._obj_to_show: PrText = PrTextFactory(self.world.find(target_id))

    @property
    def obj_to_show(self) -> PrText:
        """ PrObj to show """
        return self._obj_to_show

    # build
    def build(self):
        """ build Qt Widgets """
        # view
        self.area = QPlainTextEdit(self.obj_to_show.text)
        #self.area.setFixedSize(600, 400)
        self.area.setFocusPolicy(Qt.NoFocus)

        # input
        self.line = QLineEdit()

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.area)
        self.layout.addWidget(self.line)

        # window
        self.window = QWidget()
        self.window.setMinimumSize(640, 400)
        self.window.setWindowTitle(self.name)
        self.window.setLayout(self.layout)
        if isinstance(self.position, Position):
            if self.position == Position.BOTTOM_RIGHT:
                self.window.move(QPoint(*PrHelper.qt.bottom_right(self.window)))
        elif isinstance(self.position, QPoint):
            self.window.move(self.position)
        else:
            self.window.move(QPoint(0, 0))
        self.window.show()

    def send(self, pid: int, command: Commands, *args: list, **kwargs: dict):
        self.act.do(self.tag, pid, command, *args, **kwargs)

    # callbacks
    def on_return_pressed(self):
        text = self.line.text()

        # console feedback
        self.send(
            self.id_to_show,
            Commands.PRTEXT_APPEND_TEXT,
            text=text)

        # console command
        tokens = text.split(' ')
        cmd = Mapping.get(tokens[0])
        args = tokens[1:len(tokens)]

        if cmd:
            self.send(
                self.id_to_show,
                cmd,
                *args)
        else:
            self.send(
                self.id_to_show,
                Commands.PRTEXT_APPEND_TEXT,
                text='syntax error!')

        self.line.clear()

    def update(self, **kwargs: dict):
        self.area.setPlainText(self.obj_to_show.text)
