import pygame.transform
import shared
from pygame import Surface
from toolbox.game_objects import GameObject, GameObjectComponent


class CompGifPlayer(GameObjectComponent):
    def __init__(self, parent: GameObject, gif: list[Surface], is_playing: bool = True, play_time: float = 3.0,
                 destroy_on_end: bool = True):
        super().__init__(parent)
        self.frame_idx = 0
        self.gif_timer = 0
        self.gif = gif
        self.gif_frames = len(self.gif)
        self.gif_delta_time = play_time / self.gif_frames
        self.destroy_on_end = destroy_on_end
        self.parent.image = gif[self.frame_idx]
        self.parent.rect = gif[self.frame_idx].get_rect(center=self.parent.rect.center)
        self.is_playing = is_playing
        self.is_x_flipped = False
        self.is_y_flipped = False

    def comp_update(self, *args, **kwargs):
        if self.is_playing:
            self.gif_timer += shared.delta_time
            if self.gif_timer >= self.gif_delta_time:
                self.gif_timer = 0
                self.frame_idx += 1
                self.frame_idx %= self.gif_frames
                if self.frame_idx == 0 and self.destroy_on_end:
                    self.parent.kill()
                else:
                    rect = self.parent.rect
                    frame = pygame.transform.rotate(self.gif[self.frame_idx], self.parent.rotation)
                    img = pygame.transform.flip(frame, self.is_x_flipped, self.is_y_flipped)
                    self.parent.image = img
                    self.parent.rect = img.get_rect(center=rect.center)
                    self.parent.mask = pygame.mask.from_surface(img)
        elif self.gif_timer > 0 and not self.is_playing:
            self.gif_timer = 0
