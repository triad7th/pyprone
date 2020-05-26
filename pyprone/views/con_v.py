from typing import Union

from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QPlainTextEdit, QLineEdit, QVBoxLayout

from pyprone.core.enums.qt import WnPos, WnStatus
from pyprone.core.enums.act import PrCmds
from pyprone.agents import PrWorld, PrAct

from .view import PrView

class PrConV(PrView):
    """
    console view for PrText
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
        self.line: QLineEdit = None
        self.layout: QVBoxLayout = None
        super().__init__(name, world, act, target_id, position, status)

        # command mapping
        self.map: dict = {
            # entity based command
            "cls": self.cmd_clear,
            "clear": self.cmd_clear,

            # cross entity command
            "append": self.cmd_broadcast,
            "list": self.cmd_entity_list,

            # system command
            "exit": self.cmd_exit
        }

        # connect
        self.line.returnPressed.connect(self.on_return_pressed)
    # build
    def build(self):
        """ build Qt Widgets """
        # view
        self.area = QPlainTextEdit(self.obj_to_show.text)
        self.area.setFont(QFont('consolas', 12))
        self.area.setStyleSheet("background-color: black; color: white;")
        self.area.setMaximumBlockCount(32)
        self.area.setFocusPolicy(Qt.NoFocus)

        # input
        self.line = QLineEdit()
        self.line.setFont(QFont('consolas', 12))
        self.line.setStyleSheet("background-color: black; color: white;")

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.area)
        self.layout.addWidget(self.line)

        # window
        super().build()

        # add layout
        self.window.setLayout(self.layout)
        self.window.setStyleSheet("background-color: black; color: white;")
        self.adjust()        

    # commands
    def cmd_append(self, text: str):
        self.send(pid=self.id_to_show, command=PrCmds.PRTEXT_APPEND_TEXT, text=text)

    def cmd_add(self, text: str):
        self.send(pid=self.id_to_show, command=PrCmds.PRTEXT_ADD_TEXT, text=text)

    def cmd_clear(self, args: list):
        self.send(pid=self.id_to_show, command=PrCmds.PRTEXT_CLEAR)

    def cmd_broadcast(self, args: list):
        if len(args) > 0:
            self.send(pid=self.id_to_show, command=PrCmds.BROADCAST_TEXT, text=args[0])

    def cmd_entity_list(self, args: list):
        self.send(pid=self.id_to_show, command=PrCmds.BROADCAST_ENTITY_LIST)

    def cmd_exit(self, args: list):
        self.send(pid=self.id_to_show, command=PrCmds.SYSTEM_EXIT)

    # input
    def on_return_pressed(self):
        text = self.line.text()

        # console feedback
        self.cmd_append(text)

        # console command
        if self.run(text):
            self.cmd_add('>>>')
        else:
            self.cmd_add('syntax error!\n>>>')
        # clear line
        self.line.clear()

    # act
    def send(self, pid: int, command: PrCmds, **kwargs: dict):
        self.act.do(pid, command, **kwargs)

    def get_cmd(self, text) -> str:
        tokens = text.split(' ')
        return tokens[0]

    def get_args(self, text) -> list:
        tokens = text.split(' ')
        return tokens[1:len(tokens)]

    def run(self, text: str) -> bool:
        cmd = self.get_cmd(text)
        args = self.get_args(text)
        func = self.map.get(cmd)
        if func:
            func(args)
            return True
        return False

    # time
    def update(self, **kwargs: dict):
        if not self.area.toPlainText() == self.obj_to_show.text:
            self.area.setPlainText(self.obj_to_show.text)
            self.area.moveCursor(QTextCursor.End)

