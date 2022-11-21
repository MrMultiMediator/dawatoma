from note_dict import NoteDict
from midiutil import MIDIFile

class Melody:
    """
    MIDIFile objects created from a string that encodes all melody information in the following format:
    tempo_in_BPM # Commment
    note1 time duration
    note2 time duration
    ...
    noteN time duration
    Time and duration are in beats. The note is a string like C5 which will be interpreted with the NoteDict"""
    def gen_midi(self) -> 'MIDIFile':
        "Generate the midiutil object that stores everything needed to write a midi file with the melody."
        notes = self.dstring[1:]
        self.midi = MIDIFile(1)
        self.midi.addTempo(self.track, 0, self.tempo)

        for i, note in enumerate(notes):
            # print(note)
            pitch = NoteDict[note.split()[0]]
            time = float(note.split()[1])
            duration = float(note.split()[2])
            self.midi.addNote(self.track, self.channel, pitch, time, duration, self.volume)

    def __init__(self, dstring):
        "Setup the melody parameters"
        self.dstring = dstring.split('\n')
        self.track    = 0
        self.channel  = 0
        self.volume   = 100  # 0-127, as per the MIDI standard
        self.tempo = int(self.dstring[0].split()[0])   # In BPM