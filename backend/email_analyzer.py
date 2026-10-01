from email import policy
from email.parser import BytesParser
from email.message import EmailMessage

from urllib.parse import urlparse

import re


# =========================================================
# URL EXTRACTION
# =========================================================

URL_PATTERN = re.compile(
    r"https?://[^\s<>\"]+",
    re.IGNORECASE
)


def extract_urls_from_text(text):

    if not text:
        return []

    urls = URL_PATTERN.findall(text)

    cleaned_urls = []

    for url in urls:

        # Remove common punctuation attached to URLs
        url = url.rstrip(
            ".,;:!?)]}>\"'"
        )

        if url not in cleaned_urls:

            cleaned_urls.append(url)

    return cleaned_urls


# =========================================================
# EMAIL BODY EXTRACTION
# =========================================================

def extract_email_body(message):

    text_parts = []
    html_parts = []

    if message.is_multipart():

        for part in message.walk():

            content_type = part.get_content_type()

            content_disposition = (
                part.get_content_disposition()
            )

            # Ignore attachments
            if content_disposition == "attachment":

                continue

            try:

                content = part.get_content()

            except Exception:

                continue

            if content_type == "text/plain":

                text_parts.append(
                    str(content)
                )

            elif content_type == "text/html":

                html_parts.append(
                    str(content)
                )

    else:

        try:

            content = message.get_content()

        except Exception:

            content = ""

        if message.get_content_type() == "text/plain":

            text_parts.append(
                str(content)
            )

        elif message.get_content_type() == "text/html":

            html_parts.append(
                str(content)
            )

    return (
        "\n".join(text_parts),
        "\n".join(html_parts)
    )


# =========================================================
# SUSPICIOUS KEYWORDS
# =========================================================

SUSPICIOUS_KEYWORDS = [

    "verify your account",

    "verify account",

    "account suspended",

    "account locked",

    "urgent action",

    "immediate action",

    "confirm your identity",

    "confirm identity",

    "reset your password",

    "password expires",

    "click here",

    "login",

    "sign in",

    "security alert",

    "unusual activity",

    "payment failed",

    "payment required",

    "invoice",

    "refund",

    "bank",

    "credit card",

    "wallet",

    "crypto",

    "otp",

    "one time password"

]


# =========================================================
# KEYWORD ANALYSIS
# =========================================================

def detect_suspicious_keywords(text):

    text_lower = text.lower()

    detected = []

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in text_lower:

            detected.append(
                keyword
            )

    return detected


# =========================================================
# ATTACHMENT EXTRACTION
# =========================================================

def extract_attachments(message):

    attachments = []

    for part in message.walk():

        if part.get_content_disposition() == "attachment":

            filename = part.get_filename()

            if filename:

                attachments.append(
                    filename
                )

    return attachments


# =========================================================
# EMAIL ANALYSIS
# =========================================================

def analyze_eml(file_path):

    with open(
        file_path,
        "rb"
    ) as email_file:

        message = BytesParser(
            policy=policy.default
        ).parse(
            email_file
        )

    # -----------------------------------------------------
    # BASIC EMAIL INFORMATION
    # -----------------------------------------------------

    sender = message.get(
        "From",
        ""
    )

    recipient = message.get(
        "To",
        ""
    )

    subject = message.get(
        "Subject",
        ""
    )

    date = message.get(
        "Date",
        ""
    )

    reply_to = message.get(
        "Reply-To",
        ""
    )

    return_path = message.get(
        "Return-Path",
        ""
    )


    # -----------------------------------------------------
    # EMAIL BODY
    # -----------------------------------------------------

    plain_text, html_text = (
        extract_email_body(
            message
        )
    )

    combined_text = (
        plain_text
        + "\n"
        + html_text
    )


    # -----------------------------------------------------
    # URL EXTRACTION
    # -----------------------------------------------------

    urls = extract_urls_from_text(
        combined_text
    )


    # -----------------------------------------------------
    # ATTACHMENTS
    # -----------------------------------------------------

    attachments = extract_attachments(
        message
    )


    # -----------------------------------------------------
    # SUSPICIOUS KEYWORDS
    # -----------------------------------------------------

    suspicious_keywords = (
        detect_suspicious_keywords(
            combined_text
        )
    )


    # -----------------------------------------------------
    # HEADER INFORMATION
    # -----------------------------------------------------

    authentication_results = message.get(
        "Authentication-Results",
        ""
    )

    received_headers = message.get_all(
        "Received",
        []
    )


    # -----------------------------------------------------
    # BASIC EMAIL RISK INDICATORS
    # -----------------------------------------------------

    risk_score = 0

    reasons = []


    # Suspicious keywords
    if len(suspicious_keywords) >= 4:

        risk_score += 25

        reasons.append(
            "Email contains multiple phishing-related keywords."
        )

    elif len(suspicious_keywords) >= 2:

        risk_score += 15

        reasons.append(
            "Email contains suspicious security or account-related language."
        )


    # URLs
    if len(urls) >= 3:

        risk_score += 15

        reasons.append(
            "Email contains multiple URLs."
        )

    elif len(urls) > 0:

        risk_score += 5

        reasons.append(
            "Email contains one or more URLs."
        )


    # Attachments
    if len(attachments) > 0:

        risk_score += 15

        reasons.append(
            "Email contains one or more attachments."
        )


    # Reply-To mismatch
    if (
        sender
        and reply_to
        and sender.lower() != reply_to.lower()
    ):

        risk_score += 15

        reasons.append(
            "Reply-To address differs from the sender address."
        )


    # Missing authentication information
    if not authentication_results:

        risk_score += 5

        reasons.append(
            "Authentication-Results header is not present."
        )


    # Limit score
    risk_score = min(
        risk_score,
        100
    )


    # Determine risk level
    if risk_score >= 70:

        risk_level = "HIGH"

    elif risk_score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "sender": sender,

        "recipient": recipient,

        "subject": subject,

        "date": date,

        "reply_to": reply_to,

        "return_path": return_path,

        "urls": urls,

        "attachments": attachments,

        "suspicious_keywords":
            suspicious_keywords,

        "authentication_results":
            authentication_results,

        "received_headers":
            received_headers,

        "risk": {

            "score": risk_score,

            "level": risk_level,

            "reasons": reasons

        }

    }


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    file_path = input(
        "Enter path to .eml file: "
    ).strip()

    result = analyze_eml(
        file_path
    )

    print("\n")
    print("=" * 60)
    print("PHISHGUARD EMAIL ANALYSIS")
    print("=" * 60)

    print(
        "\nSender:",
        result["sender"]
    )

    print(
        "Recipient:",
        result["recipient"]
    )

    print(
        "Subject:",
        result["subject"]
    )

    print(
        "Date:",
        result["date"]
    )

    print(
        "\nURLs:"
    )

    for url in result["urls"]:

        print(
            "-",
            url
        )

    print(
        "\nAttachments:"
    )

    for attachment in result["attachments"]:

        print(
            "-",
            attachment
        )

    print(
        "\nSuspicious Keywords:"
    )

    for keyword in result[
        "suspicious_keywords"
    ]:

        print(
            "-",
            keyword
        )

    print(
        "\nRisk Score:",
        result["risk"]["score"]
    )

    print(
        "Risk Level:",
        result["risk"]["level"]
    )

    print(
        "\nReasons:"
    )

    for reason in result["risk"]["reasons"]:

        print(
            "-",
            reason
        )

    print("=" * 60)