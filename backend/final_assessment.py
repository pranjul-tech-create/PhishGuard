def generate_final_assessment(
    prediction,
    risk_score,
    threat_result,
    rule_reasons=None
):

    final_score = risk_score

    reasons = []

    # Rule-based reasons
    if rule_reasons:
        reasons.extend(rule_reasons)

    # Machine Learning
    if prediction == 0:

        final_score += 25

        reasons.append(
            "Machine-learning model classified the URL as phishing."
        )

    # VirusTotal
    if threat_result.get("available", False):

        malicious = threat_result.get("malicious", 0)
        suspicious = threat_result.get("suspicious", 0)

        if malicious > 0:

            final_score += 35

            reasons.append(
                f"VirusTotal reported {malicious} malicious detection(s)."
            )

        elif suspicious > 0:

            final_score += 20

            reasons.append(
                f"VirusTotal reported {suspicious} suspicious detection(s)."
            )

    # Keep score between 0 and 100
    final_score = min(max(final_score, 0), 100)

    # Final risk level
    if final_score >= 70:

        final_level = "HIGH"

    elif final_score >= 30:

        final_level = "MEDIUM"

    else:

        final_level = "LOW"

    # Remove duplicate reasons
    reasons = list(dict.fromkeys(reasons))

    return final_score, final_level, reasons