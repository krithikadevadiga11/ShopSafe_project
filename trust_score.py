from security_checker import analyze_security
from content_checker import analyze_content
from business_checker import analyze_business


def calculate_trust(url):

    # -----------------------------
    # Run all modules
    # -----------------------------

    security = analyze_security(url)
    content = analyze_content(url)
    business = analyze_business(url)

    # -----------------------------
    # Individual Scores
    # -----------------------------

    security_score = security["score"]
    content_score = content["score"]
    business_score = business["score"]

    # Maximum scores of each module
    max_security = 50
    max_content = 25
    max_business = 35

    # -----------------------------
    # Weighted Score
    # -----------------------------

    security_weight = (security_score / max_security) * 40
    content_weight = (content_score / max_content) * 30
    business_weight = (business_score / max_business) * 30

    trust_score = round(
        security_weight +
        content_weight +
        business_weight
    )

    # -----------------------------
    # Risk Level
    # -----------------------------

    if trust_score >= 80:
        risk = "LOW RISK"
        recommendation = "Website appears trustworthy."

    elif trust_score >= 60:
        risk = "MEDIUM RISK"
        recommendation = "Proceed carefully before making payments."

    else:
        risk = "HIGH RISK"
        recommendation = "This website may not be trustworthy."

    # -----------------------------
    # Merge Reasons
    # -----------------------------

    reasons = []

    reasons.extend(security["reasons"])
    reasons.extend(content["reasons"])
    reasons.extend(business["reasons"])

    # -----------------------------
    # Final Result
    # -----------------------------

    return {

        "website": url,

        "trust_score": trust_score,

        "risk": risk,

        "recommendation": recommendation,

        "security": security,

        "content": content,

        "business": business,

        "security_score": security_score,

        "content_score": content_score,

        "business_score": business_score,

        "reasons": reasons
    }
