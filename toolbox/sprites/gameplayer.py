import pygame
from pygame import Vector2, Mask

from toolbox.components.comp_grow import CompGrow
from toolbox.components.comp_input import CompInput
from toolbox.components.comp_launcher import CompTimedLauncher
from toolbox.components.comp_mouse_follower import CompMouseFollowerDirection
from toolbox.game_objects import Player, Projectile
from toolbox.resistry import asset_registry
from toolbox.sprites.bullet import Bullet


class GamePlayer(Player):
    def __init__(self, pos):
        super().__init__(pos)
        self.player_pos = pygame.Vector2(pos)
        self.move_vector = Vector2(200, 200)
        self.image, self.rect = asset_registry.get_image('fsh')
        self.mask: Mask = pygame.mask.from_surface(self.image)
        self.components.append(CompInput(self))
        self.comp_launcher = CompTimedLauncher(self, Bullet, 1, asset_registry.get_sound("hello"))
        self.components.append(self.comp_launcher)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        pygame.draw.rect(args[0], (255, 0, 0), self.rect, 3)
        self.comp_launcher.is_firing = pygame.mouse.get_pressed()[0]
