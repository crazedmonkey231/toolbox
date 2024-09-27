import shared
from toolbox.game_objects import Thing


class NPC(Thing):
    def __init__(self, pos):
        super().__init__(center=pos)
        self.image, self.rect = shared.asset_registry.get_image("npc")
        self.rect.center = pos

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)