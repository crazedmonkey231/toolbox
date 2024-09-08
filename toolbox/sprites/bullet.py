import pygame
from pygame import Vector2, Mask
from toolbox.components.comp_movement import CompMovement
from toolbox.game_objects import Projectile


class Bullet(Projectile):
    def __init__(self, pos):
        super().__init__(pos)
        self.rect.center = pos
        self.target = Vector2(pygame.mouse.get_pos())
        self.comp_targeter = CompMovement(self, self.target, 500)
        self.components.append(self.comp_targeter)
        self.mask: Mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)