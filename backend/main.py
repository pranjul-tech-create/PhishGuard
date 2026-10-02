from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import joblib
import pandas as pd
import os
import json

from url_analyzer import extract_features
from risk_engine import calculate_risk
from threat_intel import check_virustotal
from final_assessment import generate_final_assessment
from email_analyzer import analyze_eml
from database import (
    create_table,
    save_investigation,
    get_investigations,
    get_investigation_by_id
)


# ----------------------------------------------------
# FASTAPI APPLICATION
# ----------------------------------------------------

app = FastAPI(
    title="PhishGuard API",
    description="AI-Powered Phishing Detection & Investigation Platform",
    version="1.0"
)


# ----------------------------------------------------
# CREATE DATABASE TABLE
# ----------------------------------------------------

create_table()


# ----------------------------------------------------
# CORS
# ----------------------------------------------------

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://phish-guard-lemon.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------
# LOAD MACHINE LEARNING MODEL
# ----------------------------------------------------

MODEL_FILE = "phishing_model.pkl"

try:
    model = joblib.load(MODEL_FILE)
    print("Machine learning model loaded successfully.")

except Exception as error:
    print("Error loading machine learning model:")
    print(error)
    model = None


# ----------------------------------------------------
# REQUEST MODEL
# ----------------------------------------------------

class URLRequest(BaseModel):
    url: str


# ----------------------------------------------------
# HOME
# ----------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "PhishGuard API is running.",
        "status": "online",
        "version": "1.0"
    }


# ----------------------------------------------------
# COMMON URL ANALYSIS FUNCTION
# ----------------------------------------------------

def analyze_url(url):

    if model is None:
        raise ValueError(
            "Machine learning model could not be loaded."
        )

    # ------------------------------------------------
    # EXTRACT FEATURES
    # ------------------------------------------------

    features = extract_features(url)

    feature_order = [
        "url_length",
        "domain_length",
        "subdomain_length",
        "num_dots",
        "num_hyphens",
        "num_digits",
        "num_special_chars",
        "uses_https",
        "has_ip",
        "suspicious_keyword_count",
        "path_length",
        "query_length"
    ]

    missing_features = [
        feature
        for feature in feature_order
        if feature not in features
    ]

    if missing_features:
        raise ValueError(
            "Missing features: "
            + ", ".join(missing_features)
        )

    # ------------------------------------------------
    # PREPARE FEATURES FOR ML MODEL
    # ------------------------------------------------

    feature_values = pd.DataFrame(
        [[features[feature] for feature in feature_order]],
        columns=feature_order
    )

    # ------------------------------------------------
    # MACHINE LEARNING PREDICTION
    # ------------------------------------------------

    prediction = int(
        model.predict(feature_values)[0]
    )

    # ------------------------------------------------
    # ML CONFIDENCE
    # ------------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            feature_values
        )[0]

        confidence = float(
            max(probabilities) * 100
        )

    else:
        confidence = 0.0

    prediction_text = (
        "PHISHING"
        if prediction == 0
        else "LEGITIMATE"
    )

    # ------------------------------------------------
    # RULE-BASED RISK
    # ------------------------------------------------

    rule_score, rule_level, rule_reasons = calculate_risk(
        features
    )

    # ------------------------------------------------
    # VIRUSTOTAL
    # ------------------------------------------------

    threat_result = check_virustotal(url)

    # ------------------------------------------------
    # FINAL ASSESSMENT
    # ------------------------------------------------

    final_score, final_level, final_reasons = (
        generate_final_assessment(
            prediction,
            rule_score,
            threat_result,
            rule_reasons
        )
    )

    # ------------------------------------------------
    # RETURN RESULT
    # ------------------------------------------------

    return {

        "url": url,

        "prediction": prediction_text,

        "ml_confidence": round(
            confidence,
            2
        ),

        "rule_risk": {

            "score": rule_score,

            "level": rule_level,

            "reasons": rule_reasons
        },

        "threat_intelligence": {

            "available": threat_result.get(
                "available",
                False
            ),

            "found": threat_result.get(
                "found",
                False
            ),

            "verified": threat_result.get(
                "verified",
                False
            ),

            "phish_id": threat_result.get(
                "phish_id",
                None
            ),

            "malicious": threat_result.get(
                "malicious",
                0
            ),

            "suspicious": threat_result.get(
                "suspicious",
                0
            ),

            "harmless": threat_result.get(
                "harmless",
                0
            ),

            "undetected": threat_result.get(
                "undetected",
                0
            ),

            "message": threat_result.get(
                "message",
                ""
            )
        },

        "final_assessment": {

            "score": final_score,

            "level": final_level,

            "reasons": final_reasons
        },

        "features": features
    }


# ----------------------------------------------------
# URL SCANNER
# ----------------------------------------------------

