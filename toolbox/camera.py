import pygame
from pygame import Surface, Rect
from pygame.sprite import RenderUpdates
import toolbox.util
from config import (RGB_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, RGB_WHITE, SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF, MIN_ZOOM,
                    MAX_ZOOM, ZOOM_STEP)


# Todo
# Camera Renderer, auto sorts based on rect.bottom for sprites and draws to screen.
class CameraRenderer(RenderUpdates):
    def __init__(self):
        super().__init__()
        self.zoom_scale = 1
        self.screen: Surface = None
        self.screen_rect: Rect = None
        self.camera_lookat_pos = (SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF)
        self.top_left = (self.camera_lookat_pos[0] - SCREEN_WIDTH_HALF * self.zoom_scale,
                         self.camera_lookat_pos[1] - SCREEN_HEIGHT_HALF * self.zoom_scale)
        self.screen_overlay: Surface = None
        self._snapshot_rect: Rect = None
        self._snapshot_surface: Surface = None

    def pos_to_global_pos(self, pos):
        new_x = pos[0] + self.top_left[0]
        new_y = pos[1] + self.top_left[1]
        return new_x, new_y

    def update_zoom_scale(self, zoom_direction):
        if zoom_direction == 1 or zoom_direction == -1:
            new_zoom_scale = self.zoom_scale + (ZOOM_STEP * zoom_direction)
            self.zoom_scale = toolbox.util.clamp_value(new_zoom_scale, MIN_ZOOM, MAX_ZOOM)

    def draw(self, canvas):
        if not self.screen:
            self.screen = pygame.display.get_surface()
            self.screen_overlay = Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
            self.screen_overlay.fill((0, 0, 0, 0))
        surface_blit = canvas.blit
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
        # Clear screen and cache top left
        self.screen.fill(RGB_BLACK)
        self.top_left = (self.camera_lookat_pos[0] - SCREEN_WIDTH_HALF * self.zoom_scale,
                         self.camera_lookat_pos[1] - SCREEN_HEIGHT_HALF * self.zoom_scale)
        # Calculate deltas
        dx = self.top_left[0] + SCREEN_WIDTH
        dy = self.top_left[1] + SCREEN_HEIGHT

        dx_corner_top = self.top_left[0] + SCREEN_WIDTH_HALF
        dy_corner_left = self.top_left[1] + SCREEN_HEIGHT_HALF

        # Snapshot the canvas onto a scaled surface
        self._snapshot_rect = Rect(dx_corner_top, dy_corner_left, dx, dy)
        self._snapshot_surface = Surface((dx, dy)).convert_alpha()
        self._snapshot_surface.fill((0, 0, 0, 255))
        self._snapshot_surface.blit(canvas, (0, 0), self._snapshot_rect)

        # Scale snapshot to screen size and center then blit on to screen
        scaled_surface, scaled_rect = toolbox.util.scale_image_smooth(self._snapshot_surface,
                                                                      (SCREEN_WIDTH, SCREEN_HEIGHT),
                                                                      (SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF))
        self.screen.blit(scaled_surface, (0, 0), scaled_rect)
        self.screen.blit(self.screen_overlay, (0, 0))
        return dirty
