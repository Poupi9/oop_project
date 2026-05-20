import os
from PIL import Image, ImageTk

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_cache: dict[tuple, ImageTk.PhotoImage] = {}


def load(relative_path: str, size: tuple[int, int]) -> ImageTk.PhotoImage | None:
    """Load and resize an image, returning a cached PhotoImage or None on failure."""
    key = (relative_path, size)
    if key in _cache:
        return _cache[key]
    abs_path = os.path.join(PROJECT_ROOT, relative_path)
    if not os.path.exists(abs_path):
        return None
    try:
        img   = Image.open(abs_path).convert("RGB")
        img   = _cover(img, size)
        photo = ImageTk.PhotoImage(img)
        _cache[key] = photo
        return photo
    except Exception:
        return None


def load_fresh(relative_path: str, size: tuple[int, int]) -> ImageTk.PhotoImage | None:
    """Same as load() but always reloads (used for responsive homepage resize)."""
    abs_path = os.path.join(PROJECT_ROOT, relative_path)
    if not os.path.exists(abs_path):
        return None
    try:
        img   = Image.open(abs_path).convert("RGB")
        img   = _cover(img, size)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


def _cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize + crop to fill the target size (CSS object-fit: cover)."""
    tw, th = size
    iw, ih = img.size
    scale  = max(tw / iw, th / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img    = img.resize((nw, nh), Image.LANCZOS)
    left   = (nw - tw) // 2
    top    = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))
