from typing import List
from pyprone.core import PrObj
import mido

class PrMidiMsg:
    def __init__(self, msg: mido.Message = None, track: int = None):
        self.mido = msg
        self.tick = msg.time        
        self.tempo = 0
        self.track_no = track

        self.abs_tick = 0
        self.abs_time = 0

class PrMidiCursor:
    def __init__(self, msg: PrMidiMsg = None, tick: int = None):
        self.tick: int = tick
        self.msg: PrMidiMsg = msg # current msg
        self.next_msg: PrMidiMsg = None

class PrMidiTrack:
    def __init__(self, no: int):
        self.msgs: List[PrMidiMsg] = []
        self.no: int = no

    def append(self, msg: PrMidiMsg):
        self.msgs.append(msg)

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n < len(self.msgs):
            self._n += 1
            return self.msgs[self._n - 1]
        else:
            raise StopIteration

class PrMidifile(PrObj):
    """
    entity for midifile
    - midi file data
    - midi cursor data
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.midifile = None
        self.msgs: List[PrMidiMsg] = None
        self.tracks: List[PrMidiTrack] = None
        self.tempo: int = None

    # properties

    # public methods
    def total_msgs(self) -> int:
        n = 0
        for track in self.tracks:
            for msg in track:
                if msg.mido.type != 'sysex':
                    n += 1
        return n

    def load(self, path: str):
        self.midifile = mido.MidiFile(path)
        self.msgs = []
        self.tracks = []
        msg_idx = []
        track_tick_ttl = []
        cursor: PrMidiCursor = None

        # create empty tracks
        for n, track in enumerate(self.midifile.tracks):
            self.tracks.append(PrMidiTrack(n))
            track_tick_ttl.append(0)
            msg_idx.append(0)

        # get initial tempo
        for msg in self.midifile.tracks[0]:
            if msg.type == 'set_tempo':
                self.tempo = msg.tempo
                break

        # assign msgs and tracks
        go: bool = True
        while go:
            go = False
            cursor = None
            for track_n, mido_track in enumerate(self.midifile.tracks):
                go = True if msg_idx[track_n] < len(mido_track) else go
                if msg_idx[track_n] < len(mido_track):
                    next_msg = PrMidiMsg(mido_track[msg_idx[track_n]], track_n)
                    if cursor is None:
                        cursor = PrMidiCursor(next_msg, 0)
                    elif cursor.msg.tick > next_msg.tick + track_tick_ttl[next_msg.track_no]:
                        cursor.msg = next_msg

            if go:                
                pr_msg = PrMidiMsg(cursor.msg.mido, cursor.msg.track_no)
                pr_msg.abs_tick = cursor.msg.tick - (cursor.tick - track_tick_ttl[cursor.msg.track_no])            
                
                cursor.tick += pr_msg.abs_tick
                pr_msg.abs_tick = cursor.tick
                track_tick_ttl[cursor.msg.track_no] += cursor.msg.tick

                if pr_msg.mido.type == 'set_tempo':
                    self.tempo = pr_msg.mido.tempo                    
                pr_msg.abs_time = mido.tick2second(pr_msg.mido.time, self.midifile.ticks_per_beat, 0 if self.tempo is None else self.tempo)
                self.tracks[cursor.msg.track_no].msgs.append(pr_msg)
                self.msgs.append(pr_msg)
                

                msg_idx[cursor.msg.track_no] += 1 # increase msg_idx
                self.log_msg(pr_msg)


    def log_msg(self, msg: PrMidiMsg):
        msg_mido = msg.mido
        if msg.track_no != None:
            if msg_mido.is_meta or msg_mido.type == 'sysex':
                self.log(f'{msg.track_no:02} | {msg_mido.type:16} | {str(msg_mido)} | tick : {msg.abs_tick:08} | tempo : {self.tempo:08} | time : {msg.abs_time}')
            else:
                self.log(f'{msg.track_no:02} | {msg_mido.type:16} | ch : {msg_mido.channel:02} | ctl : {getattr(msg_mido, "control", 0):03} | val : {getattr(msg_mido, "value", 0):03} | mtick : {getattr(msg_mido, "time", 0):08} | tick : {msg.abs_tick:08} | tempo : {self.tempo:08} | time : {msg.abs_time}')
        else:
            if msg_mido.is_meta or msg_mido.type == 'sysex':
                self.log(f'{msg_mido.type:16} | {str(msg_mido)} | tick : {msg.abs_tick:08} | tempo : {self.tempo:08} | time : {msg.abs_time}')
            else:
                self.log(f'{msg_mido.type:16} | ch : {msg_mido.channel:02} | ctl : {getattr(msg_mido, "control", 0):03} | val : {getattr(msg_mido, "value", 0):03} | mtick : {getattr(msg_mido, "time", 0):08} | tick : {msg.abs_tick:08} | tempo : {self.tempo:08} | time : {msg.abs_time}')

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
    return PrMidifile("this is not a PrMidifile bj")
