import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from services.store_manager import StoreManager
from models.product import Apparel, Accessory, Footwear


class AdminPanel(tk.Frame):
    def __init__(self, parent, store: StoreManager):
        super().__init__(parent, bg="#f5f5f5")
        self._store = store
        self._build_ui()

    def _build_ui(self) -> None:
        tk.Label(self, text="Admin Panel", font=("Arial", 15, "bold"),
                 bg="#f5f5f5", fg="#2c3e50").pack(anchor="w", padx=16, pady=(12, 8))

        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 12))

        prod_tab = tk.Frame(nb, bg="#f5f5f5")
        logs_tab = tk.Frame(nb, bg="#f5f5f5")
        nb.add(prod_tab, text="Products")
        nb.add(logs_tab, text="Logs")

        self._build_products_tab(prod_tab)
        self._build_logs_tab(logs_tab)

    # ------------------------------------------------------------------ #
    # Products tab                                                         #
    # ------------------------------------------------------------------ #

    def _build_products_tab(self, parent: tk.Frame) -> None:
        cols = ("ID", "Name", "Type", "Price", "Stock", "Details")
        self._prod_tree = ttk.Treeview(parent, columns=cols, show="headings", height=18)
        widths = {"ID": 70, "Name": 160, "Type": 100,
                  "Price": 80, "Stock": 65, "Details": 260}
        for col in cols:
            self._prod_tree.heading(col, text=col)
            self._prod_tree.column(col, width=widths[col], anchor="w")

        sb = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self._prod_tree.yview)
        self._prod_tree.configure(yscrollcommand=sb.set)
        self._prod_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)
        sb.pack(side=tk.LEFT, fill=tk.Y, pady=8)

        btn_frame = tk.Frame(parent, bg="#f5f5f5", width=185)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=12, pady=8)
        btn_frame.pack_propagate(False)

        for text, cmd, color in [
            ("Add Product",    self._add_product,    "#27ae60"),
            ("Update Product", self._update_product, "#2980b9"),
            ("Remove Product", self._remove_product, "#e74c3c"),
        ]:
            tk.Button(btn_frame, text=text, command=cmd, bg=color, fg="white",
                      relief="flat", font=("Arial", 10), cursor="hand2", pady=7
                      ).pack(fill=tk.X, pady=4)

        self._prod_status = tk.Label(btn_frame, text="", bg="#f5f5f5",
                                     font=("Arial", 10), wraplength=170, justify="left")
        self._prod_status.pack(pady=8, anchor="w")

        self._refresh_products()

    def _refresh_products(self) -> None:
        self._prod_tree.delete(*self._prod_tree.get_children())
        for p in self._store.get_product_catalog():
            self._prod_tree.insert("", tk.END, values=(
                p.get_id(), p.get_name(), type(p).__name__,
                f"${p.get_price():.2f}", p.get_stock(), p.get_description(),
            ))

    def _add_product(self) -> None:
        dialog = _AddProductDialog(self)
        self.wait_window(dialog)
        if not dialog.result:
            return
        p_type, pid, name, price, stock, extra = dialog.result
        if p_type == "Apparel":
            product = Apparel(pid, name, price, stock, extra)
        elif p_type == "Footwear":
            product = Footwear(pid, name, price, stock, float(extra))
        else:
            product = Accessory(pid, name, price, stock)
        self._store.add_to_catalog(product)
        self._store.save_data()
        self._refresh_products()
        self._prod_status.config(text=f"'{name}' added.", fg="#27ae60")

    def _update_product(self) -> None:
        sel = self._prod_tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a product to update.")
            return
        pid     = str(self._prod_tree.item(sel[0])["values"][0])
        product = next((p for p in self._store.get_product_catalog()
                        if p.get_id() == pid), None)
        if not product:
            return
        new_name  = simpledialog.askstring(
            "Update", "Name:", initialvalue=product.get_name(), parent=self)
        new_price = simpledialog.askfloat(
            "Update", "Price:", initialvalue=product.get_price(), parent=self)
        new_stock = simpledialog.askinteger(
            "Update", "Stock:", initialvalue=product.get_stock(), parent=self)
        if new_name  is not None: product.set_name(new_name)
        if new_price is not None: product.set_price(new_price)
        if new_stock is not None: product.set_stock(new_stock)
        self._store.save_data()
        self._refresh_products()
        self._prod_status.config(text="Product updated.", fg="#2980b9")

    def _remove_product(self) -> None:
        sel = self._prod_tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a product to remove.")
            return
        pid  = str(self._prod_tree.item(sel[0])["values"][0])
        name = self._prod_tree.item(sel[0])["values"][1]
        if not messagebox.askyesno("Confirm", f"Remove '{name}'?"):
            return
        product = next((p for p in self._store.get_product_catalog()
                        if p.get_id() == pid), None)
        if product:
            self._store.remove_from_catalog(product)
            self._store.save_data()
            self._refresh_products()
            self._prod_status.config(text=f"'{name}' removed.", fg="#e74c3c")

    # ------------------------------------------------------------------ #
    # Logs tab                                                             #
    # ------------------------------------------------------------------ #

    def _build_logs_tab(self, parent: tk.Frame) -> None:
        bar = tk.Frame(parent, bg="#f5f5f5")
        bar.pack(fill=tk.X, padx=8, pady=8)
        tk.Button(bar, text="Refresh", command=self._refresh_logs,
                  bg="#2980b9", fg="white", relief="flat",
                  font=("Arial", 10), cursor="hand2", padx=12).pack(side=tk.LEFT)
        tk.Button(bar, text="Clear Logs", command=self._clear_logs,
                  bg="#e74c3c", fg="white", relief="flat",
                  font=("Arial", 10), cursor="hand2", padx=12).pack(side=tk.LEFT, padx=8)

        text_frame = tk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self._log_text = tk.Text(text_frame, font=("Courier", 10),
                                 state=tk.DISABLED, bg="#1e1e1e", fg="#d4d4d4",
                                 relief="flat", wrap=tk.NONE)
        ysb = ttk.Scrollbar(text_frame, orient=tk.VERTICAL,   command=self._log_text.yview)
        xsb = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self._log_text.xview)
        self._log_text.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self._log_text.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")
        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

        self._refresh_logs()

    def _refresh_logs(self) -> None:
        logs = self._store.get_logger().load_logs()
        self._log_text.config(state=tk.NORMAL)
        self._log_text.delete("1.0", tk.END)
        self._log_text.insert(tk.END, "".join(logs) if logs else "No logs yet.")
        self._log_text.config(state=tk.DISABLED)
        self._log_text.see(tk.END)

    def _clear_logs(self) -> None:
        if messagebox.askyesno("Confirm", "Clear all logs?"):
            self._store.get_logger().clear_logs()
            self._refresh_logs()


class _AddProductDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Product")
        self.resizable(False, False)
        self.grab_set()
        self.result = None
        self._build()
        self.geometry("+%d+%d" % (
            parent.winfo_rootx() + 120,
            parent.winfo_rooty() + 120,
        ))

    def _build(self) -> None:
        pad = {"padx": 14, "pady": 5}
        tk.Label(self, text="Type:").grid(row=0, column=0, sticky="w", **pad)
        self._type_var = tk.StringVar(value="Apparel")
        cb = ttk.Combobox(self, textvariable=self._type_var, state="readonly",
                          values=["Apparel", "Accessory", "Footwear"], width=20)
        cb.grid(row=0, column=1, **pad)
        cb.bind("<<ComboboxSelected>>", self._on_type_change)

        self._entries: dict[str, tk.Entry] = {}
        for i, (lbl, key) in enumerate(
                [("ID:", "id"), ("Name:", "name"), ("Price:", "price"), ("Stock:", "stock")],
                start=1):
            tk.Label(self, text=lbl).grid(row=i, column=0, sticky="w", **pad)
            e = tk.Entry(self, width=22)
            e.grid(row=i, column=1, **pad)
            self._entries[key] = e

        self._extra_lbl   = tk.Label(self, text="Size:")
        self._extra_entry = tk.Entry(self, width=22)
        self._extra_lbl.grid(row=5, column=0, sticky="w", **pad)
        self._extra_entry.grid(row=5, column=1, **pad)

        tk.Button(self, text="Add", command=self._confirm,
                  bg="#27ae60", fg="white", relief="flat",
                  width=12, pady=6).grid(row=6, column=0, columnspan=2, pady=14)

    def _on_type_change(self, _=None) -> None:
        t = self._type_var.get()
        if t in ("Apparel", "Footwear"):
            self._extra_lbl.config(text="Size:" if t == "Apparel" else "Shoe size:")
            self._extra_lbl.grid()
            self._extra_entry.grid()
        else:
            self._extra_lbl.grid_remove()
            self._extra_entry.grid_remove()

    def _confirm(self) -> None:
        try:
            p_type = self._type_var.get()
            pid    = self._entries["id"].get().strip()
            name   = self._entries["name"].get().strip()
            price  = float(self._entries["price"].get())
            stock  = int(self._entries["stock"].get())
            extra  = self._extra_entry.get().strip() if p_type in ("Apparel", "Footwear") else None
            if not pid or not name:
                raise ValueError("ID and Name are required.")
            self.result = (p_type, pid, name, price, stock, extra)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e), parent=self)
