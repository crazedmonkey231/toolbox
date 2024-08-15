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
        self.top_left = (self.camera_lookat_pos[0] - SCREEN_WIDTH_HALF, self.camera_lookat_pos[1] - SCREEN_HEIGHT_HALF)
        self.zoom_scale = .5

    def mouse_pos_to_global_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos[0] + self.top_left[0], mouse_pos[1] + self.top_left[1]

    def draw(self, canvas):
        if not self.screen:
            self.screen = pygame.display.get_surface()
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
        self.top_left = (self.camera_lookat_pos[0] - SCREEN_WIDTH * self.zoom_scale,
                         self.camera_lookat_pos[1] - SCREEN_HEIGHT * self.zoom_scale)
        # Calculate deltas
        dx = SCREEN_WIDTH * self.zoom_scale
        dy = SCREEN_HEIGHT * self.zoom_scale
        dx_corner_top = self.top_left[0] + SCREEN_WIDTH_HALF * self.zoom_scale
        dy_corner_left = self.top_left[1] + SCREEN_HEIGHT_HALF * self.zoom_scale

        # Snapshot the canvas onto a scaled surface
        snapshot_rect = Rect(dx_corner_top, dy_corner_left, dx, dy)
        snapshot = Surface((dx, dy)).convert_alpha()
        snapshot.fill((0, 0, 0, 255))
        snapshot.blit(canvas, (0, 0), snapshot_rect)

        # Scale snapshot to screen size and center then blit on to screen
        _s, _r = toolbox.util.scale_image_smooth(snapshot, (SCREEN_WIDTH, SCREEN_HEIGHT),
                                                 (SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF))
        self.screen.blit(_s, (0, 0), _r)
        return dirty
