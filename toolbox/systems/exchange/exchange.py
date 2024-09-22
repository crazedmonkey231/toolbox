from collections import defaultdict
from uuid import UUID
from toolbox.item import Item
from toolbox.systems.exchange.exchange_ticket import ExchangeTicket
from toolbox.wallet import Wallet


class Exchange(object):
    def __init__(self, exchange_fee: float = 0.0):
        self.offers: defaultdict[UUID, ExchangeTicket] = defaultdict()
        self.exchange_fee = round(exchange_fee, 2)

    def create_offer(self, wallet: Wallet, items: list[Item]):
        ticket = None
        if items:
            ticket = ExchangeTicket(wallet, items)
            self.offers[ticket.ticket_id] = ticket
        return ticket

    def get_ticket_price_info(self, ticket_uuid: UUID):
        ticket = self.offers.get(ticket_uuid)
        fee = round(ticket.ticket_price * self.exchange_fee, 2)
        total_price = ticket.ticket_price + fee
        return ticket, fee, total_price

    def buy_ticket(self, wallet: Wallet, ticket_uuid: UUID):
        ticket, fee, total_price = self.get_ticket_price_info(ticket_uuid)
        if wallet.cash >= total_price:
            del self.offers[ticket_uuid]
            wallet.cash -= total_price
            ticket.wallet.cash += total_price
            for item in ticket.items:
                wallet.owned_items.append(item)
