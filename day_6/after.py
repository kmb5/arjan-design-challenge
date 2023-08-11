from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union, Literal


@dataclass
class Item:
    name: str
    price: Decimal
    quantity: int

    def total_price(self) -> Decimal:
        return self.price * self.quantity

    def set_price(self, price: Decimal) -> None:
        self.price = price

    def set_quantity(self, quantity: int) -> None:
        self.quantity = quantity

    def print_item(self) -> None:
        total_price = self.total_price()
        print(
            f"{self.name:<12}${self.price:>7.2f}{self.quantity:>7}     ${total_price:>7.2f}"
        )


@dataclass
class ShoppingCart:
    items: list[Item] = field(default_factory=list)
    discount_code: Union[str, None] = None

    def total(self) -> Union[Decimal, Literal[0]]:
        return sum(item.total_price() for item in self.items)

    def print_cart(self) -> None:
        # Print the cart
        total = self.total()
        print("Shopping Cart:")
        print(f"{'Item':<10}{'Price':>10}{'Qty':>7}{'Total':>13}")
        for item in self.items:
            item.print_item()
        print("=" * 40)
        print(f"Total: ${total:>7.2f}")

    def remove_item(self, item: Item) -> None:
        self.items.remove(item)


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
    cart.items[0].set_quantity(10)
    cart.items[2].set_price(Decimal("3.50"))

    # Remove an item
    cart.remove_item(cart.items[1])

    cart.print_cart()


if __name__ == "__main__":
    main()
