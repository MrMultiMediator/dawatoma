from dawatoma import FPSequence
from dawatoma import seq_constructor_args_from_file
fps_args = seq_constructor_args_from_file("99.dawa")
seq1 = FPSequence(fps_args[0], fps_args[1])

# Generate and write .midi file of the melody
seq1.gen_midi()
seq1.write_midi()

# Derive two different melodies from the fingerprint using the alt2_s and
# rsamp_s algorithms, respectively.
seq1.alt2_s()
seq1.rsamp_s(length=12)

# Generate .midi for all derived melodies and write them to file
seq1.gen_all_midi()
seq1.write_all_midi()
seq1.write_all_dawa()

