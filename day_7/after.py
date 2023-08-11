from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, auto
from typing import Optional


class ItemNotFoundException(Exception):
    pass


@dataclass
class Item:
    name: str
    price: Decimal
    quantity: int

    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity


class DiscountType(Enum):
    PERCENTAGE = auto()
    AMOUNT = auto()


@dataclass
class DiscountCode:
    code: str
    discount_value: Decimal
    discount_type: DiscountType

    def get_discounted_price(self, amount: Decimal) -> Decimal:
        if self.discount_type == DiscountType.PERCENTAGE:
            return amount * self.discount_value
        if self.discount_type == DiscountType.AMOUNT:
            return amount - (amount - self.discount_value)
        raise ValueError("Invalid discount type")


@dataclass
class ShoppingCart:
    items: list[Item] = field(default_factory=list)
    discount_code: Optional[DiscountCode] = None

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def remove_item(self, item_name: str) -> None:
        found_item = self.find_item(item_name)
        self.items.remove(found_item)

    def find_item(self, item_name: str) -> Item:
        for item in self.items:
            if item.name == item_name:
                return item
        raise ItemNotFoundException(f"Item '{item_name}' not found.")

    @property
    def subtotal(self) -> Decimal:
        return Decimal(sum(item.subtotal for item in self.items))

    @property
    def discount(self) -> Decimal:
        if not self.discount_code:
            return Decimal("0")
        return self.discount_code.get_discounted_price(self.subtotal)

    @property
    def total(self) -> Decimal:
        return self.subtotal - self.discount

    def display(self) -> None:
        # Print the cart
        print("Shopping Cart:")
        print(f"{'Item':<10}{'Price':>10}{'Qty':>7}{'Total':>13}")
        for item in self.items:
            print(
                f"{item.name:<12}${item.price:>7.2f}{item.quantity:>7}     ${item.subtotal:>7.2f}"
            )
        print("=" * 40)
        print(f"Subtotal: ${self.subtotal:>7.2f}")
        print(f"Discount: ${self.discount:>7.2f}")
        print(f"Total:    ${self.total:>7.2f}")


def main() -> None:
    # Create a shopping cart and add some items to it
    discount_code = DiscountCode("SAVE10", Decimal("0.1"), DiscountType.AMOUNT)
    cart = ShoppingCart(
        items=[
            Item("Apple", Decimal("1.50"), 10),
            Item("Banana", Decimal("2.00"), 2),
            Item("Pizza", Decimal("11.90"), 5),
        ],
        discount_code=discount_code,
    )

    cart.display()


if __name__ == "__main__":
    main()
