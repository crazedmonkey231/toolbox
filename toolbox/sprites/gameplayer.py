from toolbox.game_objects import Player
from toolbox.sprites.components.comp_raycaster_camera import CompRaycasterCamera


class GamePlayer(Player):
    def __init__(self, pos):
        super().__init__(center=pos)
        self.components.append(CompRaycasterCamera(self, pos))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)