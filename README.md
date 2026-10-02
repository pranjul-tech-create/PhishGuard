# 🛡️ PhishGuard

### AI-Powered Phishing Detection & Investigation Platform

<p align="center">
  <img src="https://img.shields.io/badge/PhishGuard-AI%20Cybersecurity-0A66C2?style=for-the-badge&logo=shield&logoColor=white" alt="PhishGuard"/>
</p>

<p align="center">
  <strong>Detect • Investigate • Explain</strong>
</p>

<p align="center">
  <a href="https://phish-guard-lemon.vercel.app">
    <img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-Open%20PhishGuard-00C853?style=for-the-badge" alt="Live Demo"/>
  </a>
  &nbsp;
  <a href="https://github.com/pranjul-tech-create/PhishGuard">
    <img src="https://img.shields.io/badge/💻%20SOURCE%20CODE-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

---

## 🚀 Live Demo

### 👉 [Open PhishGuard](https://phish-guard-lemon.vercel.app)

> PhishGuard is deployed as a full-stack application with a React frontend on Vercel and a FastAPI backend on Render.

<p align="center">

  <a href="https://phish-guard-lemon.vercel.app">
    <img src="https://img.shields.io/badge/Frontend-Vercel-black?style=flat-square&logo=vercel&logoColor=white" alt="Vercel"/>
  </a>

  <a href="https://phishguard-backend-90ey.onrender.com/docs">
    <img src="https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  </a>

  <a href="https://github.com/pranjul-tech-create/PhishGuard">
    <img src="https://img.shields.io/github/stars/pranjul-tech-create/PhishGuard?style=flat-square&logo=github" alt="GitHub Stars"/>
  </a>

</p>

---

# 🛡️ What is PhishGuard?

**PhishGuard** is an AI-powered phishing detection and investigation platform designed to analyze:

- 🔗 Suspicious URLs
- 📧 Phishing emails
- 🌐 Domain and URL characteristics
- 🤖 Machine-learning predictions
- 🧠 Explainable AI signals
- 🛡️ Rule-based security indicators
- 🔍 VirusTotal threat intelligence
- 📊 Investigation history

Instead of depending on a single detection technique, PhishGuard combines multiple security signals into a unified investigation workflow.

---

# ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **Machine Learning** | Random Forest phishing classification |
| 🧠 **Explainable AI** | SHAP-based feature explanations |
| 🔗 **URL Analysis** | Extracts security-related URL features |
| 🛡️ **Rule Engine** | Calculates deterministic risk indicators |
| 🌐 **VirusTotal** | External threat-intelligence enrichment |
| 📧 **Email Analysis** | `.eml` header, content and URL analysis |
| 🔍 **URL Extraction** | Extracts URLs from suspicious emails |
| 💾 **Investigation History** | Stores previous investigations |
| 📊 **Dashboard** | Displays investigation statistics |
| 🚀 **Live Deployment** | Vercel + Render |

---

# 🧠 Detection Architecture

```text
                         ┌─────────────────────┐
                         │   Suspicious Input  │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                  🔗 Suspicious URL       📧 Email
                         │                     │
                         ▼                     ▼
                  Feature Extraction     Email Analysis
                         │                     │
                         ▼                     ▼
                  🤖 ML Prediction       Header Analysis
                         │                     │
                         ▼                     ▼
                   🧠 SHAP Analysis      URL Extraction
                         │                     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                           🛡️ Rule Engine
                                    │
                                    ▼
                         🌐 VirusTotal Intel
                                    │
                                    ▼
                         🎯 Final Assessment
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                  🟢 LOW         🟡 MEDIUM        🔴 HIGH
