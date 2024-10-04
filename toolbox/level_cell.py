from pygame import Surface


class LevelCell(object):
    def __init__(self, wall: Surface, ceiling: Surface, floor: Surface):
        self.wall = wall
        self.ceiling = ceiling
        self.floor = floor
