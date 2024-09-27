from toolbox.level import Level
from toolbox.sprites.gameplayer import GamePlayer
from toolbox.sprites.npc import NPC


class SplashScreen(Level):
    def __init__(self):
        super().__init__()

    def load_sprites(self):
        # Todo add sprites
        GamePlayer((2.5, 2.5))
        NPC((3.5, 3.5))
