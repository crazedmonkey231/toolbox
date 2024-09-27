import shared
from toolbox.game_objects import Thing
from toolbox.sprites.components.comp_raycaster_ai_movement import CompRaycasterAiMovement


class NPC(Thing):
    def __init__(self, pos):
        super().__init__()
        self.image, self.rect = shared.asset_registry.get_image("npc")
        self.rect.center = pos
        self.components.append(CompRaycasterAiMovement(self, pos))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)