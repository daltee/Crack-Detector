import cv2
import numpy as np


def _normalize_uint8(image):
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def apply_fft_filter(img, r=28):
    """
    Run FFT high-pass analysis and produce presentation-friendly crack output.

    Returns: grayscale input, frequency spectrum, high-pass mask visualization,
    color crack overlay, and metrics. The core remains a Gaussian high-pass FFT,
    with lightweight spatial cleanup added after reconstruction to make detected
    crack-like features easier to read.
    """
    if img is None:
        return None, None, None, None, {}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img.copy()
    gray_float = gray.astype(np.float32)

    # Windowing reduces border ringing in phone photos with hard image edges.
    rows, cols = gray.shape
    window = np.outer(np.hanning(rows), np.hanning(cols)).astype(np.float32)
    windowed = gray_float * window

    fshift = np.fft.fftshift(np.fft.fft2(windowed))

    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    magnitude_spectrum = _normalize_uint8(magnitude_spectrum)
    spectrum_color = cv2.applyColorMap(magnitude_spectrum, cv2.COLORMAP_VIRIDIS)

    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    d2 = (y - crow) ** 2 + (x - ccol) ** 2
    mask = 1 - np.exp(-d2 / (2 * (r ** 2)))
    mask_vis = cv2.applyColorMap((mask * 255).astype(np.uint8), cv2.COLORMAP_TURBO)

    filtered = np.fft.ifft2(np.fft.ifftshift(fshift * mask))
    high_pass = _normalize_uint8(np.abs(filtered))

    # Combine frequency response with a black-hat transform for dark fissures.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dark_ridges = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    fused = cv2.addWeighted(high_pass, 0.68, dark_ridges, 0.32, 0)
    fused = cv2.GaussianBlur(fused, (3, 3), 0)

    _, binary = cv2.threshold(fused, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8), iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=1)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, 8)
    cleaned = np.zeros_like(binary)
    min_area = max(8, int(rows * cols * 0.000035))
    max_area = int(rows * cols * 0.08)
    crack_count = 0
    largest_area = 0

    for label in range(1, num_labels):
        area = int(stats[label, cv2.CC_STAT_AREA])
        width = int(stats[label, cv2.CC_STAT_WIDTH])
        height = int(stats[label, cv2.CC_STAT_HEIGHT])
        elongated = max(width, height) / max(1, min(width, height)) >= 1.8
        if min_area <= area <= max_area and (elongated or area < 80):
            cleaned[labels == label] = 255
            crack_count += 1
            largest_area = max(largest_area, area)

    base = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    overlay = base.copy()
    overlay[cleaned > 0] = (35, 35, 255)  # red in BGR for crack candidates
    result = cv2.addWeighted(base, 0.55, overlay, 0.45, 0)

    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(result, contours, -1, (0, 255, 255), 1, cv2.LINE_AA)

    crack_pixels = int(np.count_nonzero(cleaned))
    metrics = {
        "crack_pixels": crack_pixels,
        "coverage_percent": round((crack_pixels / float(rows * cols)) * 100, 3),
        "feature_count": crack_count,
        "largest_feature_pixels": largest_area,
        "processed_size": f"{cols}×{rows}",
    }

    return gray, spectrum_color, mask_vis, result, metrics
