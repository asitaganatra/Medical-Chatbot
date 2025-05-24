 Medical Chatbot (Django)

📌 Project Overview

A Django-based medical chatbot application designed to provide basic medical information and assistance. The project follows a modular structure for better scalability and maintenance.

---

🗂️ Project Structure

Mchatbot/
├── members/ # User management module
├── mystaticfiles/ # Static files (CSS, JS, images)
├── myworld/ # Core chatbot functionality
├── productionfiles/ # Deployment-related files
├── manage.py # Django management script


---

✨ Features

- 🧑‍⚕️ Interactive medical chatbot interface
- 🔐 User authentication system (login/registration)
- 💻 Responsive and clean UI
- ⚙️ Django admin interface for content management
- 🧩 Modular architecture for easy maintenance

---

🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [repository-url]
   cd Mchatbot
        python -m venv venv source venv/bin/activate  # On Windows: venv\Scripts\activate
        pip install -r requirements.txt
        python manage.py migrate
        python manage.py createsuperuser
        python manage.py runserver
   





