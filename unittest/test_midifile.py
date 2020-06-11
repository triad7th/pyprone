from pyprone.entities.midifile import PrMidiFile
from pyprone.entities.midifile.track import PrMidiTrack
from pyprone.core.helpers.formats import tick2MBT, sec2HMSF
from mido import open_output
from time import sleep

midifile = PrMidiFile('midifile')
midifile.load('./pyprone/resources/midifiles/a-whole-new-world.mid')
port = open_output('Microsoft GS Wavetable Synth 0')

for track, csr, delta in midifile.run():
    print(''.join([
        f'{track.msg} | trk#: {track.no:<13} | dlta: {delta:<12.7}',
        f' |  MBT: {tick2MBT(track.tick, midifile.tpb):16} | HMSF : {sec2HMSF(track.time):<16}']))

    sleep(delta)
    if not track.msg.is_meta:
        port.send(track.msg.core)

# for msg in midifile.merge_run():
#     print(f'{msg} | tempo: {midifile.tempo}')
#     #sleep(msg.time)
#     if not msg.is_meta:
#         port.send(msg)
