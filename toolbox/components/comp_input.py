import pygame
from toolbox.game_objects import GameObject, GameObjectComponent


class CompInput(GameObjectComponent):
    def __init__(self, parent: GameObject, move_speed: float = 100):
        super().__init__(parent)
        self.move_speed = move_speed
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def comp_update(self, *args, **kwargs):
        delta_time = args[1]
        canvas_size = args[0].get_size()
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT] or self.left:
            dx = -self.move_speed * delta_time
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] or self.right:
            dx = self.move_speed * delta_time
        if keys[pygame.K_w] or keys[pygame.K_UP] or self.up:
            dy = -self.move_speed * delta_time
        if keys[pygame.K_s] or keys[pygame.K_DOWN] or self.down:
            dy = self.move_speed * delta_time
        if self.parent.rect.left < 0:
            dx = self.move_speed * delta_time
        if self.parent.rect.right > canvas_size[0]:
            dx = -self.move_speed * delta_time
        if self.parent.rect.top < 0:
            dy = self.move_speed * delta_time
        if self.parent.rect.bottom > canvas_size[1]:
            dy = -self.move_speed * delta_time
        self.parent.rect.center = round(self.parent.rect.center[0] + dx), round(self.parent.rect.center[1] + dy)
