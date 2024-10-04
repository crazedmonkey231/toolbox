from typing import Sequence
from pygame import Vector2
import shared
import toolbox.pathfinding
from toolbox.game_objects import GameObject, GameObjectComponent
from toolbox.raycaster import Raycaster


class CompRaycasterAiMovement(GameObjectComponent):
    def __init__(self, parent: GameObject):
        super().__init__(parent)
        self.move_direction: Vector2 = Vector2(0, 0)
        self.move_speed = .25
        self.is_moving = True
        self.move_to_camera = False
        self.path = []

    def comp_update(self, *args, **kwargs):
        if isinstance(shared.renderer_group, Raycaster):
            raycaster: Raycaster = shared.renderer_group
            if self.is_moving:
                position = self.parent.raycaster_draw_position
                target_location = Vector2(raycaster.position_x, raycaster.position_y)
                if self.move_to_camera:
                    self.move_direction = (target_location - position).normalize()
                    delta_move = self.move_direction * self.move_speed * shared.delta_time
                    position += delta_move
                else:
                    self.path = toolbox.pathfinding.a_star((int(position.x), int(position.x)),
                                                           (int(target_location.x), int(target_location.y)))
                    if self.path:
                        dest = self.path[-1]
                        delta_dist = dest - position
                        self.move_direction = delta_dist.normalize()
                        delta_move = self.move_direction * self.move_speed * shared.delta_time
                        position += delta_move
                self.parent.raycaster_draw_position = position
                self.parent.rect.center = position
