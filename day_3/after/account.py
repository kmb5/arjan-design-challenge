from enum import Enum
from decimal import Decimal
from dataclasses import dataclass

from payment_service import PaymentService


class AccountType(Enum):
    SAVINGS = "Savings"
    CHECKING = "Checking"


@dataclass
class Account:
    account_number: str
    balance: Decimal
    account_type: AccountType

    def deposit(self, amount: Decimal, payment_service: PaymentService) -> None:
        print(
            f"Depositing {amount} into {self.account_type.value} Account {self.account_number}."
        )
        payment_service.process_payment(amount)
        self.balance += amount

    def withdraw(self, amount: Decimal, payment_service: PaymentService) -> None:
        print(
            f"Withdrawing {amount} from {self.account_type.value} Account {self.account_number}."
        )
        payment_service.process_payout(amount)
        self.balance -= amount
