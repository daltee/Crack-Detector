import cv2
import numpy as np

def preprocess_image(image, max_size=1024):
    """
    Enhanced preprocessing for crack detection.
    Balances noise reduction with edge preservation and performance.
    """
    if image is None:
        return None

    # Step 1: Resize for performance (Capped at 1024px to ensure <5s processing)
    h, w = image.shape[:2]
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        new_size = (int(w * scale), int(h * scale))
        image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

    # Step 2: Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Step 3: Bilateral Filter (Reduces noise while keeping edges sharp - crucial for patterns)
    # Using larger d=9 for better pattern suppression
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    # Step 4: Adaptive Thresholding (Sensitive to local lighting changes)
    threshold = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        15, 4
    )

    # Step 5: Morphological Cleaning (Removes small islands and noise)
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

    return cleaned
