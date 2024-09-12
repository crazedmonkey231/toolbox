
class Achievement(object):
    def __init__(self, name: str, description: str, completed: bool = False):
        self.name = name
        self.description = description
        self.completed = completed


class Achievements(object):
    def __init__(self):
        self.achievements: dict[str, Achievement] = dict()

    def complete_achievement(self, achievement_id):
        self.achievements[achievement_id].completed = True
