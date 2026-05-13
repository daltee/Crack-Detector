import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ======================================
# STEP 1: LOAD IMAGE
# ======================================

# Replace with your image path
img = mpimg.imread('/storage/emulated/0/fonts/images (2).jpeg')

# ======================================
# STEP 2: CONVERT TO GRAYSCALE
# ======================================

# If image is RGB
if len(img.shape) == 3:
    img = np.mean(img, axis=2)

# ======================================
# STEP 3: APPLY 2D FFT
# ======================================

f = np.fft.fft2(img)

# Shift low frequencies to center
fshift = np.fft.fftshift(f)

# ======================================
# STEP 4: CREATE MAGNITUDE SPECTRUM
# ======================================

magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)

# ======================================
# STEP 5: CREATE HIGH-PASS FILTER
# ======================================

rows, cols = img.shape
crow, ccol = rows // 2, cols // 2

# Create mask
mask = np.ones((rows, cols), np.uint8)

# Radius of low-frequency block
r = 30

x, y = np.ogrid[:rows, :cols]

mask_area = (x - crow)**2 + (y - ccol)**2 <= r*r

# Remove low frequencies
mask[mask_area] = 0

# ======================================
# STEP 6: APPLY FILTER
# ======================================

fshift_filtered = fshift * mask

# ======================================
# STEP 7: INVERSE FFT
# ======================================

f_ishift = np.fft.ifftshift(fshift_filtered)

img_back = np.fft.ifft2(f_ishift)

img_back = np.abs(img_back)

# ======================================
# STEP 8: DISPLAY RESULTS
# ======================================

plt.figure(figsize=(12,8))

# Original image
plt.subplot(2,2,1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')

# Frequency spectrum
plt.subplot(2,2,2)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Frequency Spectrum')
plt.axis('off')

# High-pass filter
plt.subplot(2,2,3)
plt.imshow(mask, cmap='gray')
plt.title('High-Pass Filter')
plt.axis('off')

# Filtered image
plt.subplot(2,2,4)
plt.imshow(img_back, cmap='gray')
plt.title('Detected Crack Features')
plt.axis('off')

plt.tight_layout()
plt.show()