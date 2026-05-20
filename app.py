import json
import os
from user import hash_password

DATA_DIR      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
USERS_FILE    = os.path.join(DATA_DIR, "users.json")


def seed_if_empty() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(PRODUCTS_FILE):
        products = [
            {"type": "Apparel",   "product_id": "P001", "name": "T-Shirt",    "price": 19.99, "stock": 10, "size": "M"},
            {"type": "Apparel",   "product_id": "P002", "name": "Hoodie",     "price": 39.99, "stock": 6,  "size": "L"},
            {"type": "Accessory", "product_id": "P003", "name": "Watch",      "price": 89.99, "stock": 4},
            {"type": "Accessory", "product_id": "P004", "name": "Sunglasses", "price": 29.99, "stock": 8},
            {"type": "Footwear",  "product_id": "P005", "name": "Sneakers",   "price": 59.99, "stock": 5,  "shoe_size": 42.0},
            {"type": "Footwear",  "product_id": "P006", "name": "Loafers",    "price": 69.99, "stock": 3,  "shoe_size": 43.0},
        ]
        with open(PRODUCTS_FILE, "w") as f:
            json.dump(products, f, indent=2)

    if not os.path.exists(USERS_FILE):
        users = [
            {"type": "Customer", "name": "alice",  "password_hash": hash_password("alice123")},
            {"type": "Customer", "name": "bob",    "password_hash": hash_password("bob123")},
            {"type": "Admin",    "name": "admin",  "password_hash": hash_password("admin123")},
        ]
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)


if __name__ == "__main__":
    seed_if_empty()
    from main_window import MainWindow
    MainWindow().run()
