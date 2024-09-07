import math
import pygame
from pygame import Vector2
from toolbox.game_objects import GameObject, GameObjectComponent


class CompTargeter(GameObjectComponent):
    def __init__(self, parent: GameObject, target: Vector2, move_speed: float = 0, destroy_on_dest: bool = True):
        super().__init__(parent)
        self.original_image = parent.image
        self.target: Vector2 = target
        self.move_speed = move_speed
        self.rotation_offset = 2 * math.pi
        self._is_targeting = True
        self.destroy_on_dest = destroy_on_dest
        self.distance_buffer = 5

    def comp_update(self, *args, **kwargs):
        if self._is_targeting:
            parent = self.parent
            center = Vector2(parent.rect.center)
            delta_pos = self.target - center
            if delta_pos.length() > self.distance_buffer:
                delta_pos_n = delta_pos.normalize()
                center.angle_to(self.target)
                rot = math.atan2(delta_pos_n.y, delta_pos_n.x)
                image = pygame.transform.rotate(self.original_image, math.degrees(self.rotation_offset - rot))
                rect = image.get_rect(center=center)
                dx = (delta_pos_n.x * self.move_speed) * args[1]
                dy = (delta_pos_n.y * self.move_speed) * args[1]
                rect.center = center + Vector2(dx, dy)
                parent.image = image
                parent.rect = rect
            else:
                self._is_targeting = False
        elif not self._is_targeting and self.destroy_on_dest:
            self.parent.kill()


