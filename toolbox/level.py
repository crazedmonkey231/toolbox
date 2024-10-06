import shared
from pygame.sprite import AbstractGroup
from toolbox.level_cell import LevelCell
from toolbox.pathfinding import Pathfinding


# Todo Level
class Level(object):
    def __init__(self):
        self.level_grid: Pathfinding = None
        self.level_cells: list[list[LevelCell]] = None

    def load_sprites(self):
        pass


# Change level
def change_level(new_level: type[Level]):
    import shared
    for name, value in vars(shared).items():
        if value and isinstance(value, AbstractGroup):
            value.empty()
    shared.overlay.fill((0, 0, 0, 0))
    shared.current_level = new_level()
    shared.current_level.load_sprites()
