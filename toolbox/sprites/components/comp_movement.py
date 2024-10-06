import math
from pygame import Vector2
import shared
import toolbox.util
import toolbox.pathfinding
from toolbox.game_objects import GameObjectComponent, GameObject


# CompMovementBase
class CompMovementBase(GameObjectComponent):
    def __init__(self, parent: GameObject, target_pos: Vector2, move_speed: float = 0, update_rotation: bool = True,
                 destroy_on_dest: bool = True, is_cyclic: bool = False):
        super().__init__(parent)
        self.start_pos = Vector2(self.parent.rect.center)
        self.target_pos = target_pos
        self.destroy_on_dest = destroy_on_dest
        self.move_speed = move_speed
        self.update_rotation = update_rotation
        self.is_cyclic = is_cyclic
        self.travel_delta = 1 / move_speed
        self.travel_path: list[Vector2] = None
        self.travel_path_len: int = -1
        self.travel_idx = 0
        self.travel_timer = 0

    def comp_update(self, *args, **kwargs):
        if self.travel_path:
            self.travel_timer += shared.delta_time
            if self.travel_timer >= self.travel_delta:
                self.travel_timer = 0
                self.travel_idx += int(self.move_speed * shared.delta_time)
                if self.is_cyclic:
                    self.travel_idx %= self.travel_path_len
                elif self.travel_idx >= self.travel_path_len:
                    self.travel_idx = self.travel_path_len - 1
                    self.needs_update = False
                    if self.destroy_on_dest:
                        self.parent.kill()
                rect = self.parent.rect
                new_center = self.travel_path[self.travel_idx]
                if self.update_rotation:
                    delta_pos = new_center - Vector2(rect.center)
                    if delta_pos.length() > 0:
                        rot = math.atan2(delta_pos.y, delta_pos.x)
                        self.parent.rotation = math.degrees(2 * math.pi - rot)
                rect.center = new_center
                self.parent.draw_position = new_center
        elif self.travel_timer > 0:
            self.travel_timer = 0


# CompMovementLine
class CompMovementLine(CompMovementBase):
    def __init__(self, parent: GameObject, target_pos: Vector2, move_speed: float = 0, update_rotation: bool = True,
                 destroy_on_dest: bool = True, is_cyclic: bool = False):
        super().__init__(parent, target_pos, move_speed, update_rotation, destroy_on_dest, is_cyclic)
        self.travel_path = toolbox.util.generate_line(self.start_pos, target_pos)
        self.travel_path_len = len(self.travel_path)
        self.parent.rect.center = self.travel_path[0]
        self.parent.draw_position = self.travel_path[0]


# CompMovementArch
class CompMovementArch(CompMovementBase):
    def __init__(self, parent: GameObject, target_pos: Vector2, move_speed: float = 0, update_rotation: bool = True,
                 destroy_on_dest: bool = True, max_arch_height: float = 100, max_arch_delta: float = 10,
                 inverse: bool = False, is_cyclic: bool = False):
        super().__init__(parent, target_pos, move_speed, update_rotation, destroy_on_dest, is_cyclic)
        self.travel_path = toolbox.util.generate_arch(self.start_pos, target_pos, max_arch_height, max_arch_delta,
                                                      inverse)
        self.travel_path_len = len(self.travel_path)
        self.parent.rect.center = self.travel_path[0]
        self.parent.draw_position = self.travel_path[0]


# CompMovementCircle
class CompMovementCircle(CompMovementBase):
    def __init__(self, parent: GameObject, target_pos: Vector2, move_speed: float = 0, update_rotation: bool = True,
                 destroy_on_dest: bool = False, radius: float = 200, start_x_offset: float = 0,
                 start_y_offset: float = 0, is_cyclic: bool = True):
        super().__init__(parent, target_pos, move_speed, update_rotation, destroy_on_dest, is_cyclic)
        self.travel_path = toolbox.util.generate_circle(self.start_pos, radius, start_x_offset, start_y_offset)
        self.travel_path_len = len(self.travel_path)
        self.parent.rect.center = self.travel_path[0]
        self.parent.draw_position = self.travel_path[0]


# CompMovementAstar
class CompMovementAstar(CompMovementBase):
    def __init__(self, parent: GameObject, target_pos: Vector2, move_speed: float = 0, update_rotation: bool = True,
                 destroy_on_dest: bool = True):
        super().__init__(parent, target_pos, move_speed, update_rotation, destroy_on_dest, False)
        l_grid = shared.current_level.level_grid
        self.travel_path = l_grid.a_star((int(self.start_pos.x), int(self.start_pos.y)),
                                         (int(target_pos.x), int(target_pos.y)))
        if self.travel_path:
            self.travel_path_len = len(self.travel_path)
            self.parent.rect.center = self.travel_path[0]
            self.parent.draw_position = Vector2(self.travel_path[0])

    def comp_update(self, *args, **kwargs):
        position = self.parent.draw_position
        l_grid = shared.current_level.level_grid
        self.travel_path = l_grid.a_star((int(position.x), int(position.y)),
                                         (int(self.target_pos.x), int(self.target_pos.y)))
        self.travel_path_len = len(self.travel_path)

        if self.travel_path:
            target = Vector2(self.travel_path[-1])
            delta_dist = target - position
            move_direction = delta_dist.normalize()
            delta_move = move_direction * self.move_speed * shared.delta_time
            self.parent.draw_position += delta_move
            self.parent.rect.center += delta_move

        # delta_dist = None
        # ip = Vector2((int(position.x), int(position.y)))
        # it = Vector2((int(self.target_pos.x), int(self.target_pos.y)))
        # if self.travel_path:
        #     delta_dist = self.travel_path[-1] - position
        # elif round((self.target_pos - position).length_squared(), 2):
        #     delta_dist = self.target_pos - position
        # elif self.destroy_on_dest:
        #     self.parent.kill()
        # if delta_dist is not None:
        #     move_direction = delta_dist.normalize()
        #     delta_move = move_direction * self.move_speed * shared.delta_time
        #     position += delta_move
        #     self.parent.draw_position = position
        #     self.parent.rect.center = position
