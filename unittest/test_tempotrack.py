import datetime

from pyprone.entities.midifile.tempotrack import PrMidiTempotrack as PrTempo
from pyprone.core.helpers.formats import sec2HMSF, tick2MBT, MBT2tick, tempo2bpm
from mido import MidiFile, open_output
from time import sleep

midifile: MidiFile = MidiFile('./pyprone/resources/midifiles/ahnw-short.mid')
ports = open_output('Microsoft GS Wavetable Synth 0')
tpb = midifile.ticks_per_beat

tempotrack = PrTempo(midifile)

abs_secs = 0
for msgs in tempotrack:
    abs_secs += msgs.msg.secs
    print(f'{msgs.msg} | {str(msgs.tick):16} | {tick2MBT(msgs.tick, tpb):16} | {sec2HMSF(msgs.secs)}')

def test(tick): # run with py -i
    tempo, abs_tick, abs_secs = tempotrack.cursor(tick)
    print(f'TICK   : {tick}')
    print(f'TEMPO  : {tempo}')
    print(f'BPM    : {tempo2bpm(tempo)}')
    print(f'MBT    : {tick2MBT(abs_tick, tpb)}')
    print(f'HMSF   : {sec2HMSF(abs_secs)}')


test(7680)
print(MBT2tick(6, 1, 0, tpb))
