import numpy as np
import cv2

def apply_fft_filter(img, r=30):
    """
    Handles the 2D Fast Fourier Transform and high-pass filtering.
    Utilizes a Gaussian High-Pass Filter for better edge preservation
    and noise suppression on patterned surfaces.
    """
    if img is None:
        return None, None, None, None

    # Ensure single channel grayscale input
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # Step 1: 2D FFT & Shift
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    # Step 2: Spectrum for visualization (Log scale)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Step 3: Gaussian High-Pass Filter Generation
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2

    # Create Gaussian High-Pass Mask
    # H(u,v) = 1 - exp(-D^2 / (2 * D0^2))
    x, y = np.ogrid[:rows, :cols]
    d2 = (x - crow)**2 + (y - ccol)**2
    mask = 1 - np.exp(-d2 / (2 * (r**2)))

    # Visualization of mask (normalized)
    mask_vis = (mask * 255).astype(np.uint8)

    # Step 4: Apply Mask & Inverse Shift
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)

    # Step 5: Inverse FFT to reconstruct filtered image
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    # Step 6: Normalization and Contrast Enhancement
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Final sharpening and cleanup for the result frame
    _, result = cv2.threshold(img_back, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return gray, magnitude_spectrum, mask_vis, result
