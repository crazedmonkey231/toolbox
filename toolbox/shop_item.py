class ShopItem(object):
    def __init__(self, name: str, description: str, icon: str, cost: float, callback, callback_params):
        self.name = name
        self.description = description
        self.icon = icon
        self.cost = cost
        self.callback = callback
        self.callback_params = callback_params
