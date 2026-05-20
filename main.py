from models.product import Apparel, Accessory, Footwear
from models.user import Customer, Admin, hash_password
from models.basket import Basket
from models.exceptions import OutOfStockException, InvalidOrderException, AuthenticationException

# --- PRODUCTS ---
shirt    = Apparel  ('P001', 'T-Shirt',  19.99, 3, 'M')
watch    = Accessory('P002', 'Watch',    89.99, 1)
shoes    = Footwear ('P003', 'Sneakers', 59.99, 2, 42.0)
jacket   = Apparel  ('P004', 'Jacket',   49.99, 1, 'L')
sold_out = Footwear ('P005', 'Boots',    79.99, 0, 41.0)

print("=" * 50)
print("PRODUCTS")
print("=" * 50)
for p in [shirt, watch, shoes, jacket, sold_out]:
    print(p)

# --- BASKET: normal flow ---
print("\n" + "=" * 50)
print("BASKET — normal checkout")
print("=" * 50)
basket = Basket()
basket.add_product(shirt)
basket.add_product(watch)
basket.add_product(shoes)
print(basket)
order = basket.checkout()
print("\n" + order.get_order_details())
assert len(order.get_items()) == 3
assert abs(order.get_total_amount() - (19.99 + 89.99 + 59.99)) < 0.01
assert order.get_status() == "confirmed"
print("\nAssertions passed: items, total, status are correct")
assert shirt.get_stock() == 2
assert watch.get_stock() == 0
assert shoes.get_stock() == 1
print("Assertions passed: stock decremented correctly")
assert basket.get_items() == []
print("Assertion passed: basket cleared after checkout")

# --- EXCEPTIONS ---
print("\n" + "=" * 50)
print("EXCEPTION — empty basket")
print("=" * 50)
try:
    basket.checkout()
except InvalidOrderException as e:
    print(f"Caught: {e.get_message()}")

print("\n" + "=" * 50)
print("EXCEPTION — add product with stock=0")
print("=" * 50)
try:
    basket.add_product(sold_out)
except OutOfStockException as e:
    print(f"Caught: {e.get_message()}")

print("\n" + "=" * 50)
print("EXCEPTION — stock reaches 0 before checkout")
print("=" * 50)
basket.add_product(jacket)
jacket.set_stock(0)
try:
    basket.checkout()
except OutOfStockException as e:
    print(f"Caught: {e.get_message()}")

# --- USERS ---
print("\n" + "=" * 50)
print("USERS")
print("=" * 50)
customer = Customer('Alice', hash_password('pass123'))
admin    = Admin   ('Bob',   hash_password('adminpass'))
print(customer)
print(admin)
assert customer.login('pass123') is True
assert customer.login('wrong')   is False
print("Assertions passed: login logic correct")
customer.add_to_favorites(shirt)
customer.add_to_favorites(shoes)
customer.add_to_favorites(shirt)
assert len(customer.get_favorites()) == 2
print("Favorites:", [p.get_name() for p in customer.get_favorites()])
customer.remove_from_favorites(shirt)
assert len(customer.get_favorites()) == 1
print("After remove:", [p.get_name() for p in customer.get_favorites()])
catalog = [shirt, watch, shoes]
new_product = Accessory('P006', 'Belt', 24.99, 10)
admin.add_product(new_product, catalog)
assert new_product in catalog
admin.update_product(new_product, price=19.99, stock=8)
assert new_product.get_price() == 19.99
admin.remove_product(new_product, catalog)
assert new_product not in catalog
print("Admin operations: OK")

# --- PART 3 + 4: FILE I/O & AUTH ---
print("\n" + "=" * 50)
print("PART 3+4 — FILE I/O & AUTHENTICATION")
print("=" * 50)
import json, os
from services.store_manager import StoreManager

os.makedirs('data', exist_ok=True)
products_data = [
    {'type': 'Apparel',   'product_id': 'P010', 'name': 'Hoodie',     'price': 39.99, 'stock': 5, 'size': 'L'},
    {'type': 'Accessory', 'product_id': 'P011', 'name': 'Sunglasses', 'price': 29.99, 'stock': 8},
    {'type': 'Footwear',  'product_id': 'P012', 'name': 'Loafers',    'price': 69.99, 'stock': 3, 'shoe_size': 43.0},
]
users_data = [
    {'type': 'Customer', 'name': 'Alice', 'password_hash': hash_password('alice123')},
    {'type': 'Admin',    'name': 'Bob',   'password_hash': hash_password('admin123')},
]
with open('data/products.json', 'w') as f:
    json.dump(products_data, f, indent=2)
with open('data/users.json', 'w') as f:
    json.dump(users_data, f, indent=2)

sm = StoreManager()
sm.get_logger().clear_logs()
sm.load_data()
assert len(sm.get_product_catalog()) == 3
assert len(sm.get_user_list())    == 2
print("Load OK:", [p.get_name() for p in sm.get_product_catalog()])

basket2 = Basket()
basket2.add_product(sm.get_product_catalog()[0])
basket2.add_product(sm.get_product_catalog()[2])
order2 = basket2.checkout()
sm.process_order(order2)
sm.save_data()

sm2 = StoreManager()
sm2.load_data()
assert sm2.get_product_catalog()[0].get_stock() == 4
print("Stock persisted correctly after save/reload")

alice = sm2.authenticate('Alice', 'alice123')
assert isinstance(alice, Customer)
bob = sm2.authenticate('Bob', 'admin123')
assert isinstance(bob, Admin)
print(f"Auth OK: {alice}, {bob}")

try:
    sm2.authenticate('Alice', 'wrong')
except AuthenticationException as e:
    print(f"Caught: {e.get_message()}")

try:
    sm2.authenticate('Ghost', 'x')
except AuthenticationException as e:
    print(f"Caught: {e.get_message()}")

print("\n" + "=" * 50)
print("ALL TESTS PASSED")
print("=" * 50)
