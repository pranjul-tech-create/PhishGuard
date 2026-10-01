import React, { useState, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [url, setUrl] = useState("");
  const [urlResult, setUrlResult] = useState(null);
  const [urlLoading, setUrlLoading] = useState(false);
  const [urlError, setUrlError] = useState("");

  const [emailFile, setEmailFile] = useState(null);
  const [emailResult, setEmailResult] = useState(null);
  const [emailLoading, setEmailLoading] = useState(false);
  const [emailError, setEmailError] = useState("");

  const [activeTab, setActiveTab] = useState("url");

  const [history, setHistory] = useState([]);

  const [selectedInvestigation, setSelectedInvestigation] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [detailsError, setDetailsError] = useState("");

  const [dashboardStats, setDashboardStats] = useState({
    total: 0,
    high: 0,
    medium: 0,
    low: 0,
  });

  // ============================================================
  // LOAD DATABASE DATA
  // ============================================================

  useEffect(() => {
    loadInvestigationHistory();
    loadDashboardStats();
  }, []);

  const loadInvestigationHistory = async () => {
    try {
      const response = await fetch(
        `${API_URL}/investigations`
      );

      if (!response.ok) {
        throw new Error(
          "Failed to load investigation history"
        );
      }

      const data = await response.json();

      setHistory(data);
    } catch (error) {
      console.error(
        "Error loading investigation history:",
        error
      );
    }
  };

  const loadDashboardStats = async () => {
    try {
      const response = await fetch(
        `${API_URL}/dashboard-stats`
      );

      if (!response.ok) {
        throw new Error(
          "Failed to load dashboard statistics"
        );
      }

      const data = await response.json();

      setDashboardStats(data);
    } catch (error) {
      console.error(
        "Error loading dashboard statistics:",
        error
      );
    }
  };

  // ============================================================
  // RISK CLASS
  // ============================================================

  const getRiskClass = (level) => {
    if (level === "HIGH") return "risk-high";
    if (level === "MEDIUM") return "risk-medium";
    return "risk-low";
  };

  // ============================================================
  // REFRESH DASHBOARD DATA
  // ============================================================

  const refreshDashboard = async () => {
    await Promise.all([
      loadInvestigationHistory(),
      loadDashboardStats(),
    ]);
  };

  // ============================================================
  // INVESTIGATION DETAILS
  // ============================================================

  const handleViewDetails = async (id) => {
    if (!id) return;

    setDetailsLoading(true);
    setDetailsError("");
    setSelectedInvestigation(null);

    try {
      const response = await fetch(
        `${API_URL}/investigations/${id}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to load investigation details."
        );
      }

      setSelectedInvestigation(data);
    } catch (error) {
      setDetailsError(
        error.message || "Something went wrong."
      );
    } finally {
      setDetailsLoading(false);
    }
  };

  // ============================================================
  // URL SCAN
  // ============================================================

  const handleUrlScan = async () => {
    if (!url.trim()) {
      setUrlError("Please enter a URL.");
      return;
    }

    setUrlLoading(true);
    setUrlError("");
    setUrlResult(null);

    try {
      const response = await fetch(
        `${API_URL}/scan`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: url.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "URL scan failed."
        );
      }

      setUrlResult(data);

      // Reload database history and statistics
      await refreshDashboard();

    } catch (error) {
      setUrlError(
        error.message ||
          "Something went wrong."
      );
    } finally {
      setUrlLoading(false);
    }
  };

  // ============================================================
  // EMAIL ANALYSIS
  // ============================================================

  const handleEmailAnalysis = async () => {
    if (!emailFile) {
      setEmailError(
        "Please select an .eml file."
      );
      return;
    }

    setEmailLoading(true);
    setEmailError("");
    setEmailResult(null);

    try {
      const formData = new FormData();

      formData.append(
        "file",
        emailFile
      );

      const response = await fetch(
        `${API_URL}/analyze-email`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Email analysis failed."
        );
      }

      setEmailResult(data);

      /*
       * NOTE:
       * Your current backend saves URL investigations
       * to SQLite, but does not yet save the email itself.
       *
       * Therefore the dashboard statistics currently
       * represent investigations saved by /scan.
       */
      await refreshDashboard();

    } catch (error) {
      setEmailError(
        error.message ||
          "Something went wrong."
      );
    } finally {
      setEmailLoading(false);
    }
  };

  // ============================================================
  // SHAP / ML EXPLANATION
  // ============================================================

  const renderMlExplanation = (result) => {
    const explanation = result?.ml_explanation;

    if (!Array.isArray(explanation) || explanation.length === 0) {
      return (
        <div className="section">
          <h3 className="section-title">
            🧠 ML Risk Explanation
          </h3>

          <div className="reason">
            SHAP explanation data was not returned by the backend.
          </div>
        </div>
      );
    }

    return (
      <div className="section">
        <h3 className="section-title">
          🧠 ML Risk Explanation
        </h3>

        <div className="panel-subtitle">
          SHAP shows how each feature contributed toward the
          model's predicted class for this URL. It is separate
          from the rule-based risk score.
        </div>

        <div className="shap-list">
          {explanation.map((item, index) => {
            const impact = Number(item.impact || 0);
            const direction =
              item.direction ||
              (impact >= 0 ? "phishing" : "legitimate");

            const directionLabel =
              direction.toLowerCase() === "phishing"
                ? "→ Phishing"
                : "→ Legitimate";

            const impactText =
              `${impact >= 0 ? "+" : ""}${impact.toFixed(4)}`;

            return (
              <div className="shap-item" key={`${item.feature}-${index}`}>
                <div className="shap-feature">
                  {item.feature}
                </div>

                <div className="shap-value">
                  {String(item.value)}
                </div>

                <div className="shap-impact">
                  {impactText}
                </div>

                <div className="shap-direction">
                  {directionLabel}
                </div>
              </div>
            );
          })}
        </div>

        <div className="stat-small">
          Positive/negative impact is shown relative to the
          predicted class returned by the ML model.
        </div>
      </div>
    );
  };

  // ============================================================
  // URL RESULT
  // ============================================================

  const renderUrlResult = () => {
    if (!urlResult) {
      return null;
    }

    const finalAssessment =
      urlResult.final_assessment || {};

    const ruleRisk =
      urlResult.rule_risk || {};

    const threat =
      urlResult.threat_intelligence || {};

    const features =
      urlResult.features || {};

    const reasons =
      finalAssessment.reasons || [];

    return (
      <div className="result">

        {/* FINAL RISK */}

        <div className="risk-card">

          <div className="risk-label">
            FINAL RISK ASSESSMENT
          </div>

          <div
            className={`risk-level ${getRiskClass(
              finalAssessment.level
            )}`}
          >
            {finalAssessment.level}
          </div>

          <div className="risk-score">
            {finalAssessment.score}
            <span>/100</span>
          </div>

          <div className="risk-bar">
            <div
              className={`risk-fill ${getRiskClass(
                finalAssessment.level
              )}`}
              style={{
                width: `${finalAssessment.score || 0}%`,
              }}
            />
          </div>
        </div>

        {/* WHY FLAGGED */}

        <div className="section">

          <h3 className="section-title">
            ⚠ Why was this URL flagged?
          </h3>

          <div className="reason-list">

            {reasons.length > 0 ? (
              reasons.map(
                (reason, index) => (
                  <div
                    className="reason"
                    key={index}
                  >
                    ⚠ {reason}
                  </div>
                )
              )
            ) : (
              <div className="reason">
                No specific reasons were returned.
              </div>
            )}

          </div>
        </div>

        {/* URL STATISTICS */}

        <div className="stats-grid">

          <div className="stat-card">
            <div className="stat-title">
              Machine Learning
            </div>

            <div className="stat-value">
              {urlResult.prediction}
            </div>

            <div className="stat-small">
              Confidence:{" "}
              {urlResult.ml_confidence}%
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-title">
              Rule Engine
            </div>

            <div className="stat-value">
              {ruleRisk.score}/100
            </div>

            <div className="stat-small">
              {ruleRisk.level}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-title">
              VirusTotal
            </div>

            <div className="stat-value">
              {threat.available
                ? "Available"
                : "Unavailable"}
            </div>

            <div className="stat-small">
              Malicious:{" "}
              {threat.malicious || 0}
            </div>
          </div>

        </div>

        {/* SHAP ML EXPLANATION */}

        {renderMlExplanation(urlResult)}

        {/* RULE ENGINE */}

        <div className="section">

          <h3 className="section-title">
            🛡 Rule-Based Analysis
          </h3>

          {ruleRisk.reasons &&
          ruleRisk.reasons.length > 0 ? (
            <div className="reason-list">

              {ruleRisk.reasons.map(
                (reason, index) => (
                  <div
                    className="reason"
                    key={index}
                  >
                    • {reason}
                  </div>
                )
              )}

            </div>
          ) : (
            <div className="reason">
              No rule-based warnings detected.
            </div>
          )}

        </div>

        {/* THREAT INTELLIGENCE */}

        <div className="section">

          <h3 className="section-title">
            🌐 Threat Intelligence
          </h3>

          <div className="info-grid">

            <div>
              <div className="info-label">
                Status
              </div>

              <div className="info-value">
                {threat.available
                  ? "Available"
                  : "Unavailable"}
              </div>
            </div>

            <div>
              <div className="info-label">
                Malicious
              </div>

              <div className="info-value">
                {threat.malicious || 0}
              </div>
            </div>

            <div>
              <div className="info-label">
                Suspicious
              </div>

              <div className="info-value">
                {threat.suspicious || 0}
              </div>
            </div>

            <div>
              <div className="info-label">
                Harmless
              </div>

              <div className="info-value">
                {threat.harmless || 0}
              </div>
            </div>

            <div>
              <div className="info-label">
                Undetected
              </div>

              <div className="info-value">
                {threat.undetected || 0}
              </div>
            </div>

          </div>

          <div className="code-block">
            {threat.message ||
              "No threat intelligence message available."}
          </div>

        </div>

        {/* FEATURES */}

        <div className="section">

          <h3 className="section-title">
            🔍 Extracted URL Features
          </h3>

          <div className="info-grid">

            {Object.entries(features).map(
              ([key, value]) => (
                <div key={key}>

                  <div className="info-label">
                    {key}
                  </div>

                  <div className="info-value">
                    {String(value)}
                  </div>

                </div>
              )
            )}

          </div>

        </div>

      </div>
    );
  };

  // ============================================================
  // EMAIL RESULT
  // ============================================================

  const renderEmailResult = () => {
    if (!emailResult) {
      return null;
    }

    const email =
      emailResult.email_analysis || {};

    const assessment =
      emailResult.final_assessment || {};

    const reasons =
      assessment.reasons || [];

    return (
      <div className="result">

        {/* FINAL EMAIL RISK */}

        <div className="risk-card">

          <div className="risk-label">
            FINAL EMAIL RISK ASSESSMENT
          </div>

          <div
            className={`risk-level ${getRiskClass(
              assessment.level
            )}`}
          >
            {assessment.level}
          </div>

          <div className="risk-score">
            {assessment.score}
            <span>/100</span>
          </div>

          <div className="risk-bar">

            <div
              className={`risk-fill ${getRiskClass(
                assessment.level
              )}`}
              style={{
                width: `${assessment.score || 0}%`,
              }}
            />

          </div>

        </div>

        {/* WHY FLAGGED */}

        <div className="section">

          <h3 className="section-title">
            ⚠ Why was this email flagged?
          </h3>

          <div className="reason-list">

            {reasons.length > 0 ? (
              reasons.map(
                (reason, index) => (
                  <div
                    className="reason"
                    key={index}
                  >
                    ⚠ {reason}
                  </div>
                )
              )
            ) : (
              <div className="reason">
                No specific reasons were returned.
              </div>
            )}

          </div>

        </div>

        {/* EMAIL INFORMATION */}

        <div className="section">

          <h3 className="section-title">
            📧 Email Information
          </h3>

          <div className="info-grid">

            <div>
              <div className="info-label">
                Sender
              </div>

              <div className="info-value">
                {email.sender || "N/A"}
              </div>
            </div>

            <div>
              <div className="info-label">
                Recipient
              </div>

              <div className="info-value">
                {email.recipient || "N/A"}
              </div>
            </div>

            <div>
              <div className="info-label">
                Subject
              </div>

              <div className="info-value">
                {email.subject || "N/A"}
              </div>
            </div>

            <div>
              <div className="info-label">
                Reply-To
              </div>

              <div className="info-value">
                {email.reply_to || "N/A"}
              </div>
            </div>

          </div>

        </div>

        {/* SUSPICIOUS KEYWORDS */}

        <div className="section">

          <h3 className="section-title">
            🚨 Suspicious Keywords
          </h3>

          <div className="tags">

            {email.suspicious_keywords?.length > 0 ? (
              email.suspicious_keywords.map(
                (keyword, index) => (
                  <span
                    className="tag"
                    key={index}
                  >
                    {keyword}
                  </span>
                )
              )
            ) : (
              <div className="stat-small">
                No suspicious keywords detected.
              </div>
            )}

          </div>

        </div>

        {/* ATTACHMENTS */}

        <div className="section">

          <h3 className="section-title">
            📎 Attachments
          </h3>

          {email.attachments?.length > 0 ? (
            <div className="tags">

              {email.attachments.map(
                (attachment, index) => (
                  <span
                    className="tag"
                    key={index}
                  >
                    {attachment}
                  </span>
                )
              )}

            </div>
          ) : (
            <div className="stat-small">
              No attachments detected.
            </div>
          )}

        </div>

        {/* AUTHENTICATION */}

        <div className="section">

          <h3 className="section-title">
            🔐 Email Authentication
          </h3>

          <div className="code-block">
            {email.authentication_results ||
              "No Authentication-Results header found."}
          </div>

        </div>

        {/* URLS INSIDE EMAIL */}

        <div className="section">

          <h3 className="section-title">
            🔗 URL Investigation
          </h3>

          {emailResult.url_analysis?.length > 0 ? (

            emailResult.url_analysis.map(
              (item, index) => (

                <div
                  className="url-investigation"
                  key={index}
                >

                  <div className="url-link">
                    {item.url}
                  </div>

                  {item.error ? (

                    <div className="reason">
                      ⚠ {item.error}
                    </div>

                  ) : (

                    <>

                      <div className="url-result-grid">

                        <div className="url-stat">
                          <div className="url-stat-label">
                            Prediction
                          </div>

                          <div className="url-stat-value">
                            {item.prediction}
                          </div>
                        </div>

                        <div className="url-stat">
                          <div className="url-stat-label">
                            ML Confidence
                          </div>

                          <div className="url-stat-value">
                            {item.ml_confidence}%
                          </div>
                        </div>

                        <div className="url-stat">
                          <div className="url-stat-label">
                            Final Risk
                          </div>

                          <div className="url-stat-value">
                            {item.final_assessment?.level}
                            {" "}
                            (
                            {item.final_assessment?.score}
                            /100)
                          </div>
                        </div>

                      </div>

                      <div className="reason-list">

                        {item.final_assessment?.reasons?.map(
                          (reason, reasonIndex) => (
                            <div
                              className="reason"
                              key={reasonIndex}
                            >
                              ⚠ {reason}
                            </div>
                          )
                        )}

                      </div>

                    </>

                  )}

                </div>

              )
            )

          ) : (

            <div className="stat-small">
              No URLs found inside this email.
            </div>

          )}

        </div>

      </div>
    );
  };

  // ============================================================
  // HISTORICAL INVESTIGATION ANALYSIS
  // ============================================================

  const buildInvestigationAnalysis = (target) => {
    const empty = {
      features: {},
      ruleScore: 0,
      ruleLevel: "LOW",
      reasons: [],
      isUrl: false,
    };

    if (!target || !/^https?:\/\//i.test(target)) {
      return empty;
    }

    try {
      const parsed = new URL(target);
      const hostname = parsed.hostname || "";
      const hostParts = hostname.split(".").filter(Boolean);

      // Approximate the Python tldextract domain value.
      let domain = hostname;
      if (hostParts.length >= 2) {
        domain = hostParts[hostParts.length - 2];
      }

      const subdomain =
        hostParts.length > 2
          ? hostParts.slice(0, -2).join(".")
          : "";

      const suspiciousWords = [
        "login",
        "verify",
        "verification",
        "account",
        "update",
        "secure",
        "password",
        "signin",
        "bank",
        "confirm",
        "wallet",
      ];

      const lowerUrl = target.toLowerCase();

      let suspiciousKeywordCount = 0;
      suspiciousWords.forEach((word) => {
        if (lowerUrl.includes(word)) {
          suspiciousKeywordCount += 1;
        }
      });

      const hasIp =
        /^(?:\d{1,3}\.){3}\d{1,3}$/.test(hostname);

      const features = {
        url_length: target.length,
        domain_length: domain.length,
        subdomain_length: subdomain.length,
        num_dots: (target.match(/\./g) || []).length,
        num_hyphens: (target.match(/-/g) || []).length,
        num_digits: (target.match(/\d/g) || []).length,
        num_special_chars: (target.match(/[^a-zA-Z0-9]/g) || []).length,
        uses_https: parsed.protocol === "https:" ? 1 : 0,
        has_ip: hasIp ? 1 : 0,
        suspicious_keyword_count: suspiciousKeywordCount,
        path_length: parsed.pathname.length,
        query_length: parsed.search
          ? parsed.search.substring(1).length
          : 0,
      };

      let ruleScore = 0;
      const reasons = [];

      if (features.has_ip === 1) {
        ruleScore += 25;
        reasons.push(
          "URL uses an IP address instead of a normal domain."
        );
      }

      if (features.uses_https === 0) {
        ruleScore += 15;
        reasons.push("URL does not use HTTPS.");
      }

      if (suspiciousKeywordCount >= 3) {
        ruleScore += 25;
        reasons.push(
          `URL contains ${suspiciousKeywordCount} suspicious keywords.`
        );
      } else if (suspiciousKeywordCount > 0) {
        ruleScore += 10;
        reasons.push(
          `URL contains ${suspiciousKeywordCount} suspicious keyword(s).`
        );
      }

      if (features.url_length > 100) {
        ruleScore += 15;
        reasons.push("URL is unusually long.");
      } else if (features.url_length > 75) {
        ruleScore += 10;
        reasons.push("URL is relatively long.");
      }

      if (features.subdomain_length > 20) {
        ruleScore += 10;
        reasons.push(
          "URL contains an unusually long subdomain."
        );
      }

      if (features.num_special_chars > 15) {
        ruleScore += 10;
        reasons.push(
          "URL contains many special characters."
        );
      }

      ruleScore = Math.min(ruleScore, 100);

      const ruleLevel =
        ruleScore >= 70
          ? "HIGH"
          : ruleScore >= 40
            ? "MEDIUM"
            : "LOW";

      return {
        features,
        ruleScore,
        ruleLevel,
        reasons,
        isUrl: true,
      };
    } catch {
      return empty;
    }
  };

  // ============================================================
  // MAIN UI
  // ============================================================

  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div className="header-content">

          <div className="logo">

            <div className="logo-icon">
              🛡️
            </div>

            <div>
              <h1>
                PhishGuard
              </h1>

              <p>
                AI-Powered Phishing Detection &
                Investigation Platform
              </p>
            </div>

          </div>

          <div className="status">
            <span className="status-dot"></span>
            API Online
          </div>

        </div>

      </header>

      {/* MAIN */}

      <main className="main">

        {/* DASHBOARD OVERVIEW */}

        <section className="dashboard-overview">

          <div className="overview-header">
            <div>
              <h2>
                Security Operations Dashboard
              </h2>

              <p>
                Investigation overview and threat activity
              </p>
            </div>

            <button
              className="refresh-button"
              onClick={refreshDashboard}
            >
              ↻ Refresh
            </button>
          </div>

          <div className="dashboard-stats-grid">

            <div className="dashboard-stat-card">
              <div className="dashboard-stat-icon">
                🔎
              </div>

              <div>
                <div className="dashboard-stat-label">
                  TOTAL INVESTIGATIONS
                </div>

                <div className="dashboard-stat-value">
                  {dashboardStats.total}
                </div>
              </div>
            </div>

            <div className="dashboard-stat-card high-card">
              <div className="dashboard-stat-icon">
                🚨
              </div>

              <div>
                <div className="dashboard-stat-label">
                  HIGH RISK
                </div>

                <div className="dashboard-stat-value">
                  {dashboardStats.high}
                </div>
              </div>
            </div>

            <div className="dashboard-stat-card medium-card">
              <div className="dashboard-stat-icon">
                ⚠️
              </div>

              <div>
                <div className="dashboard-stat-label">
                  MEDIUM RISK
                </div>

                <div className="dashboard-stat-value">
                  {dashboardStats.medium}
                </div>
              </div>
            </div>

            <div className="dashboard-stat-card low-card">
              <div className="dashboard-stat-icon">
                ✓
              </div>

              <div>
                <div className="dashboard-stat-label">
                  LOW RISK
                </div>

                <div className="dashboard-stat-value">
                  {dashboardStats.low}
                </div>
              </div>
            </div>

          </div>

        </section>

        {/* TABS */}

        <div className="tabs">

          <button
            className={`tab ${
              activeTab === "url"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActiveTab("url")
            }
          >
            🔗 URL Scanner
          </button>

          <button
            className={`tab ${
              activeTab === "email"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActiveTab("email")
            }
          >
            📧 Email Analyzer
          </button>

        </div>

        {/* URL TAB */}

        {activeTab === "url" && (

          <div className="panel">

            <div className="panel-title">
              Analyze a Suspicious URL
            </div>

            <div className="panel-subtitle">
              Combine machine learning, rule-based
              analysis and threat intelligence.
            </div>

            <div className="input-row">

              <input
                className="url-input"
                type="text"
                placeholder="Enter suspicious URL..."
                value={url}
                onChange={(event) =>
                  setUrl(event.target.value)
                }
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    handleUrlScan();
                  }
                }}
              />

              <button
                className="primary-button"
                onClick={handleUrlScan}
                disabled={urlLoading}
              >
                {urlLoading
                  ? "Scanning..."
                  : "🔍 Scan URL"}
              </button>

            </div>

            {urlError && (
              <div className="error">
                ⚠ {urlError}
              </div>
            )}

            {renderUrlResult()}

          </div>

        )}

        {/* EMAIL TAB */}

        {activeTab === "email" && (

          <div className="panel">

            <div className="panel-title">
              Analyze a Suspicious Email
            </div>

            <div className="panel-subtitle">
              Upload an .eml file to investigate
              headers, keywords, attachments and URLs.
            </div>

            <div className="upload-box">

              <div className="upload-icon">
                📧
              </div>

              <input
                className="file-input"
                type="file"
                accept=".eml"
                onChange={(event) =>
                  setEmailFile(
                    event.target.files?.[0] ||
                      null
                  )
                }
              />

              {emailFile && (
                <div className="stat-small">
                  Selected:{" "}
                  {emailFile.name}
                </div>
              )}

              <button
                className="primary-button"
                onClick={handleEmailAnalysis}
                disabled={emailLoading}
              >
                {emailLoading
                  ? "Analyzing..."
                  : "📧 Analyze Email"}
              </button>

            </div>

            {emailError && (
              <div className="error">
                ⚠ {emailError}
              </div>
            )}

            {renderEmailResult()}

          </div>

        )}

        {/* HISTORY */}

        {history.length > 0 && (

          <div className="history">

            <div className="history-header">

              <div>
                <div className="history-title">
                  Recent Investigations
                </div>

                <div className="history-subtitle">
                  Latest investigations stored in PhishGuard
                </div>
              </div>

              <div className="history-count">
                {history.length}
              </div>

            </div>

            <div className="history-list">

              {history.map(
                (item, index) => {

                  const type =
                    item.investigation_type ||
                    item.type ||
                    "URL";

                  const name =
                    item.target ||
                    item.name ||
                    "Unknown";

                  const level =
                    item.risk_level ||
                    item.level ||
                    "UNKNOWN";

                  const score =
                    item.risk_score ??
                    item.score ??
                    0;

                  const timestamp =
                    item.created_at ||
                    item.time ||
                    "";

                  return (
                    <div
                      className="history-item"
                      key={item.id || index}
                    >

                      <div className="history-icon">
                        {type.toLowerCase() === "email"
                          ? "📧"
                          : "🔗"}
                      </div>

                      <div className="history-name">

                        <div className="history-type">
                          {type}
                        </div>

                        <div className="history-target">
                          {name}
                        </div>

                        <div className="history-time">
                          {timestamp}
                        </div>

                      </div>

                      <div
                        className={`history-risk ${getRiskClass(
                          level
                        )}`}
                      >
                        {level}
                      </div>

                      <div className="history-score">
                        {score}/100
                      </div>

                      <button
                        type="button"
                        className="view-details-button"
                        onClick={() => handleViewDetails(item.id)}
                        style={{
                          background: "#111827",
                          color: "#dbeafe",
                          border: "1px solid #334155",
                          borderRadius: "8px",
                          padding: "10px 16px",
                          fontSize: "14px",
                          fontWeight: "600",
                          cursor: "pointer",
                          whiteSpace: "nowrap",
                          transition: "all 0.2s ease"
                        }}
                      >
                        View Details
                      </button>

                    </div>
                  );
                }
              )}

            </div>

          </div>

        )}

        {/* INVESTIGATION DETAILS */}

        {detailsLoading && (
          <div className="section investigation-details">
            <div className="stat-small">
              Loading investigation details...
            </div>
          </div>
        )}

        {detailsError && (
          <div className="error">
            ⚠ {detailsError}
          </div>
        )}

        {selectedInvestigation && (
          <div className="section investigation-details">
            {(() => {
              const analysis = buildInvestigationAnalysis(
                selectedInvestigation.target
              );

              // Prefer evidence stored by the backend.
              // Fall back to the older reconstructed analysis only
              // for investigations created before the database upgrade.
              const storedRuleReasons =
                selectedInvestigation.rule_reasons
                  ? selectedInvestigation.rule_reasons
                      .split("\n")
                      .map((item) => item.trim())
                      .filter(Boolean)
                  : analysis.reasons;

              const storedFeatures = {};

              if (selectedInvestigation.url_features) {
                selectedInvestigation.url_features
                  .split("\n")
                  .forEach((item) => {
                    const separatorIndex = item.indexOf("=");

                    if (separatorIndex === -1) return;

                    const key = item.substring(0, separatorIndex);
                    const value = item.substring(separatorIndex + 1);

                    storedFeatures[key] = value;
                  });
              }

              const displayedFeatures =
                Object.keys(storedFeatures).length > 0
                  ? storedFeatures
                  : analysis.features;

              const displayedRuleScore =
                selectedInvestigation.rule_score !== null &&
                selectedInvestigation.rule_score !== undefined
                  ? selectedInvestigation.rule_score
                  : analysis.ruleScore;

              const displayedRuleLevel =
                selectedInvestigation.rule_level ||
                analysis.ruleLevel;

              const hasThreatIntelData =
                selectedInvestigation.vt_available !== null &&
                selectedInvestigation.vt_available !== undefined;

              return (
                <>
                  <h3 className="section-title">
                    🔎 Investigation Details
                  </h3>

                  {/* STORED INVESTIGATION DATA */}

                  <div className="stats-grid">
                    <div className="stat-card">
                      <div className="stat-title">
                        ML Prediction
                      </div>
                      <div className="stat-value">
                        {selectedInvestigation.prediction || "N/A"}
                      </div>
                      <div className="stat-small">
                        {selectedInvestigation.ml_confidence !== null &&
                        selectedInvestigation.ml_confidence !== undefined
                          ? `Confidence: ${Number(
                              selectedInvestigation.ml_confidence
                            ).toFixed(2)}%`
                          : "Confidence not stored"}
                      </div>
                    </div>

                    <div className="stat-card">
                      <div className="stat-title">
                        Final Risk
                      </div>
                      <div className="stat-value">
                        {selectedInvestigation.risk_score}/100
                      </div>
                      <div className="stat-small">
                        {selectedInvestigation.risk_level}
                      </div>
                    </div>

                    <div className="stat-card">
                      <div className="stat-title">
                        Rule Engine
                      </div>
                      <div className="stat-value">
                        {analysis.isUrl
                          ? `${displayedRuleScore}/100`
                          : "N/A"}
                      </div>
                      <div className="stat-small">
                        {analysis.isUrl
                          ? displayedRuleLevel
                          : "Not available"}
                      </div>
                    </div>
                  </div>

                  {/* INVESTIGATION METADATA */}

                  <div className="section">
                    <h3 className="section-title">
                      📋 Investigation Metadata
                    </h3>

                    <div className="info-grid">
                      <div>
                        <div className="info-label">
                          Investigation ID
                        </div>
                        <div className="info-value">
                          {selectedInvestigation.id}
                        </div>
                      </div>

                      <div>
                        <div className="info-label">
                          Type
                        </div>
                        <div className="info-value">
                          {selectedInvestigation.investigation_type}
                        </div>
                      </div>

                      <div>
                        <div className="info-label">
                          Risk Level
                        </div>
                        <div className="info-value">
                          {selectedInvestigation.risk_level}
                        </div>
                      </div>

                      <div>
                        <div className="info-label">
                          Created At
                        </div>
                        <div className="info-value">
                          {selectedInvestigation.created_at}
                        </div>
                      </div>
                    </div>

                    <div className="investigation-target">
                      <div className="info-label">
                        Target
                      </div>
                      <div className="code-block">
                        {selectedInvestigation.target}
                      </div>
                    </div>
                  </div>

                  {/* RULE ANALYSIS */}

                  {analysis.isUrl && (
                    <div className="section">
                      <h3 className="section-title">
                        🛡 Rule-Based Analysis
                      </h3>

                      {storedRuleReasons.length > 0 ? (
                        <div className="reason-list">
                          {storedRuleReasons.map(
                            (reason, index) => (
                              <div
                                className="reason"
                                key={index}
                              >
                                ⚠ {reason}
                              </div>
                            )
                          )}
                        </div>
                      ) : (
                        <div className="reason">
                          ✓ No rule-based warnings detected.
                        </div>
                      )}
                    </div>
                  )}

                  {/* URL FEATURES */}

                  {analysis.isUrl && (
                    <div className="section">
                      <h3 className="section-title">
                        🔍 Extracted URL Features
                      </h3>

                      <div className="info-grid">
                        {Object.entries(
                          displayedFeatures
                        ).map(([key, value]) => (
                          <div key={key}>
                            <div className="info-label">
                              {key}
                            </div>
                            <div className="info-value">
                              {String(value)}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* THREAT INTELLIGENCE */}

                  <div className="section">
                    <h3 className="section-title">
                      🌐 Threat Intelligence
                    </h3>

                    {hasThreatIntelData ? (
                      <>
                        <div className="stats-grid">
                          <div className="stat-card">
                            <div className="stat-title">
                              VirusTotal Status
                            </div>
                            <div className="stat-value">
                              {Number(
                                selectedInvestigation.vt_available
                              ) === 1
                                ? "Available"
                                : "Unavailable"}
                            </div>
                          </div>

                          <div className="stat-card">
                            <div className="stat-title">
                              Malicious
                            </div>
                            <div className="stat-value">
                              {selectedInvestigation.vt_malicious ?? 0}
                            </div>
                          </div>

                          <div className="stat-card">
                            <div className="stat-title">
                              Suspicious
                            </div>
                            <div className="stat-value">
                              {selectedInvestigation.vt_suspicious ?? 0}
                            </div>
                          </div>

                          <div className="stat-card">
                            <div className="stat-title">
                              Harmless
                            </div>
                            <div className="stat-value">
                              {selectedInvestigation.vt_harmless ?? 0}
                            </div>
                          </div>

                          <div className="stat-card">
                            <div className="stat-title">
                              Undetected
                            </div>
                            <div className="stat-value">
                              {selectedInvestigation.vt_undetected ?? 0}
                            </div>
                          </div>
                        </div>

                        <div className="code-block">
                          {selectedInvestigation.vt_message ||
                            "No VirusTotal message was stored."}
                        </div>
                      </>
                    ) : (
                      <div className="code-block">
                        VirusTotal evidence was not stored for this
                        investigation because it was created before
                        the investigation evidence upgrade.
                      </div>
                    )}
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={() =>
                      setSelectedInvestigation(null)
                    }
                  >
                    Close Details
                  </button>
                </>
              );
            })()}
          </div>
        )}

      </main>

      {/* FOOTER */}

      <footer className="footer">

        <p>
          PhishGuard — AI-Powered Phishing
          Detection & Investigation Platform
        </p>

      </footer>

    </div>
  );
}

export default App;