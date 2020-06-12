from typing import Union
from mido import MidiTrack, MidiFile, Message, MetaMessage, tick2second

from pyprone.core.enums.midifile import DEFAULT_TEMPO, DEFAULT_TICKS_PER_BEAT

from .msg import PrMidiMsg
from .track import PrMidiTrack

class PrMidiTempotrack(PrMidiTrack):
    TEMPO = 0
    TICK = 1
    SECS = 2

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
    def __get_msg(self, msg: MetaMessage, csr_tempo: int, delta_tick: int):
        ''' comprehead core messages and generate a new PrMidiMsg '''
        abs_tick = msg.time + delta_tick
        if abs_tick > 0:
            delta_secs = tick2second(msg.time, self.tpb, csr_tempo)
        else:
            delta_secs = 0        
        return PrMidiMsg(msg.copy(), tick=abs_tick, secs=delta_secs)

    # create tempo track from core track 0
    def load(self):
        csr_tempo, csr_delta_tick = DEFAULT_TEMPO, 0
        for msg in self._core.tracks[0]:
            csr_delta_tick = 0
            if msg.type == 'set_tempo':
                self.append(self.__get_msg(msg, csr_tempo, csr_delta_tick)) # msg.time: tempo tick
                csr_tempo = msg.tempo
            else:
                csr_delta_tick += msg.time # msg.time: other ticks
    # get cursor by given tick
    def cursor(self, tick: int) -> (int, int, int):
        ''' returns tempo, abs_tick, abs_secs from the given tick '''
        csr_tempo, csr_abs_tick, csr_abs_secs = DEFAULT_TEMPO, 0, 0
        self.rewind()
        for t in self: # find the right tempo
            if t.tick >= tick:
                break
            csr_abs_tick, csr_abs_secs, csr_tempo = t.tick, t.secs, t.msg.tempo # counting abs_time
        # delta tick / delta time
        dtick = tick - csr_abs_tick
        dsecs = tick2second(dtick, self.tpb, csr_tempo)
        # return abs_tick / abs_time
        return csr_tempo, csr_abs_tick + dtick, csr_abs_secs + dsecs
