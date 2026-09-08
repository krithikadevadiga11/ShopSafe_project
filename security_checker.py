import validators
import requests
import whois
from datetime import datetime

def analyze_security(url):

    result = {
        "valid": False,
        "https": False,
        "domain_age": "Unknown",
        "score": 0,
        "reasons": []
    }

    # Add https:// if user doesn't enter it
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Validate URL
    if not validators.url(url):
        result["reasons"].append("Invalid URL")
        return result

    result["valid"] = True

    # Check website accessibility
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            result["score"] += 10
            result["reasons"].append("Website is reachable")
    except:
        result["reasons"].append("Website is not reachable")
        return result

    # HTTPS Check
    if url.startswith("https://"):
        result["https"] = True
        result["score"] += 20
        result["reasons"].append("HTTPS secured")
    else:
        result["reasons"].append("HTTPS not found")

    # Domain Age
    try:
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]

        info = whois.whois(domain)

        creation = info.creation_date

        if isinstance(creation, list):
            creation = creation[0]

        if creation:
            years = datetime.now().year - creation.year

            result["domain_age"] = f"{years} years"

            if years >= 2:
                result["score"] += 20
                result["reasons"].append("Old trusted domain")
            else:
                result["reasons"].append("New domain")
    except:
        result["reasons"].append("Domain age unavailable")

    return result