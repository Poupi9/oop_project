class OutOfStockException(Exception):
    def __init__(self, product_name: str):
        self.__product_name = product_name
        super().__init__(f"'{product_name}' is out of stock.")

    def get_message(self) -> str:
        return str(self)


class InvalidOrderException(Exception):
    def __init__(self, reason: str):
        self.__reason = reason
        super().__init__(f"Invalid order: {reason}")

    def get_message(self) -> str:
        return str(self)


class AuthenticationException(Exception):
    def __init__(self, reason: str):
        self.__reason = reason
        super().__init__(f"Authentication failed: {reason}")

    def get_message(self) -> str:
        return str(self)
