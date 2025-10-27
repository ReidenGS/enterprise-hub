# 🌐 Enterprise Hub

A **Django-based enterprise management platform** that integrates **repair request tracking** and **automated employee data cleaning**.  
This project demonstrates full-stack web development, data automation, and cloud deployment skills.

---

## 🚀 Live Demo

🔗 [Demo on Alibaba Cloud](https://your-demo-link-here.com)  
*(Replace with your actual Alibaba Cloud public URL)*

---

## 🧾 Features

### 🧰 Repair Management System
- Employees can submit and track repair requests.
- Admins can view, approve, or close repair cases.
- Email notifications for status updates.

### 🧹 Employee Onboarding Data Cleaning
- Automatically validates and cleans onboarding Excel data.
- Detects duplicates and missing fields.
- Exports cleaned datasets for HR integration.

### 🧑‍💼 Admin Dashboard
- Centralized interface for both repair and HR data.
- Role-based access management.
- Data visualization and statistics summary.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django 5 · Python 3 |
| **Frontend** | HTML · CSS · Bootstrap |
| **Database** | SQLite (local) / MySQL (production) |
| **Deployment** | Alibaba Cloud · Nginx · Gunicorn |
| **Version Control** | Git · GitHub |

---

## ⚙️ Local Setup

```bash
# 1️⃣ Clone the repository
git clone https://github.com/yourusername/enterprise-hub.git
cd enterprise-hub

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ Run the server
python manage.py runserver
