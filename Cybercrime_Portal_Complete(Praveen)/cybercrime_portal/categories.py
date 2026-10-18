CYBERCRIME_CATEGORIES = {
    "Phishing": {
        "subcategories": [
            "Email Phishing", "SMS Phishing (Smishing)",
            "Voice Phishing (Vishing)", "Spear Phishing", "Clone Phishing"
        ],
        "description": "Fraudulent attempts to obtain sensitive information by deception"
    },
    "Ransomware": {
        "subcategories": ["Encrypting Ransomware", "Locker Ransomware", "Scareware", "Doxware"],
        "description": "Malware that blocks access to data until ransom is paid"
    },
    "Identity Theft": {
        "subcategories": ["Credit Card Fraud", "Social Security Number Misuse", "Bank Account Takeover", "Account Hijacking"],
        "description": "Unauthorized use of another person's personal information"
    },
    "Hacking": {
        "subcategories": ["Brute Force Attack", "SQL Injection", "Cross-Site Scripting (XSS)", "Unauthorized Access"],
        "description": "Unauthorized access to computer systems or networks"
    },
    "Cyber Extortion": {
        "subcategories": ["DDoS Attack Extortion", "Data Theft Extortion", "Sextortion"],
        "description": "Threatening attacks to demand money or favors"
    },
    "Malware": {
        "subcategories": ["Trojan", "Worm", "Virus", "Spyware", "Adware"],
        "description": "Malicious software designed to harm systems"
    },
    "Online Fraud": {
        "subcategories": ["E-commerce Fraud", "Online Romance Scam", "Lottery Scam", "Investment Fraud"],
        "description": "Fraudulent schemes conducted online"
    },
    "Cyberbullying": {
        "subcategories": ["Harassment", "Defamation", "Stalking", "Revenge Porn"],
        "description": "Harassment or abuse using digital platforms"
    },
    "Data Breach": {
        "subcategories": ["Stolen Credentials", "Personal Information Leak", "Business Secrets Exposure", "Healthcare Data Breach"],
        "description": "Unauthorized access or disclosure of sensitive data"
    },
    "Intellectual Property Theft": {
        "subcategories": ["Software Piracy", "Patent Infringement", "Trademark Counterfeiting", "Trade Secret Theft"],
        "description": "Theft of intellectual property or copyrighted material"
    }
}

PRIORITY_LEVELS = ["Low", "Medium", "High", "Critical"]
CASE_STATUS = ["New", "Under Review", "Investigating", "Resolved", "Closed"]

def get_all_categories():
    return list(CYBERCRIME_CATEGORIES.keys())

def get_subcategories(category):
    if category in CYBERCRIME_CATEGORIES:
        return CYBERCRIME_CATEGORIES[category]["subcategories"]
    return []

def validate_category(category):
    return category in CYBERCRIME_CATEGORIES

def validate_subcategory(category, subcategory):
    if category not in CYBERCRIME_CATEGORIES:
        return False
    return subcategory in CYBERCRIME_CATEGORIES[category]["subcategories"]
