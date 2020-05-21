import mido
msg = mido.Message('note_on', note=60)
print(msg.type)

mido.get_output_names()

mid = mido.MidiFile('./pyprone/resources/midifiles/a-whole-new-world.mid')
port = mido.open_output('Microsoft GS Wavetable Synth 0')

for msg in mid.play():
    port.send(msg)