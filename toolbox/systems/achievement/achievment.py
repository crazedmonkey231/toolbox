class Achievement(object):
    def __init__(self, name: str, description: str, icon: str, completed: bool):
        self.name = name
        self.description = description
        self.icon = icon
        self.completed = completed
