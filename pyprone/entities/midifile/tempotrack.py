from typing import Union
from mido import MidiTrack, MidiFile, Message, MetaMessage, tick2second

from pyprone.core.enums.midifile import DEFAULT_TEMPO, DEFAULT_TICKS_PER_BEAT

from .msg import PrMidiMsg
from .track import PrMidiTrack
from .cursor import PrMidiCursor

class PrMidiTempotrack(PrMidiTrack):
    def __init__(self, core: MidiFile):
        super().__init__(100, 'TempoTrack')   
        self._core = core     
        if core:
            self.load()

    @property
    def tpb(self):
        return self._core.ticks_per_beat if self._core else None

    # special methods
    def __repr__(self):
        return (f'  t-trk | {str(self.no):<16} | {str(self.name):<16}' +
            f' | msg#: {str(len(self.msgs)):<10}')

    # private methods
    def __get_msg(self, msg: MetaMessage, csr: PrMidiCursor):
        ''' comprehead core messages and generate a new PrMidiMsg '''
        tick = msg.time + csr.tick
        if tick > 0:
            delta = tick2second(msg.time, self.tpb, csr.tempo)
        else:
            delta = 0        
        return PrMidiMsg(msg.copy(), tick=tick, time=delta)

    # create tempo track from core track 0
    def load(self):
        csr = PrMidiCursor(tempo=DEFAULT_TEMPO, tick=0)
        for msg in self._core.tracks[0]:
            csr.tick = 0
            if msg.type == 'set_tempo':
                self.append(self.__get_msg(msg, csr)) # msg.time: tempo tick
                csr.tempo = msg.tempo
            else:
                csr.tick += msg.time # msg.time: other ticks
    # get cursor by given tick
    def cursor(self, tick: int) -> PrMidiCursor:
        ''' returns abs_tick, abs_time from the given tick '''
        csr = PrMidiCursor(tempo=DEFAULT_TEMPO, abs_tick=0, abs_time=0)
        self.rewind()
        for t in self: # find the right tempo
            if t.tick >= tick:
                break
            csr.abs_tick, csr.abs_time, csr.tempo = t.tick, t.time, t.msg.tempo # counting abs_time
        # delta tick / delta time
        dtick = tick - csr.abs_tick
        dtime = tick2second(dtick, self.tpb, csr.tempo)
        # return abs_tick / abs_time
        return PrMidiCursor(
            tempo=csr.tempo,
            abs_tick=csr.abs_tick + dtick,
            abs_time=csr.abs_time + dtime)
