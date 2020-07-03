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

print('setup start..')
midi_iter = iter(midifile.run(MBT2tick(4, 1, 0, midifile.tpb)))
qtimer = QTimer()
etimer = QElapsedTimer()
app = QApplication([])
print('setup end..')

print('rewind start..')
etimer.start()
track = next(midi_iter)
if track:
    csr_secs = track.secs
    print(f'rewind end, elapsed: {etimer.elapsed() / 1000}, play starts from : {csr_secs}')

def play():
    global midi_iter, track, qtimer, etimer    
    if track:
        elapsed = etimer.nsecsElapsed() / 1000000000
        if elapsed + csr_secs >= track.secs:
            # print(''.join([
            #     f'{track.msg} | trk#: {track.no:<13} | dlta: {delta:<12.7}',
            #     f' |  MBT: {tick2MBT(track.tick, midifile.tpb):16} | HMSF : {sec2HMSF(track.time):<16}',
            #     f' | ABST: {track.time:16.8}',
            #     f' | ETIM: {elapsed:16.8}']))
            if not track.msg.is_meta:
                port.send(track.msg.core)
            track = next(midi_iter)
    else:
        qtimer.stop()
        exit()

if track:
    qtimer.timeout.connect(play)
    qtimer.start(1)
    etimer.start()
    app.exec_()