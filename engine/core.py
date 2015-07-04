from pygame.locals import QUIT


class GameLoop:
    def __init__(self, pygame, root_state):
        quit = False
        clock = pygame.time.Clock()
        dt = 0

        root_state.enter()

        while not quit:
            quit = len(pygame.event.get(QUIT)) > 0
            events = pygame.event.get()
            root_state.handle_events(events)
            root_state.update(dt)
            root_state.render(pygame.display.get_surface())

            pygame.display.flip()
            dt = clock.tick(60)

        root_state.exit()
        pygame.quit()


class GameState:

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass
