import tkinter as tk
from gui import image_loader

IMG_PATH = "images/menu.jpeg"


class HomepagePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self._label  = tk.Label(self, bg="white")
        self._label.pack(fill=tk.BOTH, expand=True)
        self._after_id = None
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, e) -> None:
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(80, lambda: self._render(e.width, e.height))

    def _render(self, w: int, h: int) -> None:
        if w < 2 or h < 2:
            return
        photo = image_loader.load_fresh(IMG_PATH, (w, h))
        if photo:
            self._label.config(image=photo)
            self._label.image = photo
        else:
            self._label.config(image="", text="[ Image ]",
                               font=("Arial", 18), fg="#BBBBBB")
