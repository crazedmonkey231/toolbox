from pygame.sprite import AbstractGroup
import shared
from toolbox.sprites.gameplayer import GamePlayer


class SplashScreen(object):
    def __init__(self):
        for name, value in vars(shared).items():
            if value and isinstance(value, AbstractGroup):
                value.empty()
        GamePlayer((200, 200))