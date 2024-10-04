import shared
from toolbox.game_objects import Thing
from toolbox.sprites.components.comp_raycaster_ai_movement import CompRaycasterAiMovement


class NPC(Thing):
    def __init__(self, pos):
        super().__init__(image="npc", center=pos)
        self.components.append(CompRaycasterAiMovement(self))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)