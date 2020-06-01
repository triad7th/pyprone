from typing import List, Union
from sys import maxsize as MAXINT
from mido import MidiFile, Message, MetaMessage, tick2second
from mido.midifiles import merge_tracks

from pyprone.core import PrObj
from pyprone.core.enums.midifile import DEFAULT_TEMPO, DEFAULT_TICKS_PER_BEAT

from .msg import PrMidiMsg
from .track import PrMidiTrack
from .cursor import PrMidiCursor

class PrMidifile(PrObj):
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

    # properties
    @property
    def tempo(self):
        return self._tempo
    @property
    def tempo_track(self) -> PrMidiTrack:
        return self._tracks[0] if len(self._tracks) else None
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
    def __get_tempo(self, abs_tick: int):
        ''' get a tempo at the given tick '''
        if self.tempo_track:
            self.tempo_track.rewind()
            csr = PrMidiCursor(tempo=DEFAULT_TEMPO, abs_tick=0)
            for t in self.tempo_track:       
                csr.abs_tick += t.msg.tick
                if t.msg.type == 'set_tempo':
                    if csr.abs_tick >= abs_tick:
                        return csr.tempo
                    csr.tempo = t.msg.tempo            
        return DEFAULT_TEMPO

    def __get_msg(self, msg: Union[Message, MetaMessage], tempo: int):
        ''' comprehead core messages and generate a new PrMidiMsg '''
        if msg.time > 0:
            delta = tick2second(msg.time, self.tpb, tempo)
            #delta = msg.time * self.tempo * 1e-6 / self.tpb
        else:
            delta = 0        
        return PrMidiMsg(msg.copy(), tick=msg.time, time=delta)

    def __get_tempo_track(self) -> PrMidiTrack:
        track = PrMidiTrack(0)
        csr = PrMidiCursor(tempo=0)

        for msg in self._midifile.tracks[0]:
            track.append(self.__get_msg(msg, csr.tempo))
            if msg.type == 'set_tempo':
                csr.tempo = msg.tempo
        return track

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
        track = self.__get_tempo_track()
        # create other tracks
        for n, msgs in enumerate(self._midifile.tracks):
            if n > 0: # skip the tempo track
                track = PrMidiTrack(n)
                csr = PrMidiCursor(abs_tick=0)
                for msg in msgs:
                    if msg.type == 'track_name':
                        track.name = msg.name
                    if msg.type == 'note_on':
                        debug = True
                    tempo = self.__get_tempo(csr.abs_tick)
                    csr.abs_tick += msg.time
                    track.append(self.__get_msg(msg, self.__get_tempo(csr.abs_tick)))                    
            self.tracks.append(track)
            print(track)

    def run(self):
        csr = PrMidiCursor(time=0)
        track = PrMidiTrack() # empty track for while condition
        while track:
            track = self.__next_track() # choosing a next track
            if track:
                # yield 
                # msg and delta time
                yield track.no, track.msg, max(
                    track.time - csr.time, 0.0), float(track.time), float(csr.time) # negative value is ignored
                                                # 1. there's no minus time waiting!!
                                                # 2. ths negative value must be really small
                csr.time = track.time
                track.forward()

    def merge_run(self):
        csr = PrMidiCursor(tempo=DEFAULT_TEMPO)
        for msg in merge_tracks(self._midifile.tracks):
            yield self.__get_msg(msg, csr.tempo)
            if msg.type == 'set_tempo':
                csr.tempo = msg.tempo


    # public methods

def factory(target_obj: any) -> PrMidifile:
    """ create PrText from any givn object """
    if isinstance(target_obj, PrMidifile):
        return target_obj
    if isinstance(target_obj, str):
        name: str = target_obj
        return PrMidifile(name)
    if isinstance(target_obj, tuple):
        name: str = target_obj[0]
        path: str = target_obj[1]
        pr_midifile = PrMidifile(name)
        pr_midifile.load(path)
        return pr_midifile
    return PrMidifile("this is not a PrMidifile obj")
