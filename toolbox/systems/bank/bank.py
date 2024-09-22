import uuid
import shared
from uuid import UUID
from collections import defaultdict
from toolbox.systems.bank.bank_deposit import BankDeposit
from toolbox.systems.bank.bank_deposit_receipt import BankDepositReceipt
from toolbox.wallet import Wallet


class Bank(object):
    def __init__(self, bank_name: str = "MyBank"):
        self.bank_name = bank_name
        self.interest_rates: defaultdict[int, float] = defaultdict({
            5: 0.01,
            10: 0.0125,
            15: 0.015,
            20: 0.0175,
            25: 0.02,
            30: 0.0225,
        })
        self.deposits: defaultdict[UUID, BankDeposit] = defaultdict()

    def make_deposit(self, wallet: Wallet, amount: float, mature_time: int):
        interest_rate = self.interest_rates.get(mature_time)
        if interest_rate is not None:
            deposit_amount = round(amount, 2)
            if wallet.cash >= deposit_amount:
                wallet.cash -= deposit_amount
                deposit_id = uuid.uuid4()
                purchase_time = shared.time_running_min
                self.deposits[deposit_id] = BankDeposit(deposit_id, deposit_amount, interest_rate, mature_time,
                                                        purchase_time)
                wallet.owned_items.append(BankDepositReceipt(self.bank_name, deposit_id, deposit_amount, interest_rate,
                                                             mature_time, purchase_time))

    def make_withdraw(self, wallet: Wallet, receipt: BankDepositReceipt):
        deposit = self.deposits.get(receipt.deposit_id)
        if deposit is not None:
            current_time = shared.time_running_min
            mature_time = deposit.purchase_time + deposit.mature_time_min
            is_mature = current_time >= mature_time
            if is_mature:
                del self.deposits[receipt.deposit_id]
                for index, item in enumerate(wallet.owned_items):
                    if isinstance(item, BankDepositReceipt) and item.deposit_id == receipt.deposit_id:
                        del wallet.owned_items[index]
                        break
                interest_earned = deposit.amount * deposit.interest_rate
                total_amount = deposit.amount + interest_earned
                wallet.cash += total_amount
