from engine.core import GameState


OCTAVES = 5  # number of octaves to show

font = pygame.font.SysFont('monospace', 12)
key_graphic, kgrect = load_img('keys.png')
width, height = kgrect.width, kgrect.height
white_key_width = width / 7

# text is the surface displaying the determined chord
text = pygame.Surface((width * OCTAVES, 20))
text.fill((255, 255, 255))


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



class Game(GameState):

    def enter(self):
        self.screen = pygame.display.set_mode((OCTAVES * width, height + 20))
        pygame.display.set_caption('Mingus piano')

    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                quit = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit = True

    def render(self):
        for x in range(OCTAVES):
            screen.blit(key_graphic, (x * width, 0))

            # Blit the text surface
            screen.blit(text, (0, height))

            t = font.render("Hello", 2, (0, 0, 0))
            text.fill((255, 255, 255))
            text.blit(t, (0, 0))
