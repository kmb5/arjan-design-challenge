from decimal import Decimal
from account import Account
from payment_service import PaymentService


class BankService:
    def deposit(
        self, amount: Decimal, account: Account, payment_service: PaymentService
    ) -> None:
        account.deposit(amount, payment_service)

    def withdraw(
        self, amount: Decimal, account: Account, payment_service: PaymentService
    ) -> None:
        account.withdraw(amount, payment_service)
