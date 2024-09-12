from pygame import Vector2
import shared
import toolbox.util
from toolbox.game_objects import GameObject, GameObjectComponent


class CompTrailRect(GameObjectComponent):
    def __init__(self, parent: GameObject, trail_color=(255, 255, 255, 255), size=(36, 36), width=12, decay_factor=3):
        super().__init__(parent)
        self.trails = []
        self.color = trail_color
        self.size = size
        self.width = width
        self.decay_factor = decay_factor
        self.update_counter = 0
        self.active = True

    def comp_kill(self):
        toolbox.util.clear_rect_particles(shared.underlay, self.trails)

    def comp_update(self, *args, **kwargs):
        if self.parent.alive() and self.active:
            self.update_counter += 1
            self.update_counter %= self.decay_factor
            center = Vector2(self.parent.rect.center)

            particle_params = (shared.underlay, self.trails, self.update_counter, self.decay_factor, self.color)
            toolbox.util.update_rect_particles(*particle_params)

            particle_update_params = (shared.underlay, self.trails, self.color, center, self.size, self.width)
            toolbox.util.create_rect_particle(*particle_update_params)
