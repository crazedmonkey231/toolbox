import math
import pygame
from pygame import Vector2
import shared
from config import SCREEN_SIZE_V2
from toolbox.game_objects import GameObjectComponent, GameObject


class CompMovement(GameObjectComponent):
    def __init__(self, parent: GameObject, target_pos: Vector2, move_speed: float = 0, needs_img_rotation: bool = True,
                 destroy_on_dest: bool = True):
        super().__init__(parent)
        self.original_image = parent.image
        self.target_pos: Vector2 = target_pos
        self.move_speed = move_speed
        self.is_targeting = True
        self.needs_img_rotation = needs_img_rotation
        self.destroy_on_dest = destroy_on_dest
        self.distance_buffer = 5
        delta_pos = self.target_pos - Vector2(parent.rect.center)
        rot = math.atan2(delta_pos.y, delta_pos.x)
        self.img_rot = 2 * math.pi - rot
        self.parent.rotation = math.degrees(self.img_rot)
        self.dx = math.cos(rot) * self.move_speed
        self.dy = math.sin(rot) * self.move_speed

    def comp_update(self, *args, **kwargs):
        if self.is_targeting:
            parent = self.parent
            center = Vector2(parent.rect.center)
            if 0 <= center.x <= SCREEN_SIZE_V2.x and 0 <= center.y <= SCREEN_SIZE_V2.y:
                delta_time = shared.delta_time
                new_center = center + Vector2(self.dx * delta_time, self.dy * delta_time)
                if self.needs_img_rotation:
                    parent.image = pygame.transform.rotate(self.original_image, parent.rotation)
                    parent.rect = parent.image.get_rect(center=new_center)
                    parent.mask = pygame.mask.from_surface(parent.image)
                else:
                    parent.rect.center = new_center
            else:
                self.is_targeting = False
        elif not self.is_targeting and self.destroy_on_dest:
            self.parent.kill()
