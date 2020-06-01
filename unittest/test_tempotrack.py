import datetime

from pyprone.entities.midifile.tempotrack import PrMidiTempotrack
from pyprone.core.helpers.formats import sec2HMSF, tick2MBT
from mido import MidiFile, open_output
from time import sleep

midifile: MidiFile = MidiFile('./pyprone/resources/midifiles/ahnw.mid')
ports = open_output('Microsoft GS Wavetable Synth 0')

tempotrack = PrMidiTempotrack(midifile)

abs_time = 0
for msgs in tempotrack:
    abs_time += msgs.msg.time
    print(f'{msgs.msg} | {str(msgs.tick):16} | {sec2HMSF(msgs.time)}')

print(vars(tempotrack.cursor(7680)))

def test(tick): # run with py -i
    csr = tempotrack.cursor(tick)
    print(f'MBT  : {tick2MBT(csr.abs_tick)}')
    print(f'HMSF : {sec2HMSF(csr.abs_time)}')
