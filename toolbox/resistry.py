import os
from collections import defaultdict
from config import IMAGE_DIR, AUDIO_DIR, GIF_DIR
import toolbox
from pygame import Surface, Rect
from pygame.mixer import Sound


class AssetRegistry(object):
    def __init__(self):
        self.image_registry: defaultdict[str, tuple[Surface, Rect]] = defaultdict()
        self.sound_registry: defaultdict[str, Sound] = defaultdict()
        self.gif_registry: defaultdict[str, list[Surface]] = defaultdict()

    def load_image(self, name: str):
        self.image_registry[name.split('.')[0]] = toolbox.util.load_image(os.path.join(IMAGE_DIR, name))

    def get_image(self, name: str) -> tuple[Surface, Rect]:
        surface, rect = self.image_registry[name]
        return surface.copy(), rect.copy()

    def load_sound(self, name: str):
        self.sound_registry[name.split('.')[0]] = toolbox.util.load_sound(os.path.join(AUDIO_DIR, name))

    def get_sound(self, name: str) -> Sound:
        sound = self.sound_registry[name]
        return sound

    def load_gif(self, name: str):
        self.gif_registry[name.split('.')[0]] = toolbox.util.load_gif(os.path.join(GIF_DIR, name))

    def get_gif(self, name: str) -> list[Surface]:
        gif = [surface.copy() for surface in self.gif_registry[name]]
        return gif


asset_registry = AssetRegistry()
