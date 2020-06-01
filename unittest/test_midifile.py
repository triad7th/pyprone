from pyprone.entities.midifile import PrMidifile
from mido import open_output
from time import sleep

midifile = PrMidifile('midifile')
midifile.load('./pyprone/resources/midifiles/ahnw.mid')
port = open_output('Microsoft GS Wavetable Synth 0')

for track_no, msg, dtime, ttime, ctime in midifile.run():
    if ctime == 14.2:
        debug = True
    if msg.tick == 1480:
        debug = True
    print(f'{msg} | trk#: {track_no:<13} | dtime: {dtime:<12.7} | ttime: {ttime:<12.7} | ctime: {ctime:<12.7}')
    sleep(dtime)
    if not msg.is_meta:
        port.send(msg.core)

# for msg in midifile.merge_run():
#     print(f'{msg} | tempo: {midifile.tempo}')
#     #sleep(msg.time)
#     if not msg.is_meta:
#         port.send(msg)
