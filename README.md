# Archive-Store — Online Shopping System

A desktop e-commerce application built with Python and Tkinter as part of an Object-Oriented Programming course project (ESIEA S2). The application demonstrates core OOP principles — abstraction, encapsulation, inheritance, and polymorphism — through a fully functional fashion store with a minimalist GUI inspired by Zara and H&M.

---

## Features

- **Customer flow** — browse products by category, add to cart, checkout
- **Admin flow** — add, update, and remove products; view timestamped activity logs
- **Authentication** — SHA-256 hashed passwords, role-based routing (Customer / Admin)
- **Persistence** — catalog and user data stored as JSON; survives application restarts
- **Responsive product grid** — reflows columns on window resize
- **Real product images** — full-bleed homepage banner, cover-cropped product cards and cart thumbnails
- **Custom exceptions** — `OutOfStockException`, `InvalidOrderException`, `AuthenticationException`

---

## Project Structure

```
archive-store/
├── app.py                      # Entry point — seeds data and launches the GUI
├── main.py                     # Headless test script (Parts 1–4)
│
├── models/
│   ├── product.py              # Product (ABC), Apparel, Pants, Footwear, Accessory
│   ├── user.py                 # User (ABC), Customer, Admin; hash_password()
│   ├── basket.py               # Basket — add, remove, checkout()
│   ├── order.py                # Order — UUID, datetime, status, payment ref
│   ├── payment.py              # Payment — UUID, amount, process_payment()
│   └── exceptions.py           # OutOfStockException, InvalidOrderException, AuthenticationException
│
├── services/
│   ├── store_manager.py        # StoreManager — load/save JSON, auth, catalog management
│   └── logger.py               # Logger — timestamped append-only log file
│
├── gui/
│   ├── main_window.py          # MainWindow — header, routing, login screen
│   ├── homepage_panel.py       # Full-bleed responsive banner image
│   ├── product_catalog_panel.py# Scrollable product grid with image cards
│   ├── order_panel.py          # Cart view, checkout, order history
│   ├── admin_panel.py          # Product management + logs viewer
│   └── image_loader.py         # Pillow-based image loader (cached, cover-crop)
│
├── data/
│   ├── products.json           # Product catalog (auto-generated on launch)
│   ├── users.json              # User accounts (auto-generated on launch)
│   └── logs.txt                # Activity log
│
└── images/
    ├── menu.jpeg               # Homepage banner
    ├── top/                    # top1.jpeg – top3.jpeg
    ├── pants/                  # pants1.jpeg – pants3.jpeg
    ├── shoes/                  # shoes1.jpeg – shoes3.jpeg
    └── accessories/            # bag.jpeg, glasses.jpeg, joaillerie.jpeg
```

---

## Requirements

- Python 3.10+
- Pillow

Install the dependency:

```bash
pip install Pillow
```

---

## Running the Application

```bash
python app.py
```

This seeds `data/products.json` and `data/users.json` with the default catalog and user accounts on every launch, then opens the GUI.

### Default accounts

| Username | Password   | Role     |
|----------|------------|----------|
| alice    | alice123   | Customer |
| bob      | bob123     | Customer |
| admin    | admin123   | Admin    |

---

## Running the Headless Tests

`main.py` covers all non-GUI logic (Parts 1–4): product instantiation, basket checkout, stock management, file I/O, and authentication.

```bash
python main.py
```

Expected output ends with `ALL TESTS PASSED`.

---

## OOP Concepts Demonstrated

| Concept | Where |
|---|---|
| **Abstract classes** | `Product` (ABC), `User` (ABC) — enforce `get_description()` / `login()` |
| **Inheritance** | `Apparel`, `Pants`, `Footwear`, `Accessory` extend `Product`; `Customer`, `Admin` extend `User` |
| **Encapsulation** | All model fields are `__private`; accessed only through getters/setters |
| **Polymorphism** | `get_description()` returns type-specific strings; catalog accepts any `Product` subclass |
| **Custom exceptions** | Three domain exceptions with `get_message()`, raised on invalid business operations |

---

## GUI Navigation

```
Login screen
    ├── Customer → Homepage (banner image)
    │       ├── HOME / TOPS / PANTS / SHOES / ACCESSORIES  (header nav)
    │       ├── Product grid → Add to Cart
    │       └── CART → checkout → order history
    └── Admin → Admin Panel
            ├── Products tab (add / update / remove)
            └── Logs tab (refresh / clear)
```
