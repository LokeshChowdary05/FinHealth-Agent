🌟 Project Overview
FinHealth is a full-stack web application that combines artificial intelligence, comprehensive healthcare data, and modern web technologies to solve real-world cost transparency problems. Built for scale with 4,000+ hospitals and 77 insurance plans across the US.

✨ Core Features
AI-Powered Symptom & Intent Analysis

Nationwide Hospital & Insurance Database

Real-Time Price & Insurance Coverage Comparison

Responsive, Accessible Chat-Based UI

Dynamic Data Visualization & Sorting

Secure & Modular Flask Backend

🛠️ Tech Stack
Backend: Python 3.8+, Flask 2.3.3, Together AI API, JSON-based storage

Frontend: HTML5, CSS3, JavaScript (ES6+), AJAX/Fetch API

Tools: Git & GitHub, VS Code, Virtual Environments, Automated Testing

🚀 Quick Start
Prerequisites

Python 3.8+

Git

Internet connection for AI API

Setup Instructions

bash
git clone https://github.com/LokeshChowdary05/FinHealth-Agent.git
cd FinHealth-Agent
python -m venv env
# Activate (Windows)
.\env\Scripts\Activate.ps1
# Activate (macOS/Linux)
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your API keys if needed
python app.py
# Visit http://localhost:5000
📁 Project Structure
text
FinHealth-Agent/
├── app.py
├── medical_analyzer.py
├── hospital_data.py
├── insurance_analyzer.py
├── conversation_manager.py
├── static/
│   ├── styles.css
│   └── script.js
├── templates/
│   └── index.html
├── data/
│   ├── nationwide_hospital_data.json
│   └── hospital_pricing_data.json
├── screenshots/
│   ├── Screenshot-2025-07-01-193437.jpg
│   └── Screenshot-2025-07-01-193551.jpg
└── requirements.txt
🎯 Example Use Cases
Symptom Analysis

text
User: "I have chest pain and shortness of breath in Dallas"
→ AI suggests relevant procedures, finds hospitals, compares prices, and estimates insurance coverage.
Procedure Comparison

text
User: "I need an MRI scan in Chicago, I have Aetna insurance"
→ Compares MRI prices across hospitals, calculates insurance coverage, and shows cash discount options.
📈 Performance & Coverage
4,000+ Hospitals nationwide

77 Insurance Plans integrated

All 50 States covered

Sub-second real-time responses

🏆 Professional Highlights
PEP8-compliant, documented codebase

Modular, scalable architecture

Comprehensive error handling & security

Automated testing & CI-ready

🤝 Contributing
Contributions are welcome!
See CONTRIBUTING.md for guidelines.

📞 Contact
Lokesh Chowdary Katta
GitHub | LinkedIn | lokeshchowdary.pl@gmail.com

📜 License
This project is licensed under the MIT License. See LICENSE for details.

Built to make healthcare costs transparent and accessible for everyone.

⭐ If you found this project useful, please star the repository!

Let me know if you want further customization or additional sections!
