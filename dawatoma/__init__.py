"""
DAWATOMA stands for Digital Audio Workstation AuTOMAtion.

dawatoma allows the acceleration of creative tasks that often take place in a
DAW. It allows the generation of derived melodies given a 'fingerprint' melody
upon which the derived ones are based. The way my creative process often works
when producing music is that I have one main melody, and I build the song
around that, and a lot of that involves composing additional melodies that go
well with the main one. A portion of this is algorithmic and can be outsourced
to computational algorithms. There is, of course, already similar software out
there like arpeggiators and such that can do such things, but I wanted to
build a package that is built entirely around the idea of deriving melodies
from base melodies, with an easily expandable list of derivation protocols
that other developers can contribute to. The derived note sequences, as well
as the original, can be written to MIDI (.mid) format.

This package utilizes the plain text ".dawa" format to represent note
sequences. .dawa format looks as follows:
.dawa strings have the following format containing all note sequence information:
tempo_in_BPM # Commment
note1 time duration
note2 time duration
...
noteN time duration

Where time and duration are in beats, and time is the point in time in the
sequence that a note begins, and duration is how long the note lives. The
initial strings "not1e1", "note2", etc are strings like "C5" which will be
interpreted with the NoteDict, also included in this package.

This package depends on MIDIUtil.

"""