import random
from mingus.core import progressions
from mingus.containers import NoteContainer, Note, Track
from mingus.extra import lilypond

I   = "I"
II  = "II"
III = "III"
IV  = "IV"
V   = "V"
VI  = "VI"
VIIdim7 = "VIIdim7"


progression_map = {
    I:   [I, II, III, IV, V, VI, VIIdim7],
    II:  [V, VIIdim7],
    III: [IV, VI],
    IV:  [I, II, V, VIIdim7],
    V:   [I, VI],
    VI:  [II, IV, V],
    VIIdim7: [I],
}


def random_progression():
    prev = I
    while True:
        next_val = random.choice(progression_map[prev])
        yield next_val
        prev = next_val


progression = [n for n, _ in zip(random_progression(), range(32 + 1))]
chords = progressions.to_chords(progression, "C")
ncs = [NoteContainer([Note(note) for note in chord]) for chord in chords]

track = Track()
for nc in ncs:
    track.add_notes(nc, duration=4)

#print(track)

lily = lilypond.from_Track(track)
print(lily)
