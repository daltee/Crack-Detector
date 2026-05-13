import cv2
import numpy as np

def preprocess_image(image):
    """
    Performs image cleaning, grayscale conversion, and thresholding.
    """
    if image is None:
        return None

    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Handle different lighting conditions
    equalized = cv2.equalizeHist(gray)

    # Step 4: Smoothing (Gaussian Blur)
    blur = cv2.GaussianBlur(equalized, (5, 5), 0)

    # Step 5: Thresholding
    threshold = cv2.adaptiveThreshold(
        blur,                   # Source image
        255,                    # Maximum value
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,                     # Block size
        2                       # Constant subtraction
    )

    # Step 6: Edge enhancement
    kernel = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])
    sharpened = cv2.filter2D(threshold, -1, kernel)

    return sharpened
