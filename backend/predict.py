import pandas as pd
import joblib

from url_analyzer import extract_features
from risk_engine import calculate_risk
from threat_intel import check_virustotal
from final_assessment import generate_final_assessment


# ==================================================
# Load trained ML model
# ==================================================

model = joblib.load("../backend/phishing_model.pkl")


# ==================================================
# Ask user for URL
# ==================================================

url = input("Enter URL to scan: ")


# ==================================================
# Extract URL features
# ==================================================

features = extract_features(url)


# Convert features into DataFrame
features_df = pd.DataFrame([features])


# ==================================================
# Machine Learning Prediction
# ==================================================

prediction = model.predict(features_df)[0]


# Get prediction probabilities
probabilities = model.predict_proba(features_df)[0]

confidence = max(probabilities) * 100


# ==================================================
# Rule-Based Risk Analysis
# ==================================================

risk_score, risk_level, reasons = calculate_risk(features)


# ==================================================
# Threat Intelligence
# ==================================================

print("\nChecking threat intelligence...")

threat_result = check_virustotal(url)


# ==================================================
# Final Assessment
# ==================================================

final_score, final_level, final_reasons = generate_final_assessment(
    prediction,
    confidence,
    risk_score,
    threat_result
)


# ==================================================
# Display Main Result
# ==================================================

print("\n" + "=" * 55)
print("                 PHISHGUARD RESULT")
print("=" * 55)


# ML Prediction

if prediction == 0:

    print("Prediction        : PHISHING")

else:

    print("Prediction        : LEGITIMATE")


print(f"ML Confidence     : {confidence:.2f}%")


# Rule-based risk

print(f"Rule Risk Score   : {risk_score}/100")
print(f"Rule Risk Level   : {risk_level}")


# Final assessment

print(f"Final Risk Score  : {final_score}/100")
print(f"Final Risk Level  : {final_level}")


# ==================================================
# URL
# ==================================================

print("\nURL:")
print(url)


# ==================================================
# Threat Intelligence
# ==================================================

print("\nThreat Intelligence")
print("-" * 35)


if threat_result["available"]:

    if threat_result["found"]:

        print("Virustotal : FOUND")

        print(
            f"Verified  : {threat_result['verified']}"
        )

        if threat_result["phish_id"]:

            print(
                f"Phish ID  : {threat_result['phish_id']}"
            )

    else:

        print("Virustotal : NOT FOUND")

else:

    print("Virustotal : UNAVAILABLE")


print(
    f"Status    : {threat_result['message']}"
)


# ==================================================
# Rule-Based Explanation
# ==================================================

print("\nWhy was this URL flagged?")
print("-" * 35)


if reasons:

    for reason in reasons:

        print("⚠", reason)

else:

    print(
        "No major suspicious indicators detected."
    )


# ==================================================
# Final Assessment Explanation
# ==================================================

print("\nFinal Assessment")
print("-" * 35)


for reason in final_reasons:

    print("⚠", reason)


# ==================================================
# Extracted Features
# ==================================================

print("\nExtracted Features")
print("-" * 35)


for feature, value in features.items():

    print(f"{feature}: {value}")


print("=" * 55)