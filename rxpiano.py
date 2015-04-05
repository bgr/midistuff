#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from pygame import midi
import midis2events
from rx.concurrency import PyGameScheduler
from rx.subjects import Subject
from collections import namedtuple


midi.init()
midi_in = midi.Input(midi.get_default_input_id())


class MidiEvents(Subject):

    def __init__(self, pygame_midi_input, scheduler):
        super().__init__()

        def _check_for_events(scheduler, state):
            raw_events = pygame_midi_input.read(40)
            device_id = pygame_midi_input.device_id
            for e in midis2events.midis2events(raw_events, device_id):
                self.on_next(e)
            scheduler.schedule(_check_for_events)

        _check_for_events(scheduler, pygame_midi_input)


NoteOn = namedtuple("NoteOn", "number, velocity")
NoteOff = namedtuple("NoteOff", "number")


scheduler = PyGameScheduler()

#midi_events = Subject()
#midi_events.observe_on(scheduler).subscribe(on_next, on_error=on_error)

midi_events = MidiEvents(midi_in, scheduler)


raw_ons = midi_events.filter(lambda ev: ev.command == midis2events.NOTE_ON)
raw_offs = midi_events.filter(lambda ev: ev.command == midis2events.NOTE_OFF)

note_ons = raw_ons.map(lambda ev: NoteOn(ev.data1, ev.data2))
note_offs = raw_offs.map(lambda ev: NoteOff(ev.data1))

#note_ons.subscribe(lambda n: print("ON: {}".format(n)))
#note_offs.subscribe(lambda n: print("OFF: {}".format(n)))


def acc_press_or_release(acc, cur):
    note = cur.data1
    if cur.command == midis2events.NOTE_ON:
        acc.add(note)
    elif cur.command == midis2events.NOTE_OFF:
        acc.discard(note)
    return acc

currently_pressed = midi_events.scan(acc_press_or_release, set())
currently_pressed.subscribe(print)

print("Running, press Ctrl-C to quit")


while True:
    scheduler.run()

#pygame.quit()
