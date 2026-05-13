# Crack Detector

THE Crack Detector leverages 2D Fast Fourier Transform (FFT) for automated crack detection. It converts images into frequency spectra, where high-pass filters are applied to extract fine structural edges. This mathematical approach successfully isolates structural defects from background noise, enabling rapid, autonomous monitoring of critical civil infrastructure.

## Features

- **2D FFT Core Logic**: Math-driven approach to cleanly separate defects from background textures and noise.
- **Modern GUI**: Built with `CustomTkinter` for a professional, sleek desktop interface.
- **Real-Time Camera Integration**: Capture photos of walls or roads directly from your PC or mobile hardware (via tools like DroidCam).
- **Theme & Appearance Customization**: Native Light/Dark mode toggling and Accent Color (Green/Cyan) choices that do not interrupt workflow.
- **Performance Optimized**: Heavy mathematical tasks are processed on background threads to prevent UI freezing.

## Tech Stack

- **Python 3.x**
- **OpenCV (`cv2`)**: For hardware camera access and image array management.
- **NumPy**: For efficient matrix calculations during FFT.
- **CustomTkinter / Tkinter**: For the modern desktop GUI framework.
- **Pillow (PIL)**: For responsive, high-quality image resampling in the interface.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/daltee/Crack-Detector.git
   cd Crack-Detector
   ```

2. **Install the required dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```
   *If you do not have a `requirements.txt`, you can install the packages directly:*
   ```bash
   pip install customtkinter opencv-python Pillow numpy
   ```

## Usage

1. **Start the Application:**
   ```bash
   python main_gui.py
   ```

2. **Upload or Capture:**
   - Click **"Upload Image"** to browse your local device for an existing photo of infrastructure.
   - Click **"Start Camera Feed"** to open your webcam or connected camera. Align the camera with the surface, then click **"Capture & Process"**.

3. **View Results:**
   The interface will display a side-by-side comparison of your original image and the processed FFT output showing detected cracks.

## Project Structure

- `main_gui.py`: The entry point for the desktop application containing the CustomTkinter UI.
- `preprocessing.py`: Handles the initial image cleaning, grayscale conversion, and thresholding.
- `fft_logic.py`: Contains the core mathematical logic for the 2D FFT conversion and high-pass filtering.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

## License

This project is open-source and available under the [MIT License](LICENSE).
