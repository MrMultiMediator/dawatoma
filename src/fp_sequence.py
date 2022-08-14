import sys, os
from sgen import alt2, asc, desc
from sequence import Sequence

class FPSequence(Sequence):
    """Fingerprint sequence. d_dict : A dictionary with keys corresponding to the different types of derivations
    that are possible, and values corresponding the total number of derived sequences there are of that type.
    derseq = Dictionary of derived sequences. keys are names. Values are the Sequence objects.
    TO DO:
    1.) Make it so you can combine all (or 16 at a time) derived sequences into a single midi, with each derived
    sequence on its own channel.
    2.) Add functionality to convert a derived sequence into a fingerprint sequence. That is, write a function
    that makes a copy of a derived sequence, but returns that copy as a fingerprint sequence."""
    is_fprint = True
    d_dict = {'rsamp':0, 'alt2':0, 'asc':0, 'desc':0}
    derseq = {}

    def gen_all_midi(self):
        """Generate midiutil objects for all derived sequences that store everything needed to write a midi
        file with the melody."""
        for name in self.derseq.keys():
            self.derseq[name].gen_midi()

    def write_all_midi(self):
        """Write a .midi file for all derived sequences. They will all be called '<name>.mid'"""
        for name in self.derseq.keys():
            self.derseq[name].write_midi()

    def rsamp(self):
        """Create a sequence of notes randomly sampled from the notes in this fingerprint sequence
        in the octave range specified"""
        return

    def alt2_s(self, freq=1, oc1=5, oc2=5, duration=12):
        """Create a sequence of two notes alternating at the specified frequency in beats.
        Sample from the notes in this fingerprint sequence, and use the octaves specified."""
        name = 'alt2_'+str(self.d_dict['alt2'])
        notes = self.dstring.split('\n')[1:]
        self.derseq[name] = alt2(name, self.melody.tempo, notes, freq, oc1, oc2, duration)
        self.d_dict['alt2'] += 1

    def asc_s(self, freq=0.5, oc=4, duration=16., period=4., note1=None, dec_prob=0.):
        name = 'asc_'+str(self.d_dict['asc'])
        notes = self.dstring.split('\n')[1:]
        self.derseq[name] = asc(name, self.melody.tempo, notes, freq=freq, oc=oc, duration=duration, period=period, dec_prob=dec_prob)
        self.d_dict['asc'] += 1

    def desc_s(self, freq=0.5, oc=4, duration=16., period=4., note1=None, asc_prob=0.):
        name = 'desc_'+str(self.d_dict['desc'])
        notes = self.dstring.split('\n')[1:]
        self.derseq[name] = desc(name, self.melody.tempo, notes, freq=freq, oc=oc, duration=duration, period=period, asc_prob=asc_prob)
        self.d_dict['desc'] += 1

if __name__ == '__main__':
    "Make a fingerprint sequence/melody from a dawa file, write it to .midi, and derive additional melodies from it."
    seq1 = FPSequence(open(sys.argv[1],'r').read(), sys.argv[1].split('.')[0])
    seq1.gen_midi()
    seq1.write_midi()
    print(seq1.is_fprint)
    seq1.alt2_s()
    seq1.asc_s()
    seq1.desc_s()
    #os.system('fluidsynth -i -a alsa ~/code/python/music/soundfonts/Ultima*/000_Florestan_Piano.sf2 '+sys.argv[1].split('.')[0]+'.mid')