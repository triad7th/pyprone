from typing import List, Union
from sys import maxsize as MAXINT
from mido import MidiFile, Message, MetaMessage, tick2second
from mido.midifiles import merge_tracks

from pyprone.core import PrObj
from pyprone.core.enums.midifile import DEFAULT_TEMPO, DEFAULT_TICKS_PER_BEAT

from .msg import PrMidiMsg
from .track import PrMidiTrack
from .cursor import PrMidiCursor
from .tempotrack import PrMidiTempotrack

class PrMidiFile(PrObj):
    """
    entity for midifile (mido wrapper)
    - midi file data
    - midi cursor data
    """

    def __init__(self, name: str):
        super().__init__(name)
        self._midifile: MidiFile = None
        self._tempo: int = DEFAULT_TEMPO
        self._tracks: List[PrMidiTrack] = []
        self._tempotrack: PrMidiTempotrack = None

    # properties
    @property
    def tempo(self):
        return self._tempo
    @property
    def tempotrack(self) -> PrMidiTempotrack:
        return self._tempotrack if self._tempotrack else None
    @property
    def tracks(self):
        return self._tracks
    @tracks.setter
    def tracks(self, tracks: List[PrMidiTrack]):
        self._tracks = tracks
    @property
    def tpb(self): # ticks per beat
        if self._midifile:
            return self._midifile.ticks_per_beat

    # private methods
    def __next_track(self) -> PrMidiTrack:
        '''
        [return 1st]\n
        None: stuck, can't go anymore | PrMidiTrack: the track that has next message\n
        '''
        csr = PrMidiCursor(tick=MAXINT, track=None)
        for track in self.tracks:
            if not track.stuck:
                csr.stuck = False
                if csr.tick > track.tick:
                    csr.tick = track.tick
                    csr.track = track
        return csr.track

    # public methods
    def load(self, path: str):      
        # open midifile
        self._midifile = MidiFile(path)         
        # create a tempo track
        self._tempotrack = PrMidiTempotrack(self._midifile)
        # create other tracks
        for n, msgs in enumerate(self._midifile.tracks):
            if n > 0: # skip the tempo track
                csr = PrMidiCursor(abs_tick=0, abs_time=0)
                track = PrMidiTrack(n)
                for msg in msgs:
                    if msg.type == 'track_name':
                        track.name = msg.name
                    if msg.time > 0:
                        csr.abs_tick += msg.time
                        delta = self.tempotrack.cursor(csr.abs_tick).abs_time - csr.abs_time
                        csr.abs_time += delta
                    else:
                        delta = 0
                    track.append(PrMidiMsg(msg.copy(), tick=msg.time, time=delta))
                track.rewind()
                self.tracks.append(track)
                print(track)

    def run(self):
        csr = PrMidiCursor(abs_time=0)
        track = PrMidiTrack() # empty track for while condition
        while track:
            track = self.__next_track() # choosing a next track
            if track:
                # yield 
                # msg and delta time
                yield (
                    track, csr,
                    max(track.time - csr.abs_time, 0.0))    # negative value is ignored                                                        
                                                            # 1. there's no minus time waiting!!
                                                            # 2. ths negative value must be really small

                csr.abs_time = track.time
                track.forward()

    def merge_run(self):
        csr = PrMidiCursor(tempo=DEFAULT_TEMPO)
        for msg in merge_tracks(self._midifile.tracks):
            yield self.__get_msg(msg, csr.tempo)
            if msg.type == 'set_tempo':
                csr.tempo = msg.tempo


    # public methods

def factory(target_obj: any) -> PrMidiFile:
    """ create PrText from any givn object """
    if isinstance(target_obj, PrMidiFile):
        return target_obj
    if isinstance(target_obj, str):
        name: str = target_obj
        return PrMidiFile(name)
    if isinstance(target_obj, tuple):
        name: str = target_obj[0]
        path: str = target_obj[1]
        pr_midifile = PrMidiFile(name)
        pr_midifile.load(path)
        return pr_midifile
    return PrMidiFile("this is not a PrMidiFile obj")
