from time import sleep
from PyQt5.QtCore import QTimer, QElapsedTimer
from PyQt5.QtWidgets import QApplication

from pyprone.entities.midifile import PrMidiFile
from pyprone.entities.midifile.track import PrMidiTrack
from pyprone.core.helpers.formats import sec2HMSF, tick2MBT, MBT2tick, tempo2bpm
from mido import open_output

midifile = PrMidiFile('midifile')
midifile.load('./pyprone/resources/midifiles/a-whole-new-world.mid')
port = open_output('Microsoft GS Wavetable Synth 0')

etimer = QElapsedTimer()
etimerT = QElapsedTimer()

etimerT.start()
for track in midifile.tracks:
    etimer.start()
    for t in track:
        pass
    print(f'{track.no} : {etimer.elapsed()}')

print(f'total elapsed : {etimerT.elapsed()}')

midifile.tracks[0].rewind(MBT2tick(7, 1, 0, midifile.tpb))
print(midifile.tracks[0])
print(midifile.tracks[0].idx)
print(midifile.tracks[0].msg)