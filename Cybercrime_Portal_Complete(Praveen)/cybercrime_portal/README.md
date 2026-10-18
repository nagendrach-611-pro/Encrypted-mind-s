# 🛡️ Cybercrime Incident Classification & Reporting Portal

A Streamlit BTech project prototype for cybercrime complaint intake, preliminary AI-assisted classification, case management, evidence hashing, officer notes, audit logs, analytics and PDF reporting.

## Included
- Admin login/session
- Complaint reporting form
- Explainable offline classifier
- Category/subcategory/priority/confidence
- SQLite case database
- Officer dashboard and charts
- Case search and investigation workflow
- Evidence upload + SHA-256 hashing
- Status history and audit logs
- PDF case reports

## Run on Windows
```powershell
cd cybercrime_portal
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Demo login
- Username: `admin`
- Password: `admin123`

Change the demo credential before deployment. This is a project prototype; do not use it for real law-enforcement data without proper security, legal, privacy and operational controls.

## Main files
`app.py` — UI/workflows  
`database.py` — SQLite persistence  
`ai_classifier.py` — preliminary classification  
`categories.py` — crime taxonomy  
`report_generator.py` — PDF/text reports  
`sample_data.py` — sample data loader

## Recommended future upgrades
PostgreSQL, FastAPI, Argon2/bcrypt password hashing, RBAC/MFA, encrypted evidence storage, antivirus scanning, rate limiting, secrets management, retention policies, production audit controls, and a trained/validated ML model.
