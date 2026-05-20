import tkinter as tk
from tkinter import ttk, messagebox
from store_manager import StoreManager
from basket import Basket
from exceptions import OutOfStockException

BG       = "white"
CARD_BG  = "white"
HOVER_BG = "#F7F7F7"
IMG_BG   = "#F0F0F0"
FG       = "#1A1A1A"
MUTED    = "#777777"
BORDER   = "#E8E8E8"

CARD_W   = 210   # card pixel width
CARD_SLOT = 250  # slot width (card + gap)


class ProductCatalogPanel(tk.Frame):
    def __init__(self, parent, store: StoreManager, basket: Basket,
                 category: str | None, search_var: tk.StringVar):
        super().__init__(parent, bg=BG)
        self._store      = store
        self._basket     = basket
        self._category   = category
        self._search_var = search_var
        self._cards: list[tk.Frame] = []
        self._canvas     = None
        self._inner      = None
        self._win        = None
        self._build_ui()
        search_var.trace_add("write", lambda *_: self._refresh())

    def _build_ui(self) -> None:
        title = {"Apparel": "CLOTHING", "Footwear": "SHOES",
                 "Accessory": "ACCESSORIES"}.get(self._category, "ALL PRODUCTS")

        tk.Label(self, text=title, font=("Arial", 12, "bold"),
                 bg=BG, fg=FG).pack(anchor="w", padx=28, pady=(18, 4))
        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X, padx=28, pady=(0, 10))

        outer = tk.Frame(self, bg=BG)
        outer.pack(fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=self._canvas.yview)
        self._inner = tk.Frame(self._canvas, bg=BG)
        self._win   = self._canvas.create_window((0, 0), window=self._inner, anchor="nw")

        self._inner.bind("<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>", self._on_resize)
        self._canvas.configure(yscrollcommand=sb.set)

        # Mousewheel — bind only while cursor is inside the panel
        self._canvas.bind("<Enter>",
            lambda e: self._canvas.bind_all("<MouseWheel>", self._on_scroll))
        self._canvas.bind("<Leave>",
            lambda e: self._canvas.unbind_all("<MouseWheel>"))

        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._refresh()

    def _on_scroll(self, e) -> None:
        self._canvas.yview_scroll(-1 * (e.delta // 120), "units")

    def _on_resize(self, e) -> None:
        self._canvas.itemconfig(self._win, width=e.width)
        if self._cards:
            self._reflow(e.width)

    def _refresh(self) -> None:
        for w in self._inner.winfo_children():
            w.destroy()
        self._cards.clear()

        keyword  = self._search_var.get().lower()
        products = [
            p for p in self._store.get_product_catalog()
            if (self._category is None or type(p).__name__ == self._category)
            and (not keyword or keyword in p.get_name().lower())
        ]

        if not products:
            tk.Label(self._inner, text="No products found.",
                     font=("Arial", 11), bg=BG, fg=MUTED).pack(pady=40)
            return

        for p in products:
            self._cards.append(self._make_card(p))

        self._reflow(self._canvas.winfo_width() or 900)

    def _reflow(self, width: int) -> None:
        cols = max(2, (width - 30) // CARD_SLOT)
        for i, card in enumerate(self._cards):
            r, c = divmod(i, cols)
            card.grid(row=r, column=c, padx=14, pady=14, sticky="n")
        for c in range(cols):
            self._inner.columnconfigure(c, weight=1)

    def _make_card(self, product) -> tk.Frame:
        card = tk.Frame(self._inner, bg=CARD_BG, width=CARD_W, cursor="hand2")
        card.grid_propagate(False)

        # Image placeholder
        img = tk.Canvas(card, width=CARD_W, height=220,
                        bg=IMG_BG, highlightthickness=0)
        img.pack()
        img.create_text(CARD_W // 2, 110, text="[ Photo ]",
                        font=("Arial", 10), fill="#C0C0C0")

        # Info row
        info = tk.Frame(card, bg=CARD_BG, padx=10, pady=8)
        info.pack(fill=tk.X)

        tk.Label(info, text=product.get_name(), font=("Arial", 10),
                 bg=CARD_BG, fg=FG, anchor="w").pack(fill=tk.X)
        tk.Label(info, text=f"${product.get_price():.2f}", font=("Arial", 10),
                 bg=CARD_BG, fg=MUTED, anchor="w").pack(fill=tk.X)

        if product.get_stock() == 0:
            tk.Label(info, text="Out of stock", font=("Arial", 9),
                     bg=CARD_BG, fg="#CC3333", anchor="w").pack(fill=tk.X)

        # Add button
        add_btn = tk.Button(
            card, text="ADD TO CART",
            font=("Arial", 9), relief="flat", cursor="hand2",
            bg=FG, fg="white", pady=7,
            activebackground="#333333", activeforeground="white",
            command=lambda p=product: self._add(p, card)
        )
        add_btn.pack(fill=tk.X, padx=10, pady=(4, 10))

        if product.get_stock() == 0:
            add_btn.config(state=tk.DISABLED, bg="#CCCCCC")

        # Hover effect on card frame + image + info
        all_widgets = [card, img, info] + list(info.winfo_children())
        for w in all_widgets:
            w.bind("<Enter>", lambda e, ws=all_widgets, btn=add_btn:
                   [x.config(bg=HOVER_BG) for x in ws if x is not btn])
            w.bind("<Leave>", lambda e, ws=all_widgets, btn=add_btn:
                   [x.config(bg=CARD_BG) for x in ws if x is not btn])

        return card

    def _add(self, product, card: tk.Frame) -> None:
        try:
            self._basket.add_product(product)
            # brief green flash on the card
            widgets = [card] + list(card.winfo_children())
            for w in widgets:
                try:
                    w.config(bg="#E8F5E9")
                except tk.TclError:
                    pass
            card.after(500, lambda: [w.config(bg=CARD_BG)
                                     for w in widgets
                                     if isinstance(w, (tk.Frame, tk.Label))])
        except OutOfStockException as e:
            messagebox.showwarning("Out of stock", e.get_message(), parent=self)
