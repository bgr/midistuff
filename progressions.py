import random
from mingus.core import progressions
from mingus.containers import NoteContainer, Note, Track
from mingus.extra import lilypond


TITLE = "Randomations No. 16"
KEY = "A"
LENGTH = 64


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


def random_progression(next_val=III):
    rand = random.Random(TITLE)
    while True:
        yield next_val
        next_val = rand.choice(progression_map[next_val])


progression = [n for n, _ in zip(random_progression(), range(LENGTH + 1))]
chords = progressions.to_chords(progression, KEY)
ncs = [NoteContainer([Note(note) for note in chord]) for chord in chords]

track = Track()
for nc in ncs:
    track.add_notes(nc, duration=4)


lily_template = """
\\version "2.18.0"

\\header {{
    title = "{title}"
    composer = "bgr's Python script"
}}

prog = {notes}

\\score {{

  \\new Staff {{
    \\time 4/4

    \\prog
  }}

  \\layout {{}}
  \\midi {{}}
}}
""".strip()

print(lily_template.format(
    title=TITLE,
    notes=lilypond.from_Track(track)
))
