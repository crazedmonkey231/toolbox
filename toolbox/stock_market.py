from toolbox.stock import Stock
from toolbox.wallet import Wallet

STOCK_DEFAULTS = [
    ("BTC", "Bootcoin", "icon", 10.0, 1, 0)
]


class StockMarket(object):
    def __init__(self):
        self.stocks: dict[str, Stock] = {s[0]: Stock(*s) for s in STOCK_DEFAULTS}

    def reset(self):
        self.stocks: dict[str, Stock] = {s[0]: Stock(*s) for s in STOCK_DEFAULTS}

    def daily_stock_update(self):
        for stock in self.stocks.values():
            stock.daily_update()

    def buy(self, stock_id: str, amount: int, wallet: Wallet):
        stock: Stock = self.stocks[stock_id]
        price = stock.stock_price * amount
        if stock.available > 0 and 0 < amount <= stock.available and wallet.cash >= price:
            stock.available -= amount
            wallet.cash -= price
            if stock_id in wallet.owned_stocks:
                wallet.owned_stocks[stock_id] += amount
            else:
                wallet.owned_stocks[stock_id] = amount
            return True
        return False

    def sell(self, stock_id: str, amount: int, wallet: Wallet):
        if stock_id in self.stocks:
            stock: Stock = self.stocks[stock_id]
            if stock_id in wallet.owned_stocks and wallet.owned_stocks[stock_id] >= amount:
                stock.available += amount
                wallet.cash += stock.stock_price * amount
                wallet.owned_stocks[stock_id] -= amount
                return True
        return False

    def apply_dividends(self, wallet: Wallet):
        total_gained: float = 0
        for s_id in wallet.owned_stocks:
            stock: Stock = self.stocks[s_id]
            amount = stock.get_dividend_amount()
            wallet.cash += amount
            total_gained += amount
        return total_gained