@app.post("/scan")
def scan_url(request: URLRequest):

    url = request.url.strip()

    if not url:

        raise HTTPException(
            status_code=400,
            detail="URL cannot be empty."
        )

    try:

        print("\n" + "=" * 60)
        print("PHISHGUARD URL SCAN")
        print("=" * 60)

        print("\nURL:")
        print(url)

        # ------------------------------------------------
        # ANALYZE URL
        # ------------------------------------------------

        result = analyze_url(url)

        # ------------------------------------------------
        # SAVE COMPLETE INVESTIGATION EVIDENCE
        # ------------------------------------------------

        threat = result["threat_intelligence"]
        rule_risk = result["rule_risk"]
        final_assessment = result["final_assessment"]

        save_investigation(
            investigation_type="URL",
            target=url,
            prediction=result["prediction"],
            risk_score=final_assessment["score"],
            risk_level=final_assessment["level"],
            ml_confidence=result["ml_confidence"],
            rule_score=rule_risk["score"],
            rule_level=rule_risk["level"],
            rule_reasons="\n".join(rule_risk["reasons"]),
            url_features="\n".join(
                f"{feature}={value}"
                for feature, value in result["features"].items()
            ),
            vt_available=int(bool(threat.get("available", False))),
            vt_malicious=threat.get("malicious", 0),
            vt_suspicious=threat.get("suspicious", 0),
            vt_harmless=threat.get("harmless", 0),
            vt_undetected=threat.get("undetected", 0),
            vt_message=threat.get("message", ""),
            final_reasons="\n".join(final_assessment["reasons"])
        )

        # ------------------------------------------------
        # PRINT FEATURES
        # ------------------------------------------------

        print("\nExtracted Features:")

        for feature, value in result[
            "features"
        ].items():

            print(
                f"{feature}: {value}"
            )

        # ------------------------------------------------
        # PRINT RESULT
        # ------------------------------------------------

        print("\n" + "=" * 60)
        print("PHISHGUARD RESULT")
        print("=" * 60)

        print(
            f"Prediction        : "
            f"{result['prediction']}"
        )

        print(
            f"ML Confidence     : "
            f"{result['ml_confidence']:.2f}%"
        )

        print(
            f"Rule Risk Score   : "
            f"{result['rule_risk']['score']}/100"
        )

        print(
            f"Rule Risk Level   : "
            f"{result['rule_risk']['level']}"
        )

        print(
            f"Final Risk Score  : "
            f"{result['final_assessment']['score']}/100"
        )

        print(
            f"Final Risk Level  : "
            f"{result['final_assessment']['level']}"
        )

        print("\nWhy was this URL flagged?")

        for reason in result[
            "final_assessment"
        ]["reasons"]:

            print("-", reason)

        print("\nVirusTotal:")

        print(
            result[
                "threat_intelligence"
            ]["message"]
        )

        print("=" * 60)

        return result

    except Exception as error:

        print(
            "\nERROR DURING URL SCAN:"
        )

        print(error)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ----------------------------------------------------
# EMAIL ANALYZER
# ----------------------------------------------------

