def calculate_risk(features):

    score = 0
    reasons = []

    # IP address
    if features["has_ip"] == 1:
        score += 25
        reasons.append("URL uses an IP address instead of a normal domain.")

    # HTTPS
    if features["uses_https"] == 0:
        score += 15
        reasons.append("URL does not use HTTPS.")

    # Suspicious keywords
    keyword_count = features["suspicious_keyword_count"]

    if keyword_count >= 3:
        score += 25
        reasons.append(
            f"URL contains {keyword_count} suspicious keywords."
        )

    elif keyword_count > 0:
        score += 10
        reasons.append(
            f"URL contains {keyword_count} suspicious keyword(s)."
        )

    # Long URL
    if features["url_length"] > 100:
        score += 15
        reasons.append("URL is unusually long.")

    elif features["url_length"] > 75:
        score += 10
        reasons.append("URL is relatively long.")

    # Many subdomains
    if features["subdomain_length"] > 20:
        score += 10
        reasons.append("URL contains an unusually long subdomain.")

    # Many special characters
    if features["num_special_chars"] > 15:
        score += 10
        reasons.append("URL contains many special characters.")

    # Cap score at 100
    score = min(score, 100)

    # Risk level
    if score >= 70:
        risk_level = "HIGH"

    elif score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return score, risk_level, reasons