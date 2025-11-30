# 📹 Video to Code Generator

## 💡 Project Overview

The **Video to Code Generator** is a Flask-based web application that simulates an advanced Vision LLM pipeline. It takes a screen recording (video) of code being displayed in an editor and generates the corresponding clean HTML, CSS, and JavaScript code by analyzing the visual content of the video frames.

This project was built using Python, Flask, OpenCV, and Tesseract OCR, showcasing the integration of computer vision into web applications.

---

## ✨ Core Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend / Web Server** | **Flask (Python)** | Handles URL routing, manages file uploads, and serves the frontend. |
| **Video Processing** | **OpenCV** | Extracts frames from the video and applies image preprocessing. |
| **OCR (AI Core)** | **Tesseract OCR / PyTesseract** | Recognizes and extracts text (code) from the processed video frames. |
| **AI Logic** | **Heuristic Classification** | Python logic that analyzes the extracted text to separate it into HTML, CSS, and JS blocks. |
| **Frontend** | **HTML/CSS/JS** | Provides a responsive, video-themed interface for uploading videos and viewing the generated code. |

---

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### 1. Prerequisites

You need **Python 3.8+** and **Tesseract OCR** installed on your system.

* **Python Libraries:** Install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```
* **Tesseract OCR:** Download and install the Tesseract executable for your OS.
    * **Default Path (Windows):** `C:\Program Files\Tesseract-OCR\tesseract.exe`

### 2. File Structure

```
video-to-code-generator/
├── app.py
├── video_processor.py
├── requirements.txt
├── static/
│   ├── css/
│   ├── js/
│   └── img/
└── templates/
    └── index.html
```

### 3. Configuration Setup

1. Open `video_processor.py`
2. Update Tesseract Path:
    ```python
    TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    ```
3. Adjust ROI settings:
    ```python
    X_START_PERCENT = 500
    X_END_PERCENT = 1000
    Y_START_PERCENT = 150
    Y_END_PERCENT = 950
    ```

---

## ▶️ Running the Application

```bash
python app.py
```

Navigate to: **http://127.0.0.1:5000**

---

## 🎯 How to Use

* Upload a screen recording of code displayed in VS Code.
* Use high resolution and high contrast.
* Ensure code is static in the ROI.
