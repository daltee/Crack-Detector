# 🏗️ Crack Detector Pro: Advanced Surface Analysis Suite

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Live_App-black?logo=vercel&style=for-the-badge)](https://vercel.app/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?logo=python&style=for-the-badge)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Crack Detector Pro** is a high-performance diagnostic toolkit designed for automated crack detection in diverse structural environments. By leveraging **2D Fast Fourier Transform (FFT)** and advanced morphological processing, the application effectively isolates structural defects even on highly textured or patterned surfaces like tiles, concrete, and terrazzo.

---

## ✨ Key Features

- **🧠 Intelligent Detection Engine**: Combines Bilateral filtering with Gaussian High-Pass FFT for superior noise suppression and edge preservation.
- **📱 Responsive Web Dashboard**: Optimized for mobile and desktop viewports, featuring a premium glassmorphism UI.
- **📸 5-Panel Diagnostic Grid**: Real-time camera feed integrated alongside four stages of frequency and spatial analysis.
- **🖼️ Session Queue Management**: Capture multiple photos in a single session, process them individually, and discard results as needed.
- **🎨 Visual Personalization**: Native support for Dark/Light modes and customizable accent colors (Green/Cyan).
- **🚀 Cloud Ready**: Pre-configured for immediate deployment on Vercel with headless OpenCV support.

---

## 🔬 How It Works

The detection pipeline utilizes a multi-stage frequency domain filter:

| Stage | Process | Objective |
| :--- | :--- | :--- |
| **1. Live Feed** | MediaStream API | Real-time positioning and capture for on-site inspection. |
| **2. Preprocessing** | Bilateral Filter | Suppresses texture noise while maintaining sharp edge gradients. |
| **3. FFT Spectrum** | 2D Fast Fourier | Visualizes image components in the frequency domain. |
| **4. Gaussian Mask** | High-Pass Filter | Blocks low-frequency surface patterns while isolating high-frequency cracks. |
| **5. Final Result** | Inverse FFT + Otsu | Reconstructs the spatial image for binary feature extraction. |

---

## 🚀 Installation & Usage

### Local Development
1. **Clone & Install**:
   ```bash
   git clone https://github.com/daltee/Crack-Detector.git
   cd Crack-Detector
   pip install -r requirements.txt
   ```
2. **Launch Web App**:
   ```bash
   python app.py
   ```
3. **Launch Desktop GUI**:
   ```bash
   python main_gui.py
   ```

---

## ☁️ Vercel Deployment

This repository is optimized for **Vercel** serverless functions.

1. **Push** your code to GitHub.
2. **Import** the project on [Vercel Dashboard](https://vercel.com/new).
3. The `vercel.json` and `requirements.txt` (using `opencv-python-headless`) ensure a zero-config deployment.
4. Access your scanner from any mobile device via the generated Vercel URL.

---

<p align="center">
  <i>Engineered for Infrastructure Safety & Modern Inspection Workflows.</i>
</p>
