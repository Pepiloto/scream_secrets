import pygame
from random import randint


class Object:
    def __init__(self) -> None:
        self.pos = (randint(0, 600), randint(0, 200))

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.pos, 3)
