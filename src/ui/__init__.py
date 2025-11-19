import pygame


class GameWindow:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Trekking AI")

    def update(self):
        self.screen.fill((20, 20, 20))
        pygame.display.flip()
