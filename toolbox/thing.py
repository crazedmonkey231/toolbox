import pygame
from pygame import Surface, Mask
from pygame.sprite import Sprite


class Thing(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((64, 64)).convert_alpha()
        self.image.fill((255, 255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask: Mask = pygame.mask.from_surface(self.image)
