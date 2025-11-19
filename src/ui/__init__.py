import pygame


class GameWindow:
    def __init__(self, width=800, height=600):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Trekking AI")

    def update(self, cones=None):
        self.screen.fill((20, 20, 20))

        if cones:
            for x, y in cones:
                pygame.draw.circle(self.screen, (255, 150, 0), (x, y), 10)

        pygame.display.flip()
