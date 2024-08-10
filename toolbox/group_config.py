from pygame.sprite import LayeredUpdates, Group, GroupSingle

# Main renderer
render_sprites: LayeredUpdates = LayeredUpdates()

# Organizational Groups
player_group: GroupSingle = GroupSingle()
enemy_group: Group = Group()
pickup_group: Group = Group()
effect_group: Group = Group()
projectile_group: Group = Group()
widget_group: Group = Group()
