from typing import List, Union

from pyprone.enums.act import Commands as Cmds
from pyprone.core import PrObj
from pyprone.agents import PrWorld
from pyprone.entities import PrText, PrTextFactory

class PrAct(PrObj):
    """
    give some action to the Entities in the World
    """
    def __init__(self, name: str, world: PrWorld):
        super().__init__(name)
        self.world = world
        self.funcs: dict = {
            # entity based command
            Cmds.PRTEXT_APPEND_TEXT: self.prtext_append_text,
            Cmds.PRTEXT_CLEAR: self.prtext_clear_screen,

            # cross entity command
            Cmds.BROADCAST_TEXT: self.broadcast_text,

            # system command
            Cmds.SYSTEM_EXIT: self.system_exit_application
        }

    def do(self, tag: str, pid: int, command: Cmds, *args: list, **kwargs: dict):
        """ do action """
        func: callable = self.parse(tag, command)
        func(pid, *args, **kwargs)

    def parse(self, tag: str, command: Cmds) -> callable:
        """ parse command and return act function """
        func: callable = self.funcs[command]
        return func

    # act functions
    def prtext_append_text(self, pid: int, *args, **kwargs):
        """
        append text to PrText
        args: None
        kwargs: text(str: text to append)
        """
        if kwargs.get('text'):
            pr_text: PrText = self.world.find(pid)
            pr_text.append(kwargs.get('text'))

    def prtext_clear_screen(self, pid: int, *args, **kwargs):
        """
        clear text in PrText
        args: None
        kwargs: None
        """
        pr_text: PrText = self.world.find(pid)
        pr_text.clear()

    def broadcast_text(self, pid: int, *args, **kwargs):
        """
        broadcast text to all PrMon
        args: text to broadcast(str)
        kwargs: None
        """
        if args:
            text = args[0]
            if text:
                mon: PrText = self.world.find('mon')
                if mon:
                    mon.append(text)

    def system_exit_application(self, pid: int, *args, **kwargs):
        """
        exit application
        args: None
        kwargs: None
        """
        exit()
