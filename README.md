# 🏗️ Crack Detector Pro: Advanced Frequency Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployment-black?logo=vercel)](https://vercel.com/)

**Crack Detector Pro** is a high-performance image processing suite designed for automated crack detection in infrastructure. By leveraging **2D Fast Fourier Transform (FFT)**, the tool separates structural defects from complex background textures, providing engineers with a powerful diagnostic tool.

---

## ✨ Key Features

- **🧠 Advanced Frequency Analysis**: Uses 2D FFT to isolate high-frequency crack signatures from low-frequency surface textures.
- **📱 Premium Web Experience**: A high-end, glassmorphism-inspired web interface that is fully responsive and optimized for mobile devices.
- **🖼️ Smart Session Queue**: Manage multiple images in a session. Upload, capture, select, and process images individually with real-time status indicators.
- **🖥️ Professional Desktop App**: A dedicated desktop application for high-resolution analysis with a modern `CustomTkinter` UI.
- **🛠️ Multi-Stage Visuals**: High-fidelity visualization of the Original Image, Frequency Spectrum, High-Pass Filter Mask, and Detected Features.
- **🚀 Cloud-Native**: Pre-configured for seamless deployment to **Vercel** with headless browser/OS support.

---

## 🔬 How It Works

1. **Preprocessing**: The image is denoised using bilateral filtering to preserve edge sharpness while removing background grain.
2. **Fourier Transform**: The spatial image is converted into the frequency domain using 2D FFT.
3. **High-Pass Filtering**: Low-frequency components (uniform surfaces, large textures) are suppressed via a Gaussian high-pass mask.
4. **Reconstruction**: The inverse FFT reconstructs the image, emphasizing the sharp structural edges and cracks.

---

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/daltee/Crack-Detector.git
cd Crack-Detector
pip install -r requirements.txt
```

### Usage
#### Desktop Application
```bash
python main_gui.py
```
#### Local Web Server
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

---

## ☁️ Vercel Deployment

This repository is optimized for Vercel.

1. Connect your GitHub repository to [Vercel](https://vercel.com).
2. The `vercel.json` and `requirements.txt` will be automatically detected.
3. Deploy! Your scanner is now live on the web with mobile camera support.

---

## 📂 Architecture

- `app.py`: Flask backend optimized for cloud/serverless.
- `main_gui.py`: Modern desktop GUI frontend.
- `fft_logic.py`: Core mathematical engine for frequency analysis.
- `preprocessing.py`: Image conditioning and noise reduction logic.
- `static/` & `templates/`: High-performance, responsive web assets.

---

<p align="center">
  Developed for Infrastructure Safety & Modern Engineering Workflows
</p>
