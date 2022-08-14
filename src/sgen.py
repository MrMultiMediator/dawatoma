"""
Sequence generation routines. Fingerprint sequences use these to generate other
derived sequences. This can be used by artists with writer's block to get ideas
for agreeable melodies to include in their track to make it more complex and
layered.
"""
from sequence import Sequence
import random

def two_unique_notes(notes):
    "See if a list of notes in .dawa format contains at least 2 unique notes. If yes, return True. If no, return False."
    n1 = notes[0].split()[0][:-1]

    for note in notes[1:]:
        if note.split()[0][:-1] != n1:
            return True

    return False

def get_unique_notes(notes, show=False):
    "Get all unique notes in the .dawa sequence. Ignore the octave."
    un = []

    for note in notes:
        if note.split()[0][:-1] not in un:
            un.append(note.split()[0][:-1])

    if show:
        print(f"{len(un)} unique notes : {un}")

    return un

def alt2(name, tempo, notes, freq: "beats", oc1, oc2, duration: "beats") -> Sequence:
    """
    Return a sequence of two notes alternating at the specified frequency in beats.
    Sample from the notes passed in to the function, and use the octaves specified.
    ---------------------------------------------------------------------------------------------------------
    name : The corresponding name for a .midi or .dawa file that could be written from the generated sequence
    tempo : Tempo in beats/minute
    notes : Notes in .dawa format split by line excluding the header line
    freq : Period between notes in beats
    oc1 : Octave 1
    oc2 : Octave 2
    duration : Length of the desired sequence in beats
    """
    try:
        test = notes[1]
    except:
        raise ValueError("ERROR! There must be more than 1 note in a sequence to use alt2")
        return

    if not two_unique_notes(notes):
        raise ValueError("ERROR! There must be at least two unique notes to use alt2")
        return

    un = get_unique_notes(notes, True)

    d_string = str(tempo)
    note1 = un.pop(un.index(random.choice(un)))+str(oc1)
    note2 = un.pop(un.index(random.choice(un)))+str(oc2)
    time = 0.
    counter = 0

    # alt2 main algorithm
    while time+freq <= duration:
        if counter % 2 == 0:
            d_string += '\n'+note1+' '+str(time)+' '+str(freq)
        else:
            d_string += '\n'+note2+' '+str(time)+' '+str(freq)
        counter += 1
        time += freq

    return Sequence(d_string, name)

def get_ad_note_order(note1, direction = 'asc'):
    "Return an ascending or descending order of notes that starts with note1, rather than 'C'"
    if direction == 'asc':
        octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    else:
        octave = ['B', 'A#', 'A', 'G#', 'G', 'F#', 'F', 'E', 'D#', 'D', 'C#', 'C']

    index = octave.index(note1)
    note_order = []
    for note in octave[octave.index(note1):]:
        note_order.append(note)
    for note in octave[:octave.index(note1)]:
        note_order.append(note)

    return note_order

def get_ad_notes(note, un_order, oc, direction = 'asc'):
    """Generate a list of ascending or descending (a/d) notes (i.e. A#4, B4, C5, ...) using only the unique
    notes in un_order, starting at note and going no further than B8 (for 'asc') and no further than
    C0 (for 'desc')"""
    if direction == 'asc':
        octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    elif direction == 'desc':
        octave = ['B', 'A#', 'A', 'G#', 'G', 'F#', 'F', 'E', 'D#', 'D', 'C#', 'C']
    else:
        raise ValueError("ERROR! direction MUST be 'desc' or 'asc'")

    ad_notes = []
    index = 0; prev = -1
    while True:
        ad_notes.append(un_order[index]+str(oc))

        # Manage the current index in the unique ordered note list
        index += 1
        if index >= len(un_order):
            index = 0

        # Mange the octave number. If we pass or land on C, increase it
        if octave.index(un_order[index]) < octave.index(un_order[prev]) and prev != -1:
            if direction == 'asc':
                oc += 1
            if direction == 'desc':
                oc -= 1

        prev = index

        if direction == 'asc' and oc >= 9:
            break
        if direction == 'desc' and oc < 0:
            break

    return ad_notes

