# 🛡️ ScamLens AI – Intelligent Scam Detection Platform

<p align="center">
  <strong>Detect Scams. Understand Risks. Stay Protected.</strong>
</p>

<p align="center">
  An AI-powered scam detection platform that analyzes suspicious messages, URLs, and screenshots to identify potential scams and provide actionable safety recommendations.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange?logo=scikitlearn" />
  <img src="https://img.shields.io/badge/EasyOCR-Text%20Recognition-green" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

---

## 📌 Overview

**ScamLens AI** is an intelligent scam detection platform designed to help users identify potentially fraudulent digital communications before they become victims.

With the increasing number of phishing messages, fake websites, fraudulent payment requests, and online scams, identifying suspicious content has become increasingly important.

ScamLens combines **Machine Learning, Natural Language Processing (NLP), Optical Character Recognition (OCR), and rule-based analysis** to examine suspicious content and generate understandable risk assessments.

Users can submit text messages, URLs, or screenshots and receive:

- 🎯 Scam risk scores and risk classifications.
- 🤖 Machine Learning-based spam predictions.
- 🔍 Detected suspicious indicators.
- 📊 Spam and legitimate message probabilities.
- 💡 Actionable safety recommendations.

---

## ✨ Key Features

### 1. 📝 Text Message Analysis
- Analyze suspicious SMS messages, emails, and text content.
- Identify spam-like language and suspicious patterns.
- Apply a trained Machine Learning model for spam classification.
- Display spam and legitimate message probabilities.

### 2. 🔗 URL Scam Detection
- Analyze suspicious website URLs.
- Identify potentially dangerous URL patterns.
- Detect suspicious links and phishing-related indicators.
- Generate risk assessments based on detected indicators.

### 3. 📸 Screenshot Analysis
- Upload screenshots containing suspicious messages or payment-related information.
- Extract text using **EasyOCR (Optical Character Recognition)**.
- Analyze extracted text for suspicious patterns.
- Generate risk assessments and safety recommendations.

### 4. 🤖 Hybrid AI/ML Analysis
Combines multiple detection techniques:

- Machine Learning-based text classification.
- TF-IDF-based text feature extraction.
- Logistic Regression prediction.
- Rule-based scam indicator detection.
- OCR-based text extraction.

### 5. 📊 Risk Assessment
Provides an understandable analysis containing:

- Overall risk score (0–100).
- Risk classification: Low, Medium, or High.
- Detected suspicious indicators.
- AI/ML prediction results.
- Safety recommendations.

---

## 🧠 Machine Learning Implementation

The core Machine Learning component of ScamLens is built using **Natural Language Processing (NLP)** and supervised classification.

### Dataset

The model is trained using the **UCI SMS Spam Collection Dataset**.

| Dataset Information | Details |
|---|---|
| Dataset | UCI SMS Spam Collection |
| Total Messages | 5,572 |
| Legitimate Messages (Ham) | 4,825 |
| Spam Messages | 747 |
| Learning Type | Supervised Learning |
| Classification | Binary Classification |

### ML Workflow

**1. Data Preprocessing**

- Load and process the SMS dataset.
- Separate message text and corresponding labels.
- Prepare data for model training.

**2. Feature Extraction – TF-IDF**

TF-IDF (Term Frequency–Inverse Document Frequency) converts text messages into numerical feature vectors that the ML algorithm can understand.

Configuration:
- Lowercase conversion enabled.
- English stop-word removal.
- Unigrams and bigrams `(1, 2)`.
- Maximum features: 5,000.

**3. Model Training – Logistic Regression**

Logistic Regression is used to classify messages into:

- `spam` – Potentially fraudulent or unwanted messages.
- `ham` – Legitimate messages.

Model configuration:
- Maximum iterations: 1,000.
- Class balancing enabled.
- Random state: 42.
- Stratified 80:20 train-test split.

**4. Model Serialization**

The trained model is saved using Joblib:

`backend/models/scamlens_model.pkl`

This allows the backend to load and reuse the trained model for predictions without retraining every time.

### ML Pipeline

```text
       SMS Message
            |
            ▼
     Text Preprocessing
            |
            ▼
       TF-IDF Vectorizer
            |
            ▼
     Numerical Feature Vectors
            |
            ▼
      Logistic Regression
            |
            ▼
       Spam / Ham Prediction
            |
            ▼
      Probability Analysis
            |
            ▼
       Final ML Result
```

