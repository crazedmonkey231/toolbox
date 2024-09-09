import os
from collections import defaultdict
import pygame
from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from config import IMAGE_DIR, AUDIO_DIR, GIF_DIR
from pygame import Surface, Rect
from pygame.mixer import Sound


class AssetRegistry(object):
    def __init__(self):
        self.image_registry: defaultdict[str, tuple[Surface, Rect]] = defaultdict()
        self.sound_registry: defaultdict[str, Sound] = defaultdict()
        self.gif_registry: defaultdict[str, list[Surface]] = defaultdict()

    def load_registry(self, images: list[str], sounds: list[str], gifs: list[str]):
        for image in images:
            self.load_image(image)
        for sound in sounds:
            self.load_sound(sound)
        for gif in gifs:
            self.load_gif(gif)

    def load_image(self, name: str, color_key=None, scale=1):
        name_key = name.split('.')[0]
        image = pygame.image.load(os.path.join(IMAGE_DIR, name)).convert_alpha()
        size = image.get_size()
        image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        self.image_registry[name_key] = (image, image.get_rect())

    def get_image(self, name: str) -> tuple[Surface, Rect]:
        surface, rect = self.image_registry[name]
        return surface.copy(), rect.copy()

    def load_sound(self, name: str):
        name_key = name.split('.')[0]
        if not pygame.mixer:
            class NoneSound(object):
                def play(self):
                    pass
            sound = NoneSound()
        else:
            sound = pygame.mixer.Sound(os.path.join(AUDIO_DIR, name))
        self.sound_registry[name_key] = sound

    def get_sound(self, name: str) -> Sound:
        sound = self.sound_registry[name]
        return sound

    def load_gif(self, name: str):
        name_key = name.split('.')[0]
        surfaces = []
        gif: GifImageFile = Image.open(os.path.join(GIF_DIR, name))
        for frame_index in range(gif.n_frames):
            gif.seek(frame_index)
            frame_rgba = gif.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
            )
            pygame_image.set_colorkey((255, 255, 255, 255))
            surfaces.append(pygame_image)
        self.gif_registry[name_key] = surfaces

    def get_gif(self, name: str) -> list[Surface]:
        gif = [surface.copy() for surface in self.gif_registry[name]]
        return gif


asset_registry = AssetRegistry()
