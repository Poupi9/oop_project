import tkinter as tk
from services.store_manager import StoreManager
from models.basket import Basket
from models.user import Admin
from models.exceptions import AuthenticationException

BG    = "white"
FG    = "#1A1A1A"
MUTED = "#777777"
BORDER = "#E8E8E8"


class MainWindow:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Archive-Store")
        self._root.geometry("1100x720")
        self._root.configure(bg=BG)
        self._root.minsize(900, 600)

        self._store            = StoreManager()
        self._store.load_data()
        self._current_user     = None
        self._basket           = None
        self._search_var       = tk.StringVar()
        self._current_category = None

        self._header = tk.Frame(self._root, bg=BG, height=56)
        self._header.pack(fill=tk.X)
        self._header.pack_propagate(False)

        tk.Frame(self._root, bg=BORDER, height=1).pack(fill=tk.X)

        self._content = tk.Frame(self._root, bg=BG)
        self._content.pack(fill=tk.BOTH, expand=True)

        self._show_login_panel()

    def run(self) -> None:
        self._root.mainloop()

    # ------------------------------------------------------------------ #
    # helpers                                                              #
    # ------------------------------------------------------------------ #

    def _clear(self) -> None:
        for w in self._content.winfo_children():
            w.destroy()
        for w in self._header.winfo_children():
            w.destroy()

    def _nav_label(self, parent, text, command) -> tk.Label:
        lbl = tk.Label(parent, text=text, font=("Arial", 9),
                       bg=BG, fg=MUTED, cursor="hand2")
        lbl.bind("<Button-1>", lambda e: command())
        lbl.bind("<Enter>",    lambda e: lbl.config(fg=FG))
        lbl.bind("<Leave>",    lambda e: lbl.config(fg=MUTED))
        return lbl

    def _build_customer_header(self) -> None:
        left = tk.Frame(self._header, bg=BG)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(24, 0))

        tk.Label(left, text="ARCHIVE-STORE", font=("Arial", 13, "bold"),
                 bg=BG, fg=FG).pack(side=tk.LEFT, padx=(0, 32))

        home = self._nav_label(left, "HOME", self._show_homepage)
        home.pack(side=tk.LEFT, padx=12)

        for label, cat in [("TOPS",         "Apparel"),
                            ("PANTS",        "Pants"),
                            ("SHOES",        "Footwear"),
                            ("ACCESSORIES",  "Accessory")]:
            lbl = self._nav_label(left, label,
                                  lambda c=cat: self._show_catalog_panel(c))
            lbl.pack(side=tk.LEFT, padx=12)

        right = tk.Frame(self._header, bg=BG)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 24))

        lout = self._nav_label(right, "LOGOUT", self._logout)
        lout.pack(side=tk.RIGHT, padx=(14, 0))

        count    = len(self._basket.get_items()) if self._basket else 0
        cart_lbl = tk.Label(right, text=f"CART  ({count})",
                            font=("Arial", 9, "bold"), bg=BG, fg=FG, cursor="hand2")
        cart_lbl.pack(side=tk.RIGHT, padx=14)
        cart_lbl.bind("<Button-1>", lambda e: self._show_order_panel())

        sf = tk.Frame(right, bg="#F3F3F3", padx=10)
        sf.pack(side=tk.RIGHT, padx=14)
        tk.Label(sf, text="⌕", font=("Arial", 12),
                 bg="#F3F3F3", fg=MUTED).pack(side=tk.LEFT)
        se = tk.Entry(sf, textvariable=self._search_var, width=17,
                      font=("Arial", 9), relief="flat", bg="#F3F3F3",
                      fg=FG, insertbackground=FG)
        se.pack(side=tk.LEFT, ipady=5)
        se.bind("<Return>",
                lambda e: self._show_catalog_panel(self._current_category))

    def _build_admin_header(self) -> None:
        tk.Label(self._header, text="ARCHIVE-STORE  —  ADMIN",
                 font=("Arial", 13, "bold"), bg=BG, fg=FG
                 ).pack(side=tk.LEFT, padx=24)
        lout = self._nav_label(self._header, "LOGOUT", self._logout)
        lout.pack(side=tk.RIGHT, padx=24)

    # ------------------------------------------------------------------ #
    # panel routing                                                        #
    # ------------------------------------------------------------------ #

    def _show_login_panel(self) -> None:
        self._clear()

        card = tk.Frame(self._content, bg=BG, padx=48, pady=48)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="ARCHIVE-STORE", font=("Arial", 22, "bold"),
                 bg=BG, fg=FG).pack(pady=(0, 36))

        entries = {}
        for label, key, hidden in [("Username", "name", False),
                                    ("Password", "pass", True)]:
            tk.Label(card, text=label, bg=BG,
                     font=("Arial", 9), fg=MUTED).pack(anchor="w")
            e = tk.Entry(card, width=30, font=("Arial", 11), relief="flat",
                         bg="#F5F5F5", fg=FG, insertbackground=FG)
            if hidden:
                e.config(show="*")
            e.pack(pady=(3, 14), ipady=7)
            entries[key] = e
        entries["name"].focus_set()

        err = tk.Label(card, text="", fg="#C0392B", bg=BG, font=("Arial", 10))
        err.pack()

        def attempt(_event=None):
            try:
                user = self._store.authenticate(
                    entries["name"].get().strip(), entries["pass"].get())
                self._current_user = user
                if isinstance(user, Admin):
                    self._show_admin_panel()
                else:
                    self._basket = Basket()
                    self._show_homepage()
            except AuthenticationException as e:
                err.config(text=e.get_message())

        entries["pass"].bind("<Return>", attempt)
        tk.Button(card, text="LOGIN", command=attempt,
                  bg=FG, fg="white", font=("Arial", 10, "bold"),
                  width=28, pady=9, relief="flat", cursor="hand2",
                  activebackground="#333333", activeforeground="white"
                  ).pack(pady=(10, 0))

    def _show_homepage(self) -> None:
        from gui.homepage_panel import HomepagePanel
        self._clear()
        self._build_customer_header()
        HomepagePanel(self._content).pack(fill=tk.BOTH, expand=True)

    def _show_catalog_panel(self, category: str = None) -> None:
        from gui.product_catalog_panel import ProductCatalogPanel
        self._current_category = category
        self._clear()
        self._build_customer_header()
        ProductCatalogPanel(
            self._content, self._store, self._basket,
            category, self._search_var
        ).pack(fill=tk.BOTH, expand=True)

    def _show_order_panel(self) -> None:
        from gui.order_panel import OrderPanel
        self._clear()
        self._build_customer_header()
        OrderPanel(
            self._content, self._store, self._basket,
            on_continue=lambda: self._show_catalog_panel(self._current_category)
        ).pack(fill=tk.BOTH, expand=True)

    def _show_admin_panel(self) -> None:
        from gui.admin_panel import AdminPanel
        self._clear()
        self._build_admin_header()
        AdminPanel(self._content, self._store).pack(fill=tk.BOTH, expand=True)

    def _logout(self) -> None:
        self._store.save_data()
        self._current_user     = None
        self._basket           = None
        self._current_category = None
        self._search_var.set("")
        self._show_login_panel()
