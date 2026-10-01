from urllib.parse import urlparse
import tldextract
import re


def extract_features(url):

    parsed = urlparse(url)

    extracted = tldextract.extract(url)

    domain = extracted.domain
    subdomain = extracted.subdomain

    features = {}

    # 1. URL length
    features["url_length"] = len(url)

    # 2. Domain length
    features["domain_length"] = len(domain)

    # 3. Subdomain length
    features["subdomain_length"] = len(subdomain)

    # 4. Number of dots
    features["num_dots"] = url.count(".")

    # 5. Number of hyphens
    features["num_hyphens"] = url.count("-")

    # 6. Number of digits
    features["num_digits"] = sum(c.isdigit() for c in url)

    # 7. Number of special characters
    features["num_special_chars"] = len(
        re.findall(r"[^a-zA-Z0-9]", url)
    )

    # 8. HTTPS check
    features["uses_https"] = 1 if parsed.scheme == "https" else 0

    # 9. IP address check
    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    hostname = parsed.hostname or ""

    features["has_ip"] = (
        1 if re.match(ip_pattern, hostname) else 0
    )

    # 10. Suspicious keyword detection
    suspicious_words = [
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
        "wallet"
    ]

    url_lower = url.lower()

    suspicious_count = 0

    for word in suspicious_words:
        if word in url_lower:
            suspicious_count += 1

    features["suspicious_keyword_count"] = suspicious_count

    # 11. URL path length
    features["path_length"] = len(parsed.path)

    # 12. Query length
    features["query_length"] = len(parsed.query)

    return features


# Testing
if __name__ == "__main__":

    url = input("Enter URL: ")

    features = extract_features(url)

    print("\nURL FEATURES")
    print("-" * 40)

    for feature, value in features.items():
        print(f"{feature}: {value}")