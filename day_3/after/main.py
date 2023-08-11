from decimal import Decimal
from account import Account, AccountType
from bank import BankService
from payment_service import StripePaymentService

API_KEY = "sk_test_1234567890"


def main() -> None:
    savings_account = Account("SA001", Decimal("1000"), AccountType.SAVINGS)
    checking_account = Account("CA001", Decimal("500"), AccountType.CHECKING)

    bank_service = BankService()
    payment_service = StripePaymentService(api_key=API_KEY)

    bank_service.deposit(Decimal("200"), savings_account, payment_service)
    bank_service.deposit(Decimal("300"), checking_account, payment_service)

    bank_service.withdraw(Decimal("100"), savings_account, payment_service)
    bank_service.withdraw(Decimal("200"), checking_account, payment_service)

    print(f"Savings Account Balance: {savings_account.balance}")
    print(f"Checking Account Balance: {checking_account.balance}")


if __name__ == "__main__":
    main()
