import copy
import os
from collections import defaultdict
import dir_config
import toolbox
from pygame import Surface, Rect
from pygame.mixer import Sound


class AssetRegistry(object):
    def __init__(self):
        self.__image_dir = dir_config.image_dir
        self.image_registry: defaultdict[str, tuple[Surface, Rect]] = defaultdict()
        self.__sound_dir = dir_config.audio_dir
        self.sound_registry: defaultdict[str, Sound] = defaultdict()
        self.__gif_dir = dir_config.gif_dir
        self.gif_registry: defaultdict[str, list[Surface]] = defaultdict()

    def load_image(self, name: str):
        self.image_registry[name.split('.')[0]] = toolbox.util.load_image(os.path.join(self.__image_dir, name))

    def get_image(self, name: str) -> tuple[Surface, Rect]:
        surface, rect = self.image_registry[name]
        return surface.copy(), rect.copy()

    def load_sound(self, name: str):
        self.sound_registry[name.split('.')[0]] = toolbox.util.load_sound(os.path.join(self.__sound_dir, name))

    def get_sound(self, name: str) -> Sound:
        return copy.deepcopy(self.sound_registry[name])

    def load_gif(self, name: str):
        self.gif_registry[name.split('.')[0]] = toolbox.util.load_gif(os.path.join(self.__gif_dir, name))

    def get_gif(self, name: str) -> list[Surface]:
        gif = [surface.copy() for surface in self.gif_registry[name]]
        return gif


asset_registry = AssetRegistry()
