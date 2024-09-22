from toolbox.level import Level
from toolbox.sprites.gameplayer import GamePlayer


class SplashScreen(Level):
    def __init__(self):
        super().__init__()

    def load_sprites(self):
        # Todo add sprites
        GamePlayer((200, 200))
