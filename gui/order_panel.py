import tkinter as tk
from tkinter import ttk
from services.store_manager import StoreManager
from models.basket import Basket
from models.exceptions import InvalidOrderException, OutOfStockException

BG     = "white"
FG     = "#1A1A1A"
MUTED  = "#777777"
BORDER = "#E8E8E8"
IMG_BG = "#F0F0F0"


class OrderPanel(tk.Frame):
    def __init__(self, parent, store: StoreManager, basket: Basket,
                 on_continue=None):
        super().__init__(parent, bg=BG)
        self._store       = store
        self._basket      = basket
        self._on_continue = on_continue
        self._orders      = []
        self._build_ui()

    def _build_ui(self) -> None:
        body = tk.Frame(self, bg=BG)
        body.pack(fill=tk.BOTH, expand=True, padx=48, pady=28)

        # LEFT: items list
        left = tk.Frame(body, bg=BG)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 40))

        tk.Label(left, text="YOUR CART", font=("Arial", 12, "bold"),
                 bg=BG, fg=FG).pack(anchor="w", pady=(0, 14))
        tk.Frame(left, bg=BORDER, height=1).pack(fill=tk.X, pady=(0, 10))

        self._items_frame = tk.Frame(left, bg=BG)
        self._items_frame.pack(fill=tk.BOTH, expand=True)

        cont = tk.Label(left, text="← Continue Shopping",
                        font=("Arial", 9), bg=BG, fg=MUTED, cursor="hand2")
        cont.pack(anchor="w", pady=(18, 0))
        cont.bind("<Button-1>",
                  lambda e: self._on_continue() if self._on_continue else None)
        cont.bind("<Enter>", lambda e: cont.config(fg=FG))
        cont.bind("<Leave>", lambda e: cont.config(fg=MUTED))

        # RIGHT: order summary
        right = tk.Frame(body, bg=BG, width=270)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)

        tk.Label(right, text="ORDER SUMMARY",
                 font=("Arial", 10, "bold"), bg=BG, fg=FG).pack(anchor="w", pady=(0, 14))
        tk.Frame(right, bg=BORDER, height=1).pack(fill=tk.X, pady=(0, 18))

        self._total_lbl = tk.Label(right, text="Total:  $0.00",
                                   font=("Arial", 14, "bold"), bg=BG, fg=FG)
        self._total_lbl.pack(anchor="e", pady=(0, 24))

        tk.Button(right, text="CHECKOUT", command=self._checkout,
                  bg=FG, fg="white", font=("Arial", 10, "bold"),
                  relief="flat", cursor="hand2", pady=12,
                  activebackground="#333333", activeforeground="white"
                  ).pack(fill=tk.X)

        self._msg_lbl = tk.Label(right, text="", bg=BG, font=("Arial", 9),
                                 fg="#27ae60", wraplength=260, justify="left")
        self._msg_lbl.pack(pady=10, anchor="w")

        # Order history
        hist = tk.Frame(self, bg=BG)
        hist.pack(fill=tk.X, padx=48, pady=(0, 28))

        tk.Label(hist, text="ORDER HISTORY", font=("Arial", 10, "bold"),
                 bg=BG, fg=FG).pack(anchor="w", pady=(0, 10))
        tk.Frame(hist, bg=BORDER, height=1).pack(fill=tk.X, pady=(0, 8))

        cols = ("Order ID", "Total", "Status", "Items")
        self._hist = ttk.Treeview(hist, columns=cols, show="headings", height=4)
        for col, w in zip(cols, [100, 90, 100, 520]):
            self._hist.heading(col, text=col)
            self._hist.column(col, width=w, anchor="w")
        self._hist.pack(fill=tk.X)

        self._refresh_items()

    def _refresh_items(self) -> None:
        for w in self._items_frame.winfo_children():
            w.destroy()

        items = self._basket.get_items()
        if not items:
            tk.Label(self._items_frame, text="Your cart is empty.",
                     font=("Arial", 10), bg=BG, fg="#AAAAAA").pack(anchor="w", pady=12)
        else:
            for item in items:
                self._make_row(item)

        self._total_lbl.config(text=f"Total:  ${self._basket.calculate_total():.2f}")

    def _make_row(self, product) -> None:
        row = tk.Frame(self._items_frame, bg=BG)
        row.pack(fill=tk.X, pady=8)

        img = tk.Canvas(row, width=76, height=76,
                        bg=IMG_BG, highlightthickness=0)
        img.pack(side=tk.LEFT, padx=(0, 18))
        img.create_text(38, 38, text="[ ]", font=("Arial", 9), fill="#C0C0C0")

        info = tk.Frame(row, bg=BG)
        info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(info, text=product.get_name(), font=("Arial", 10),
                 bg=BG, fg=FG, anchor="w").pack(fill=tk.X)
        tk.Label(info, text=f"${product.get_price():.2f}", font=("Arial", 10),
                 bg=BG, fg=MUTED, anchor="w").pack(fill=tk.X)
        tk.Label(info, text="Qty: 1", font=("Arial", 9),
                 bg=BG, fg="#BBBBBB", anchor="w").pack(fill=tk.X)

        rm = tk.Label(row, text="✕", font=("Arial", 13),
                      bg=BG, fg="#CCCCCC", cursor="hand2")
        rm.pack(side=tk.RIGHT, padx=(12, 0))
        rm.bind("<Enter>",    lambda e: rm.config(fg="#CC3333"))
        rm.bind("<Leave>",    lambda e: rm.config(fg="#CCCCCC"))
        rm.bind("<Button-1>", lambda e, p=product: self._remove(p))

        tk.Frame(self._items_frame, bg=BORDER, height=1).pack(fill=tk.X)

    def _remove(self, product) -> None:
        self._basket.remove_product(product)
        self._refresh_items()

    def _checkout(self) -> None:
        try:
            order = self._basket.checkout()
            self._store.process_order(order)
            self._store.save_data()
            self._orders.append(order)
            self._refresh_items()
            self._refresh_history()
            self._msg_lbl.config(
                text=f"✓  Order confirmed\n"
                     f"    ID: {order.get_order_id()}\n"
                     f"    Total: ${order.get_total_amount():.2f}",
                fg="#27ae60")
        except (InvalidOrderException, OutOfStockException) as e:
            self._msg_lbl.config(text=e.get_message(), fg="#C0392B")

    def _refresh_history(self) -> None:
        self._hist.delete(*self._hist.get_children())
        for order in reversed(self._orders):
            items_str = ", ".join(p.get_name() for p in order.get_items())
            self._hist.insert("", tk.END, values=(
                order.get_order_id(),
                f"${order.get_total_amount():.2f}",
                order.get_status(),
                items_str,
            ))
