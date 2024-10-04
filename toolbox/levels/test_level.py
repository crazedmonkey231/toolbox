import os
import pygame
from config import IMAGE_DIR
from toolbox.level import Level
from toolbox.level_cell import LevelCell
from toolbox.sprites.gameplayer import GamePlayer
from toolbox.sprites.npc import NPC


class TestLevel(Level):
    def __init__(self):
        super().__init__()
        self.level_grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 0, 0, 0, 0, 0, 0, 0, 1],
                           [1, 0, 0, 0, 0, 0, 0, 0, 1],
                           [1, 0, 0, 0, 0, 0, 0, 0, 1],
                           [1, 0, 0, 0, 0, 0, 0, 0, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1],]

        wall_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_wall.png"))
        floor_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_floor.png"))
        ceiling_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_ceiling.png"))

        self.level_cells = [[None] * len(self.level_grid[0]) for _ in range(len(self.level_grid))]

        for x in range(len(self.level_grid)):
            for y in range(len(self.level_grid[0])):
                wall = None
                ceiling = ceiling_texture
                floor = floor_texture
                grid_spot = self.level_grid[x][y]
                if grid_spot == 1:
                    wall = wall_texture
                self.level_cells[x][y] = LevelCell(wall, ceiling, floor)

    def load_sprites(self):
        GamePlayer((2.5, 2.5))
        NPC((3.5, 3.5))
