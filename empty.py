import pygame
from pygame.locals import *


pygame.init()
pygame.font.init()


quit = False


from game.core import Game

game = Game(pygame)


while not quit:

    game.handle_events(pygame.event.get())
    for event in pygame.event.get():

    # Blit the picture of one octave OCTAVES times.

    for x in range(OCTAVES):
        screen.blit(key_graphic, (x * width, 0))

    # Blit the text surface
    screen.blit(text, (0, height))

    t = font.render("Hello", 2, (0, 0, 0))
    text.fill((255, 255, 255))
    text.blit(t, (0, 0))

    # Check for keypresses

    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit = True

    pygame.display.update()

pygame.quit()
