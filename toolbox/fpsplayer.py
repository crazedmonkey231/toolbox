import pygame
from pygame import Vector2, Mask

from toolbox.components.comp_grow import CompGrow
from toolbox.components.comp_input import CompInput
from toolbox.components.comp_launcher import CompTimedLauncher
from toolbox.components.comp_mouse_follower import CompMouseFollowerDirection
from toolbox.game_objects import Player, Projectile
from toolbox.resistry import asset_registry


class FpsPlayer(Player):
    def __init__(self, pos):
        super().__init__(pos)
        self.player_pos = pygame.Vector2(pos)
        self.move_vector = Vector2(200, 200)
        self.image, self.rect = asset_registry.get_image('fsh')
        self.hello_sound = asset_registry.get_sound('hello')
        self.mask: Mask = pygame.mask.from_surface(self.image)
        self.original_image = self.image
        self.image_x_flipped = pygame.transform.flip(self.original_image, True, False)
        self.current_angle = 0
        self.rotation_speed = 3
        self.image_rot_offset = 180
        self.trails = []
        self.rect.center = self.player_pos
        self.mode = 1
        self.grow = 0
        self.hovered = False
        self.collision_rect = self.rect
        self.move_speed = 100
        self.components.append(CompInput(self))
        self.comp_launcher = CompTimedLauncher(self, Projectile)
        self.components.append(self.comp_launcher)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        pygame.draw.rect(args[0], (255, 0, 0), self.rect, 3)
        self.comp_launcher.is_firing = pygame.mouse.get_pressed()[0]
