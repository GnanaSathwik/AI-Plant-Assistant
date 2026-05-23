from PIL import Image
import numpy as np


def is_leaf_image(image: Image.Image) -> bool:
    """Return True when green pixels dominate enough to treat the image as a leaf."""
    try:
        img = image.convert("RGB")
        img = img.resize((128, 128))
        arr = np.array(img)

        # Extract RGB channels.
        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]

        # Condition: green should dominate.
        green_pixels = np.sum((g > r) & (g > b))
        total_pixels = arr.shape[0] * arr.shape[1]
        green_ratio = green_pixels / total_pixels

        # Threshold can be tuned for stricter or looser validation.
        return green_ratio > 0.2
    except Exception:
        return False
