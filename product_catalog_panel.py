import tkinter as tk
from tkinter import ttk, messagebox
from store_manager import StoreManager
from basket import Basket
from exceptions import OutOfStockException


class ProductCatalogPanel(tk.Frame):
    def __init__(self, parent, store: StoreManager, basket: Basket):
        super().__init__(parent, bg="#f5f5f5")
        self._store  = store
        self._basket = basket
        self._build_ui()

    def _build_ui(self) -> None:
        # --- top bar ---
        top = tk.Frame(self, bg="#f5f5f5")
        top.pack(fill=tk.X, padx=16, pady=(12, 6))

        tk.Label(top, text="Product Catalog", font=("Arial", 15, "bold"),
                 bg="#f5f5f5", fg="#2c3e50").pack(side=tk.LEFT)

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh())
        tk.Label(top, text="Search:", bg="#f5f5f5", font=("Arial", 11)).pack(side=tk.RIGHT, padx=(0, 4))
        tk.Entry(top, textvariable=self._search_var, width=22,
                 font=("Arial", 11)).pack(side=tk.RIGHT)

        # --- treeview ---
        tree_frame = tk.Frame(self, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 8))

        cols = ("ID", "Name", "Type", "Price", "Stock", "Details")
        self._tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=20)
        widths = {"ID": 70, "Name": 160, "Type": 100, "Price": 80, "Stock": 65, "Details": 300}
        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=widths[col], anchor="w")

        sb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.LEFT, fill=tk.Y)

        # --- right panel ---
        right = tk.Frame(self, bg="#f5f5f5", width=180)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=16, pady=8)
        right.pack_propagate(False)

        tk.Button(
            right, text="Add to Basket", command=self._add_to_basket,
            bg="#27ae60", fg="white", font=("Arial", 11), relief="flat",
            cursor="hand2", pady=8
        ).pack(fill=tk.X, pady=(40, 0))

        self._status = tk.Label(right, text="", bg="#f5f5f5", font=("Arial", 10),
                                wraplength=165, justify="left")
        self._status.pack(pady=8, anchor="w")

        self._refresh()

    def _refresh(self) -> None:
        keyword = self._search_var.get().lower()
        self._tree.delete(*self._tree.get_children())
        for p in self._store.get_product_catalog():
            if keyword and keyword not in p.get_name().lower():
                continue
            tag = "oos" if p.get_stock() == 0 else ""
            self._tree.insert("", tk.END, tags=(tag,), values=(
                p.get_id(), p.get_name(), type(p).__name__,
                f"${p.get_price():.2f}", p.get_stock(), p.get_description(),
            ))
        self._tree.tag_configure("oos", foreground="#aaaaaa")

    def _add_to_basket(self) -> None:
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a product first.")
            return
        pid     = self._tree.item(sel[0])["values"][0]
        product = next((p for p in self._store.get_product_catalog()
                        if p.get_id() == str(pid)), None)
        if not product:
            return
        try:
            self._basket.add_product(product)
            self._status.config(
                text=f"'{product.get_name()}' added to basket.", fg="#27ae60")
            self._refresh()
        except OutOfStockException as e:
            self._status.config(text=e.get_message(), fg="#e74c3c")
