from pygame.sprite import LayeredUpdates, Group, GroupSingle
from toolbox.camera import CameraRenderer

#
# Main renderer
#

# No camera renderer, uses _layer attribute to draw sprites in a given order.
# render_sprites: LayeredUpdates = LayeredUpdates()

# Use camera renderer, auto sorts sprites for simulated world depth.
render_sprites: CameraRenderer = CameraRenderer()

#
# Organizational Groups
#
player_group: GroupSingle = GroupSingle()
enemy_group: Group = Group()
pickup_group: Group = Group()
effect_group: Group = Group()
projectile_group: Group = Group()
widget_group: Group = Group()
button_group: Group = Group()
