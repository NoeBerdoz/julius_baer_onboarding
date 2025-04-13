# julius_baer_onboarding


# Project Setup Guide (Ubuntu Linux)

This project consists of a Python backend and a JavaScript frontend. The following instructions describe how to set up the development environment manually on Ubuntu.

---

## 🔧 Installing prerequisites

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

See https://nodejs.org/en/download : Install v20.19.0 or higher

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

4. **Setup environment variables**

```bash
cp .env.example .env
```
And fill in your values and API keys in the newly created `.env` file.

---

## 🧪 Development Workflow

- Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

- To run the backend:

```bash
python app.py
```

- To run the frontend:

```bash
cd frontend
npm run dev
```

Then open your browser to http://localhost:5174/ (or the address displayed after running `npm run dev`)