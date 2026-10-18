"""
AI-assisted cybercrime classification.

This starter version works without an API key.
It provides simple keyword-based classification so the project can run locally.
"""

from categories import CYBERCRIME_CATEGORIES


def classify_incident(description: str):
    text = description.lower()

    keyword_map = {
        "Phishing": ["phishing", "fake email", "fake sms", "smishing", "vishing", "otp"],
        "Ransomware": ["ransomware", "ransom", "encrypted files", "locked files"],
        "Identity Theft": ["identity theft", "identity stolen", "account takeover", "stolen identity"],
        "Hacking": ["hacked", "brute force", "sql injection", "xss", "unauthorized access"],
        "Cyber Extortion": ["extortion", "sextortion", "ddos extortion", "blackmail"],
        "Malware": ["malware", "trojan", "worm", "virus", "spyware", "adware"],
        "Online Fraud": ["online fraud", "scam", "romance scam", "lottery", "investment fraud"],
        "Cyberbullying": ["cyberbullying", "harassment", "stalking", "defamation"],
        "Data Breach": ["data breach", "data leak", "stolen credentials", "personal information leak"],
        "Intellectual Property Theft": ["software piracy", "patent", "trademark", "trade secret"]
    }

    category = "Online Fraud"
    confidence = 0.40

    for name, keywords in keyword_map.items():
        if any(keyword in text for keyword in keywords):
            category = name
            confidence = 0.85
            break

    subcategory = CYBERCRIME_CATEGORIES[category]["subcategories"][0]

    if any(word in text for word in ["urgent", "money", "ransom", "blackmail", "threat"]):
        priority = "High"
    else:
        priority = "Medium"

    summary = (
        f"The incident was classified as {category}. "
        f"Possible subcategory: {subcategory}. "
        f"This is an AI-assisted preliminary classification and should be reviewed by an officer."
    )

    return {
        "category": category,
        "subcategory": subcategory,
        "priority": priority,
        "confidence": confidence,
        "summary": summary
    }
