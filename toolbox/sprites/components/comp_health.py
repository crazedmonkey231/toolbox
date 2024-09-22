import toolbox.util
from toolbox.game_objects import GameObject, GameObjectComponent


class CompHealth(GameObjectComponent):
    def __init__(self, parent: GameObject, max_health: float = 100, health_regen: float = 0):
        super().__init__(parent)
        self.health = max_health
        self.max_health = max_health
        self.health_regen = health_regen

    def update_health(self, amount: float = 0):
        if amount != 0 or self.health_regen != 0:
            new_health = toolbox.util.clamp_value(self.health + self.health_regen + amount, 0, self.max_health)
            self.health = round(new_health, 2)
        if self.health == 0:
            self.parent.kill()

    def comp_update(self, *args, **kwargs):
        self.update_health()
