Coding Plan — Online Shopping System
The rule: each part must run and be testable before moving to the next. Never touch the GUI until the logic underneath works.

## Part 1 — Data models (no logic, just structure)
Files to create:

product.py → Product (abstract), Apparel, Accessory, Footwear
user.py → User (abstract), Customer, Admin
exceptions.py → OutOfStockException, InvalidOrderException, AuthenticationException
What you test: instantiate objects in a main.py scratch file, print their fields. Nothing runs yet, just checking that classes don't crash.

## Part 2 — Business logic (core shopping flow)
Files to create:

payment.py → Payment
order.py → Order
basket.py → Basket (including checkout() which creates an Order)
What you test: manually create a basket, add products, call checkout(), check the returned Order has the right items and total. Test OutOfStockException fires when stock is 0.

## Part 3 — File I/O and persistence
Files to create:

logger.py → Logger
store_manager.py → StoreManager (loadData(), saveData(), processOrder())
data/ folder → products.json, users.json, logs.txt
What you test: save a few products and users to file, restart, check they reload correctly. Log an action, check logs.txt is written.

## Part 4 — Login & authentication
In user.py: implement login(password) with hashed password check, raise AuthenticationException on failure.

In store_manager.py: add a authenticate(name, password) method that returns the right User subtype.

What you test: correct password returns a Customer or Admin object. Wrong password raises the exception.

## Part 5 — GUI
Files to create:

main_window.py → MainWindow (login screen + panel switcher)
product_catalog_panel.py → ProductCatalogPanel
order_panel.py → OrderPanel
admin_panel.py → AdminPanel
Order inside Part 5:

Login screen → redirects to the right panel based on user type
ProductCatalogPanel — display + add to basket
OrderPanel — show basket, confirm order, payment
AdminPanel — add/remove/update products, view logs
What you test: full happy path — login as customer, browse, add to basket, checkout. Then login as admin, add a product, check it appears in catalog.

## Final check before submission
All data survives a restart (File I/O works end to end)
All 3 exceptions are triggered at least once in normal usage
No hardcoded data — everything loads from files
Run through the grading criteria: functionality, code quality, OOP concepts all visible