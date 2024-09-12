from pygame.sprite import Group, GroupSingle, LayeredUpdates

# Shared systems
asset_registry = None
achievement_system = None
loaded_experience = None

# Pygame stuff
screen = None
overlay = None
clock = None
running = True
delta_time = 0
delta_slowdown = 1000

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
