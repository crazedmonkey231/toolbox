import math
import pygame
from pygame import Vector2
from toolbox.game_objects import GameObject, GameObjectComponent


class CompMouseFollowerPosition(GameObjectComponent):
    def __init__(self, parent: GameObject):
        super().__init__(parent)

    def comp_update(self, *args, **kwargs):
        self.parent.rect.center = pygame.mouse.get_pos()


class CompMouseFollowerDirection(GameObjectComponent):
    def __init__(self, parent: GameObject, rotation_offset: float = 2 * math.pi):
        super().__init__(parent)
        self.original_image = parent.image
        self.rotation_offset = rotation_offset

    def comp_update(self, *args, **kwargs):
        parent = self.parent
        center = Vector2(parent.rect.center)
        mouse_pos = Vector2(pygame.mouse.get_pos())
        delta_pos = mouse_pos - center
        rotation = math.atan2(delta_pos.y, delta_pos.x)
        parent.rotation = math.degrees(self.rotation_offset - rotation)
