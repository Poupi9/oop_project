import json
import os
from product import Product, Apparel, Accessory, Footwear
from user import User, Customer, Admin, hash_password
from order import Order
from logger import Logger
from exceptions import AuthenticationException

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
USERS_FILE    = os.path.join(DATA_DIR, 'users.json')
LOGS_FILE     = os.path.join(DATA_DIR, 'logs.txt')


class StoreManager:
    def __init__(self):
        self.__product_catalog: list[Product] = []
        self.__user_list: list[User] = []
        self.__logger = Logger(LOGS_FILE)

    # --- public API ---

    def load_data(self) -> None:
        self.__load_products()
        self.__load_users()
        self.__logger.log("Data loaded from disk.")

    def save_data(self) -> None:
        os.makedirs(DATA_DIR, exist_ok=True)
        self.__save_products()
        self.__save_users()
        self.__logger.log("Data saved to disk.")

    def process_order(self, order: Order) -> None:
        items_str = ', '.join(p.get_name() for p in order.get_items())
        self.__logger.log(
            f"Order[{order.get_order_id()}] confirmed — "
            f"items: [{items_str}] — total: ${order.get_total_amount():.2f}"
        )
        order.set_status("processed")

    def get_product_catalog(self) -> list[Product]:
        return list(self.__product_catalog)

    def get_user_list(self) -> list[User]:
        return list(self.__user_list)

    def add_to_catalog(self, product: Product) -> None:
        self.__product_catalog.append(product)
        self.__logger.log(f"Admin added product '{product.get_name()}'.")

    def remove_from_catalog(self, product: Product) -> None:
        if product in self.__product_catalog:
            self.__product_catalog.remove(product)
            self.__logger.log(f"Admin removed product '{product.get_name()}'.")

    def authenticate(self, name: str, password: str) -> User:
        for user in self.__user_list:
            if user.get_name() == name:
                if user.login(password):
                    self.__logger.log(f"User '{name}' logged in.")
                    return user
                self.__logger.log(f"Failed login for '{name}' — wrong password.")
                raise AuthenticationException("wrong password")
        self.__logger.log(f"Failed login — user '{name}' not found.")
        raise AuthenticationException(f"user '{name}' not found")

    def register_user(self, name: str, password: str, role: str = "customer") -> User:
        for user in self.__user_list:
            if user.get_name() == name:
                raise ValueError(f"User '{name}' already exists.")
        hashed = hash_password(password)
        user = Admin(name, hashed) if role == "admin" else Customer(name, hashed)
        self.__user_list.append(user)
        self.__logger.log(f"User '{name}' registered as {role}.")
        return user

    def get_logger(self) -> Logger:
        return self.__logger

    # --- private: products ---

    def __load_products(self) -> None:
        if not os.path.exists(PRODUCTS_FILE):
            return
        try:
            with open(PRODUCTS_FILE, 'r') as f:
                data = json.load(f)
            self.__product_catalog = [self.__dict_to_product(d) for d in data]
            self.__product_catalog = [p for p in self.__product_catalog if p is not None]
        except (json.JSONDecodeError, KeyError, IOError) as e:
            self.__logger.log(f"ERROR loading products: {e}")

    def __save_products(self) -> None:
        try:
            with open(PRODUCTS_FILE, 'w') as f:
                json.dump([self.__product_to_dict(p) for p in self.__product_catalog], f, indent=2)
        except IOError as e:
            self.__logger.log(f"ERROR saving products: {e}")

    def __product_to_dict(self, p: Product) -> dict:
        d = {
            'type':       type(p).__name__,
            'product_id': p.get_id(),
            'name':       p.get_name(),
            'price':      p.get_price(),
            'stock':      p.get_stock(),
        }
        if isinstance(p, Apparel):
            d['size'] = p.get_size()
        elif isinstance(p, Footwear):
            d['shoe_size'] = p.get_shoe_size()
        return d

    def __dict_to_product(self, d: dict) -> Product | None:
        t = d.get('type')
        if t == 'Apparel':
            return Apparel(d['product_id'], d['name'], d['price'], d['stock'], d['size'])
        if t == 'Accessory':
            return Accessory(d['product_id'], d['name'], d['price'], d['stock'])
        if t == 'Footwear':
            return Footwear(d['product_id'], d['name'], d['price'], d['stock'], d['shoe_size'])
        return None

    # --- private: users ---

    def __load_users(self) -> None:
        if not os.path.exists(USERS_FILE):
            return
        try:
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
            self.__user_list = [self.__dict_to_user(d) for d in data]
            self.__user_list = [u for u in self.__user_list if u is not None]
        except (json.JSONDecodeError, KeyError, IOError) as e:
            self.__logger.log(f"ERROR loading users: {e}")

    def __save_users(self) -> None:
        try:
            with open(USERS_FILE, 'w') as f:
                json.dump([self.__user_to_dict(u) for u in self.__user_list], f, indent=2)
        except IOError as e:
            self.__logger.log(f"ERROR saving users: {e}")

    def __user_to_dict(self, u: User) -> dict:
        return {
            'type':          type(u).__name__,
            'name':          u.get_name(),
            'password_hash': u._get_password_hash(),
        }

    def __dict_to_user(self, d: dict) -> User | None:
        t = d.get('type')
        if t == 'Customer':
            return Customer(d['name'], d['password_hash'])
        if t == 'Admin':
            return Admin(d['name'], d['password_hash'])
        return None
