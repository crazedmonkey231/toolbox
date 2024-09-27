from typing import Sequence
from pygame import Vector2
import shared
import toolbox.pathfinding
from toolbox.game_objects import GameObject, GameObjectComponent


class CompRaycasterAiMovement(GameObjectComponent):
    def __init__(self, parent: GameObject, position: Sequence[float]):
        super().__init__(parent)
        self.position: Vector2 = Vector2(position)
        self.move_direction: Vector2 = Vector2(0, 0)
        self.move_speed = .25
        self.is_moving = True
        self.move_to_camera = False
        self.path = []

    def comp_update(self, *args, **kwargs):
        if self.is_moving:
            target_location = Vector2(shared.renderer_group.position_x, shared.renderer_group.position_y)
            if self.move_to_camera:
                self.move_direction = (target_location - self.position).normalize()
                delta_move = self.move_direction * self.move_speed * shared.delta_time
                self.position += delta_move
                self.parent.center_position = self.position
            else:
                self.path = toolbox.pathfinding.a_star((int(self.position.x), int(self.position.x)),
                                                       (int(target_location.x), int(target_location.y)))
                if self.path:
                    self.move_direction = (self.path[-1] - self.position).normalize()
                    delta_move = self.move_direction * self.move_speed * shared.delta_time
                    self.position += delta_move
                    self.parent.center_position = self.position
