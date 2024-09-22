from toolbox.shop_item import ShopItem


class Wallet(object):
    def __init__(self):
        self.cash = 0
        self.owned_items: list[ShopItem] = list()
        self.owned_stocks: dict[str, int] = dict()
