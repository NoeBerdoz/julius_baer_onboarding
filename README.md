# Julius Baer Onboarding

An interactive onboarding simulation system designed for Julius Baer, a decision-based game interface. This project helps users understand client interaction scenarios and decision-making processes in a private banking context.


## 🔍 Features

- Interactive client scenario simulations
- AI-powered decision recommendations
- Real-time scoring and feedback
- Progress tracking
- Document processing capabilities
- Comprehensive validation system

## 🎯 Project Overview

The Julius Baer Onboarding Simulation is a full-stack application that:
- Simulates real-world client interaction scenarios
- Provides AI-powered decision recommendations
- Tracks user performance and learning progress
- Offers an intuitive and engaging user interface

## 🏗️ Architecture

### Backend (Python/Flask)
- RESTful API endpoints for game management
- Integration with Julius Baer's API
- AI advisor for decision recommendations
- Game state management and scoring system
- OCR capabilities for document processing

### Frontend (Alpine.js & Bootsrap)
- Modern, responsive user interface
- Interactive game flow
- Real-time decision feedback
- Score tracking and progress visualization

## ✅ Prerequisites

Install the following system dependencies:

- Python 3.12
- pip
- virtualenv
- Node.js (v16+)
- npm
- tesseract-ocr

## 🔧 Installation Steps

### 1. Install Python 3.11+ and Required Tools

#### For Ubuntu 22.04+

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
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

## 📁 Project Structure

```
julius_baer_onboarding/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── frontend/            # Frontend application
├── services/            # Backend services
├── dto/                 # Data Transfer Objects
├── validation/          # Validation logic
├── utils/              # Utility functions
├── game_files/         # Game-related files
└── tests/              # Test suite
```

## 🧪 Development Workflow

1. **Start the backend server**

```bash
source .venv/bin/activate
python app.py
```

2. **Start the frontend development server**

```bash
cd frontend
npm run dev
```

# Screenshots of the app
The user has a view to see all documents  
![image](https://github.com/user-attachments/assets/d8a8f4eb-2c4c-408b-aa5d-d51649a04a46)

When the AI suggest that the dossier is fine
![image](https://github.com/user-attachments/assets/1f459e3d-2b78-4f99-a08f-be3ea53fa845)

When the AI suggest that the dossier has an issue
![image](https://github.com/user-attachments/assets/b137dfa0-bbc2-4bfe-bd89-89e22f9300cf)

The AI adapts to each dossier
![image](https://github.com/user-attachments/assets/22e04cda-f54d-4a07-9dfa-5b5eceb2618a)

The user makes the final decision and has interface feedbacks, loadings, game over screen...
![image](https://github.com/user-attachments/assets/66b1e9aa-2a0a-4291-9d3d-839b8bbea589)






