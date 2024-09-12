import pygame
from pygame import Surface, Mask, Vector2
from pygame.sprite import Sprite
from shared import *


# Todo GameObject
class GameObject(Sprite):
    def __init__(self, layer=0, groups=None, *args, **kwargs):
        self._layer = layer
        self.a_props: list = list(*args)
        self.k_props: dict = dict(**kwargs)
        self.mask: Mask = None
        self.rotation = 0
        self.components: list[GameObjectComponent] = list()
        super().__init__(groups)
        self.image = Surface((48, 48)).convert()
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = kwargs["center"] if "center" in kwargs else Vector2(0, 0)

    def update(self, *args, **kwargs):
        if self.components:
            for comp in [c for c in self.components if c.needs_update]:
                comp.comp_update(*args, **kwargs)

    def on_damage(self, *args, **kwargs) -> float:
        pass

    def kill(self):
        self.on_end_play()
        super().kill()

    def on_end_play(self):
        pass

    def on_hover_start(self):
        pass

    def on_hovered_end(self):
        pass

    def on_click_start(self):
        pass

    def on_click_end(self):
        pass

    def cutscene_start(self):
        pass

    def cutscene_skip(self):
        pass


# Todo GameObjectComponent
class GameObjectComponent(object):
    def __init__(self, parent: GameObject):
        self.parent: GameObject = parent
        self.needs_update = True

    def comp_update(self, *args, **kwargs):
        pass


def get_component_by_type(game_object: GameObject, comp_type: type[GameObjectComponent]):
    return [comp for comp in game_object.components if isinstance(comp, comp_type)]


# Todo Thing
class Thing(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(0, [renderer_group], args, **kwargs)
        # self.mask: Mask = pygame.mask.from_surface(self.image)


# Todo Pickup
class Pickup(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(0, [renderer_group, pickup_group], *args, **kwargs)
        # self.mask: Mask = pygame.mask.from_surface(self.image)


# Todo Player
class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(1, [renderer_group, player_ref_group], *args, **kwargs)
        # self.mask: Mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)


# Todo Enemy
class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(1, [renderer_group, enemy_group], *args, **kwargs)
        # self.mask: Mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)


# Todo Projectile
class Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(2, [renderer_group, projectile_group], *args, **kwargs)
        # self.mask: Mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)


# Todo Effect
class Effect(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(3, [renderer_group, effect_group], *args, **kwargs)
        # self.mask: Mask = pygame.mask.from_surface(self.image)
        
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)


# Todo Widget
class Widget(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(4, [renderer_group, widget_group], *args, **kwargs)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)