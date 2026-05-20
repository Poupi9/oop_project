from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, image_path: str = ""):
        self.__product_id = product_id
        self.__name       = name
        self.__price      = price
        self.__stock      = stock
        self.__image_path = image_path

    def get_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_image_path(self) -> str:
        return self.__image_path

    def set_stock(self, new_stock: int) -> None:
        self.__stock = new_stock

    def set_price(self, new_price: float) -> None:
        self.__price = new_price

    def set_name(self, new_name: str) -> None:
        self.__name = new_name

    def set_image_path(self, path: str) -> None:
        self.__image_path = path

    @abstractmethod
    def get_description(self) -> str:
        pass

    def __str__(self) -> str:
        return (f"[{self.__product_id}] {self.__name} "
                f"- ${self.__price:.2f} (stock: {self.__stock})")


class Apparel(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, size: str, image_path: str = ""):
        super().__init__(product_id, name, price, stock, image_path)
        self.__size = size

    def get_size(self) -> str:
        return self.__size

    def get_description(self) -> str:
        return f"{self.get_name()} | Size: {self.__size}"


class Pants(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, size: str, image_path: str = ""):
        super().__init__(product_id, name, price, stock, image_path)
        self.__size = size

    def get_size(self) -> str:
        return self.__size

    def get_description(self) -> str:
        return f"{self.get_name()} | Size: {self.__size}"


class Accessory(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, image_path: str = ""):
        super().__init__(product_id, name, price, stock, image_path)

    def get_description(self) -> str:
        return f"{self.get_name()} | Accessory"


class Footwear(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, shoe_size: float, image_path: str = ""):
        super().__init__(product_id, name, price, stock, image_path)
        self.__shoe_size = shoe_size

    def get_shoe_size(self) -> float:
        return self.__shoe_size

    def get_description(self) -> str:
        return f"{self.get_name()} | Shoe size: {self.__shoe_size}"
