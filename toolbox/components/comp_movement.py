import math

import pygame
from pygame import Vector2

from config import SCREEN_SIZE_V2
from toolbox.game_objects import GameObjectComponent, GameObject


class CompMovement(GameObjectComponent):
    def __init__(self, parent: GameObject, target: Vector2, move_speed: float = 0, destroy_on_dest: bool = True):
        super().__init__(parent)
        self.original_image = parent.image
        self.target: Vector2 = target
        self.move_speed = move_speed
        self.rotation_offset = 2 * math.pi
        self._is_targeting = True
        self.destroy_on_dest = destroy_on_dest
        self.distance_buffer = 5
        center = Vector2(parent.rect.center)
        delta_pos = self.target - center
        rot = math.atan2(delta_pos.y, delta_pos.x)
        self.img_rot = self.rotation_offset - rot
        self.dx = math.cos(rot) * self.move_speed
        self.dy = math.sin(rot) * self.move_speed

    def comp_update(self, *args, **kwargs):
        if self._is_targeting:
            parent = self.parent
            center = Vector2(parent.rect.center)
            if 0 <= center.x <= SCREEN_SIZE_V2.x and 0 <= center.y <= SCREEN_SIZE_V2.y:
                center = center + Vector2(self.dx * args[1], self.dy * args[1])
                image = pygame.transform.rotate(self.original_image, math.degrees(self.img_rot))
                rect = image.get_rect(center=center)
                parent.image = image
                parent.rect = rect
            else:
                self._is_targeting = False
        elif not self._is_targeting and self.destroy_on_dest:
            self.parent.kill()
