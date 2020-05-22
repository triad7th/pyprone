from pyprone.objects import PrSys

class PrSysCmd():
    def __init__(self, objects):
        # object
        self.syscon = objects.get('syscon', None)
        self.sysmon = objects.get('sysmon', None)
        self.objects = objects

        # command list
        self.commands = {
            'cls': self.cls,
            'exit': self.exit,
            'monitor': self.monitor
        }

    # public methods
    def add(self, cmd, func):
        self.commands[cmd] = func

    def mon(self, text):
        if self.sysmon:
            self.sysmon.text += f'{text}\n'

    def con(self, text):
        if self.syscon:
            self.syscon.text += f'{text}\n'

    # private
    def command(self, text):
        self.con(f'>{text}')
        args = text.split()
        cmd = args[0]
        func = self.commands.get(cmd, self.error)
        return func(args)

    # commands
    def cls(self, args):
        self.syscon.text = ''

    def exit(self, args):
        exit()

    def monitor(self, args):
        self.mon('monitor')

    def error(self, args):
        self.con("syntax error")
