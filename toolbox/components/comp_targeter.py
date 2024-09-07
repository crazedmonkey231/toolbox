import math
import pygame
from pygame import Vector2
from toolbox.game_objects import GameObject, GameObjectComponent


class CompTargeter(GameObjectComponent):
    def __init__(self, parent: GameObject, target: Vector2):
        super().__init__(parent)
        self.original_image = parent.image
        self.target: Vector2 = target

    def comp_update(self, *args, **kwargs):
        if self.target:
            parent = self.parent
            center = Vector2(parent.rect.center)
            delta_pos = self.target - center
            rot = math.atan2(delta_pos.y, delta_pos.x)
            image = pygame.transform.rotate(self.original_image, math.degrees(2 * math.pi - rot))
            rect = image.get_rect(center=center)
            parent.image = image
            parent.rect = rect
