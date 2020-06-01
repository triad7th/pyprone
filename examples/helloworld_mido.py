from typing import List
import mido
mido_msg = mido.Message('note_on', note=60)
#print(mido_msg.type)

mido.get_output_names()

midifile = mido.MidiFile('./pyprone/resources/midifiles/a-whole-new-world.mid')
port = mido.open_output('Microsoft GS Wavetable Synth 0')

# midi play
for msg in midifile.play():
    print(msg)
    port.send(msg)
