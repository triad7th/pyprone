from typing import List
from sys import maxsize as MAXINT
from mido import MidiFile

from pyprone.core import PrObj
from pyprone.core.enums.midifile import DEFAULT_TEMPO

from .msg import PrMidiMsg
from .track import PrMidiTrack
from .tempotrack import PrMidiTempotrack as PrTempo

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
        self._tempotrack: PrTempo = None

    # properties
    @property
    def tempo(self):
        return self._tempo
    @property
    def tempotrack(self) -> PrTempo:
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
        csr_abs_tick, csr_track = MAXINT, None
        for track in self.tracks:
            if not track.stuck:
                if csr_abs_tick > track.tick:
                    csr_abs_tick = track.tick
                    csr_track = track
        return csr_track

    def __rewind(self, tick=0):
        ''' set playhead to the given tick '''
        for track in self.tracks:
            track.rewind(tick)

    # public methods
    def load(self, path: str):
        """ load a midifile """
        # open midifile
        self._midifile = MidiFile(path)
        # create a tempo track
        self._tempotrack = PrTempo(self._midifile)
        # create other tracks
        for n, msgs in enumerate(self._midifile.tracks):
            if n > 0: # skip the tempo track
                csr_abs_tick, csr_abs_secs = 0, 0
                track = PrMidiTrack(n)
                for msg in msgs:
                    if msg.type == 'track_name':
                        track.name = msg.name
                    if msg.time > 0:
                        csr_abs_tick += msg.time
                        delta = self.tempotrack.cursor(csr_abs_tick)[PrTempo.SECS] - csr_abs_secs
                        csr_abs_secs += delta
                    else:
                        delta = 0
                    track.append(PrMidiMsg(msg.copy(), tick=msg.time, secs=delta))
                track.rewind()
                self.tracks.append(track)
                print(track)

    def run(self, tick=0):
        """ return iterator from the given tick """
        self.__rewind(tick)
        track = PrMidiTrack()
        while track:
            track = self.__next_track() # choosing a next track
            if track:
                yield track
                track.forward()
        yield None

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
