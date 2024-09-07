from pygame import Vector2
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
    def __init__(self, parent: GameObject, projectile: type[Projectile], cooldown: float = 1):
        super().__init__(parent)
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.original_image = parent.image
        self.projectile: type[Projectile] = projectile
        self.is_firing = False

    def launch_projectile(self):
        if self.projectile:
            parent = self.parent
            center = Vector2(parent.rect.center)
            self.projectile(center)

    def comp_update(self, *args, **kwargs):
        if self.current_cooldown > 0:
            self.current_cooldown = toolbox.util.clamp_value(self.current_cooldown - args[1], 0, self.cooldown)
        if self.is_firing and self.current_cooldown == 0:
            self.launch_projectile()
            self.current_cooldown = self.cooldown
