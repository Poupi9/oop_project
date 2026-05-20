from product import Apparel, Accessory, Footwear
from user import Customer, Admin, hash_password
from basket import Basket
from exceptions import OutOfStockException, InvalidOrderException, AuthenticationException

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

# --- EXCEPTION: empty basket ---
print("\n" + "=" * 50)
print("EXCEPTION — empty basket")
print("=" * 50)
try:
    basket.checkout()
except InvalidOrderException as e:
    print(f"Caught: {e.get_message()}")

# --- EXCEPTION: out of stock at add time ---
print("\n" + "=" * 50)
print("EXCEPTION — add product with stock=0")
print("=" * 50)
try:
    basket.add_product(sold_out)
except OutOfStockException as e:
    print(f"Caught: {e.get_message()}")

# --- EXCEPTION: stock runs out between add and checkout ---
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
print("\nCatalog after admin add:", [p.get_name() for p in catalog])

admin.update_product(new_product, price=19.99, stock=8)
assert new_product.get_price() == 19.99
assert new_product.get_stock() == 8
print("Belt after update:", new_product)

admin.remove_product(new_product, catalog)
assert new_product not in catalog
print("Catalog after admin remove:", [p.get_name() for p in catalog])

# --- PART 3: FILE I/O & STORE MANAGER ---
print("\n" + "=" * 50)
print("PART 3 — FILE I/O & STORE MANAGER")
print("=" * 50)

import json, os
from store_manager import StoreManager

sm = StoreManager()
sm.get_logger().clear_logs()
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

sm2 = StoreManager()
sm2.load_data()

loaded_products = sm2.get_product_catalog()
loaded_users    = sm2.get_user_list()

assert len(loaded_products) == 3
assert len(loaded_users)    == 2
assert loaded_products[0].get_name()      == 'Hoodie'
assert loaded_products[2].get_shoe_size() == 43.0
assert loaded_users[0].get_name()         == 'Alice'
print("Assertions passed: products and users loaded correctly")
print("Loaded products:", [p.get_name() for p in loaded_products])
print("Loaded users:   ", [u.get_name() for u in loaded_users])

basket2 = Basket()
basket2.add_product(loaded_products[0])
basket2.add_product(loaded_products[2])
order2 = basket2.checkout()
sm2.process_order(order2)

assert order2.get_status() == "processed"
print(f"\nOrder processed: {order2}")

sm2.save_data()

sm3 = StoreManager()
sm3.load_data()
hoodie_stock = sm3.get_product_catalog()[0].get_stock()
assert hoodie_stock == 4, f"expected 4, got {hoodie_stock}"
print(f"Assertion passed: Hoodie stock persisted as {hoodie_stock} after save/reload")

logs = sm2.get_logger().load_logs()
assert any("Hoodie" in line for line in logs)
print(f"\nLog entries ({len(logs)} total):")
for line in logs:
    print(" ", line.strip())

# --- PART 4: AUTHENTICATION ---
print("\n" + "=" * 50)
print("PART 4 — AUTHENTICATION")
print("=" * 50)

sm4 = StoreManager()
sm4.load_data()

# correct credentials → returns right type
alice = sm4.authenticate('Alice', 'alice123')
assert isinstance(alice, Customer), "Alice should be a Customer"
print(f"Authenticated: {alice}")

bob = sm4.authenticate('Bob', 'admin123')
assert isinstance(bob, Admin), "Bob should be an Admin"
print(f"Authenticated: {bob}")

# wrong password
try:
    sm4.authenticate('Alice', 'wrongpass')
except AuthenticationException as e:
    print(f"Caught: {e.get_message()}")

# unknown user
try:
    sm4.authenticate('Charlie', 'any')
except AuthenticationException as e:
    print(f"Caught: {e.get_message()}")

# register a new user then authenticate
sm4.register_user('Carol', 'carol456', role='customer')
carol = sm4.authenticate('Carol', 'carol456')
assert isinstance(carol, Customer)
print(f"Registered and authenticated: {carol}")

# duplicate registration
try:
    sm4.register_user('Carol', 'other')
except ValueError as e:
    print(f"Caught: {e}")

# check all auth events appear in logs
sm4.save_data()
logs4 = sm4.get_logger().load_logs()
print(f"\nAuth log entries ({len(logs4)} total):")
for line in logs4:
    print(" ", line.strip())

print("\n" + "=" * 50)
print("ALL TESTS PASSED")
print("=" * 50)
