from models.product import Product
from models.payment import Payment
from models.order import Order
from models.exceptions import OutOfStockException, InvalidOrderException


class Basket:
    def __init__(self):
        self.__items: list[Product] = []

    def add_product(self, p: Product) -> None:
        if p.get_stock() <= 0:
            raise OutOfStockException(p.get_name())
        self.__items.append(p)

    def remove_product(self, p: Product) -> None:
        if p in self.__items:
            self.__items.remove(p)

    def calculate_total(self) -> float:
        return sum(p.get_price() for p in self.__items)

    def get_items(self) -> list[Product]:
        return list(self.__items)

    def clear(self) -> None:
        self.__items.clear()

    def checkout(self) -> Order:
        if not self.__items:
            raise InvalidOrderException("basket is empty")

        for item in self.__items:
            if item.get_stock() <= 0:
                raise OutOfStockException(item.get_name())

        for item in self.__items:
            item.set_stock(item.get_stock() - 1)

        total   = self.calculate_total()
        payment = Payment(total)
        payment.process_payment()

        order = Order(self.__items, total, payment)
        self.clear()
        return order

    def __str__(self) -> str:
        if not self.__items:
            return "Basket is empty"
        lines = [f"  - {p.get_name()} (${p.get_price():.2f})" for p in self.__items]
        lines.append(f"  Total: ${self.calculate_total():.2f}")
        return "Basket:\n" + "\n".join(lines)
