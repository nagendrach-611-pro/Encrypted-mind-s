"""
Insert sample cases for testing.
"""

from database import CybercrimeDatabase


def add_sample_data():
    db = CybercrimeDatabase()

    samples = [
        {
            "complainant_name": "Sample User",
            "contact_number": "9876543210",
            "incident_location": "Hyderabad",
            "complaint_description": "Received a fake email asking for OTP and bank details.",
            "evidence_info": "Email screenshot available",
            "incident_date": "2026-10-01",
            "category": "Phishing",
            "subcategory": "Email Phishing",
            "priority": "High",
            "confidence": 0.90,
            "ai_summary": "Possible phishing attempt involving sensitive banking information."
        }
    ]

    for sample in samples:
        success, result = db.insert_case(sample)
        print(result if success else f"Error: {result}")


if __name__ == "__main__":
    add_sample_data()
