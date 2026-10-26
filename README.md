
# 🔐 Advanced Password Security Suite

A mini cybersecurity project built with Python and Streamlit to help users analyze password strength, generate secure passwords, compare passwords, and learn safer password practices.

## ✨ Features

- **Password Analysis:** Score out of 100, security checklist, risk level, and recommendations.
- **Password Generator:** Cryptographically random passwords from 16–24 characters.
- **Strength Comparison:** Compare two passwords using the same security rules.
- **Security Insights:** Practical password security guidance.
- **Breach Check:** Check against known breached passwords using the Have I Been Pwned range API.
- **Downloadable Report:** Export analysis results without including the password.
- **Privacy-Focused:** No password history or account system.

## 🛠️ Technologies

- Python
- Streamlit
- Requests
- GitHub

## 🚀 Run Locally

1. Install Python 3.10 or later.
2. Clone this repository.
3. Open a terminal in the project folder.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Start the application:

   `streamlit run app.py`

## 🔒 Privacy Notes

- The application does not intentionally save password analysis history.
- Never test with passwords used for real accounts.
- The breach checker sends only a partial SHA-1 hash prefix to the external service, not the raw password.
- Password strength scores are estimates, not guarantees of security.

## 📌 Project Scope

This is an educational mini cybersecurity project. Pattern detection uses a limited rule set and cannot identify every weak password.

## 👩‍💻 Project Status

Under development.
