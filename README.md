# 🏗️ Crack Detector Pro: Advanced Frequency Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployment-black?logo=vercel)](https://vercel.app/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/daltee/Crack-Detector/graphs/commit-activity)

**Crack Detector Pro** is a professional-grade image processing suite designed for automated crack detection in infrastructure. By leveraging **2D Fast Fourier Transform (FFT)**, the tool isolates structural defects from complex background textures, providing a powerful diagnostic tool for engineers.

---

## ✨ Key Features

- **🧠 Advanced Frequency Analysis**: Uses 2D FFT to isolate high-frequency crack signatures from low-frequency surface textures.
- **📱 Premium Web Experience**: A high-end, glassmorphism-inspired web interface, fully responsive and optimized for mobile devices.
- **🖼️ Smart Session Queue**: Manage multiple images in a single session. Upload, capture, and process images individually.
- **🖥️ Desktop & Web Parity**: Both platforms utilize a 4-panel diagnostic grid for consistent analysis results.
- **🚀 Vercel Ready**: Optimized for seamless cloud deployment with `opencv-python-headless`.

---

## 🔬 Diagnostic Visuals

The system provides a 4-panel diagnostic output to help you understand the detection process:

| Stage | Description |
| :--- | :--- |
| **Original Source** | The input image after noise reduction. |
| **Frequency Spectrum** | A log-scale visualization of the 2D FFT magnitude. |
| **High-Pass Filter Mask** | The Gaussian mask used to suppress low frequencies. |
| **Detected Crack Features** | The reconstructed image highlighting structural defects. |

---

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/daltee/Crack-Detector.git
cd Crack-Detector
pip install -r requirements.txt
```

### Usage
#### 🌐 Web Application (Local)
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

#### 🖥️ Desktop Application
```bash
python main_gui.py
```

---

## ☁️ Vercel Deployment

This repository is optimized for Vercel.

1. Connect your GitHub repository to [Vercel](https://vercel.com).
2. The `vercel.json` and `requirements.txt` will be automatically detected.
3. Deploy! Your scanner is now live with mobile camera support.

---

<p align="center">
  Developed for Infrastructure Safety & Modern Engineering Workflows
</p>
