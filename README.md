# 🏛️ Delhi High Court Case Lookup

A lightweight web application that allows users to fetch case details from the Delhi High Court website using case type, number, year, and CAPTCHA input. Built with a React frontend and Django REST backend.

---

video link
https://www.loom.com/share/08da79bef30543bfb35ad6b4f1974310?sid=ae676d3a-d1b4-4029-8a94-48d93bf26c44


## 🚀 Features

- 🔍 Real-time case data retrieval from the official Delhi HC site
- 🔐 Manual CAPTCHA input for secure access
- 📄 Displays party names, filing date, next hearing date, and latest order PDF
- 🗂 Logs raw HTML responses for debugging and audit purposes

---

## 🛠️ Tech Stack

| Layer      | Technology               |
|------------|--------------------------|
| Frontend   | React                    |
| Backend    | Django REST Framework    |
| Scraping   | BeautifulSoup + requests |
| Database   | Django ORM (CaseQueryLog) |

---

## 📦 Installation

### Backend (Django)

```bash
git clone https://github.com/yourname/dhc-case-lookup.git
cd backend/
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
