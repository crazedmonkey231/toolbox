import math

import pygame
from pygame import Vector2, Mask

from toolbox.components.comp_gif_player import CompGifPlayer
from toolbox.components.comp_movement import CompMovement
from toolbox.game_objects import Projectile
from toolbox.resistry import asset_registry


class Bullet(Projectile):
    def __init__(self, pos):
        super().__init__(pos)
        self.image, self.rect = asset_registry.get_image("bullet")
        self.mask: Mask = pygame.mask.from_surface(self.image)
        self.rect.center = pos
        self.target = Vector2(pygame.mouse.get_pos())
        self.components.append(CompMovement(self, self.target, 500))
        # self.components.append(CompGifPlayer(self, asset_registry.get_gif("fire"), True, 0.5, False))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)