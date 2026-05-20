from abc import ABC, abstractmethod
from product import Product


class User(ABC):
    def __init__(self, name: str, password_hash: str):
        self.__name = name
        self.__password_hash = password_hash

    def login(self, password: str) -> bool:
        return self.__password_hash == password

    def logout(self) -> None:
        pass

    def get_name(self) -> str:
        return self.__name

    def _get_password_hash(self) -> str:
        return self.__password_hash

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.__name}"


class Customer(User):
    def __init__(self, name: str, password_hash: str):
        super().__init__(name, password_hash)
        self.__favorite_list: list[Product] = []

    def add_to_favorites(self, p: Product) -> None:
        if p not in self.__favorite_list:
            self.__favorite_list.append(p)

    def remove_from_favorites(self, p: Product) -> None:
        if p in self.__favorite_list:
            self.__favorite_list.remove(p)

    def get_favorites(self) -> list[Product]:
        return list(self.__favorite_list)


class Admin(User):
    def __init__(self, name: str, password_hash: str):
        super().__init__(name, password_hash)

    def add_product(self, p: Product, catalog: list) -> None:
        catalog.append(p)

    def remove_product(self, p: Product, catalog: list) -> None:
        if p in catalog:
            catalog.remove(p)

    def update_product(self, p: Product, name: str = None, price: float = None, stock: int = None) -> None:
        if name is not None:
            p.set_name(name)
        if price is not None:
            p.set_price(price)
        if stock is not None:
            p.set_stock(stock)
