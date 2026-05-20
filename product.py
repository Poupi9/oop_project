from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def set_stock(self, new_stock: int) -> None:
        self.__stock = new_stock

    def set_price(self, new_price: float) -> None:
        self.__price = new_price

    def set_name(self, new_name: str) -> None:
        self.__name = new_name

    @abstractmethod
    def get_description(self) -> str:
        pass

    def __str__(self) -> str:
        return f"[{self.__product_id}] {self.__name} - ${self.__price:.2f} (stock: {self.__stock})"


class Apparel(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, size: str):
        super().__init__(product_id, name, price, stock)
        self.__size = size

    def get_size(self) -> str:
        return self.__size

    def get_description(self) -> str:
        return f"{self.get_name()} | Size: {self.__size}"


class Accessory(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        super().__init__(product_id, name, price, stock)

    def get_description(self) -> str:
        return f"{self.get_name()} | Accessory"


class Footwear(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, shoe_size: float):
        super().__init__(product_id, name, price, stock)
        self.__shoe_size = shoe_size

    def get_shoe_size(self) -> float:
        return self.__shoe_size

    def get_description(self) -> str:
        return f"{self.get_name()} | Shoe size: {self.__shoe_size}"
