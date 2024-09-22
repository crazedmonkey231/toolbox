import uuid
from toolbox.item import Item
from toolbox.wallet import Wallet


class ExchangeTicket(object):
    def __init__(self, wallet: Wallet, items: list[Item]):
        self.ticket_id = uuid.uuid4()
        self.wallet = wallet
        self.items = items
        self.ticket_price = 0
        for item in items:
            self.ticket_price += item.item_value
        self.ticket_price = round(self.ticket_price, 2)
