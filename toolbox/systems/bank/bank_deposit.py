from uuid import UUID


class BankDeposit(object):
    def __init__(self, deposit_id: UUID, amount: float, interest_rate: float, mature_time_min: int,
                 purchase_time: float):
        self.deposit_id = deposit_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.mature_time_min = mature_time_min
        self.purchase_time = purchase_time