---

## 🏗️ System Architecture

ScamLens follows a frontend-backend architecture.

```text
             USER
               |
               ▼
       HTML / CSS / JavaScript
               |
               ▼
         FastAPI Backend
               |
       ┌───────┼────────┐
       ▼       ▼        ▼
     Text     URL     Screenshot
   Analysis Analysis   Analysis
       |       |        |
       ▼       ▼        ▼
     NLP    Rule-Based  EasyOCR
     + ML   Analysis   Text Extraction
       |       |        |
       └───────┼────────┘
               |
               ▼
       Hybrid Risk Analysis
               |
               ▼
        Risk Score & Level
               |
               ▼
      Detection Indicators
               |
               ▼
      Safety Recommendations
               |
               ▼
         USER INTERFACE
```

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn |
| NLP | TF-IDF |
| ML Algorithm | Logistic Regression |
| OCR | EasyOCR |
| Data Processing | Pandas, NumPy |
| Image Processing | Pillow |
| Model Serialization | Joblib |
| Dataset | UCI SMS Spam Collection |

---

## 📂 Project Structure

```text
ScamLens/
│
├── backend/
│   ├── app/
│   │   ├── ml/
│   │   │   ├── train_model.py
│   │   │   └── test_predictor.py
│   │   │
│   │   └── ...
│   │
│   ├── data/
│   │   └── SMSSpamCollection
│   │
│   ├── models/
│   │   └── scamlens_model.pkl
│   │
│   └── ...
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── ...
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

Follow these steps to run ScamLens AI locally.

### Prerequisites

- Python 3.x
- pip
- Git
- Modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/Agrasha29/Scam-Lens-AI.git
```

```bash
cd Scam-Lens-AI
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the Backend Server

From the backend directory, start the FastAPI application using its configured application entry point:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend API:

`http://127.0.0.1:8000`

FastAPI documentation:

`http://127.0.0.1:8000/docs`

### 4. Start the Frontend

Open another terminal:

```bash
cd frontend
```

Start the local frontend server:

```bash
python -m http.server 5500
```

Open your browser:

`http://localhost:5500`

---

## 🔌 API Endpoints

ScamLens provides REST API endpoints through FastAPI.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend root endpoint |
| GET | `/health` | Check backend health |
| POST | `/analyze` | Analyze suspicious text |
| POST | `/analyze-url` | Analyze suspicious URLs |
| POST | `/analyze-image` | Analyze uploaded screenshots |

---

## 📊 Example ML Prediction

**Input Message:**

"Congratulations! You won a free prize. Claim now."

**ML Prediction:**

```text
Prediction: SPAM
Spam Probability: 97.61%
```

The trained model identifies suspicious language patterns and generates a spam classification with its associated probability.

---

## 🎯 What Makes ScamLens Different?

| Traditional Detection | ScamLens AI |
|---|---|
| Primarily basic keyword matching | Hybrid ML and rule-based analysis |
| Limited input formats | Text, URLs, and screenshots |
| Generic warnings | Risk scores and detected indicators |
| Limited explanations | Explainable detection insights |
| Basic spam classification | Multiple analysis techniques |

---

## 🔮 Future Enhancements

- 🌐 Real-time malicious URL intelligence integration.
- 📧 Email phishing detection.
- 🧠 Advanced NLP and transformer-based models.
- 📱 Browser extension for instant scam detection.
- 🗃️ Scam pattern database and historical analysis.
- 📈 Improved model evaluation and performance monitoring.
- 🔔 Real-time alerts for suspicious digital communications.

---

## 👩‍💻 Developer

**Agrasha Patel**

B.Tech – Computer Science and Engineering  
Specialization: Artificial Intelligence and Machine Learning

**Areas of Interest:**
- Artificial Intelligence & Machine Learning
- Natural Language Processing
- Full-Stack Development
- Intelligent Security Systems

---

## 📬 Repository

**GitHub:** [ScamLens AI](https://github.com/Agrasha29/Scam-Lens-AI)

---

<p align="center">
  <strong>🛡️ ScamLens AI – Think Before You Click. Stay Safe Online.</strong>
</p>

<p align="center">
  If you find this project interesting, consider giving it a ⭐ on GitHub!
</p>
