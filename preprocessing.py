import cv2
import numpy as np

def preprocess_image(image):
    """
    Handles image cleaning, grayscale conversion, and thresholding.
    Optimized for real-time infrastructure analysis.
    """
    if image is None:
        return None

    # Step 2: Convert to grayscale (Essential for mathematical analysis)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Histogram Equalization (Improves contrast for better crack visibility)
    equalized = cv2.equalizeHist(gray)

    # Step 4: Gaussian Smoothing (Reduces high-frequency noise/texture)
    blur = cv2.GaussianBlur(equalized, (5, 5), 0)

    # Step 5: Adaptive Thresholding (Robust against varying lighting conditions)
    threshold = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # Step 6: Edge Enhancement (Sharpening kernel to emphasize structural defects)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(threshold, -1, kernel)

    return sharpened
