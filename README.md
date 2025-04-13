# Julius Baer - AI-Powered Onboarding Dossier Review

**Project for SwissHacks 2025 Hackathon - Challenge by Julius Baer**

## 🎯 The Challenge

Julius Baer faces challenges in managing the client onboarding process, which involves significant manual effort by employees to analyze and validate new client dossiers. This manual process can be time-consuming and prone to inconsistencies.

## 💡 Our Solution

This project presents an AI-powered system designed to streamline the client onboarding dossier review process for Julius Baer employees. It combines Optical Character Recognition (OCR) and Large Language Model (LLM) reasoning to automatically analyze client documents and provide decision support to the reviewing employee.

The system features a user-friendly frontend interface where employees can:
* View client onboarding documents (Passport, Account Details, Profile, Description).
* See the AI's analysis and recommendation (Accept/Reject) based on data consistency checks across documents.
* Make the final decision to validate or refuse the client's dossier.

This aims to reduce manual workload, improve consistency, and potentially speed up the onboarding process.

## 🔍 Key Features

* **AI-Powered Dossier Analysis**: Utilizes OCR and LLM (via services like OpenAI's GPT models) to extract and cross-validate information from various client documents (PNG, PDF, DOCX, TXT).
* **Frontend Interface**: An interactive web application (built with Alpine.js and Bootstrap) for employees to view documents, AI recommendations, and make final decisions.
* **Document Handling**: Processes various document formats commonly found in client dossiers.
* **Decision Support**: Provides employees with AI-generated reasons for accepting or rejecting a dossier based on detected inconsistencies.
* **Gamified Simulation (Based on API)**: Interacts with the Julius Baer Hackathon API, simulating the process of receiving and deciding on client dossiers in a game-like format.

## 🏗️ Architecture

![image](https://github.com/user-attachments/assets/ac0117eb-f3ec-41af-8438-560d96785bff)

### Backend (Python/Flask)
* RESTful API endpoints (`/new-game`, `/next`) to manage the onboarding simulation flow.
* Integrates with the Julius Baer Hackathon API Client.
* **AI Advisor Service (`services/advisor.py`)**:
    * Orchestrates the extraction of data from documents using OCR/parsing utilities (`utils/parsers/`).
    * Uses LLMs (e.g., GPT-4o via Langchain) to analyze extracted data, check for inconsistencies, and generate Accept/Reject recommendations with reasoning.
    * Uses Pydantic models (`validation/`) for structured data handling and validation.
* **Data Extraction Service (`services/extractor.py`)**: Handles the processing of different file types (Passport PNG, Account PDF, Profile DOCX, Description TXT) and interfacing with the LLM for data extraction.
* Stores game round data and decoded files locally (`utils/storage/game_files_manager.py`).

### Frontend (Alpine.js & Bootstrap)
* Responsive user interface (`frontend/src/index.html`).
* Dynamically displays client documents (PNG, PDF, DOCX preview via Mammoth.js, TXT).
* Shows AI recommendations and reasons.
* Allows users (employees) to submit Accept/Reject decisions.
* Manages game state (score, status) received from the backend.

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

### Configure Environment Variables  
Create a .env file based on .env.exemple and add your API keys/settings  

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






