import tkinter as tk
from tkinter import messagebox
from store_manager import StoreManager
from basket import Basket
from user import Customer, Admin
from exceptions import AuthenticationException


class MainWindow:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("ShopApp")
        self._root.geometry("1000x650")
        self._root.configure(bg="#f5f5f5")

        self._store        = StoreManager()
        self._store.load_data()
        self._current_user = None
        self._basket       = None

        self._nav_frame     = tk.Frame(self._root, bg="#2c3e50", height=46)
        self._nav_frame.pack(fill=tk.X, side=tk.TOP)
        self._nav_frame.pack_propagate(False)

        self._content_frame = tk.Frame(self._root, bg="#f5f5f5")
        self._content_frame.pack(fill=tk.BOTH, expand=True)

        self._show_login_panel()

    def run(self) -> None:
        self._root.mainloop()

    # ------------------------------------------------------------------ #
    # panel switching                                                      #
    # ------------------------------------------------------------------ #

    def _clear(self) -> None:
        for w in self._content_frame.winfo_children():
            w.destroy()
        for w in self._nav_frame.winfo_children():
            w.destroy()

    def _build_nav(self, buttons: list) -> None:
        tk.Label(
            self._nav_frame, text="ShopApp",
            bg="#2c3e50", fg="white", font=("Arial", 13, "bold")
        ).pack(side=tk.LEFT, padx=16)

        for label, cmd in buttons:
            tk.Button(
                self._nav_frame, text=label, command=cmd,
                bg="#2c3e50", fg="white", relief="flat",
                font=("Arial", 10), cursor="hand2", padx=12
            ).pack(side=tk.LEFT)

        tk.Button(
            self._nav_frame, text="Logout", command=self._logout,
            bg="#e74c3c", fg="black", relief="flat",
            font=("Arial", 10), cursor="hand2", padx=12
        ).pack(side=tk.RIGHT, padx=8)

        tk.Label(
            self._nav_frame,
            text=f"  {self._current_user.get_name()}  ",
            bg="#2c3e50", fg="#bdc3c7", font=("Arial", 10)
        ).pack(side=tk.RIGHT)

    def _show_login_panel(self) -> None:
        self._clear()

        card = tk.Frame(self._content_frame, bg="white", padx=40, pady=40,
                        relief="groove", bd=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="ShopApp", font=("Arial", 26, "bold"),
                 bg="white", fg="#2c3e50").pack(pady=(0, 28))

        tk.Label(card, text="Username", bg="white", font=("Arial", 11)).pack(anchor="w")
        name_entry = tk.Entry(card, width=30, font=("Arial", 11))
        name_entry.pack(pady=(3, 12))
        name_entry.focus_set()

        tk.Label(card, text="Password", bg="white", font=("Arial", 11)).pack(anchor="w")
        pass_entry = tk.Entry(card, width=30, show="*", font=("Arial", 11))
        pass_entry.pack(pady=(3, 18))

        error_lbl = tk.Label(card, text="", fg="#e74c3c", bg="white", font=("Arial", 10))
        error_lbl.pack()

        def attempt_login(_event=None):
            name = name_entry.get().strip()
            pwd  = pass_entry.get()
            try:
                user = self._store.authenticate(name, pwd)
                self._current_user = user
                if isinstance(user, Admin):
                    self._show_admin_panel()
                else:
                    self._basket = Basket()
                    self._show_catalog_panel()
            except AuthenticationException as e:
                error_lbl.config(text=e.get_message())

        pass_entry.bind("<Return>", attempt_login)
        tk.Button(
            card, text="Login", command=attempt_login,
            bg="#2c3e50", fg="white", font=("Arial", 11),
            width=28, pady=7, relief="flat", cursor="hand2"
        ).pack(pady=(6, 0))

    def _show_catalog_panel(self) -> None:
        from product_catalog_panel import ProductCatalogPanel
        self._clear()
        self._build_nav([
            ("Catalog",   self._show_catalog_panel),
            ("My Basket", self._show_order_panel),
        ])
        ProductCatalogPanel(self._content_frame, self._store, self._basket).pack(
            fill=tk.BOTH, expand=True)

    def _show_order_panel(self) -> None:
        from order_panel import OrderPanel
        self._clear()
        self._build_nav([
            ("Catalog",   self._show_catalog_panel),
            ("My Basket", self._show_order_panel),
        ])
        OrderPanel(self._content_frame, self._store, self._basket).pack(
            fill=tk.BOTH, expand=True)

    def _show_admin_panel(self) -> None:
        from admin_panel import AdminPanel
        self._clear()
        self._build_nav([])
        AdminPanel(self._content_frame, self._store).pack(fill=tk.BOTH, expand=True)

    def _logout(self) -> None:
        self._store.save_data()
        self._current_user = None
        self._basket       = None
        self._show_login_panel()
