import random
from toolbox.shop_item import ShopItem
from toolbox.wallet import Wallet


def default(t: int):
    print(t)


shop_items = [
    ("name", "desc", "icon", 5, default, [1]),
    ("name2", "desc", "icon", 5, default, [1]),
]


class Shop(object):
    def __init__(self):
        self.available_shop_items: list[ShopItem] = []

    def refresh(self, sample_size=3):
        self.available_shop_items.clear()
        sample = min(len(shop_items), sample_size)
        for item in random.sample(shop_items, k=sample):
            self.available_shop_items.append(ShopItem(*item))

    def purchase_item(self, idx: int, wallet: Wallet):
        success = False
        if 0 <= idx < len(self.available_shop_items):
            shop_item: ShopItem = self.available_shop_items[idx]
            if wallet.cash >= shop_item.cost:
                del self.available_shop_items[idx]
                wallet.cash -= shop_item.cost
                wallet.owned_items.append(shop_item)
                success = True
        return success
