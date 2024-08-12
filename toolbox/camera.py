import pygame
from pygame import Surface, Rect
from pygame.sprite import RenderUpdates
import toolbox.util
from config import RGB_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, RGB_WHITE, SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF


# Camera Renderer, auto sorts based on rect.bottom for sprites and draws to screen.
class CameraRenderer(RenderUpdates):
    def __init__(self):
        super().__init__()
        self.screen: Surface = None
        self.screen_rect: Rect = None
        self.camera_lookat_pos = (SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF)

    def draw(self, surface):
        if not self.screen:
            self.screen = pygame.display.get_surface()
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.bottom):
            old_rect = self.spritedict[sprite]
            new_rect = surface_blit(sprite.image, sprite.rect)
            if old_rect:
                if new_rect.colliderect(old_rect):
                    dirty_append(new_rect.union(old_rect))
                else:
                    dirty_append(new_rect)
                    dirty_append(old_rect)
            else:
                dirty_append(new_rect)
            self.spritedict[sprite] = new_rect
        self.screen.fill(RGB_BLACK)
        self.screen_rect = Rect(self.camera_lookat_pos[0] - SCREEN_WIDTH_HALF,
                                self.camera_lookat_pos[1] - SCREEN_HEIGHT_HALF,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.blit(surface, (0, 0), self.screen_rect)
        return dirty
