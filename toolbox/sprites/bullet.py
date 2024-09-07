import pygame
from pygame import Vector2, Mask
from toolbox.components.comp_targeter import CompTargeter
from toolbox.game_objects import Projectile
from toolbox.group_config import *


class Bullet(Projectile):
    def __init__(self, pos):
        super().__init__(pos)
        self.rect.center = pos
        self.comp_targeter = CompTargeter(self, Vector2(pygame.mouse.get_pos()), 500)
        self.components.append(self.comp_targeter)
        self.mask: Mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)