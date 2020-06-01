from pyprone.core.enums.act import PrCmds as Cmds
from pyprone.core import PrObj
from pyprone.entities import PrText

from .world import PrWorld
from .actfuncs import ActfuncConsole

class PrAct(PrObj, ActfuncConsole):
    """
    give some action to the Entities in the World
    """
    def __init__(self, name: str, world: PrWorld):
        super().__init__(name)
        self.world = world
        self.funcs: dict = {
            # entity based command
            Cmds.PRTEXT_APPEND_TEXT: self.prtext_append_text,
            Cmds.PRTEXT_BACK_TEXT: self.prtext_back_text,
            Cmds.PRTEXT_CLEAR: self.prtext_clear_screen,

            # cross entity command
            Cmds.BROADCAST_TEXT: self.broadcast_text,
            Cmds.BROADCAST_ENTITY_LIST: self.broadcast_entity_list,

            # system command
            Cmds.SYSTEM_EXIT: self.system_exit_application
        }

    def do(self, pid: int, command: Cmds, **kwargs: dict):
        """ do action """
        pr_obj = self.world.find(pid)
        if pr_obj:
            func: callable = self.parse(pr_obj.tag, command)
            kwargs['pid'] = pid
            func(**kwargs)

    def parse(self, tag: str, command: Cmds) -> callable:
        """ parse command and return act function """
        func: callable = self.funcs[command]
        return func