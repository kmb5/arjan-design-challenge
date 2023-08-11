from decimal import Decimal
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional


class OrderType(Enum):
    ONLINE = "online"
    IN_STORE = "in store"


@dataclass
class Item:
    name: str
    price: Decimal


class EmailType(Enum):
    ORDER_CONFIRMATION = "Order Confirmation"
    ORDER_SHIPPING_NOTIFICATION = "Order Shipping Notification"


@dataclass
class Email:
    body: str
    subject: str
    recipient: str
    sender: str


@dataclass
class Order:
    id: int
    type: OrderType
    customer_email: str
    items: Iterable[Item]

    def calculate_total_price(self, discount: Optional[Decimal] = None) -> Decimal:
        price = Decimal(sum(item.price for item in self.items))
        if discount:
            price = price - (price * discount)
        return price

    def process(self) -> None:
        print(f"Processing {self.type.value} order...")
        print(self.generate_email(EmailType.ORDER_CONFIRMATION))
        print("Shipping the order...")
        print(self.generate_email(EmailType.ORDER_SHIPPING_NOTIFICATION))
        print("Order processed successfully.")

    def generate_email(self, email_type: EmailType) -> Email:
        if email_type == EmailType.ORDER_CONFIRMATION:
            body = (
                f"Thank you for your order! Your order #{self.id} has been confirmed."
            )
        elif email_type == EmailType.ORDER_SHIPPING_NOTIFICATION:
            body = (
                f"Good news! Your order #{self.id} has been shipped and is on its way."
            )
        else:
            raise ValueError(f"Invalid email type: {email_type}")

        return Email(
            body=body,
            subject=email_type.value,
            recipient=self.customer_email,
            sender="sales@webshop.com",
        )


def main() -> None:
    items = [
        Item(name="T-Shirt", price=Decimal("19.99")),
        Item(name="Jeans", price=Decimal("49.99")),
        Item(name="Shoes", price=Decimal("79.99")),
    ]

    online_order = Order(
        id=123, type=OrderType.ONLINE, customer_email="sarah@gmail.com", items=items
    )

    total_price = online_order.calculate_total_price()
    print("Total price:", total_price)

    discounted_price = online_order.calculate_total_price(discount=Decimal("0.1"))
    print("Discounted price:", discounted_price)

    online_order.process()

    in_store_order = Order(
        id=456, type=OrderType.IN_STORE, customer_email="john@gmail.com", items=items
    )

    in_store_order.process()


if __name__ == "__main__":
    main()
