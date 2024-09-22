from toolbox.item import Item


class Wallet(object):
    def __init__(self):
        self.cash = 0
        self.owned_items: list[Item] = list()
