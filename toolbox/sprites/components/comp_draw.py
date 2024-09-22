import pygame
from pygame import Surface
import shared
from toolbox.game_objects import GameObject, GameObjectComponent


class CompDraw(GameObjectComponent):
    def __init__(self, parent: GameObject, size: int = 12, color="black", brush_outline_color="red"):
        super().__init__(parent)
        self.size = size
        self.color = color
        self.brush_outline_color = brush_outline_color
        self.brush = Surface((self.size, self.size)).convert()
        self.brush.fill(self.color)

    def update_brush(self, size, color="black", brush_outline_color="red"):
        self.size = size
        self.color = color
        self.brush_outline_color = brush_outline_color
        self.brush = Surface((self.size, self.size)).convert()
        self.brush.fill(self.color)

    def comp_update(self, *args, **kwargs):
        mouse = pygame.mouse
        x, y = mouse.get_pos()
        rect = self.parent.rect
        if rect.collidepoint((x, y)):
            dx = x - self.size / 2
            dy = y - self.size / 2
            pygame.draw.rect(shared.screen, self.brush_outline_color, (dx, dy, self.size, self.size), 2)
            if mouse.get_pressed()[0]:
                dw = dx - rect.topleft[0]
                dh = dy - rect.topleft[1]
                self.parent.image.blit(self.brush, (dw, dh))
