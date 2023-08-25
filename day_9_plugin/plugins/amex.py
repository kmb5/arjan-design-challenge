from decimal import Decimal


def get_payment_method() -> str:
    return "amex"


def process_payment(total: Decimal) -> None:
    card_id = input("Please enter your amex card ID: ")
    card_id = card_id[-4:].rjust(len(card_id), "*")
    print(f"Processing Amex payment of ${total:.2f} with card ID {card_id}...")
