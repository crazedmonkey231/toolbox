from pygame import Vector2
import toolbox.util
from toolbox.game_objects import GameObject, GameObjectComponent


class CompGrow(GameObjectComponent):
    def __init__(self, parent: GameObject, grow_speed: float = 100, growth_size: int = 50, is_cyclic: bool = False):
        super().__init__(parent)
        self.grow = True
        self.growth = 0
        self.growth_max = 100
        self.current_growth = 0
        self.original_image = self.parent.image
        self.original_size = Vector2(self.original_image.get_size())
        self.grow_speed = grow_speed
        self.growth_size = growth_size
        self.is_cyclic = is_cyclic

    def comp_update(self, *args, **kwargs):
        if self.is_cyclic:
            if self.growth == self.growth_max:
                self.grow = False
            if self.growth == 0:
                self.grow = True
        cached_growth = self.growth
        if self.growth < self.growth_max and self.grow:
            self.growth = toolbox.util.clamp_value(self.growth + self.grow_speed * args[1], 0, self.growth_max)
            self.current_growth = toolbox.util.map_range_clamped(self.growth, 0, self.growth_max, 1, self.growth_size)
        elif self.growth > 0 and not self.grow:
            self.growth = toolbox.util.clamp_value(self.growth - self.grow_speed * args[1], 0, self.growth_max)
            self.current_growth = toolbox.util.map_range_clamped(self.growth, 0, self.growth_max, 1, self.growth_size)
        if cached_growth != self.growth and 0 < self.growth < self.growth_max:
            parent = self.parent
            new_growth = round(self.current_growth)
            new_size = self.original_size + Vector2(new_growth, new_growth)
            _s, _r = toolbox.util.scale_image_smooth(self.original_image, new_size, parent.rect.center)
            parent.image = _s
            parent.rect = _r
