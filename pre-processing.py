# =========================================================
# PRE-PROCESSING FOR CRACK DETECTION
# =========================================================
# This code performs:
# 1. Image loading
# 2. Grayscale conversion
# 3. Lighting correction
# 4. Gaussian smoothing
# 5. Thresholding
# 6. Edge enhancement
#
# Goal:
# Prepare the image so FFT or crack detection
# algorithms can work better.
#
# =========================================================

# ---------------- IMPORT LIBRARIES ----------------
import cv2
import numpy as np


# =========================================================
# STEP 1: LOAD IMAGE
# =========================================================
# Replace with your image path

image = cv2.imread("/storage/emulated/0/Download/crack.jpg")

# Check if image loaded successfully
if image is None:
    print("Image not found.")
    exit()

# Keep original image
original = image.copy()


# =========================================================
# STEP 2: CONVERT TO GRAYSCALE
# =========================================================
# Simplifies the image by removing colors

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# =========================================================
# STEP 3: HANDLE DIFFERENT LIGHTING CONDITIONS
# =========================================================
# Histogram Equalization improves contrast
# and makes cracks visible even in dark/bright images

equalized = cv2.equalizeHist(gray)


# =========================================================
# STEP 4: SMOOTHING (GAUSSIAN BLUR)
# =========================================================
# Removes noise while preserving major structures

blur = cv2.GaussianBlur(equalized, (5, 5), 0)


# =========================================================
# STEP 5: THRESHOLDING
# =========================================================
# Adaptive threshold works better under
# different lighting conditions

threshold = cv2.adaptiveThreshold(
    blur,                   # Source image
    255,                    # Maximum value
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    11,                     # Block size
    2                       # Constant subtraction
)


# =========================================================
# STEP 6: EDGE ENHANCEMENT
# =========================================================
# Sharpen image to make cracks more visible

kernel = np.array([
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1]
])

sharpened = cv2.filter2D(threshold, -1, kernel)


# =========================================================
# STEP 7: OPTIONAL EDGE DETECTION
# =========================================================
# Makes cracks even more obvious

edges = cv2.Canny(sharpened, 50, 150)


# =========================================================
# STEP 8: SAVE RESULTS
# =========================================================
# Saves processed images to phone storage

cv2.imwrite("/storage/emulated/0/Download/gray.jpg", gray)

cv2.imwrite("/storage/emulated/0/Download/equalized.jpg", equalized)

cv2.imwrite("/storage/emulated/0/Download/blur.jpg", blur)

cv2.imwrite("/storage/emulated/0/Download/threshold.jpg", threshold)

cv2.imwrite("/storage/emulated/0/Download/sharpened.jpg", sharpened)

cv2.imwrite("/storage/emulated/0/Download/edges.jpg", edges)


# =========================================================
# FINISHED
# =========================================================

print("Pre-processing completed successfully.")

print("Processed images saved in Download folder.")