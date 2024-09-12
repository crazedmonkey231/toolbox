import pygame
from pygame import Mask
import shared
from toolbox.components.comp_gif_player import CompGifPlayer
from toolbox.components.comp_input import CompInput
from toolbox.components.comp_launcher import CompTimedLauncher
from toolbox.components.comp_mouse_follower import CompMouseFollowerPosition
from toolbox.components.comp_trail import CompTrailRect
from toolbox.game_objects import Player
from toolbox.sprites.bullet import Bullet


class GamePlayer(Player):
    def __init__(self, pos):
        super().__init__(pos)
        self.player_pos = pygame.Vector2(pos)
        self.image, self.rect = shared.asset_registry.get_image('fsh')
        # self.image = Surface((400, 400)).convert_alpha()
        # self.image.fill((0, 0, 0, 0))
        # self.rect = self.image.get_rect(center=self.player_pos)
        self.mask: Mask = pygame.mask.from_surface(self.image)
        self.components.append(CompInput(self))
        # self.components.append(CompMouseFollowerPosition(self))
        self.comp_launcher = CompTimedLauncher(self, Bullet, 0.3)
        self.components.append(self.comp_launcher)
        # self.components.append(CompGifPlayer(self, asset_registry.get_gif("fire"), True, 0.5, False))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        pygame.draw.rect(shared.screen, (255, 0, 0), self.rect, 3)
        self.comp_launcher.is_firing = pygame.mouse.get_pressed()[0]
