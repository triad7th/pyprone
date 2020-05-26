from pyprone.core.enums.act import PrCmds as Cmds
from pyprone.core import PrObj
from pyprone.agents import PrWorld
from pyprone.entities import PrText

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
            Cmds.PRTEXT_ADD_TEXT: self.prtext_add_text,
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

    # act functions
    def prtext_append_text(self, pid: int, text: str, **kwargs: dict):
        """ append text to PrText """
        pr_text: PrText = self.world.find(pid)
        pr_text.append(text)

    def prtext_add_text(self, pid: int, text: str, **kwargs: dict):
        """ append text to PrText """
        pr_text: PrText = self.world.find(pid)
        pr_text.add(text)

    def prtext_clear_screen(self, pid: int, **kwargs: dict):
        """ clear text in PrText """
        pr_text: PrText = self.world.find(pid)
        pr_text.clear()

    def broadcast_text(self, text: str, **kwargs: dict):
        """ broadcast text to all PrMon """
        mon: PrText = self.world.find('mon')
        if mon:
            mon.append(text)

    def broadcast_entity_list(self, pid: int, **kwargs: dict):
        """ broadcast entity list to all PrMon """
        pr_text: PrText = self.world.find(pid)
        mon: PrText = self.world.find('mon')
        if mon:
            for entity in self.world.entities:
                mon.append(entity.whoami)
            pr_text.append(f'{len(self.world.entities)} entities loaded')

    def system_exit_application(self, **kwargs: dict):
        """ exit application """
        exit()
