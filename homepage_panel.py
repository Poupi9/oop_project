import tkinter as tk


class HomepagePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self._build()

    def _build(self) -> None:
        # Full-bleed placeholder — replace canvas with tk.Label(image=...) later
        placeholder = tk.Canvas(self, bg="#F0F0F0", highlightthickness=0)
        placeholder.pack(fill=tk.BOTH, expand=True)

        # Centered label inside canvas (repositions on resize)
        text_id = placeholder.create_text(
            0, 0,
            text="[ Image ]",
            font=("Arial", 18),
            fill="#BBBBBB",
            anchor="center",
        )

        def _reposition(e):
            placeholder.coords(text_id, e.width // 2, e.height // 2)

        placeholder.bind("<Configure>", _reposition)
