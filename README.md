# 🏗️ Crack Detector Pro: 2D FFT Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployment-black?logo=vercel)](https://vercel.com/)

**Crack Detector Pro** is a high-performance image processing suite designed for automated crack detection in infrastructure. By leveraging **2D Fast Fourier Transform (FFT)**, the tool separates structural defects from complex background textures, providing engineers with a powerful diagnostic tool.

---

## ✨ Key Features

- **🧠 Advanced Frequency Analysis**: Uses 2D FFT to isolate high-frequency crack signatures from low-frequency surface textures.
- **📱 Multi-Image Web App**: A mobile-responsive web interface that supports bulk uploads, camera captures, and a processing queue.
- **🖼️ Diagnostic Gallery**: Manage multiple images in a session. Discard individual photos or clear the entire queue with one click.
- **🖥️ Desktop Power**: A dedicated desktop application for high-resolution analysis with a modern `CustomTkinter` UI.
- **🛠️ Multi-Stage Visuals**: Visualizes the original image, frequency spectrum, high-pass filter mask, and final detected features.
- **🚀 One-Click Cloud Deployment**: Pre-configured for seamless deployment to **Vercel**.

---

## 🔬 How It Works

1. **Preprocessing**: The image is denoised using bilateral filtering to preserve edge sharpness.
2. **Fourier Transform**: The spatial image is converted into the frequency domain.
3. **High-Pass Filtering**: Low-frequency components (smooth surfaces, uniform textures) are suppressed.
4. **Reconstruction**: The inverse FFT reconstructs the image, leaving only the sharp structural edges (cracks).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenCV & NumPy

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

This repository is optimized for Vercel's serverless environment.

1. Connect your GitHub repository to [Vercel](https://vercel.com).
2. The `vercel.json` and `requirements.txt` will be automatically detected.
3. Deploy! Your scanner is now live on the web.

---

## 📂 Architecture

- `app.py`: Flask backend for the web application.
- `main_gui.py`: Modern desktop GUI frontend.
- `fft_logic.py`: Core mathematical engine for frequency analysis.
- `preprocessing.py`: Image conditioning and noise reduction.
- `static/` & `templates/`: Professional web frontend assets.

---

<p align="center">
  Developed for Infrastructure Safety & Modern Engineering Workflows
</p>
