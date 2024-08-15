import pygame
from pygame import Surface, Mask
from pygame.sprite import Sprite
from config import RGBA_RED


class Thing(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((64, 64)).convert_alpha()
        self.image.fill(RGBA_RED)
        self.rect = self.image.get_rect()
        self.mask: Mask = pygame.mask.from_surface(self.image)
