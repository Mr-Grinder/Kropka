IP-Logger — README
A simple Flask-based IP logger for quickly tracking visitors with an instant redirect to the target page. Ideal for legitimate analytics, link testing (with consent), and demonstrations.
Do not use it for harm — this is for learning, testing and security research only. 😉
What It Does
This project accepts a visitor on a “landing” page, collects basic information (IP, UA, geo via ipinfo, a simple browser fingerprint), stores everything in CSV files, and instantly redirects the visitor to the original site. It comes with simple HTML templates for / → landing page, /friend → logging + redirect, and /check → displays IP to the user.
Features
Logs: timestamp, IP, city/region/country/org (via ipinfo), User-Agent + parsing (user_agents), referrer, Accept-Language.
Collects client-side “fingerprint” via JS (timezone, language, platform, hwConcurrency, screen, visitorId).
Writes to visitors.csv and fingerprints.csv.
Redirects to the external target after logging.
Simple template + static CSS included.
Recommended File Structure
ip-logger/
├─ app.py                # Flask code
├─ templates/
│  ├─ invite.html
│
├─ static/
│  └─ fake_site.css
├─ visitors.csv
├─ fingerprints.csv
├─ requirements.txt
Quick Start (local)
Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate
pip install Flask user_agents requests
# or pip install -r requirements.txt
Run:
python app.py
Open in your browser http://localhost:8080/ or send someone https://your.domain/friend.
