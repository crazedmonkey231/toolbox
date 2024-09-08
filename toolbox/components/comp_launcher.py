from pygame import Vector2
from pygame.mixer import Sound
import shared
import toolbox.util
from toolbox.game_objects import GameObject, GameObjectComponent, Projectile


class CompLauncher(GameObjectComponent):
    def __init__(self, parent: GameObject, projectile: type[Projectile]):
        super().__init__(parent)
        self.needs_update = False
        self.projectile: type[Projectile] = projectile

    def launch_projectile(self):
        if self.projectile:
            parent = self.parent
            center = Vector2(parent.rect.center)
            self.projectile(center)


class CompTimedLauncher(GameObjectComponent):
    def __init__(self, parent: GameObject, projectile: type[Projectile], cooldown: float = 1,
                 launch_sound: Sound = None):
        super().__init__(parent)
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.original_image = parent.image
        self.projectile: type[Projectile] = projectile
        self.is_firing = False
        self.launch_sound = launch_sound
        self.projectile_ref: Projectile = None

    def launch_projectile(self):
        if self.projectile:
            parent = self.parent
            center = Vector2(parent.rect.center)
            self.projectile_ref = self.projectile(center)
            if self.launch_sound:
                self.launch_sound.play()

    def comp_update(self, *args, **kwargs):
        if self.current_cooldown > 0:
            self.current_cooldown = toolbox.util.clamp_value(self.current_cooldown - shared.delta_time, 0, self.cooldown)
        if self.is_firing and self.current_cooldown == 0:
            self.launch_projectile()
            self.current_cooldown = self.cooldown
