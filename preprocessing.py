import cv2
import numpy as np

def preprocess_image(image):
    """
    Refined preprocessing for crack detection.
    Balances noise reduction with edge preservation.
    """
    if image is None:
        return None

    # Step 1: Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Step 2: Bilateral Filter (Reduces noise while keeping edges sharp)
    # Better than Gaussian blur for structural defects like cracks
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    # Step 3: Adaptive Thresholding
    # Converts to binary to emphasize structural patterns
    threshold = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # Step 4: Morphological Cleaning
    # Removes small speckles (salt and pepper noise)
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

    return cleaned
