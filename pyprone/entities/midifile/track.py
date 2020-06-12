from .msg import PrMidiMsg

class PrMidiTrack():
    def __init__(self, no: int = None, name: str = None):
        self._msgs: PrMidiMsg = []
        self._name: str = name
        self._no: int = no
        self._idx: int = 0
        self._tick: int = 0
        self._secs: float = 0

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name: str):
        self._name = name
    @property
    def no(self):
        return self._no
    @no.setter
    def no(self, no: int):
        self._no = no
    @property
    def msgs(self):
        return self._msgs
    @property
    def idx(self):
        ''' index for messages that this track has '''
        return self._idx
    @property
    def end(self):
        ''' if the internal message index is stuck at the end '''
        return self.idx >= len(self.msgs)
    @property
    def stuck(self):
        ''' if the internal message index is stuck at the end '''
        return self.idx >= len(self.msgs)
    @property
    def tick(self):
        ''' absolute tick time as of the message index '''
        return self._tick + self.lookup().tick if not self.stuck else 0            
    @property
    def secs(self):
        ''' absolute time(sec) as of the message index '''
        return self._secs + self.lookup().secs if not self.stuck else 0            
    @property
    def msg(self) -> PrMidiMsg:
        ''' get a msg at the idx '''
        return self.lookup()
    @property
    def length(self) -> int:
        ''' get a length of msg list '''
        return len(self.msgs)

    # public methods
    def append(self, msg: PrMidiMsg):
        self._msgs.append(msg)
        self.forward()
    def rewind(self):
        ''' rewind the internal cursor to zero '''
        self._idx = 0
        self._tick = 0
        self._secs = 0
    def lookup(self) -> PrMidiMsg:
        ''' look up the vaule before get '''
        if not self.stuck:
            return self.msgs[self.idx]
    def forward(self):
        ''' calculate the tick(abs) and increase the internal message idx '''
        if not self.stuck:
            self._tick += self.lookup().tick
            self._secs += self.lookup().secs
            self._idx += 1

    # special methods
    def __repr__(self):
        return (f' track | {str(self.no):<16} | {str(self.name):<16}' +
            f' | msg#: {str(len(self.msgs)):<10}')

    def __iter__(self):
        self.rewind()
        while not self.stuck:
            yield self
            self.forward()
