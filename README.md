# 🛡️ PhishGuard

### AI-Powered Phishing Detection & Investigation Platform

PhishGuard is an AI-assisted cybersecurity platform designed to analyze suspicious URLs and email files, combine machine-learning predictions with rule-based security analysis and threat intelligence, and provide explainable investigation results through a centralized dashboard.

---

## 🚀 Key Features

- 🔎 **URL Phishing Detection**
  - Extracts security-related URL features
  - Uses a Random Forest machine-learning model
  - Provides phishing/legitimate classification
  - Displays model confidence

- 🧠 **Explainable AI**
  - Uses SHAP to explain ML predictions
  - Shows feature-level contribution toward the predicted class

- 🛡️ **Rule-Based Risk Engine**
  - Detects suspicious URL characteristics
  - Generates a rule-based risk score
  - Provides human-readable reasons

- 🌐 **VirusTotal Threat Intelligence**
  - Checks URLs against VirusTotal
  - Displays malicious, suspicious, harmless and undetected results
  - Handles unavailable or rate-limited API responses

- 📧 **Email Investigation**
  - Supports `.eml` files
  - Extracts sender, recipient, subject and Reply-To
  - Analyzes suspicious keywords
  - Extracts embedded URLs
  - Detects attachments
  - Reads authentication results
  - Investigates embedded URLs using the URL analysis pipeline

- 📊 **Investigation Dashboard**
  - Recent investigation history
  - Risk distribution
  - Investigation details
  - URL feature analysis
  - Email evidence
  - ML explanations

- 💾 **SQLite Investigation History**
  - Stores investigation results locally
  - Supports investigation retrieval and detailed review

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   React Dashboard   │
                    │      / Vite         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       URL Feature        Rule-Based       Email Analyzer
       Extraction         Risk Engine             │
              │                │                  │
              ▼                │                  ▼
       Random Forest           │          Embedded URLs
              │                │                  │
              └────────┬───────┘                  │
                       ▼                          │
                Final Assessment ◄────────────────┘
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        VirusTotal            SHAP
       Threat Intel       Explainability
              │                 │
              └────────┬────────┘
                       ▼
                 SQLite History