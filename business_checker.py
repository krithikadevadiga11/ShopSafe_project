import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def analyze_business(url):

    result = {
        "emails": [],
        "phones": [],
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "twitter": "",
        "whatsapp": "",
        "score": 0,
        "reasons": []
    }

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    pages = [
        "",
        "/contact",
        "/contact-us",
        "/about",
        "/about-us",
        "/support",
        "/help"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    emails = set()
    phones = set()

    try:

        for page in pages:

            page_url = urljoin(url, page)

            try:
                response = requests.get(page_url, headers=headers, timeout=8)

                if response.status_code != 200:
                    continue

                html = response.text

                soup = BeautifulSoup(html, "html.parser")

                # -------------------------
                # EMAIL
                # -------------------------

                found_emails = re.findall(
                    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                    html
                )

                for email in found_emails:
                    emails.add(email)

                # -------------------------
                # PHONE
                # -------------------------

                found_phones = re.findall(
                    r"(?:\+91[- ]?)?[6-9]\d{9}",
                    html
                )

                for phone in found_phones:

                    phone = phone.replace(" ", "").replace("-", "")

                    # ignore repeated digits
                    if len(set(phone[-10:])) == 1:
                        continue

                    phones.add(phone)

                # -------------------------
                # SOCIAL LINKS
                # -------------------------

                for link in soup.find_all("a", href=True):

                    href = link["href"]

                    if "instagram.com" in href and result["instagram"] == "":
                        result["instagram"] = href

                    elif "facebook.com" in href and result["facebook"] == "":
                        result["facebook"] = href

                    elif "linkedin.com" in href and result["linkedin"] == "":
                        result["linkedin"] = href

                    elif "twitter.com" in href or "x.com" in href:
                        if result["twitter"] == "":
                            result["twitter"] = href

                    elif "wa.me" in href or "whatsapp" in href:
                        if result["whatsapp"] == "":
                            result["whatsapp"] = href

            except:
                pass

        # -------------------------
        # Store Results
        # -------------------------

        result["emails"] = sorted(list(emails))[:5]
        result["phones"] = sorted(list(phones))[:5]

        if result["emails"]:
            result["score"] += 10
            result["reasons"].append("Business email found")

        if result["phones"]:
            result["score"] += 10
            result["reasons"].append("Phone number found")

        if result["instagram"]:
            result["score"] += 5
            result["reasons"].append("Instagram page found")

        if result["facebook"]:
            result["score"] += 5
            result["reasons"].append("Facebook page found")

        if result["linkedin"]:
            result["score"] += 5
            result["reasons"].append("LinkedIn page found")

        if result["twitter"]:
            result["score"] += 5
            result["reasons"].append("Twitter/X page found")

        if result["whatsapp"]:
            result["score"] += 5
            result["reasons"].append("WhatsApp contact found")

    except Exception as e:

        result["reasons"].append(str(e))

    return result