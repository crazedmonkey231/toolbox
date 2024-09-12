import pygame
from pygame import Vector2

import shared
from toolbox.components.comp_gif_player import CompGifPlayer
from toolbox.components.comp_movement import CompMovementCircle
from toolbox.game_objects import Projectile


class Bullet(Projectile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.image, self.rect = asset_registry.get_image("bullet")
        # self.mask: Mask = pygame.mask.from_surface(self.image)
        self.target = Vector2(pygame.mouse.get_pos())
        self.components.append(CompMovementCircle(self, None, 200, update_rotation=True, destroy_on_dest=True, is_cyclic=False))
        self.components.append(CompGifPlayer(self, shared.asset_registry.get_gif("fire"), True, 0.5, False))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
