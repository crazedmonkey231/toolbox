import shared
import toolbox.util
from toolbox.game_objects import GameObject, GameObjectComponent


class CompCharger(GameObjectComponent):
    def __init__(self, parent: GameObject, start_charge: float = 0, charge_amount: float = 1, charge_speed: float = 1,
                 charge_max: float = 100, call_back=None):
        super().__init__(parent)
        self.charge = start_charge
        self.charge_max = charge_max
        self.charge_amount = charge_amount
        self.charge_speed = charge_speed
        self.charge_timer = 0
        self.call_back = call_back

    def comp_update(self, *args, **kwargs):
        if self.charge < self.charge_max:
            self.charge_timer += shared.delta_time
            if self.charge_timer >= self.charge_speed:
                self.charge_timer = 0
                self.charge = toolbox.util.clamp_value(self.charge + self.charge_amount, 0, self.charge_max)
        elif self.charge > self.charge_max:
            self.charge_amount = self.charge_max
        elif self.charge == self.charge_max:
            if self.charge_timer > 0:
                self.charge_timer = 0
            if self.call_back:
                self.call_back()
                self.charge = 0
