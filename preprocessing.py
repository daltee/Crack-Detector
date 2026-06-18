import cv2
import numpy as np


def preprocess_image(image, max_size=960):
    """
    Prepare a field photo for FFT-based crack detection.

    The output stays grayscale rather than binary so the Fourier transform can
    still see fine surface texture, shadows, and crack edges. Work is capped to
    keep browser uploads and classroom demos responsive.
    """
    if image is None:
        return None

    h, w = image.shape[:2]
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        image = cv2.resize(
            image,
            (max(1, int(w * scale)), max(1, int(h * scale))),
            interpolation=cv2.INTER_AREA,
        )

    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # CLAHE evens out phone-photo lighting without flattening hairline cracks.
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Median blur is fast and removes isolated sensor/grain noise while keeping
    # thin dark crack lines crisper than a large Gaussian blur would.
    denoised = cv2.medianBlur(enhanced, 3)

    return denoised
