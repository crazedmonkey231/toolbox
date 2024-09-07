import pygame
from pygame import Surface
from toolbox.game_objects import GameObject, GameObjectComponent


class CompDraw(GameObjectComponent):
    def __init__(self, parent: GameObject):
        super().__init__(parent)
        self.brush = Surface((48, 48)).convert_alpha()
        self.brush.fill((0, 0, 255, 255))

    def comp_update(self, *args, **kwargs):
        if pygame.mouse.get_pressed()[0]:
            args[0].blit(self.brush, self.parent.rect.topleft)
