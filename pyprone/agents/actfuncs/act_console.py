class ActfuncConsole:
    # act functions for console
    def prtext_append_text(self, pid: int, text: str, **kwargs: dict):
        """ append text to PrText """
        pr_text: PrText = self.world.find(pid)
        pr_text.append(text)

    def prtext_back_text(self, pid: int, blocker: str, **kwargs: dict):
        """ append text to PrText """
        pr_text: PrText = self.world.find(pid)
        pr_text.back(blocker)

    def prtext_clear_screen(self, pid: int, **kwargs: dict):
        """ clear text in PrText """
        pr_text: PrText = self.world.find(pid)
        pr_text.clear()

    def broadcast_text(self, text: str, **kwargs: dict):
        """ broadcast text to all PrMon """
        mon: PrText = self.world.find('mon')
        if mon:
            mon.append(text + '\n')

    def broadcast_entity_list(self, pid: int, **kwargs: dict):
        """ broadcast entity list to all PrMon """
        pr_text: PrText = self.world.find(pid)
        mon: PrText = self.world.find('mon')
        if mon:
            for entity in self.world.entities:
                mon.append(entity.whoami + '\n')
            pr_text.append(f'{len(self.world.entities)} entities loaded\n')

    def system_exit_application(self, **kwargs: dict):
        """ exit application """
        exit()