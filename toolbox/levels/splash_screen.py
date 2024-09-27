from toolbox.level import Level
from toolbox.pathfinding import create_bounds
from toolbox.sprites.gameplayer import GamePlayer
from toolbox.sprites.npc import NPC


class SplashScreen(Level):
    def __init__(self):
        super().__init__()
        self.level_grid = create_bounds()
        # self.level_grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        #                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
        #                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
        #                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
        #                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
        #                    [1, 1, 1, 1, 1, 1, 1, 1, 1],]

    def load_sprites(self):
        # Todo add sprites
        GamePlayer((2.5, 2.5))
        NPC((3.5, 3.5))
