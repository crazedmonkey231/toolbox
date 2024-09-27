import pygame
import shared
from shared import renderer_group
from toolbox.game_objects import GameObject, GameObjectComponent
from pygame.locals import *


class CompRaycasterCamera(GameObjectComponent):
    def __init__(self, parent: GameObject, pos):
        super().__init__(parent)
        renderer_group.owner = parent
        renderer_group.position_x = pos[0]
        renderer_group.position_y = pos[1]
        self.move_speed = 1.5
        self.rotation_speed = 1.5
        self.transform = []
        self.mouse_sensitivity = 0.2

    def comp_update(self, *args, **kwargs):
        self.transform = [renderer_group.position_x, renderer_group.direction_y,
                          renderer_group.direction_x, renderer_group.direction_y]

        delta_move = self.move_speed * shared.delta_time

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        delta_rotation = mouse_dx * self.mouse_sensitivity * shared.delta_time

        keys = pygame.key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            self.transform = renderer_group.move(delta_move, 0, forward=True)
        if keys[K_s] or keys[K_DOWN]:
            self.transform = renderer_group.move(delta_move, 0, backward=True)
        if keys[K_a] or keys[K_LEFT]:
            self.transform = renderer_group.move(delta_move, 0, strafe_left=True)
        if keys[K_d] or keys[K_RIGHT]:
            self.transform = renderer_group.move(delta_move, 0, strafe_right=True)
        if mouse_dx < 0:
            self.transform = renderer_group.move(0, delta_rotation, right=True)
        if mouse_dx > 0:
            self.transform = renderer_group.move(0, -delta_rotation, left=True)
        self.parent.rect.center = (self.transform[0], self.transform[1])
