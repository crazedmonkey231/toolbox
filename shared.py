from pygame import Surface, Clock
from pygame.sprite import Group, GroupSingle, LayeredUpdates

# Shared systems
asset_registry = None
achievement_system = None
loaded_experience = None

# Pygame stuff
screen: Surface = None
underlay: Surface = None
overlay: Surface = None
clock: Clock = None
running: bool = True
delta_time: float = 0
delta_slowdown: float = 1000

# Main renderer
renderer_group: LayeredUpdates = LayeredUpdates()

# Player ref group
player_ref_group: GroupSingle = GroupSingle()

# Organizational Groups
enemy_group: Group = Group()
pickup_group: Group = Group()
effect_group: Group = Group()
projectile_group: Group = Group()
widget_group: Group = Group()
