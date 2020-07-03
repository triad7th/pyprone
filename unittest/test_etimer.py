from time import sleep
from PyQt5.QtCore import QTimer, QElapsedTimer
from PyQt5.QtWidgets import QApplication

from pyprone.entities.midifile import PrMidiFile
from pyprone.entities.midifile.track import PrMidiTrack
from pyprone.core.helpers.formats import sec2HMSF, tick2MBT, MBT2tick, tempo2bpm
from mido import open_output

etimer = QElapsedTimer()

etimer.start()
print('abc')
print(etimer.nsecsElapsed())


etimer.start()
a = 100 + 234
print(etimer.nsecsElapsed())

etimer.start()
a = 123123123 * 1000000000
print(etimer.nsecsElapsed())

etimer.start()
a = 123123123 / 10002323000000
print(etimer.nsecsElapsed())