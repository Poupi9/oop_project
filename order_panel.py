import tkinter as tk
from tkinter import ttk, messagebox
from store_manager import StoreManager
from basket import Basket
from exceptions import InvalidOrderException, OutOfStockException


class OrderPanel(tk.Frame):
    def __init__(self, parent, store: StoreManager, basket: Basket):
        super().__init__(parent, bg="#f5f5f5")
        self._store   = store
        self._basket  = basket
        self._orders  = []
        self._build_ui()

    def _build_ui(self) -> None:
        # --- basket section ---
        tk.Label(self, text="My Basket", font=("Arial", 15, "bold"),
                 bg="#f5f5f5", fg="#2c3e50").pack(anchor="w", padx=16, pady=(12, 4))

        basket_frame = tk.Frame(self, bg="#f5f5f5")
        basket_frame.pack(fill=tk.BOTH, padx=16, pady=(0, 8))

        cols = ("Name", "Price")
        self._basket_tree = ttk.Treeview(basket_frame, columns=cols,
                                         show="headings", height=8)
        self._basket_tree.heading("Name",  text="Product")
        self._basket_tree.heading("Price", text="Price")
        self._basket_tree.column("Name",  width=340, anchor="w")
        self._basket_tree.column("Price", width=100, anchor="e")
        self._basket_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- right controls ---
        ctrl = tk.Frame(basket_frame, bg="#f5f5f5", width=190)
        ctrl.pack(side=tk.RIGHT, fill=tk.Y, padx=(12, 0))
        ctrl.pack_propagate(False)

        self._total_lbl = tk.Label(ctrl, text="Total: $0.00",
                                   font=("Arial", 13, "bold"), bg="#f5f5f5")
        self._total_lbl.pack(pady=(20, 12))

        tk.Button(ctrl, text="Remove Selected", command=self._remove_item,
                  bg="#e74c3c", fg="white", relief="flat",
                  font=("Arial", 10), cursor="hand2", pady=6).pack(fill=tk.X, pady=(0, 8))

        tk.Button(ctrl, text="Checkout", command=self._checkout,
                  bg="#2980b9", fg="white", relief="flat",
                  font=("Arial", 12), cursor="hand2", pady=8).pack(fill=tk.X)

        self._msg_lbl = tk.Label(ctrl, text="", bg="#f5f5f5",
                                 font=("Arial", 10), wraplength=175, justify="left")
        self._msg_lbl.pack(pady=8, anchor="w")

        # --- order history ---
        tk.Label(self, text="Order History", font=("Arial", 14, "bold"),
                 bg="#f5f5f5", fg="#2c3e50").pack(anchor="w", padx=16, pady=(8, 4))

        hist_cols = ("Order ID", "Total", "Status", "Items")
        self._hist_tree = ttk.Treeview(self, columns=hist_cols, show="headings", height=7)
        widths = {"Order ID": 100, "Total": 90, "Status": 100, "Items": 500}
        for col in hist_cols:
            self._hist_tree.heading(col, text=col)
            self._hist_tree.column(col, width=widths[col], anchor="w")
        self._hist_tree.pack(fill=tk.BOTH, padx=16, pady=(0, 12))

        self._refresh_basket()

    def _refresh_basket(self) -> None:
        self._basket_tree.delete(*self._basket_tree.get_children())
        for item in self._basket.get_items():
            self._basket_tree.insert("", tk.END,
                                     values=(item.get_name(), f"${item.get_price():.2f}"))
        self._total_lbl.config(text=f"Total: ${self._basket.calculate_total():.2f}")

    def _remove_item(self) -> None:
        sel = self._basket_tree.selection()
        if not sel:
            return
        name    = self._basket_tree.item(sel[0])["values"][0]
        product = next((p for p in self._basket.get_items()
                        if p.get_name() == name), None)
        if product:
            self._basket.remove_product(product)
            self._refresh_basket()

    def _checkout(self) -> None:
        try:
            order = self._basket.checkout()
            self._store.process_order(order)
            self._store.save_data()
            self._orders.append(order)
            self._refresh_basket()
            self._refresh_history()
            self._msg_lbl.config(
                text=f"Order confirmed!\nID: {order.get_order_id()}\n"
                     f"Total: ${order.get_total_amount():.2f}",
                fg="#27ae60")
        except (InvalidOrderException, OutOfStockException) as e:
            self._msg_lbl.config(text=e.get_message(), fg="#e74c3c")

    def _refresh_history(self) -> None:
        self._hist_tree.delete(*self._hist_tree.get_children())
        for order in reversed(self._orders):
            items_str = ", ".join(p.get_name() for p in order.get_items())
            self._hist_tree.insert("", tk.END, values=(
                order.get_order_id(),
                f"${order.get_total_amount():.2f}",
                order.get_status(),
                items_str,
            ))
