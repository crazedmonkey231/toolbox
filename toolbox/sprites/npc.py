import shared
from pygame import Vector2
from toolbox.game_objects import Thing
from toolbox.sprites.components.comp_movement import CompMovementAstar


class NPC(Thing):
    def __init__(self, pos):
        super().__init__(image="npc", center=pos)
        self.components.append(CompMovementAstar(self, Vector2(50, 200), 100, destroy_on_dest=False))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
