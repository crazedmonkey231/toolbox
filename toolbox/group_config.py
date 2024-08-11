from pygame.sprite import LayeredUpdates, Group, GroupSingle
from toolbox.camera import CameraGroup

#
# Main renderer
#

# No camera renderer
# render_sprites: LayeredUpdates = LayeredUpdates()

# Use camera renderer
render_sprites: CameraGroup = CameraGroup()

#
# Organizational Groups
#
player_group: GroupSingle = GroupSingle()
enemy_group: Group = Group()
pickup_group: Group = Group()
effect_group: Group = Group()
projectile_group: Group = Group()
widget_group: Group = Group()
