import toolbox.util
from uuid import UUID
from toolbox.item import Item


class BankDepositReceipt(Item):
    def __init__(self, bank_name: str, deposit_id: UUID, deposit_amount: float, interest_rate: float, mature_time: int,
                 purchase_time: float):
        receipt_id = toolbox.util.generate_simple_id()
        receipt_name = "Bank deposit receipt."
        receipt_description = f"Bank deposit receipt for {bank_name}."
        receipt_icon = "bank_deposit_receipt"
        super().__init__(receipt_id, receipt_name, receipt_description, receipt_icon, 0)
        self.bank_name = bank_name
        self.deposit_id = deposit_id
        self.deposit_amount = deposit_amount
        self.interest_rate = interest_rate
        self.mature_time = mature_time
        self.purchase_time = purchase_time
