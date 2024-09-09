import math
import pygame
from pygame import Vector2
import shared
import toolbox.util
from config import SCREEN_SIZE_V2
from toolbox.game_objects import GameObjectComponent, GameObject


class CompMovementArch(GameObjectComponent):
    def __init__(self, parent: GameObject, target_pos: Vector2, move_speed: float = 0, max_arch_height: float = 100,
                 max_arch_delta: float = 10, inverse: bool = False, destroy_on_dest: bool = True):
        super().__init__(parent)
        self.original_image = parent.image
        self.is_targeting = True
        self.destroy_on_dest = destroy_on_dest
        self.inverse = -1 if inverse else 1

        self.start_pos = Vector2(self.parent.rect.center)
        self.target_pos: Vector2 = target_pos

        self.move_speed = move_speed

        self.dist_target = self.target_pos - self.start_pos
        self.dist_target_norm = self.dist_target.normalize()
        self.dist_target_abs = Vector2(abs(self.dist_target.x), abs(self.dist_target.y))

        self.rect_x = self.start_pos.x
        self.rect_y = self.start_pos.y

        self.direction = 1 if target_pos.x > self.start_pos.x else -1

        self.arch_height_max = max_arch_height
        self.distance_buffer = 10

        self.arch_height = toolbox.util.clamp_value(self.dist_target_abs.x, 1, self.arch_height_max)
        self.delta_arch = toolbox.util.map_range_clamped(self.dist_target.length(), 0, 1000, 1, max_arch_delta)

    def comp_update(self, *args, **kwargs):
        if self.is_targeting:
            if (self.target_pos - Vector2(self.parent.rect.center)).length() > self.distance_buffer:
                self.rect_x += self.move_speed * self.dist_target_norm.x * shared.delta_time
                norm_position = abs((self.rect_x - self.start_pos.x) / (self.dist_target_abs.x + shared.epsilon))
                self.rect_y = ((1 - norm_position) * self.start_pos.y + norm_position * self.target_pos.y -
                               self.arch_height * self.inverse * self.delta_arch * norm_position * (1 - norm_position))
            else:
                self.rect_x = self.target_pos.x
                self.rect_y = self.target_pos.y
                self.is_targeting = False
            self.parent.rect.center = (self.rect_x, self.rect_y)
        else:
            center = Vector2(self.parent.rect.center)
            should_destroy = self.destroy_on_dest or (0 > center.x or center.x > SCREEN_SIZE_V2.x or
                                                      0 > center.y or center.y > SCREEN_SIZE_V2.y)
            if should_destroy:
                self.parent.kill()
