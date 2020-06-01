from .track import PrMidiTrack
from .msg import PrMidiMsg

class PrMidiCursor():
    ''' cursor for midifile '''
    def __init__(self,
        tick: int = None,
        abs_tick: int = None,
        time: float = None,
        abs_time: float = None,
        track: PrMidiTrack = None, 
        msg: PrMidiMsg = None,
        stuck: bool = False,
        tempo: int = None):
        self.tick: int = tick
        self.abs_tick: int = abs_tick
        self.time: float = time
        self.abs_time: float = abs_time
        self.track: PrMidiTrack = track
        self.msg: PrMidiMsg = msg
        self.stuck: bool = stuck
        self.tempo: int = tempo

