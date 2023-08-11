from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union


@dataclass
class Item:
    name: str
    price: Decimal
    quantity: int

    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity

    def set_price(self, price: Decimal) -> None:
        self.price = price

    def set_quantity(self, quantity: int) -> None:
        self.quantity = quantity

    def print_item(self) -> None:
        total_price = self.subtotal
        print(
            f"{self.name:<12}${self.price:>7.2f}{self.quantity:>7}     ${total_price:>7.2f}"
        )


class ItemNotFoundException(Exception):
    pass


@dataclass
class ShoppingCart:
    items: list[Item] = field(default_factory=list)
    discount_code: Union[str, None] = None

    @property
    def total(self) -> Decimal:
        return Decimal(sum(item.subtotal for item in self.items))

    def display(self) -> None:
        # Print the cart
        print("Shopping Cart:")
        print(f"{'Item':<10}{'Price':>10}{'Qty':>7}{'Total':>13}")
        for item in self.items:
            item.print_item()
        print("=" * 40)
        print(f"Total: ${self.total:>7.2f}")

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item_name: str) -> None:
        found_item = self.find_item(item_name)
        self.items.remove(found_item)

    def find_item(self, item_name: str) -> Item:
        for item in self.items:
            if item.name == item_name:
                return item
        raise ItemNotFoundException(f"Item {item_name} not found in cart")

    def update_item_quantity(self, item_name: str, quantity: int) -> None:
        item = self.find_item(item_name)
        item.set_quantity(quantity)

    def update_item_price(self, item_name: str, price: Decimal) -> None:
        item = self.find_item(item_name)
        item.set_price(price)


def main() -> None:
    # Create a shopping cart and add some items to it
    cart = ShoppingCart(
        items=[
            Item("Apple", Decimal("1.5"), 10),
            Item("Banana", Decimal("2"), 2),
            Item("Pizza", Decimal("11.90"), 5),
        ],
    )

    # Update some items' quantity and price
    cart.update_item_quantity("Apple", 10)
    cart.update_item_price("Pizza", Decimal("3.50"))

    # Remove an item
    cart.remove_item("Banana")

    cart.display()


if __name__ == "__main__":
    main()
