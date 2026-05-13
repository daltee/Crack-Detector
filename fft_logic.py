import numpy as np
import cv2

def apply_fft_filter(img, r=30):
    """
    Applies 2D FFT and a high-pass filter to extract crack features.
    """
    if img is None:
        return None

    # Ensure image is grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply 2D FFT
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # Step 5: Create High-Pass Filter
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2

    # Create mask
    mask = np.ones((rows, cols), np.uint8)
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - crow)**2 + (y - ccol)**2 <= r*r
    mask[mask_area] = 0

    # Step 6: Apply Filter
    fshift_filtered = fshift * mask

    # Step 7: Inverse FFT
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    # Normalize result to 0-255 range
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX)
    return img_back.astype(np.uint8)
