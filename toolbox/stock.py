import random
import toolbox


class Stock(object):
    def __init__(self, st_id: str, st_name: str, icon: str, available_amt: int, st_price: float, st_volatility: float,
                 st_dividend_percent: float):
        self.stock_id = st_id
        self.stock_name = st_name
        self.icon = icon
        self.available = available_amt
        self.available_max = available_amt
        self.stock_price = st_price
        self.volatility = st_volatility
        self.dividend_percent = st_dividend_percent
        self.previous_day_data: list[tuple[int, float, float]] = []

    def get_dividend_amount(self):
        return round(self.dividend_percent * self.stock_price, 2)

    def get_dividend_ratio(self):
        return round(self.dividend_percent * 100, 2)

    def get_stock_info(self):
        return (self.stock_id, self.stock_name, self.stock_price, self.get_previous_price(), self.volatility,
                self.get_dividend_ratio(), self.get_dividend_amount())

    def update_stock_price(self, change_amount: float):
        self.stock_price = round(toolbox.util.clamp_value(self.stock_price + change_amount, 0.01, 1000000), 2)

    def update_stock_volatility(self, change_amount: float):
        self.volatility = round(toolbox.util.clamp_value(self.volatility + change_amount, 0, 1000000), 2)

    def update_stock_dividend_percent(self, change_amount: float):
        self.dividend_percent = round(toolbox.util.clamp_value(self.dividend_percent + change_amount, 0, 1000000), 2)

    def daily_update(self):
        day_data = (self.available, self.stock_price, self.volatility)
        self.previous_day_data.append(day_data)
        change_min = int(-100 * self.volatility)
        change_max = int(100 * self.volatility)
        price_change = random.randint(change_min, change_max) / 100
        price_change += (1 - (self.available / self.available_max)) * self.get_demand_trend()
        self.stock_price = round(toolbox.util.clamp_value(self.stock_price + price_change, 0.01, 1000000), 2)

    def get_previous_price(self):
        if self.previous_day_data:
            return self.previous_day_data[-1][1]
        else:
            return self.stock_price

    def get_demand_trend(self, length: int = 7):
        return toolbox.util.get_data_trend(self.previous_day_data, 0, length)

    def get_price_trend(self, length: int = 7):
        return toolbox.util.get_data_trend(self.previous_day_data, 1, length)

    def get_volatility_trend(self, length: int = 7):
        return toolbox.util.get_data_trend(self.previous_day_data, 2, length)

    def get_volatility_text(self):
        return toolbox.util.get_multiplier_text(self.volatility)