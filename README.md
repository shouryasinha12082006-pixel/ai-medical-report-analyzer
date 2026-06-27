# Dooper AI Medical Report Analyzer

An AI-powered medical report analyzer web application designed with the official **Dooper** healthcare brand theme (Red/Grey color palette, custom cards, Outfit typography) and supporting a settings panel with an appearance toggle (Light/Dark Mode).

## Tech Stack
- **Backend:** Flask (Python 3)
- **Database:** MySQL
- **Frontend:** Vanilla HTML5, CSS3, ES6 JavaScript, FontAwesome
- **Charts:** Chart.js (via CDN)
- **PDF Generation:** ReportLab
- **PDF Parser:** PyPDF

## Features
1. **Authentication Module:** Secure registration and login with input validation, password hashing (`werkzeug.security`), protected session routing, and logout.
2. **Interactive Dashboard:** Dynamic analytics metrics showing total scans, normal scans, moderate warnings, and critical reports, alongside a Chart.js severity breakdown and report history.
3. **AI Medical Report Analyzer:** Allows uploading PDF reports and images (PNG, JPG, JPEG). Features a rules-based NLP parser that extracts parameters (Glucose, Hemoglobin, Cholesterol, Vitamin D) and flags out-of-range metrics.
4. **Report History:** Access previously uploaded and processed reports. Revisit complete breakdowns at any time.
5. **Appearance Toggle:** Global Settings option allowing live toggle between light and dark modes (responsive color schemes mapped via CSS Variables).
6. **Bonus Features Implemented:**
   - **Download Analysis as PDF:** Automatically generates a branded medical summary PDF using `reportlab`.
   - **Voice Summary:** Interactive Web Speech TTS player.
   - **Charts & Statistics:** Reactive donut chart for severity logs.

# Project Structure

```text
Dooper-AI-Medical-Report-Analyzer/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── uploads/
│   └── images/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── history.html
│   └── settings.html
│
├── uploads/
│
├── app.py
├── database.py
├── setup.py
├── medical_analyzer.sql
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Navigate to the Project Folder:**
   ```bash
   cd "C:\Users\Shourya Sinha\.gemini\antigravity-ide\scratch\ai_medical_report_analyzer"
   ```

2. **Initialize Python Virtual Environment & Activate:**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database & Copy Logo:**
   Run the setup script which creates the SQLite tables and copies the official `logo.png` from the `dooper_bi_dashboard` project:
   ```bash
   python setup.py
   ```

5. **Start Flask Server:**
   ```bash
   python app.py
   ```
   The application will start running at `http://127.0.0.1:5000/`.

## Environment Variables
The application runs with a default built-in session secret key. If deployed to production, set:
- `FLASK_SECRET_KEY`: Custom cryptographic key for signing sessions.
