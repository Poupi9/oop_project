import uuid


class Payment:
    def __init__(self, amount: float):
        self.__payment_id = str(uuid.uuid4())[:8]
        self.__amount = amount
        self.__status = "pending"

    def process_payment(self) -> bool:
        self.__status = "confirmed"
        return True

    def get_status(self) -> str:
        return self.__status

    def get_amount(self) -> float:
        return self.__amount

    def get_payment_id(self) -> str:
        return self.__payment_id

    def __str__(self) -> str:
        return f"Payment[{self.__payment_id}] ${self.__amount:.2f} - {self.__status}"
