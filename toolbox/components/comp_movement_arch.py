import math
import pygame
from pygame import Vector2
import shared
import toolbox.util
from config import SCREEN_SIZE_V2
from toolbox.game_objects import GameObjectComponent, GameObject


class CompMovementArch(GameObjectComponent):
    def __init__(self, parent: GameObject, target_pos: Vector2, move_speed: float = 0, destroy_on_dest: bool = True,
                 max_arch_height: float = 100, max_arch_delta: float = 10, inverse: bool = False):
        super().__init__(parent)
        self.original_image = parent.image
        self.destroy_on_dest = destroy_on_dest
        self.move_speed = move_speed
        center = Vector2(self.parent.rect.center)
        self.arch_path = toolbox.util.gen_arch(center, target_pos, max_arch_height, max_arch_delta, inverse)
        self.arch_path_len = len(self.arch_path)
        self.travel_idx = 0
        self.travel_timer = 0
        self.travel_delta = 1 / move_speed

    def comp_update(self, *args, **kwargs):
        self.travel_timer += shared.delta_time
        if self.travel_timer >= self.travel_delta:
            self.travel_idx += int(self.move_speed * shared.delta_time)
            if self.travel_idx >= self.arch_path_len:
                self.travel_idx = self.arch_path_len - 1
                self.needs_update = False
                if self.destroy_on_dest:
                    self.parent.kill()
            else:
                self.parent.rect.center = self.arch_path[self.travel_idx]