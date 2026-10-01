import os
import base64
import requests
from dotenv import load_dotenv


load_dotenv()

VT_API_KEY = os.getenv("VT_API_KEY")

VT_URL = "https://www.virustotal.com/api/v3/urls"


def empty_result(message):

    return {
        "available": False,
        "found": False,
        "verified": False,
        "phish_id": None,
        "malicious": 0,
        "suspicious": 0,
        "harmless": 0,
        "undetected": 0,
        "message": message
    }


def check_virustotal(url):

    if not VT_API_KEY:
        return empty_result(
            "VirusTotal API key is not configured."
        )

    try:

        url_id = base64.urlsafe_b64encode(
            url.encode()
        ).decode().strip("=")

        endpoint = f"{VT_URL}/{url_id}"

        headers = {
            "x-apikey": VT_API_KEY,
            "accept": "application/json"
        }

        response = requests.get(
            endpoint,
            headers=headers,
            timeout=15
        )

        print(
            f"VirusTotal HTTP Status: "
            f"{response.status_code}"
        )

        if response.status_code == 404:

            return empty_result(
                "URL is not present in the VirusTotal dataset."
            )

        if response.status_code == 401:

            return empty_result(
                "VirusTotal API key is invalid."
            )

        if response.status_code == 403:

            return empty_result(
                "VirusTotal API access was forbidden."
            )

        if response.status_code == 429:

            return empty_result(
                "VirusTotal API rate limit reached."
            )

        if response.status_code != 200:

            return empty_result(
                f"VirusTotal returned HTTP "
                f"{response.status_code}"
            )

        result = response.json()

        attributes = (
            result
            .get("data", {})
            .get("attributes", {})
        )

        stats = attributes.get(
            "last_analysis_stats",
            {}
        )

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)
        undetected = stats.get("undetected", 0)

        found = (
            malicious > 0
            or suspicious > 0
        )

        if malicious > 0:

            message = (
                f"VirusTotal detected the URL as "
                f"malicious with {malicious} detection(s)."
            )

        elif suspicious > 0:

            message = (
                f"VirusTotal reported "
                f"{suspicious} suspicious detection(s)."
            )

        else:

            message = (
                "VirusTotal returned no malicious "
                "or suspicious detections."
            )

        return {
            "available": True,
            "found": found,
            "verified": malicious > 0,
            "phish_id": None,
            "malicious": malicious,
            "suspicious": suspicious,
            "harmless": harmless,
            "undetected": undetected,
            "message": message
        }

    except requests.exceptions.Timeout:

        return empty_result(
            "VirusTotal request timed out."
        )

    except requests.exceptions.RequestException as error:

        return empty_result(
            f"VirusTotal network error: {error}"
        )

    except ValueError:

        return empty_result(
            "VirusTotal returned an invalid response."
        )