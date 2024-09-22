
achievement_list = [
    ("name", "desc", "icon", False)
]


class Achievements(object):
    def __init__(self):
        self.achievements: dict[str, Achievement] = {a[0]: Achievement(*a) for a in achievement_list}

    def complete_achievement(self, achievement_id):
        self.achievements[achievement_id].completed = True


class Achievement(object):
    def __init__(self, name: str, description: str, icon: str, completed: bool):
        self.name = name
        self.description = description
        self.icon = icon
        self.completed = completed
