from toolbox.systems.achievement.achievment import Achievement


achievement_list = [
    ("name", "desc", "icon", False)
]


class Achievements(object):
    def __init__(self):
        self.accomplishments: dict[str, Achievement] = {a[0]: Achievement(*a) for a in achievement_list}

    def complete_achievement(self, achievement_id):
        self.accomplishments[achievement_id].completed = True
