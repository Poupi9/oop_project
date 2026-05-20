import json
import os
from models.user import hash_password

DATA_DIR      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
USERS_FILE    = os.path.join(DATA_DIR, "users.json")

PRODUCTS = [
    # ── Tops ───────────────────────────────────────────────────────
    {"type": "Apparel", "product_id": "T001", "name": "Striped Linen Blouse",
     "price": 49.99, "stock": 10, "size": "M", "image_path": "images/top/top1.jpeg"},
    {"type": "Apparel", "product_id": "T002", "name": "White Fitted Tee",
     "price": 29.99, "stock": 8,  "size": "S", "image_path": "images/top/top2.jpeg"},
    {"type": "Apparel", "product_id": "T003", "name": "Blue Top Shirt",
     "price": 39.99, "stock": 6,  "size": "L", "image_path": "images/top/top3.jpeg"},
    # ── Pants ──────────────────────────────────────────────────────
    {"type": "Pants",   "product_id": "P001", "name": "Baggy Pants",
     "price": 59.99, "stock": 7,  "size": "M", "image_path": "images/pants/pants1.jpeg"},
    {"type": "Pants",   "product_id": "P002", "name": "Wide Leg Trousers",
     "price": 69.99, "stock": 5,  "size": "L", "image_path": "images/pants/pants2.jpeg"},
    {"type": "Pants",   "product_id": "P003", "name": "White Pants",
     "price": 49.99, "stock": 9,  "size": "S", "image_path": "images/pants/pants3.jpeg"},
    # ── Shoes ──────────────────────────────────────────────────────
    {"type": "Footwear", "product_id": "S001", "name": "Leather Sneakers",
     "price": 89.99, "stock": 5, "shoe_size": 42.0, "image_path": "images/shoes/shoes1.jpeg"},
    {"type": "Footwear", "product_id": "S002", "name": "Oxford Sneakers",
     "price": 79.99, "stock": 4, "shoe_size": 41.0, "image_path": "images/shoes/shoes2.jpeg"},
    {"type": "Footwear", "product_id": "S003", "name": "Ballerina",
     "price": 99.99, "stock": 3, "shoe_size": 38.0, "image_path": "images/shoes/shoes3.jpeg"},
    # ── Accessories ────────────────────────────────────────────────
    {"type": "Accessory", "product_id": "A001", "name": "Leather Bag",
     "price": 119.99, "stock": 4, "image_path": "images/accessories/bag.jpeg"},
    {"type": "Accessory", "product_id": "A002", "name": "Classic Sunglasses",
     "price": 29.99,  "stock": 8, "image_path": "images/accessories/glasses.jpeg"},
    {"type": "Accessory", "product_id": "A003", "name": "Gold Bracelet",
     "price": 59.99,  "stock": 6, "image_path": "images/accessories/joaillerie.jpeg"},
]

USERS = [
    {"type": "Customer", "name": "alice", "password_hash": hash_password("alice123")},
    {"type": "Customer", "name": "bob",   "password_hash": hash_password("bob123")},
    {"type": "Admin",    "name": "admin", "password_hash": hash_password("admin123")},
]


def seed_if_empty() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "w") as f:
            json.dump(PRODUCTS, f, indent=2)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump(USERS, f, indent=2)


def reset_data() -> None:
    """Force-overwrite data files with fresh seed (useful during dev)."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(PRODUCTS, f, indent=2)
    with open(USERS_FILE, "w") as f:
        json.dump(USERS, f, indent=2)


if __name__ == "__main__":
    reset_data()          # always start with clean catalog when launching
    from gui.main_window import MainWindow
    MainWindow().run()
