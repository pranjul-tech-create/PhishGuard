# 🛡️ PhishGuard

## AI-Powered Phishing Detection & Investigation Platform

**Detect • Investigate • Explain • Document**

PhishGuard is a full-stack cybersecurity platform designed to detect and investigate suspicious URLs and phishing emails using Machine Learning, rule-based security analysis, threat intelligence, and Explainable AI.

The platform combines automated URL analysis, email investigation, VirusTotal integration, SHAP-based explanations, risk assessment, and SQLite investigation history in a centralized security dashboard.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Key Features](#-key-features)
- [System Workflow](#-system-workflow)
- [System Architecture](#-system-architecture)
- [Machine Learning Model](#-machine-learning-model)
- [Dataset](#-dataset)
- [Feature Engineering](#-feature-engineering)
- [Model Evaluation](#-model-evaluation)
- [Rule-Based Risk Engine](#-rule-based-risk-engine)
- [VirusTotal Integration](#-virustotal-integration)
- [Email Investigation](#-email-investigation)
- [Explainable AI](#-explainable-ai)
- [Investigation History](#-investigation-history)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Testing](#-testing)
- [Security Considerations](#-security-considerations)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [Project Status](#-project-status)
- [References](#-references)
- [Author](#-author)

---

## 🚀 Overview

Phishing attacks use deceptive URLs, fraudulent emails, account-verification requests, and misleading security alerts to trick users into revealing sensitive information.

Traditional detection approaches may rely on static blacklists, manual investigation, keyword matching, or individual detection rules.

PhishGuard combines multiple analysis techniques to help users investigate suspicious indicators through a single interface.

### How PhishGuard Works

```text
          Suspicious URL / Email
                    |
                    v
             Feature Extraction
                    |
                    v
           Machine Learning Model
                    |
                    v
            Rule-Based Analysis
                    |
                    v
          Threat Intelligence Check
                    |
                    v
           Explainable AI (SHAP)
                    |
                    v
            Final Risk Assessment
                    |
                    v
          Investigation History
                    |
                    v
             Security Dashboard
```

The objective is not simply to classify a URL or email, but also to present relevant evidence and explanations that support further investigation.

---

## 🎯 Problem Statement

Phishing detection involves identifying suspicious URLs, deceptive email content, potentially misleading sender information, and other indicators associated with malicious activity.

A basic classifier might return a result such as:

```text
Prediction: PHISHING
```

However, a useful investigation workflow should also help answer:

- Which URL characteristics appear suspicious?
- What did the machine-learning model predict?
- What factors contributed to the prediction?
- Does external threat intelligence contain relevant information?
- Does an email contain suspicious language or embedded URLs?
- Are sender and Reply-To addresses different?
- What evidence contributed to the final risk assessment?

PhishGuard addresses these requirements by combining:

**Machine Learning + Rule-Based Analysis + Threat Intelligence + Email Analysis + Explainable AI**

---

## 🎯 Objectives

The primary objectives of PhishGuard are:

1. Detect suspicious URLs using machine learning.
2. Extract numerical features from submitted URLs.
3. Identify suspicious characteristics using a rule-based engine.
4. Enrich URL investigations with VirusTotal threat intelligence.
5. Analyze suspicious `.eml` email files.
6. Extract and investigate URLs embedded in emails.
7. Inspect available email headers and suspicious indicators.
8. Explain model predictions using SHAP.
9. Generate a final risk assessment.
10. Store investigation results using SQLite.
11. Provide a centralized security investigation dashboard.
12. Demonstrate the practical integration of AI and cybersecurity.

---

# ✨ Key Features

## 🔎 1. AI-Based URL Phishing Detection

Users can submit a URL for automated analysis.

The system extracts characteristics such as:

- URL length
- Domain length
- Subdomain length
- Number of dots
- Number of hyphens
- Number of digits
- Number of special characters
- HTTPS usage
- IP-based hostname detection
- Suspicious keyword count
- Path length
- Query length

The extracted feature vector is passed to a trained Random Forest classifier.

### Example

```text
Input:
http://192.168.1.100/login

Output:
Prediction: PHISHING
```

*The example demonstrates the input format; actual predictions depend on the model and analysis results.*

---

## 🤖 2. Random Forest Classification

PhishGuard uses a Random Forest classifier to categorize URLs as:

- `PHISHING`
- `LEGITIMATE`

### Model Pipeline

```text
Raw URL
   |
   v
Feature Extraction
   |
   v
Numerical Feature Vector
   |
   v
Random Forest Classifier
   |
   v
Predicted Class + Confidence
```

The model is trained using the PhiUSIIL Phishing URL Dataset.

The backend loads the trained model from `phishing_model.pkl` and uses it to analyze submitted URLs.

---

## 🛡️ 3. Rule-Based Risk Assessment

PhishGuard includes a separate rule-based engine that evaluates suspicious URL characteristics.

The engine considers indicators such as:

- IP address instead of a conventional domain
- Missing HTTPS
- Suspicious keywords
- Unusually long URLs
- Long subdomains
- Excessive special characters

Each matching rule contributes to the rule-based risk score.

### Risk Levels

| Score | Risk Level |
|---|---|
| 0–39 | LOW |
| 40–69 | MEDIUM |
| 70–100 | HIGH |

The rule-based score is distinct from the machine-learning prediction.

This separation allows users to inspect different sources of evidence instead of treating them as a single unexplained result.

---

## 🌐 4. VirusTotal Threat Intelligence

PhishGuard integrates the VirusTotal API to retrieve available threat intelligence for submitted URLs.

The application can display:

- Malicious detections
- Suspicious detections
- Harmless detections
- Undetected results
- API availability
- Threat intelligence messages

### Example Response

```text
VirusTotal Analysis
-------------------
Malicious:   0
Suspicious:  0
Harmless:   63
Undetected: 29
```

The numbers above are illustrative.

> **Important:** No malicious or suspicious detections do not guarantee that a URL is safe. Threat intelligence results depend on available data, analysis coverage, and service availability.

If VirusTotal is unavailable or the API limit is reached, the application can report that the external check was unavailable.

---

## 📧 5. Phishing Email Investigation

PhishGuard supports the analysis of `.eml` email files.

The email analyzer extracts available information, including:

- Sender
- Recipient
- Subject
- Date
- Reply-To
- Return-Path
- Authentication-Results
- Received headers
- Embedded URLs
- Attachment filenames
- Suspicious keywords

This information supports a structured examination of suspicious email messages.

### Example

```text
From:
security-alert@example.com

Reply-To:
suspicious@example.net

Finding:
Reply-To address differs from the sender address.
```

This is a synthetic example intended to demonstrate the type of evidence the application can display.

---

## 🔍 6. Email Security Indicators

The email analyzer searches for suspicious language and structural indicators, including:

- Urgent account-related messages
- Account verification requests
- Password reset requests
- Security alerts
- Payment-related messages
- OTP-related language
- Suspicious URLs
- Attachments
- Reply-To mismatches
- Missing Authentication-Results headers

These indicators contribute to the email risk score.

**A single indicator does not prove that an email is malicious.** Findings should be interpreted together with the available evidence.

---

## 🔗 7. Embedded URL Investigation

Phishing emails can contain links that require separate investigation.

PhishGuard extracts URLs from the email body and analyzes them through the URL investigation pipeline.

```text
          Uploaded Email
                 |
                 v
          Parse Email Body
                 |
                 v
          Extract Embedded URLs
                 |
                 v
          URL Feature Extraction
                 |
                 v
          ML Classification
                 |
                 v
          Rule-Based Analysis
                 |
                 v
          Threat Intelligence
                 |
                 v
          URL Risk Assessment
```

This enables investigation of both the email itself and the URLs it contains.

---

## 🧠 8. Explainable AI with SHAP

PhishGuard integrates SHAP (SHapley Additive exPlanations) to explain the contributions of URL features to the model's prediction.

Instead of presenting only a classification, the application can display feature-level impact information.

### Illustrative Example

| Feature | Value | Example Impact |
|---|---:|---:|
| `url_length` | 87 | +0.12 |
| `has_ip` | 1 | +0.21 |
| `suspicious_keyword_count` | 3 | +0.18 |
| `uses_https` | 0 | +0.08 |
| `num_special_chars` | 14 | +0.04 |

*These values are illustrative, not measured results from a particular investigation.*

SHAP explanations help answer:

**Why did the model make this prediction?**

The SHAP explanation is displayed separately from the rule-based score because the two components represent different analysis methods.

---

## 📊 9. Security Dashboard

PhishGuard provides a dark-themed, SOC-inspired dashboard for reviewing investigations.

Implemented dashboard functionality includes:

- Total investigations
- URL investigations
- Email investigations
- Risk distribution
- Recent investigation history
- Investigation details
- ML prediction
- ML confidence
- Rule-based risk score
- Threat intelligence information
- Extracted URL features
- SHAP explanation
- Email metadata
- Embedded URL analysis

The interface brings the main investigation components together in one place.

---

## 🗂️ 10. Investigation History

PhishGuard uses SQLite to store investigation records.

Depending on the investigation type, stored information can include:

```text
Investigation ID
Input Type
URL / Email Information
ML Prediction
ML Confidence
Rule Score
Rule Reasons
Final Risk Score
Final Risk Level
Threat Intelligence Results
Email Metadata
Embedded URLs
Attachments
Authentication Information
Timestamp
```

The application provides endpoints to retrieve recent investigations and inspect the details of an individual investigation.

---

# 🏗️ System Architecture

```text
                     +----------------------+
                     |         User         |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |    React Frontend    |
                     |  Security Dashboard  |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |      FastAPI API     |
                     +----------+-----------+
                                |
                +---------------+---------------+
                |               |               |
                v               v               v
       +----------------+ +-------------+ +---------------+
       |  URL Analyzer  | |Email Analyzer| | Random Forest |
       +--------+-------+ +------+------+ +-------+-------+
                |               |                |
                +---------------+----------------+
                                |
                                v
                     +----------------------+
                     |    Rule-Based Engine |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | VirusTotal API       |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | SHAP Explainability  |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Final Risk Assessment|
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | SQLite Investigation |
                     |       History        |
                     +----------------------+
```

---

# 🧠 Machine Learning Model

The project uses a Random Forest classifier from Scikit-learn.

### Current Model Configuration

| Parameter | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Number of estimators | 100 |
| Random state | 42 |
| Test set size | 20% |
| Stratified split | Yes |
| Model serialization | Joblib |

The trained model is saved as:

```text
backend/phishing_model.pkl
```

The FastAPI backend loads this model to classify URL feature vectors.

---

# 📚 Dataset

PhishGuard uses the **PhiUSIIL Phishing URL Dataset** for machine-learning experimentation.

The original CSV used in the project contains:

- 235,795 records
- 56 original columns

The project selects URL and label information and generates a smaller dataset containing custom URL features.

### Dataset Labels

The dataset label mapping used in the project is:

```text
0 = Phishing
1 = Legitimate
```

### Dataset Source

**PhiUSIIL Phishing URL Dataset — UCI Machine Learning Repository**

https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset

---

# ⚙️ Dataset Processing

The preparation script processes the raw dataset into the format used by the model.

```text
Raw CSV Dataset
       |
       v
Read Dataset
       |
       v
Select URL and Label
       |
       v
Remove Missing Values
       |
       v
Extract Custom URL Features
       |
       v
Create Processed DataFrame
       |
       v
Save processed_dataset.csv
```

The processed dataset contains 12 custom URL features and one label column.

---

# 📊 Feature Engineering

The current URL feature set contains the following features.

| Feature | Description |
|---|---|
| `url_length` | Total URL length |
| `domain_length` | Length of the extracted domain |
| `subdomain_length` | Length of the extracted subdomain |
| `num_dots` | Number of dots in the URL |
| `num_hyphens` | Number of hyphens in the URL |
| `num_digits` | Number of numeric characters |
| `num_special_chars` | Number of non-alphanumeric characters |
| `uses_https` | Whether the parsed scheme is HTTPS |
| `has_ip` | Whether the hostname matches the implemented IPv4 pattern |
| `suspicious_keyword_count` | Number of configured suspicious keywords found |
| `path_length` | Length of the URL path |
| `query_length` | Length of the URL query |

These features convert URL strings into numerical data that can be used by the classifier.

---

# 📈 Model Evaluation

The current model training run produced the following results using an 80/20 stratified train/test split.

```text
Training Samples : 188,636
Testing Samples  : 47,159
Accuracy         : approximately 99.74%
```

### Confusion Matrix

```text
                 Predicted
               Phishing  Legitimate

Actual Phishing    20079      110
Actual Legitimate    11     26959
```

The project also includes a separate validation script:

```text
backend/validate_generalization.py
```

This script supports additional evaluation work.

> **Evaluation note:** These results describe the reported dataset and split. They do not establish guaranteed real-world accuracy. Dataset overlap, feature design, distribution differences, and evaluation methodology should be considered when interpreting model performance.

---

# 🔄 URL Investigation Workflow

```text
1. User submits a URL
          |
          v
2. Extract URL features
          |
          v
3. Run Random Forest classification
          |
          v
4. Calculate model confidence
          |
          v
5. Calculate rule-based risk
          |
          v
6. Check VirusTotal threat intelligence
          |
          v
7. Generate SHAP explanation
          |
          v
8. Calculate final risk assessment
          |
          v
9. Save investigation in SQLite
          |
          v
10. Display results on the dashboard
```

---

# 📧 Email Investigation Workflow

```text
1. User uploads an .eml file
          |
          v
2. Parse email headers and body
          |
          v
3. Extract sender and recipient information
          |
          v
4. Detect configured suspicious keywords
          |
          v
5. Extract embedded URLs
          |
          v
6. Identify attachment filenames
          |
          v
7. Inspect available authentication headers
          |
          v
8. Investigate embedded URLs
          |
          v
9. Calculate email risk
          |
          v
10. Save investigation in SQLite
          |
          v
11. Display results on the dashboard
```

---

# 🧰 Technology Stack

## Backend

| Technology | Purpose |
|---|---|
| Python | Backend logic and machine learning |
| FastAPI | REST API |
| Pandas | Dataset processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine-learning model |
| Random Forest | URL classification |
| SHAP | Explainable AI |
| tldextract | Domain extraction |
| Requests | HTTP requests to VirusTotal |
| python-dotenv | Environment variable configuration |
| python-multipart | Multipart file uploads |
| Joblib | Model serialization |
| SQLite | Investigation storage |

## Frontend

| Technology | Purpose |
|---|---|
| React | User interface |
| Vite | Frontend development and build tooling |
| JavaScript | Application logic |
| CSS | Dashboard styling |

## Security Components

- URL feature extraction
- Machine-learning classification
- Rule-based risk scoring
- VirusTotal threat intelligence
- Email header inspection
- Embedded URL analysis
- SHAP-based model explanations
- Investigation history

---

# 📁 Project Structure

```text
PhishGuard/
│
├── backend/
│   ├── main.py
│   ├── url_analyzer.py
│   ├── prepare_dataset.py
│   ├── train_model.py
│   ├── predict.py
│   ├── risk_engine.py
│   ├── threat_intel.py
│   ├── final_assessment.py
│   ├── email_analyzer.py
│   ├── validate_generalization.py
│   ├── database.py
│   └── phishing_model.pkl
│
├── dataset/
│   └── processed_dataset.csv
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

The raw dataset, local environment files, virtual environments, and local database files should not be committed unless there is a specific reason to include them.

---

# 🔌 API Endpoints

The backend exposes endpoints for URL analysis, email analysis, and investigation history.

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/scan` | Analyze a submitted URL |
| `POST` | `/analyze-email` | Analyze an uploaded `.eml` file |
| `GET` | `/investigations` | Retrieve investigation history |
| `GET` | `/investigations/{investigation_id}` | Retrieve details for one investigation |

FastAPI interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# ⚙️ Installation

## Prerequisites

Install the following before running the application:

- Python 3
- Node.js
- npm
- Git

## 1. Clone the Repository

```bash
git clone https://github.com/pranjul-tech-create/PhishGuard.git
cd PhishGuard
```

## 2. Set Up the Backend

Open a terminal and navigate to the backend directory:

```powershell
cd backend
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an appropriate local execution-policy setting or activate the environment using another supported terminal.

## 3. Install Backend Dependencies

```powershell
pip install fastapi uvicorn pandas numpy scikit-learn joblib tldextract requests python-dotenv python-multipart shap
```

## 4. Configure VirusTotal

Create a file named `.env` inside the `backend` directory.

File path:

```text
backend/.env
```

Add your own VirusTotal API key:

```env
VT_API_KEY=your_api_key_here
```

Replace the placeholder with your own API key.

**Never commit your actual `.env` file or expose your API key publicly.**

## 5. Set Up the Frontend

Open a second terminal:

```powershell
cd frontend
```

Install the frontend dependencies:

```powershell
npm install
```

---

# ▶️ Running the Project

## Start the Backend

Open a terminal and run:

```powershell
cd C:\Users\hp\Documents\PhishGuard\backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

Backend address:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## Start the Frontend

Open a separate terminal:

```powershell
cd C:\Users\hp\Documents\PhishGuard\frontend
npm run dev
```

Open the local development URL displayed by Vite in the terminal.

Keep both development servers running while using the application.

> The commands above use the local Windows development path. If you clone the project to a different location, replace the path accordingly.

---

# 🧪 Testing

The application has been tested with legitimate and suspicious URL examples, as well as a synthetic email file.

## Legitimate URL Examples

```text
https://www.google.com
https://github.com
```

## Suspicious URL Examples

```text
http://192.168.1.100/login

http://example.com/verify-account-password

https://secure-login-verify-account.com/update
```

These are test inputs, not guarantees that every URL will receive a particular classification.

## Synthetic Email Testing

A synthetic phishing-style `.eml` file was used to test the email investigation workflow.

The test included:

- Urgent account-verification language
- A Reply-To address different from the sender
- SPF/DKIM failure information in the supplied authentication header
- An embedded URL
- A password-reset request

The email analyzer was tested for extracting metadata, suspicious keywords, embedded URLs, and available authentication information.

---

# 🔐 Security Considerations

## 1. API Key Protection

VirusTotal credentials should be stored in environment variables.

The `.env` file should be excluded from version control.

A public repository must never contain a working API key.

## 2. URL Analysis

The current URL analysis focuses on the submitted URL string and extracted metadata. It does not blindly browse arbitrary submitted webpages.

Any future webpage fetching or redirect analysis should use appropriate isolation, network restrictions, timeout controls, and SSRF protections.

## 3. Threat Intelligence Interpretation

Threat intelligence is one source of evidence, not an absolute determination of safety.

An unavailable result or a result with no detections should not automatically be interpreted as proof that a URL is safe.

## 4. Email Authentication

Authentication results are inspected from the supplied email data. A header contained in an uploaded `.eml` file is not, by itself, proof that the original sending server performed a valid authentication check.

Reliable SPF, DKIM, and DMARC verification generally requires appropriate mail-server or DNS-based verification.

## 5. Safe Testing

Use synthetic emails and controlled test cases. Do not open suspicious links or execute unknown attachments on your personal system.

---

# ⚠️ Limitations

PhishGuard is an academic and portfolio project. Its output should support investigation rather than replace professional security analysis.

### Dataset Dependence

Model performance depends on the training dataset, label quality, feature design, and evaluation methodology.

### URL Feature Dependence

The current classifier primarily uses URL-level features. It does not perform comprehensive webpage behavioral analysis.

### Threat Intelligence Availability

VirusTotal results depend on API availability, rate limits, and available analysis records.

### Email Authentication

The email analyzer inspects available headers, but the presence or absence of a header is not equivalent to independently verifying the sending infrastructure.

### False Positives and False Negatives

Legitimate URLs may appear suspicious, and malicious URLs may avoid detection.

### Risk Score Interpretation

The rule-based score and final risk score are application-specific heuristics. They are not calibrated probabilities of an attack.

---

# 🔮 Future Enhancements

Potential future improvements include:

- Browser extension for URL analysis
- DNS and WHOIS intelligence
- Domain registration age analysis
- SSL certificate analysis
- Controlled redirect-chain analysis
- Isolated webpage sandboxing
- HTML and JavaScript inspection
- Screenshot-based phishing detection
- Independent SPF/DKIM/DMARC verification
- Attachment malware analysis in a sandbox
- Additional URL reputation providers
- SIEM integration
- SOC alert generation
- Investigation export as PDF or JSON
- Advanced analytics and reporting
- More rigorous cross-domain model evaluation
- Automated model monitoring and retraining

These are potential enhancements and should not be considered implemented features unless added and tested.

---

# 📌 Project Status

**Status: Active Academic / Portfolio Project**

### Implemented Features

- [x] URL analysis
- [x] URL feature extraction
- [x] Random Forest classification
- [x] ML prediction confidence
- [x] Rule-based risk engine
- [x] VirusTotal integration
- [x] SHAP explainability
- [x] `.eml` email analysis
- [x] Email metadata extraction
- [x] Suspicious keyword detection
- [x] Embedded URL investigation
- [x] SQLite investigation history
- [x] Security dashboard
- [x] Risk distribution
- [x] Investigation details
- [x] ML explanation display
- [x] Legitimate URL testing
- [x] Suspicious URL testing
- [x] Synthetic email testing

---

# 💼 Engineering Highlights

PhishGuard demonstrates practical integration of:

- Python backend development
- REST API development with FastAPI
- React frontend development
- Data processing and feature engineering
- Supervised machine learning
- Random Forest classification
- Model evaluation
- Explainable AI using SHAP
- Threat intelligence API integration
- Email security analysis
- URL analysis
- SQLite database management
- Full-stack application development
- Security-focused system design

---

# 📚 References

### Dataset

**PhiUSIIL Phishing URL Dataset**

UCI Machine Learning Repository:

https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset

### Threat Intelligence

**VirusTotal**

https://www.virustotal.com/

### Explainable AI

**SHAP Documentation**

https://shap.readthedocs.io/

### Backend Framework

**FastAPI Documentation**

https://fastapi.tiangolo.com/

### Machine Learning

**Scikit-learn Documentation**

https://scikit-learn.org/stable/

### Frontend Framework

**React Documentation**

https://react.dev/

---

# 👨‍💻 Author

## Pranjul Parashar

**B.Tech Computer Science**  
**Cyber Security & Digital Forensics**

GitHub: https://github.com/pranjul-tech-create

Project Repository: https://github.com/pranjul-tech-create/PhishGuard

---

# ⭐ Project Vision

PhishGuard aims to make phishing investigation more explainable, structured, and accessible by combining machine learning with traditional security analysis and threat intelligence.

The project focuses on a complete investigation workflow:

```text
Detect
  |
  v
Analyze
  |
  v
Correlate Evidence
  |
  v
Explain
  |
  v
Assess Risk
  |
  v
Document Findings
```

The goal is to help users understand what was detected, which indicators contributed to the result, what external intelligence reported, and what may require further investigation.

---

# 🛡️ PhishGuard

### Detect. Investigate. Explain. Document.

**Built for cybersecurity learning, research, and practical security investigation.**
