from pygame import Surface, Clock
from pygame.sprite import Group, GroupSingle, LayeredUpdates

from toolbox.raycaster import Raycaster
from toolbox.systems.achievement.achievments import Achievements
from toolbox.level import Level
from toolbox.resistry import AssetRegistry

# Shared systems
asset_registry: AssetRegistry = None
achievement_system: Achievements = None
current_level: Level = None

# Pygame stuff
screen: Surface = None
underlay: Surface = None
overlay: Surface = None
clock: Clock = None
running: bool = True
mouse_grabbed = False
delta_time: float = 0
delta_slowdown: float = 1000
time_running_sec = 0
time_running_min = 0
time_running_hour = 0

# Main renderer
renderer_group: LayeredUpdates = LayeredUpdates()
# renderer_group: Raycaster = Raycaster()

# Player ref group
player_ref_group: GroupSingle = GroupSingle()

# Organizational Groups
enemy_group: Group = Group()
pickup_group: Group = Group()
effect_group: Group = Group()
projectile_group: Group = Group()
widget_group: Group = Group()
