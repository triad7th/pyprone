from time import sleep
from PyQt5.QtCore import QTimer, QElapsedTimer
from PyQt5.QtWidgets import QApplication

from pyprone.entities.midifile import PrMidiFile
from pyprone.entities.midifile.track import PrMidiTrack
from pyprone.core.helpers.formats import tick2MBT, sec2HMSF
from mido import open_output

midifile = PrMidiFile('midifile')
midifile.load('./pyprone/resources/midifiles/a-whole-new-world.mid')
port = open_output('Microsoft GS Wavetable Synth 0')

# for track, csr, delta in midifile.run():
#     print(''.join([
#         f'{track.msg} | trk#: {track.no:<13} | dlta: {delta:<12.7}',
#         f' |  MBT: {tick2MBT(track.tick, midifile.tpb):16} | HMSF : {sec2HMSF(track.time):<16}'
#         f' | ABST: {track.time}']))

#     sleep(delta)
#     if not track.msg.is_meta:
#         port.send(track.msg.core)

# for msg in midifile.merge_run():
#     print(f'{msg} | tempo: {midifile.tempo}')
#     #sleep(msg.time)
#     if not msg.is_meta:
#         port.send(msg)


midi_iter = iter(midifile.run())
qtimer = QTimer()
etimer = QElapsedTimer()
app = QApplication([])

cur_iter = next(midi_iter)

def play():
    global midi_iter, cur_iter, qtimer, etimer    
    if cur_iter:
        track, csr, delta = cur_iter
        elapsed = etimer.nsecsElapsed() / 1000000000
        if elapsed >= track.secs:
            # print(''.join([
            #     f'{track.msg} | trk#: {track.no:<13} | dlta: {delta:<12.7}',
            #     f' |  MBT: {tick2MBT(track.tick, midifile.tpb):16} | HMSF : {sec2HMSF(track.time):<16}',
            #     f' | ABST: {track.time:16.8}',
            #     f' | ETIM: {elapsed:16.8}']))
            if not track.msg.is_meta:
                port.send(track.msg.core)
            cur_iter = next(midi_iter)
    else:
        qtimer.stop()
        exit()

qtimer.timeout.connect(play)
qtimer.start(1)
etimer.start()

app.exec_()