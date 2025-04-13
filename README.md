# julius_baer_onboarding


# Project Setup Guide (Ubuntu Linux)

This project consists of a Python backend and a JavaScript frontend. The following instructions describe how to set up the development environment manually on Ubuntu.

---

## ✅ Prerequisites

Install the following system dependencies:

- Python 3.12
- pip
- virtualenv
- Node.js (v16+)
- npm
- tesseract-ocr

---

## 🔧 Installation Steps

### 1. Install Python 3.12 and Required Tools

#### For Ubuntu 22.04+

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

#### For Ubuntu 20.04

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

### 2. Install Tesseract OCR

```bash
sudo apt install tesseract-ocr
```

### 3. Install Node.js and npm

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## 🚀 Project Setup

1. **Clone the repository**

```bash
git clone https://github.com/NoeBerdoz/julius_baer_onboarding
cd julius_baer_onboarding
```

2. **Set up the Python virtual environment**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Install frontend dependencies**

```bash
cd frontend
npm install
cd ..
```

---

## 📁 Project Structure

- `requirements.txt` — Python dependencies
- `.venv/` — Python virtual environment
- `frontend/` — JavaScript frontend (managed with npm)

---

## 🧪 Development Workflow

- Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

- To run the frontend:

```bash
cd frontend
npm run dev
```

- To run the backend:

```bash
python app.py
```