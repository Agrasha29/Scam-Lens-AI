
import re
from urllib.parse import urlparse
import ipaddress
from app.ml.predictor import predict_message

# ScamLens - Improved Rule-Based Scam Detection Engine

SCAM_PATTERNS = {
    "urgency": {
        "weight": 15,
        "patterns": [
            r"\burgent\b",
            r"\bimmediately\b",
            r"\bact now\b",
            r"\blimited time\b",
            r"\bwithin 24 hours\b",
            r"\bfinal warning\b",
            r"\bexpires today\b"
        ],
        "reason": "The message creates urgency and pressures the recipient to act quickly."
    },

    "personal_information": {
        "weight": 25,
        "patterns": [
            r"\botp\b",
            r"\bpassword\b",
            r"\bpin\b",
            r"\bcvv\b",
            r"\bshare your details\b",
            r"\bverify your account\b",
            r"\baccount credentials\b"
        ],
        "reason": "The message requests sensitive personal or financial information."
    },

    "financial_fraud": {
        "weight": 20,
        "patterns": [
            r"\bbank account\b",
            r"\bcredit card\b",
            r"\bdebit card\b",
            r"\baccount blocked\b",
            r"\bpayment pending\b",
            r"\bclaim your refund\b",
            r"\btransfer money\b",
            r"\bpay processing fee\b"
        ],
        "reason": "The message contains a financial request or account-related warning."
    },

    "fake_rewards": {
        "weight": 15,
        "patterns": [
            r"\byou won\b",
            r"\blottery\b",
            r"\bfree gift\b",
            r"\bcash prize\b",
            r"\bcongratulations\b",
            r"\bclaim your prize\b",
            r"\blucky winner\b"
        ],
        "reason": "The message uses a prize or reward claim that could be fraudulent."
    },

    "threats": {
        "weight": 20,
        "patterns": [
            r"\blegal action\b",
            r"\bpolice case\b",
            r"\baccount will be blocked\b",
            r"\baccount suspended\b",
            r"\byour sim will be blocked\b",
            r"\barrest warrant\b"
        ],
        "reason": "The message uses threats or fear to pressure the recipient."
    },

    "impersonation": {
        "weight": 15,
        "patterns": [
            r"\bwe are from your bank\b",
            r"\bbank representative\b",
            r"\bcustomer care executive\b",
            r"\bgovernment official\b",
            r"\bkyc update\b",
            r"\bverify kyc\b"
        ],
        "reason": "The message may be pretending to represent a trusted organization."
    }
}


def analyze_message(message: str):

    text = message.lower()
    # Machine Learning prediction
    ml_result = predict_message(message) if message.strip() else {
        "prediction": "ham",
        "spam_probability": 0.0
    }
    detected_indicators = []
    risk_score = 0
    detected_categories = set()

    # Check message against scam patterns
    for category, details in SCAM_PATTERNS.items():

        for pattern in details["patterns"]:

            match = re.search(pattern, text)

            if match:
                detected_indicators.append({
                    "category": category,
                    "keyword": match.group(),
                    "reason": details["reason"]
                })

                risk_score += details["weight"]
                detected_categories.add(category)

    # Detect URLs separately
    urls = re.findall(
        r"https?://[^\s]+|www\.[^\s]+",
        text
    )

    if urls:
        detected_indicators.append({
            "category": "link_detected",
            "keyword": urls[0],
            "reason": "A link is present. Its safety has not been verified."
        })

        # A link alone does not prove a message is fraudulent.
        risk_score += 5

    # Keep score within 0-100
    risk_score = min(risk_score, 100)

    # Determine risk level
    if risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Generate recommendations
    recommendations = []

    if "personal_information" in detected_categories:
        recommendations.append(
            "Never share your OTP, PIN, CVV or password."
        )

    if "financial_fraud" in detected_categories:
        recommendations.append(
            "Verify unexpected payment or banking requests through official channels."
        )

    if "fake_rewards" in detected_categories:
        recommendations.append(
            "Be cautious of unexpected prizes. Never pay a fee to claim a suspicious reward."
        )

    if "urgency" in detected_categories or "threats" in detected_categories:
        recommendations.append(
            "Do not panic or act under pressure. Verify the message independently."
        )

    if "impersonation" in detected_categories:
        recommendations.append(
            "Contact the organization using its official website or verified phone number."
        )

    if urls:
        recommendations.append(
            "Do not open suspicious links. Check the website independently."
        )

    if not recommendations:
        recommendations.append(
            "No strong scam indicators were detected. Still verify unexpected requests."
        )

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "detected_indicators": detected_indicators,
        "recommendations": recommendations,
        "ml_prediction": ml_result["prediction"],
        "ml_spam_probability": ml_result["spam_probability"]
    }




def analyze_url(url: str):

    original_url = url.strip()

    # Add a scheme if the user did not provide one
    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    parsed = urlparse(original_url)
    hostname = parsed.hostname

    indicators = []
    risk_score = 0

    def add_indicator(category, keyword, reason, points):
        nonlocal risk_score

        indicators.append({
            "category": category,
            "keyword": keyword,
            "reason": reason
        })

        risk_score += points

    # Validate hostname
    if not hostname:
        return {
            "risk_score": 100,
            "risk_level": "High",
            "detected_indicators": [{
                "category": "invalid_url",
                "keyword": original_url,
                "reason": "The URL does not contain a valid hostname."
            }],
            "recommendations": [
                "Do not open invalid or suspicious links."
            ]
        }

    hostname = hostname.lower()

    # Check HTTPS
    if parsed.scheme != "https":
        add_indicator(
            "insecure_connection",
            parsed.scheme,
            "The URL does not use HTTPS encryption.",
            15
        )

    # Check IP address instead of domain
    try:
        ipaddress.ip_address(hostname)

        add_indicator(
            "ip_address",
            hostname,
            "The URL uses an IP address instead of a normal domain name.",
            25
        )

    except ValueError:
        pass

    # Check URL shorteners
    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "is.gd",
        "cutt.ly",
        "shorturl.at"
    ]

    if hostname in shorteners:
        add_indicator(
            "url_shortener",
            hostname,
            "Shortened URLs hide the original destination.",
            20
        )

    # Check suspicious domain patterns
    if "xn--" in hostname:
        add_indicator(
            "punycode_domain",
            hostname,
            "The domain uses encoded characters that may disguise its appearance.",
            25
        )

    if "@" in parsed.netloc:
        add_indicator(
            "misleading_url",
            parsed.netloc,
            "The URL contains an @ symbol, which can make its destination misleading.",
            25
        )

    if hostname.count("-") >= 3:
        add_indicator(
            "unusual_domain",
            hostname,
            "The domain contains multiple hyphens, which may be suspicious.",
            10
        )

    # Final score
    risk_score = min(risk_score, 100)

    if risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    recommendations = []

    if indicators:
        recommendations.append(
            "Do not enter passwords, OTPs or payment details on an unverified website."
        )

        recommendations.append(
            "Verify the domain through the organization's official website."
        )
    else:
        recommendations.append(
            "No obvious suspicious URL patterns were detected. This does not guarantee the website is safe."
        )

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "detected_indicators": indicators,
        "recommendations": recommendations
    }

