<div align="center">

# 🛡️ PhishGuard

### AI-Powered Phishing Detection & Investigation Platform

**Detect. Investigate. Explain. Protect.**

An AI-powered cybersecurity platform that combines **Machine Learning**, **rule-based analysis**, **threat intelligence**, and **explainable AI** to detect and investigate phishing URLs and suspicious emails.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel&logoColor=white)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![SHAP](https://img.shields.io/badge/Explainable%20AI-SHAP-purple)
![VirusTotal](https://img.shields.io/badge/Threat%20Intel-VirusTotal-394EFF)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 🌐 Live Demo

| Component | Link |
|-----------|------|
| 🚀 **Frontend** | [https://phish-guard-lemon.vercel.app](https://phish-guard-lemon.vercel.app/) |
| ⚙️ **Backend API** | [https://phishguard-backend-90ey.onrender.com](https://phishguard-backend-90ey.onrender.com/) |
| 📚 **API Documentation** | [https://phishguard-backend-90ey.onrender.com/docs](https://phishguard-backend-90ey.onrender.com/docs) |
| 💻 **GitHub Repository** | [https://github.com/pranjul-tech-create/PhishGuard](https://github.com/pranjul-tech-create/PhishGuard) |

> ⚠️ The backend is hosted on Render's free tier, so the first request after inactivity may take 30–60 seconds while the server wakes up.

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [How PhishGuard Works](#-how-phishguard-works)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [URL Feature Engineering](#-url-feature-engineering)
- [Rule-Based Risk Engine](#-rule-based-risk-engine)
- [Explainable AI with SHAP](#-explainable-ai-with-shap)
- [VirusTotal Threat Intelligence](#-virustotal-threat-intelligence)
- [Email Investigation](#-email-investigation)
- [Investigation History](#-investigation-history)
- [Dataset](#-dataset)
- [Model Performance](#-model-performance)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [Running the Project](#-running-the-project)
- [API Endpoints](#-api-endpoints)
- [Deployment](#-deployment)
- [Security Considerations](#-security-considerations)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [Learning Outcomes](#-learning-outcomes)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🧠 About the Project

PhishGuard is an AI-powered phishing detection and investigation platform designed to analyze suspicious URLs and emails.

Instead of depending on a single detection technique, PhishGuard combines multiple layers of analysis:

```
URL / Email
     ↓
Feature Extraction
     ↓
Machine Learning Model
     ↓
Rule-Based Risk Engine
     ↓
Threat Intelligence
     ↓
Explainable AI
     ↓
Final Risk Assessment
     ↓
Investigation Report
```

---

## ❗ Problem Statement

Phishing remains one of the most common and damaging cyber threats. Attackers constantly create new domains, mimic trusted brands, and craft convincing emails that bypass traditional blacklist-based filters.

Existing approaches have clear gaps:

- **Blacklists** only catch already-known threats and miss newly registered phishing domains.
- **Pure ML classifiers** act as black boxes — users get a verdict but no reasoning.
- **Manual investigation** is slow and requires security expertise.
- **Email phishing** often hides behind spoofed headers and disguised links.

---

## 💡 Solution

PhishGuard addresses these gaps with a **hybrid, explainable detection pipeline**:

1. **ML model** learns patterns from lexical and structural URL features.
2. **Rule-based engine** catches known suspicious indicators with deterministic logic.
3. **Threat intelligence** (VirusTotal) cross-checks against global security vendor verdicts.
4. **SHAP explainability** shows *why* a URL was flagged.
5. **Investigation reports** consolidate everything into one readable verdict.

---

## ✨ Key Features

- 🔗 **URL Phishing Detection** — instant analysis of suspicious links
- 📧 **Email Investigation** — analyze sender, headers, body, and embedded links
- 🤖 **Machine Learning Classification** — trained on labeled phishing/legitimate URLs
- 📏 **Rule-Based Risk Engine** — transparent, auditable heuristics
- 🌍 **VirusTotal Integration** — multi-vendor threat intelligence
- 🔍 **Explainable AI (SHAP)** — feature-level reasoning behind every prediction
- 📊 **Risk Scoring** — combined score with Low / Medium / High severity
- 🗂️ **Investigation History** — review past scans and reports
- 📖 **Auto-generated API Docs** — interactive Swagger UI at `/docs`
- ☁️ **Cloud Deployed** — frontend on Vercel, backend on Render

---

## ⚙️ How PhishGuard Works

1. **Input** — The user submits a URL or pastes a suspicious email.
2. **Feature Extraction** — Lexical, host-based, and structural features are extracted.
3. **ML Prediction** — The trained model outputs a phishing probability.
4. **Rule Evaluation** — The risk engine checks for suspicious patterns (IP address in URL, `@` symbol, excessive subdomains, etc.).
5. **Threat Intelligence** — VirusTotal is queried for existing vendor detections.
6. **Explainability** — SHAP values identify which features pushed the prediction toward phishing or safe.
7. **Final Assessment** — Scores are combined into a final risk level.
8. **Report** — A complete investigation report is returned and stored in history.

---

## 🏗️ System Architecture

```
┌──────────────────────────┐
│     Frontend (Vercel)    │
│   Web UI · Dashboard     │
└────────────┬─────────────┘
             │ HTTPS / REST
             ▼
┌──────────────────────────┐
│   Backend API (Render)   │
│        FastAPI           │
└────────────┬─────────────┘
             │
   ┌─────────┼───────────────────────┐
   ▼         ▼                       ▼
┌────────┐ ┌──────────────┐  ┌───────────────┐
│Feature │ │ ML Model     │  │ Rule-Based    │
│Extract │ │ (Classifier) │  │ Risk Engine   │
└────────┘ └──────┬───────┘  └───────┬───────┘
                  │                  │
                  ▼                  ▼
          ┌──────────────┐   ┌───────────────┐
          │ SHAP         │   │ VirusTotal    │
          │ Explainer    │   │ Threat Intel  │
          └──────┬───────┘   └───────┬───────┘
                 └─────────┬─────────┘
                           ▼
               ┌───────────────────────┐
               │ Final Risk Assessment │
               │ + Investigation Report│
               └───────────────────────┘
```

---

## 🧰 Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | HTML / CSS / JavaScript (or React), deployed on **Vercel** |
| **Backend** | **Python**, **FastAPI**, Uvicorn, deployed on **Render** |
| **Machine Learning** | scikit-learn, pandas, NumPy, joblib |
| **Explainable AI** | SHAP |
| **Threat Intelligence** | VirusTotal API v3 |
| **Data Storage** | SQLite / JSON-based history store |
| **Tooling** | Git, GitHub, Postman / Swagger UI |

> 📝 Adjust this table to match the exact libraries and frameworks used in your repository.

---

## 🤖 Machine Learning Pipeline

```
Raw Dataset
    ↓
Data Cleaning & Deduplication
    ↓
Feature Engineering
    ↓
Train / Test Split
    ↓
Model Training (Random Forest / Gradient Boosting)
    ↓
Evaluation (Accuracy, Precision, Recall, F1, ROC-AUC)
    ↓
Model Serialization (.pkl via joblib)
    ↓
Served through FastAPI
```

**Steps in detail:**

1. **Data preprocessing** — remove duplicates, handle missing values, normalize URLs.
2. **Feature extraction** — convert each URL into a numeric feature vector.
3. **Training** — fit the classifier on labeled phishing and legitimate URLs.
4. **Evaluation** — validate on a held-out test set.
5. **Serialization** — save the trained model for fast inference.
6. **Inference** — load the model once at API startup and predict per request.

---

## 🔬 URL Feature Engineering

PhishGuard extracts features that capture how phishing URLs commonly look:

| Category | Example Features |
|----------|------------------|
| **Length-based** | URL length, hostname length, path length |
| **Character-based** | Count of `.`, `-`, `_`, `@`, `?`, `=`, `&`, `%`, digits |
| **Host-based** | IP address used as host, number of subdomains, TLD type |
| **Protocol** | HTTPS present or absent |
| **Lexical** | Suspicious keywords (`login`, `verify`, `secure`, `update`, `account`, `bank`) |
| **Structural** | Presence of URL shorteners, port numbers, double slashes in path |
| **Entropy** | Randomness of domain string |

---

## 📏 Rule-Based Risk Engine

Alongside ML, a deterministic rule engine assigns weighted points for suspicious indicators:

| Rule | Risk Contribution |
|------|-------------------|
| IP address used instead of domain | High |
| `@` symbol in URL | High |
| No HTTPS | Medium |
| Excessive subdomains | Medium |
| Very long URL | Low–Medium |
| Suspicious keywords in URL | Medium |
| URL shortener detected | Medium |
| Suspicious or uncommon TLD | Medium |

**Risk levels:**

| Score | Level |
|-------|-------|
| 0 – 30 | 🟢 Low Risk |
| 31 – 70 | 🟡 Medium Risk |
| 71 – 100 | 🔴 High Risk |

> 📝 Update the weights and thresholds to match your actual implementation.

---

## 🔍 Explainable AI with SHAP

Most phishing detectors return only a label. PhishGuard explains **why**.

Using **SHAP (SHapley Additive exPlanations)**, every prediction includes:

- Top features contributing to the phishing verdict
- Direction of influence (↑ increases risk / ↓ decreases risk)
- Per-feature contribution values

**Example explanation:**

```
Prediction: PHISHING (confidence 94%)

Top contributing factors:
  ▲ URL contains IP address            +0.31
  ▲ Suspicious keyword "verify"        +0.18
  ▲ Number of subdomains = 5           +0.12
  ▼ HTTPS enabled                      -0.05
```

This builds trust, helps analysts validate results, and makes the system educational.

---

## 🌍 VirusTotal Threat Intelligence

PhishGuard integrates the **VirusTotal API** to enrich every URL analysis:

- Number of security vendors flagging the URL as malicious or suspicious
- Harmless / undetected vendor counts
- Aggregated reputation signal fed into the final risk score

This lets PhishGuard catch threats the ML model might not have seen, while the ML model catches new threats not yet in VirusTotal.

> 🔑 A free VirusTotal API key is required. See [Environment Variables](#-environment-variables).

---

## 📧 Email Investigation

Beyond URLs, PhishGuard can investigate suspicious emails:

- **Sender analysis** — display name vs. actual address mismatch
- **Header inspection** — SPF / DKIM / DMARC indicators and routing anomalies
- **Content analysis** — urgency language, credential requests, financial lures
- **Link extraction** — every embedded URL is run through the full URL pipeline
- **Attachment indicators** — suspicious file types flagged
- **Consolidated verdict** — combined email + link risk assessment

---

## 🗂️ Investigation History

Every analysis is stored so users can:

- Review previous scans and verdicts
- Revisit full investigation reports
- Compare risk scores over time
- Track repeat offenders and recurring domains

---

## 📊 Dataset

The ML model is trained on a labeled dataset of phishing and legitimate URLs.

| Property | Value |
|----------|-------|
| **Source** | `<Kaggle / PhishTank / UCI — add your source>` |
| **Total samples** | `<add count>` |
| **Phishing URLs** | `<add count>` |
| **Legitimate URLs** | `<add count>` |
| **Features used** | `<add count>` |

> 📝 Replace the placeholders with your actual dataset details.

---

## 📈 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | `XX.XX%` |
| Precision | `XX.XX%` |
| Recall | `XX.XX%` |
| F1-Score | `XX.XX%` |
| ROC-AUC | `X.XXX` |

> 📝 Replace with the real numbers from your evaluation notebook. You can also add a confusion matrix or ROC curve image:
>
> `![Confusion Matrix](docs/confusion_matrix.png)`

---

## 📁 Project Structure

```
PhishGuard/
│
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── routes/                # API route handlers
│   │   ├── services/
│   │   │   ├── feature_extractor.py
│   │   │   ├── ml_predictor.py
│   │   │   ├── risk_engine.py
│   │   │   ├── explainer.py       # SHAP logic
│   │   │   ├── virustotal.py
│   │   │   └── email_analyzer.py
│   │   ├── models/                # Pydantic schemas
│   │   └── utils/
│   ├── model/
│   │   └── phishing_model.pkl     # Trained ML model
│   ├── data/                      # Dataset & history storage
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/ (or index.html, css, js)
│   ├── package.json
│   └── ...
│
├── notebooks/
│   └── model_training.ipynb
│
├── docs/                          # Screenshots & diagrams
├── README.md
└── LICENSE
```

> 📝 Edit this tree to mirror your real folder layout.

---

## 🛠️ Installation & Setup

### Prerequisites

- Python **3.10+**
- Node.js **18+** (if the frontend uses a build step)
- Git
- A free [VirusTotal API key](https://www.virustotal.com/gui/join-us)

### 1. Clone the Repository

```bash
git clone https://github.com/pranjul-tech-create/PhishGuard.git
cd PhishGuard
```

### 2. Backend Setup

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

---

## 🔐 Environment Variables

Create a `.env` file inside the `backend/` directory:

```env
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://phish-guard-lemon.vercel.app
ENVIRONMENT=development
```

For the frontend, create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
# or REACT_APP_API_BASE_URL / NEXT_PUBLIC_API_BASE_URL depending on your setup
```

> ⚠️ **Never commit `.env` files.** Make sure `.env` is listed in `.gitignore`.

---

## ▶️ Running the Project

### Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Start the Frontend

```bash
cd frontend
npm run dev
```

Open the URL shown in the terminal (typically `http://localhost:3000` or `http://localhost:5173`).

---

## 🔌 API Endpoints

Full interactive documentation is available at
👉 **[/docs](https://phishguard-backend-90ey.onrender.com/docs)**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/analyze/url` | Analyze a URL for phishing |
| `POST` | `/analyze/email` | Investigate a suspicious email |
| `GET` | `/history` | Retrieve past investigations |
| `GET` | `/history/{id}` | Get a specific investigation report |
| `DELETE` | `/history/{id}` | Delete an investigation record |

> 📝 Update paths to match the routes defined in your FastAPI app.

### Example Request

```bash
curl -X POST "https://phishguard-backend-90ey.onrender.com/analyze/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://secure-login-verify.example-bank.xyz/account"}'
```

### Example Response

```json
{
  "url": "http://secure-login-verify.example-bank.xyz/account",
  "ml_prediction": "phishing",
  "ml_confidence": 0.94,
  "rule_risk_score": 78,
  "virustotal": {
    "malicious": 7,
    "suspicious": 2,
    "harmless": 60,
    "undetected": 15
  },
  "final_risk_level": "High",
  "explanation": [
    { "feature": "suspicious_keyword_count", "impact": 0.18 },
    { "feature": "no_https", "impact": 0.09 }
  ],
  "timestamp": "2026-10-02T10:30:00Z"
}
```

---

## ☁️ Deployment

| Service | Platform | Notes |
|---------|----------|-------|
| **Frontend** | [Vercel](https://vercel.com) | Auto-deploys from the `master` branch |
| **Backend** | [Render](https://render.com) | Web service running Uvicorn |

### Backend on Render

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment variables:** add `VIRUSTOTAL_API_KEY` and `ALLOWED_ORIGINS` in the Render dashboard.

### Frontend on Vercel

- Import the GitHub repo and set the root directory to `frontend/`.
- Add `API_BASE_URL` pointing to the Render backend.

---

## 🔒 Security Considerations

- API keys are stored in environment variables, never in source code.
- CORS is restricted to trusted origins.
- User-submitted URLs are **analyzed, never visited or executed** by the server.
- Input validation is enforced with Pydantic schemas.
- Rate limiting is recommended for public deployments to protect VirusTotal quota.
- Analyze suspicious links only through PhishGuard — **do not open them directly in your browser.**

---

## ⚠️ Limitations

- ML accuracy depends on the training dataset and may degrade against novel attack patterns (concept drift).
- Detection is primarily URL-feature based; page content and visual similarity are not analyzed.
- VirusTotal's free API tier has rate limits (about 4 requests/minute).
- Email analysis is heuristic-based and may produce false positives on legitimate marketing emails.
- The free-tier backend may have cold-start delays.
- PhishGuard is an **assistive tool** and should not replace professional security judgment.

---

## 🚀 Future Enhancements

- [ ] Browser extension for real-time link scanning
- [ ] Webpage content and HTML analysis
- [ ] Visual similarity detection (logo / brand impersonation)
- [ ] WHOIS and domain-age enrichment
- [ ] Deep learning / transformer-based email classification
- [ ] Attachment sandboxing
- [ ] User authentication and per-user history
- [ ] Batch scanning and CSV export
- [ ] PDF investigation report download
- [ ] Docker containerization and CI/CD pipeline
- [ ] Multi-language phishing email detection

---

## 🎓 Learning Outcomes

Building PhishGuard provided hands-on experience with:

- End-to-end ML workflow: data → features → training → deployment
- Designing hybrid detection systems (ML + rules + threat intel)
- Explainable AI using SHAP
- Building and documenting REST APIs with FastAPI
- Integrating third-party security APIs
- Phishing attack patterns and email forensics
- Full-stack deployment on Vercel and Render

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Pranjul**
B.Tech Computer Science (Cyber Security & Digital Forensics) — VIT  University

- 💻 GitHub: [@pranjul-tech-create](https://github.com/pranjul-tech-create)
- 🔗 Project: [PhishGuard](https://github.com/pranjul-tech-create/PhishGuard)

---

<div align="center">

⭐ If you found this project useful, consider giving it a star!

**Detect. Investigate. Explain. Protect.** 🛡️

</div>
