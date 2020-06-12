from typing import Union
from mido import Message, MetaMessage, tick2second
from mido.midifiles import meta

class PrMidiMsg():
    def __init__(self, core: Union[Message, MetaMessage], **kwargs: dict):
        self._core = core
        self._tick = kwargs.get('tick', None)
        self._secs = kwargs.get('secs', None)

        if set(['tpb', 'tempo']) <= set(kwargs):
            self.update(kwargs['tpb'], kwargs['tempo'])

    def bytes(self):
        return self._core.bytes()

    def update(self, tpb: int, tempo: int):
        self._tick = self._core.time
        self._secs = tick2second(self._core.time, tpb, tempo)
    @property
    def core(self):
        return self._core
    @property
    def type(self):
        return getattr(self._core, 'type', None)
    @property
    def tick(self):
        return getattr(self, '_tick', None)
    @property
    def secs(self):
        return float(getattr(self, '_secs', None))
    @property
    def channel(self):
        return getattr(self._core, 'channel', None)
    @property
    def note(self):
        return getattr(self._core, 'note', None)
    @property
    def velocity(self):
        return getattr(self._core, 'velocity', None)
    @property
    def value(self):
        return getattr(self._core, 'value', None)
    @property
    def program(self):
        return getattr(self._core, 'program', None)
    @property
    def control(self):
        return getattr(self._core, 'control', None)
    @property
    def pitch(self):
        return getattr(self._core, 'pitch', None)
    @property
    def data(self):
        return getattr(self._core, 'data', None)
    @property
    def inf(self):
        return getattr(self._core, 'inf', None)
    @property
    def frame_type(self):
        return getattr(self._core, 'frame_type', None)
    @property
    def frame_value(self):
        return getattr(self._core, 'frame_value', None)
    @property
    def pos(self):
        return getattr(self._core, 'pos', None)
    @property
    def song(self):
        return getattr(self._core, 'song', None)
    @property
    def name(self):
        return getattr(self._core, 'name', None)
    @property
    def tempo(self):
        return getattr(self._core, 'tempo', None)

    @property
    def is_meta(self) -> bool:
        return self._core.is_meta

    def __repr__(self):
        if self.is_meta:
            rep = f'  meta | {self.type:16}'
            spec = meta._META_SPEC_BY_TYPE[self.type]
            attributes = []
            for name in spec.attributes:
                attributes.append('{:16} | {:16}'.format(
                    name[0:16], str(getattr(self._core, name))[0:16]))
            attributes = ' | '.join(attributes[0:1])
            if attributes:
                rep += f' | {str(attributes)}'
        else:
            rep = f'   msg | {self.type:16}'
            if self.type == 'note_off' or self.type == 'note_on':
                rep += f' | ch  : {self.channel:<10} | note: {self.note:<10}'
                rep += f' | vel : {self.velocity:<10}'
            elif self.type == 'playtouch':
                rep += f' | ch  : {self.channel:<10} | note: {self.note:<10}'
                rep += f' | val : {self.value:<10}'
            elif self.type == 'control_change':
                rep += f' | ch  : {self.channel:<10} | ctrl: {self.control:<10}'
                rep += f' | val : {self.value:<10}'
            elif self.type == 'program_change':
                rep += f' | ch  : {self.channel:<10} | prgm: {self.program:<10} |'
            elif self.type == 'aftertouch':
                rep += f' | ch  : {self.channel:<10} | val : {self.program:<10} |'
            elif self.type == 'pitchwheel':
                rep += f' | ch  : {self.channel:<10} | pich: {self.pitch:<10} |'
            elif self.type == 'sysex':
                rep += f' | data: {str(self.data)[0:10]:<10} | inf : {str(self.inf)[0:10]:<10} |'
            elif self.type == 'quarter_frame':
                rep += f' | type: {str(self.frame_type)[0:10]:<10}'
                rep += f' | val  : {str(self.frame_value)[0:10]:<10} |'
            elif self.type == 'songpos':
                rep += f' | pos : {str(self.pos)[0:10]:<10}'
            elif self.type == 'song_select':
                rep += f' | song: {str(self.song)[0:10]:<10}'
            elif self.type == 'tune_request':
                pass

        return f'{rep[0:82]:82} | tick: {self.tick:>10} | secs: {self.secs:>16.4}'
