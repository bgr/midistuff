import pygame
from pygame import midi as pygame_midi
from midis2events import midis2events

pygame.init()
pygame.font.init()
pygame_midi.init()


print("Found {} midi devices".format(pygame_midi.get_count()))

for i in range(pygame_midi.get_count()):
    print("#{}: {}".format(i, pygame_midi.get_device_info(i)))


midi_input_id = pygame_midi.get_default_input_id()
midi_input = pygame_midi.Input(midi_input_id)

print("Using input #{}".format(midi_input_id))


while True:
    if not midi_input.poll():
        continue

    events = midis2events(midi_input.read(40), midi_input_id)
    for event in events:
        print(event)
