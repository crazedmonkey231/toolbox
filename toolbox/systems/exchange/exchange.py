from collections import defaultdict
from uuid import UUID
from toolbox.item import Item
from toolbox.systems.exchange.exchange_ticket import ExchangeTicket
from toolbox.wallet import Wallet


class Exchange(object):
    def __init__(self):
        self.offers: defaultdict[UUID, ExchangeTicket] = defaultdict()

    def create_offer(self, wallet: Wallet, items: list[Item]):
        ticket = None
        if items:
            ticket = ExchangeTicket(wallet, items)
            self.offers[ticket.ticket_id] = ticket
        return ticket

    def buy_ticket(self, wallet: Wallet, ticket_uuid: UUID):
        success = False
        ticket = self.offers.get(ticket_uuid)
        if ticket is not None and wallet.cash >= ticket.ticket_price:
            del self.offers[ticket_uuid]
            total_price = ticket.ticket_price
            wallet.cash -= total_price
            ticket.wallet.cash += total_price
            for item in ticket.items:
                wallet.owned_items.append(item)
            success = True
        return success