def gen_ad_d_string(ad_notes, freq, duration, period, da_prob):
    """Generate a .dawa string (missing the header line) of ascending or descending (a/d=ad) notes given the
    parameters. Parameters are explained in the 'asc' and 'desc' function documentation."""
    time = 0.
    periods = 0.
    d_string = ''
    index = 0

    while (periods*period)+time+freq < duration:
        d_string += '\n'+ad_notes[index]+' '+str((periods*period)+time)+' '+str(freq)

        time += freq

        if time > period:
            index = 0
            periods += 1.
            time -= period
        else:
            if random.random() < da_prob and index > 0:
                index -= 1
            else:
                index += 1

    return d_string

def asc(name, tempo, notes, freq: "beats"=0.5, oc=4, duration: "beats"=16., period: "beats"=4., note1=None, dec_prob=0.) -> Sequence:
    """
    Return a series of ascending notes as a Sequence to the length of time specified (duration).
    ---------------------------------------------------------------------------------------------------------
    name : The corresponding name for a .midi or .dawa file that could be written from the generated sequence
    tempo : Tempo in beats/minute
    notes : Notes in .dawa format split by line excluding the header line
    freq : The length of each note in the Sequence.
    oc : Octave of the starting note
    duration : Length of the desired sequence in beats
    period : Number of beats per ascending subsequence. Once this is reached, start at the bottom again.
    note1 : First note to be used in the sequence. It will ascend from there
    dec_prob : Probability (0 to 1) that the sequence will descend rather than ascend from one note to the other
    LINEARITY : An idea for a parameter (or two) that determine(s) the odds that a note is skipped in a sequence
    """
    asc_notes = [] # All notes to be sampled
    un = get_unique_notes(notes)

    if note1 is None:
        note1 = random.choice(un)

    note_order = get_ad_note_order(note1, direction = 'asc')

    # Unique note order is a list of the unique notes in ascending order, starting with note1
    un_order = [n for n in note_order if n in un]

    # Arrange notes in ascending order starting with note1 at the selected octave
    note = note1
    asc_notes = get_ad_notes(note1, un_order, oc, direction = 'asc')
    d_string = str(tempo)+gen_ad_d_string(asc_notes, freq, duration, period, dec_prob)

    return Sequence(d_string, name)

def desc(name, tempo, notes, freq: "beats"=0.5, oc=4, duration: "beats"=16., period: "beats"=4., note1=None, asc_prob=0.) -> Sequence:
    """
    Return a series of descending notes as a Sequence to the length of time specified (duration).
    ---------------------------------------------------------------------------------------------------------
    name : The corresponding name for a .midi or .dawa file that could be written from the generated sequence
    tempo : Tempo in beats/minute
    notes : Notes in .dawa format split by line excluding the header line
    freq : The length of each note in the Sequence.
    oc : Octave of the starting note
    duration : Length of the desired sequence in beats
    period : Number of beats per descending subsequence. Once this is reached, start at the bottom again.
    note1 : First note to be used in the sequence. It will descend from there
    dec_prob : Probability (0 to 1) that the sequence will ascend rather than descend from one note to the other
    LINEARITY : An idea for a parameter (or two) that determine(s) the odds that a note is skipped in a sequence
    """
    desc_notes = [] # All notes to be sampled
    un = get_unique_notes(notes)

    if note1 is None:
        note1 = random.choice(un)

    note_order = get_ad_note_order(note1, direction = 'desc')

    # Unique note order is a list of the unique notes in descending order, starting with note1
    un_order = [n for n in note_order if n in un]

    # Arrange notes in ascending order starting with note1 at the selected octave
    note = note1
    desc_notes = get_ad_notes(note1, un_order, oc, direction = 'desc')
    d_string = str(tempo)+gen_ad_d_string(desc_notes, freq, duration, period, asc_prob)

    return Sequence(d_string, name)