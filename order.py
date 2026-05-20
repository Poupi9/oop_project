import uuid
from datetime import datetime
from product import Product
from payment import Payment


class Order:
    def __init__(self, purchased_items: list[Product], total_amount: float, payment: Payment):
        self.__order_id = str(uuid.uuid4())[:8]
        self.__order_date = datetime.now()
        self.__purchased_items = list(purchased_items)
        self.__total_amount = total_amount
        self.__status = "confirmed"
        self.__payment = payment

    def get_order_id(self) -> str:
        return self.__order_id

    def get_status(self) -> str:
        return self.__status

    def set_status(self, status: str) -> None:
        self.__status = status

    def get_total_amount(self) -> float:
        return self.__total_amount

    def get_items(self) -> list[Product]:
        return list(self.__purchased_items)

    def get_order_details(self) -> str:
        lines = [
            f"Order ID : {self.__order_id}",
            f"Date     : {self.__order_date.strftime('%Y-%m-%d %H:%M')}",
            f"Status   : {self.__status}",
            f"Payment  : {self.__payment}",
            f"Items    :",
        ]
        for item in self.__purchased_items:
            lines.append(f"  - {item.get_name()} (${item.get_price():.2f})")
        lines.append(f"Total    : ${self.__total_amount:.2f}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return f"Order[{self.__order_id}] ${self.__total_amount:.2f} - {self.__status}"