@app.post("/analyze-email")
async def analyze_email(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    if not file.filename.lower().endswith(".eml"):

        raise HTTPException(
            status_code=400,
            detail="Only .eml files are supported."
        )

    temp_file = "temp_uploaded_email.eml"

    try:

        print("\n" + "=" * 60)
        print("PHISHGUARD EMAIL ANALYSIS")
        print("=" * 60)

        print("\nUploaded file:")
        print(file.filename)

        # ------------------------------------------------
        # SAVE TEMPORARY EMAIL
        # ------------------------------------------------

        file_content = await file.read()

        if not file_content:

            raise HTTPException(
                status_code=400,
                detail="Uploaded email file is empty."
            )

        with open(
            temp_file,
            "wb"
        ) as email_file:

            email_file.write(
                file_content
            )

        # ------------------------------------------------
        # ANALYZE EMAIL
        # ------------------------------------------------

        email_result = analyze_eml(
            temp_file
        )

        # ------------------------------------------------
        # ANALYZE EMBEDDED URLS
        # ------------------------------------------------

        url_results = []

        print(
            "\nAnalyzing URLs found inside email..."
        )

        for url in email_result["urls"]:

            print(
                "\nAnalyzing:",
                url
            )

            try:

                url_result = analyze_url(
                    url
                )

                url_results.append(
                    url_result
                )

            except Exception as error:

                print(
                    "URL analysis failed:",
                    error
                )

                url_results.append({
                    "url": url,
                    "error": str(error)
                })

        # ------------------------------------------------
        # CALCULATE FINAL EMAIL RISK
        # ------------------------------------------------

        email_score = (
            email_result["risk"]["score"]
        )

        final_email_score = email_score

        email_reasons = list(
            email_result[
                "risk"
            ]["reasons"]
        )

        for url_result in url_results:

            if "final_assessment" not in url_result:
                continue

            url_score = (
                url_result[
                    "final_assessment"
                ]["score"]
            )

            if url_score >= 70:

                final_email_score += 25

                email_reasons.append(
                    "Email contains a URL "
                    "with HIGH phishing risk."
                )

            elif url_score >= 40:

                final_email_score += 15

                email_reasons.append(
                    "Email contains a URL "
                    "with MEDIUM phishing risk."
                )

            elif url_score > 0:

                final_email_score += 5

        final_email_score = min(
            final_email_score,
            100
        )

        # ------------------------------------------------
        # EMAIL RISK LEVEL
        # ------------------------------------------------

        if final_email_score >= 70:

            final_email_level = "HIGH"

        elif final_email_score >= 40:

            final_email_level = "MEDIUM"

        else:

            final_email_level = "LOW"

        email_reasons = list(
            dict.fromkeys(
                email_reasons
            )
        )

        # ------------------------------------------------
        # FINAL RESULT
        # ------------------------------------------------

        final_result = {

            "filename": file.filename,

            "email_analysis": {

                "sender":
                    email_result["sender"],

                "recipient":
                    email_result["recipient"],

                "subject":
                    email_result["subject"],

                "date":
                    email_result["date"],

                "reply_to":
                    email_result["reply_to"],

                "return_path":
                    email_result["return_path"],

                "urls":
                    email_result["urls"],

                "attachments":
                    email_result["attachments"],

                "suspicious_keywords":
                    email_result[
                        "suspicious_keywords"
                    ],

                "authentication_results":
                    email_result[
                        "authentication_results"
                    ],

                "received_headers":
                    email_result[
                        "received_headers"
                    ]
            },

            "url_analysis":
                url_results,

            "final_assessment": {

                "score":
                    final_email_score,

                "level":
                    final_email_level,

                "reasons":
                    email_reasons
            }
        }

        # ------------------------------------------------
        # SAVE EMAIL INVESTIGATION
        # ------------------------------------------------

        save_investigation(
            investigation_type="EMAIL",
            target=file.filename,
            prediction=final_email_level,
            risk_score=final_email_score,
            risk_level=final_email_level,

            # Email risk is rule/header based, so ML is not used here.
            ml_confidence=None,
            rule_score=email_result["risk"]["score"],
            rule_level=email_result["risk"]["level"],
            rule_reasons=json.dumps(
                email_result["risk"]["reasons"]
            ),

            # No standalone URL feature vector belongs to the email itself.
            url_features=None,

            # VirusTotal fields are not directly generated by the email analyzer.
            vt_available=None,
            vt_malicious=None,
            vt_suspicious=None,
            vt_harmless=None,
            vt_undetected=None,
            vt_message=None,

            final_reasons=json.dumps(
                email_reasons
            ),

            # Email evidence
            email_sender=email_result["sender"],
            email_recipient=email_result["recipient"],
            email_subject=email_result["subject"],
            email_date=email_result["date"],
            email_reply_to=email_result["reply_to"],
            email_return_path=email_result["return_path"],
            email_suspicious_keywords=json.dumps(
                email_result["suspicious_keywords"]
            ),
            email_attachments=json.dumps(
                email_result["attachments"]
            ),
            email_authentication_results=email_result[
                "authentication_results"
            ],
            email_received_headers=json.dumps(
                email_result["received_headers"]
            ),
            email_urls=json.dumps(
                email_result["urls"]
            ),
            email_reasons=json.dumps(
                email_reasons
            )
        )

        # ------------------------------------------------
        # PRINT EMAIL RESULT
        # ------------------------------------------------

        print("\n" + "=" * 60)
        print("PHISHGUARD EMAIL RESULT")
        print("=" * 60)

        print(
            "Sender:",
            email_result["sender"]
        )

        print(
            "Subject:",
            email_result["subject"]
        )

        print(
            "URLs found:",
            len(email_result["urls"])
        )

        print(
            "Attachments:",
            len(
                email_result[
                    "attachments"
                ]
            )
        )

        print(
            "Final Email Risk Score:",
            final_email_score
        )

        print(
            "Final Email Risk Level:",
            final_email_level
        )

        print("\nReasons:")

        for reason in email_reasons:

            print(
                "-",
                reason
            )

        print("=" * 60)

        return final_result

    except HTTPException:

        raise

    except Exception as error:

        print(
            "\nERROR DURING EMAIL ANALYSIS:"
        )

        print(error)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:

        # ------------------------------------------------
        # DELETE TEMPORARY EMAIL FILE
        # ------------------------------------------------

        if os.path.exists(
            temp_file
        ):

            try:

                os.remove(
                    temp_file
                )

            except Exception:

                pass


# ----------------------------------------------------
# INVESTIGATION HISTORY
# ----------------------------------------------------

@app.get("/investigations")
def investigations():

    return get_investigations()
@app.get("/investigations/{investigation_id}")
def investigation_details(investigation_id: int):
    investigation = get_investigation_by_id(investigation_id)

    if investigation is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found."
        )

    return investigation

# DASHBOARD
# ----------------------------------------------------

@app.get("/dashboard-stats")
def dashboard_stats():

    investigations = get_investigations()

    total = len(investigations)

    high = 0
    medium = 0
    low = 0

    for investigation in investigations:

        risk_level = investigation["risk_level"]

        if risk_level == "HIGH":
            high += 1

        elif risk_level == "MEDIUM":
            medium += 1

        elif risk_level == "LOW":
            low += 1

    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low
    }