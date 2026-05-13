# 🏗️ Crack Detector: 2D FFT Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployment-black?logo=vercel)](https://vercel.com/)

**Crack Detector** is an advanced image processing tool that leverages **2D Fast Fourier Transform (FFT)** for automated crack detection in civil infrastructure. It converts images into frequency spectra, applying high-pass filters to isolate fine structural edges and defects from background noise.

---

## 🌟 Key Features

- **🧠 2D FFT Core Logic**: Mathematical approach to cleanly separate defects from background textures.
- **💻 Desktop GUI**: A sleek, modern desktop interface built with `CustomTkinter`.
- **🌐 Web Application**: A responsive web-based version that can be accessed from any device (Phone/PC).
- **📸 Real-Time Integration**: Support for live camera feeds and instant processing.
- **⚡ Performance Optimized**: Mathematical tasks run on background threads for a smooth user experience.
- **🚀 Cloud Ready**: Fully configured for one-click deployment to **Vercel**.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask (Web), OpenCV, NumPy
- **Frontend**: CustomTkinter (Desktop), HTML5, CSS3, JavaScript (Web)
- **Deployment**: Vercel

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/daltee/Crack-Detector.git
   cd Crack-Detector
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Usage

### Desktop Application
Run the modern GUI for a full-featured desktop experience:
```bash
python main_gui.py
```

### Web Application
Run the local web server to access via browser:
```bash
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

---

## ☁️ Deployment

This project is ready to be deployed on **Vercel**.

1. Push your code to a GitHub repository.
2. Connect your repository to Vercel.
3. Vercel will automatically detect the `vercel.json` and deploy the Flask app.

---

## 📂 Project Structure

- `app.py`: Flask web application entry point.
- `main_gui.py`: Desktop application entry point.
- `preprocessing.py`: Image cleaning and enhancement logic.
- `fft_logic.py`: Core 2D FFT and filtering mathematical logic.
- `templates/` & `static/`: Frontend assets for the web application.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Developed with ❤️ for Infrastructure Safety
</p>
