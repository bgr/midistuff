#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

*** Description ***

    A pygame MIDI piano.


    This piano is completely controlled by the keyboard, no MIDI hardware is
    required. You only have to set the SF2 variable to a valid soundfont file.


*** Keys ****


    Base octave:

        z,x,c,v,b,n,m    C,D,E,F,G,A,B
        s,d,g,h,j    C#,D#,F#,G#,A#

    Octave higher:

        w,e,r,t,y,u,i   C,D,E,F,G,A,B
        3,4,6,7,8    C#,D#,F#,G#,A#

    Control octaves (default = 4):

        -        octave down
        =        octave up


    Control channels (default = 8):

        backspace    channel down
        \        channel up


"""

import pygame
from pygame import midi

from pygame.locals import *
from mingus.core import chords
from mingus.containers import *

import midis2events


OCTAVES = 5  # number of octaves to show
LOWEST = 2  # lowest octave to show
FADEOUT = 0.25  # coloration fadeout time (1 tick = 0.001)
WHITE_KEY = 0
BLACK_KEY = 1
WHITE_KEYS = [
    'C',
    'D',
    'E',
    'F',
    'G',
    'A',
    'B',
    ]
BLACK_KEYS = ['C#', 'D#', 'F#', 'G#', 'A#']


def load_img(name):
    """Load image and return an image object"""

    fullname = name
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print("Error: couldn't load image: ", fullname)
        raise SystemExit(message)
    return (image, image.get_rect())

pygame.init()
pygame.font.init()
midi.init()
midi_out_id = 3  # Sound Blaster Synth on my machine, lower latency
midi_out = midi.Output(midi_out_id)
midi_in_id = midi.get_default_input_id()
midi_in = midi.Input(midi_in_id)

font = pygame.font.SysFont('monospace', 12)
screen = pygame.display.set_mode((640, 480))

(key_graphic, kgrect) = load_img('keys.png')
(width, height) = (kgrect.width, kgrect.height)
white_key_width = width / 7

# Reset display to wrap around the keyboard image

pygame.display.set_mode((OCTAVES * width, height + 20))
pygame.display.set_caption('mingus piano')
octave = 4
channel = 8

# pressed is a surface that is used to show where a key has been pressed

pressed = pygame.Surface((white_key_width, height))
pressed.fill((0, 230, 0))

# text is the surface displaying the determined chord

text = pygame.Surface((width * OCTAVES, 20))
text.fill((255, 255, 255))
playing_w = []  # white keys being played right now
playing_b = []  # black keys being played right now
quit = False
tick = 0.0


def play_note(note):
    """play_note determines the coordinates of a note on the keyboard image
    and sends a request to play the note """

    global text
    octave_offset = (note.octave - LOWEST) * width
    if note.name in WHITE_KEYS:

        # Getting the x coordinate of a white key can be done automatically

        w = WHITE_KEYS.index(note.name) * white_key_width
        w = w + octave_offset

        # Add a list containing the x coordinate, the tick at the current time
        # and of course the note itself to playing_w

        playing_w.append([w, tick, note])
    else:

        # For black keys I hard coded the x coordinates. It's ugly.

        i = BLACK_KEYS.index(note.name)
        if i == 0:
            w = 18
        elif i == 1:
            w = 58
        elif i == 2:
            w = 115
        elif i == 3:
            w = 151
        else:
            w = 187
        w = w + octave_offset
        playing_b.append([w, tick, note])

    # To find out what sort of chord is being played we have to look at both the
    # white and black keys, obviously:

    notes = playing_w + playing_b
    notes.sort()
    notenames = []
    for n in notes:
        notenames.append(n[2].name)

    # Determine the chord

    det = chords.determine(notenames)
    if det != []:
        det = det[0]
    else:
        det = ''

    # And render it onto the text surface

    t = font.render(det, 2, (0, 0, 0))
    text.fill((255, 255, 255))
    text.blit(t, (0, 0))

    # Play the note

    midi_out.note_on(int(note) + 12, 100, channel)


KEY_MAP = {
    K_z: Note('C', octave),
    K_s: Note('C#', octave),
    K_x: Note('D', octave),
    K_d: Note('D#', octave),
    K_c: Note('E', octave),
    K_v: Note('F', octave),
    K_g: Note('F#', octave),
    K_b: Note('G', octave),
    K_h: Note('G#', octave),
    K_n: Note('A', octave),
    K_j: Note('A#', octave),
    K_m: Note('B', octave),
    K_COMMA: Note('C', octave + 1),
    K_l: Note('C#', octave + 1),
    K_PERIOD: Note('D', octave + 1),
    K_SEMICOLON: Note('D#', octave + 1),
    K_SLASH: Note('E', octave + 1),
    K_q: Note('B', octave),
    K_w: Note('C', octave + 1),
    K_3: Note('C#', octave + 1),
    K_e: Note('D', octave + 1),
    K_4: Note('D#', octave + 1),
    K_r: Note('E', octave + 1),
    K_t: Note('F', octave + 1),
    K_6: Note('F#', octave + 1),
    K_y: Note('G', octave + 1),
    K_7: Note('G#', octave + 1),
    K_u: Note('A', octave + 1),
    K_8: Note('A#', octave + 1),
    K_i: Note('B', octave + 1),
    K_o: Note('C', octave + 2),
    K_0: Note('C#', octave + 2),
    K_p: Note('D', octave + 2),
}

while not quit:

    # Blit the picture of one octave OCTAVES times.

    for x in range(OCTAVES):
        screen.blit(key_graphic, (x * width, 0))

    # Blit the text surface

    screen.blit(text, (0, height))

    # Check all the white keys

    for note in playing_w:
        diff = tick - note[1]

        # If a is past its prime, remove it, otherwise blit the pressed surface
        # with a 'cool' fading effect.

        if diff > FADEOUT:
            midi_out.note_off(int(note[2]) + 12, channel)
            playing_w.remove(note)
        else:
            pressed.fill((0, ((FADEOUT - diff) / FADEOUT) * 255, 124))
            screen.blit(pressed, (note[0], 0), None, pygame.BLEND_SUB)

    # Now check all the black keys. This redundancy could have been prevented,
    # but it isn't any less clear like this

    for note in playing_b:
        diff = tick - note[1]

        # Instead of SUB we ADD this time, and change the coloration

        if diff > FADEOUT:
            midi_out.note_off(int(note[2]) + 12, channel)
            playing_b.remove(note)
        else:
            pressed.fill((((FADEOUT - diff) / FADEOUT) * 125, 0, 125))
            screen.blit(pressed, (note[0], 1), (0, 0, 19, 68), pygame.BLEND_ADD)

    # Check for keypresses

    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        if event.type == KEYDOWN:
            if event.key in KEY_MAP:
                play_note(KEY_MAP[event.key])
            elif event.key == K_MINUS:
                octave -= 1
            elif event.key == K_EQUALS:
                octave += 1
            elif event.key == K_BACKSPACE:
                channel -= 1
            elif event.key == K_BACKSLASH:
                channel += 1
            elif event.key == K_ESCAPE:
                quit = True

    for event in midis2events.midis2events(midi_in.read(40), midi_in_id):
        if event.command == midis2events.NOTE_ON:
            play_note(Note().from_int(event.data1))
        #elif event["command"] == midis2events.NOTE_OFF:
            #midi_out.note_off(event["data1"], event["data2"], channel)

    # Update the screen

    pygame.display.update()
    tick += 0.001

pygame.quit()
