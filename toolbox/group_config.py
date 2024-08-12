from pygame.sprite import LayeredUpdates, Group, GroupSingle
from toolbox.camera import CameraRenderer

#
# Main renderer
#

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
