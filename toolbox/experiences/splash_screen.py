from toolbox.game_objects import Experience
from toolbox.sprites.gameplayer import GamePlayer


class SplashScreen(Experience):
    def __init__(self):
        super().__init__()

    def load_sprites(self):
        # Todo add sprites
        GamePlayer((200, 200))
