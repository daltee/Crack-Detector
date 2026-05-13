import numpy as np
import cv2

def apply_fft_filter(img, r=30):
    """
    Handles the 2D Fast Fourier Transform and high-pass filtering.
    Isolates high-frequency structural features (cracks).
    """
    if img is None:
        return None

    # Ensure single channel grayscale input
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 1: 2D FFT & Shift
    # Using np.fft for mathematical clarity as per core requirements
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # Step 2: High-Pass Mask Generation
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2

    mask = np.ones((rows, cols), np.uint8)
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - crow)**2 + (y - ccol)**2 <= r*r
    mask[mask_area] = 0

    # Step 3: Apply Mask & Inverse Shift
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)

    # Step 4: Inverse FFT to reconstruct filtered image
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    # Step 5: Normalization for visual output (0-255)
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX)

    return img_back.astype(np.uint8)
