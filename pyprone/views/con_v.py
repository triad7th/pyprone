from typing import Union
from os import listdir

from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QPlainTextEdit, QLineEdit, QVBoxLayout

from pyprone.core.enums import WnPos, WnStatus, PrCmds
from pyprone.core.widgets import QConsole

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
        self.area: QConsole = None
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
            "files": self.cmd_files,
            "help": self.cmd_help,
            "exit": self.cmd_exit
        }

    # build
    def build(self):
        """ build Qt Widgets """
        # view
        self.area = QConsole()
        self.area.on_text_pressed = self.on_text_pressed
        self.area.on_backspace_pressed = self.on_backspace_pressed
        self.area.on_return_pressed = self.on_return_pressed
        self.area.setFocusPolicy(Qt.StrongFocus)

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.area)

        # window
        super().build()

        # add layout
        self.window.setLayout(self.layout)
        self.window.setStyleSheet("background-color: black; color: white;")
        self.adjust()
        

    # commands
    def cmd_append(self, text: str):
        self.send(command=PrCmds.PRTEXT_APPEND_TEXT, text=text)

    def cmd_back(self, blocker: str):
        self.send(command=PrCmds.PRTEXT_BACK_TEXT, blocker=blocker)

    def cmd_clear(self, args: list):
        self.send(command=PrCmds.PRTEXT_CLEAR)

    def cmd_broadcast(self, args: list):
        if len(args) > 0:
            self.send(command=PrCmds.BROADCAST_TEXT, text=args[0])

    def cmd_entity_list(self, args: list):
        self.send(command=PrCmds.BROADCAST_ENTITY_LIST)

    def cmd_help(self, args: list):
        self.send(command=PrCmds.PRTEXT_APPEND_TEXT, text=f'{" ".join(self.map.keys())}\n')

    def cmd_files(self, args: list):
        self.send(command=PrCmds.PRTEXT_APPEND_TEXT, text=f'{" ".join(listdir("./pyprone/resources/midifiles"))}\n')

    def cmd_exit(self, args: list):
        self.send(command=PrCmds.SYSTEM_EXIT)

    # input
    def on_text_pressed(self, text):
        self.cmd_append(text)

    def on_backspace_pressed(self, cursor):
        self.cmd_back('>>>')

    def on_return_pressed(self, cursor):
        cmd = self.obj_to_show.lastline('>>>')
        self.cmd_append('\n') # add return character to the entity
        if self.run(cmd):
            self.cmd_append('>>>')
        else:
            self.cmd_append('syntax error!\n>>>')

    # act
    def send(self, command: PrCmds, **kwargs: dict):
        """ pid : self.id_to_show """
        self.act.do(kwargs['pid'] if kwargs.get('pid') else self.id_to_show, command, **kwargs)

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
