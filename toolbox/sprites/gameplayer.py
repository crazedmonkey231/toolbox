import pygame
from pygame import Mask, Vector2, Surface
import shared
import toolbox.util
from toolbox.sprites.components.comp_input import CompInput
from toolbox.sprites.components.comp_launcher import CompTimedLauncher
from toolbox.game_objects import Player
from toolbox.sprites.bullet import Bullet


class GamePlayer(Player):
    def __init__(self, pos):
        super().__init__(pos)
        self.player_pos = Vector2(pos)
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

        buff = 25
        buff_half = buff / 2
        size = (self.rect.size[0] - buff, self.rect.size[1] - buff)
        self.draw_points = toolbox.util.get_graph_points(size, [5, 3, 5, 8, 5, 3])
        s = Surface(self.rect.size).convert_alpha()
        s.fill((0, 0, 0, 0))
        pygame.draw.lines(s, "cyan", False, self.draw_points, 3)
        self.image.blit(s, (buff_half, buff_half))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        pygame.draw.rect(shared.screen, (255, 0, 0), self.rect, 3)
        # self.comp_launcher.is_firing = pygame.mouse.get_pressed()[0]

