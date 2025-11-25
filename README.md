<div align="center">
  
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)
<h1>maria-tutor</h1>
Personal website for biology/chemistry tutor Maria Seredinskaya
  <h3>✨ Check it Out!</h3>
  <a href="https://www.maria-tutor.ru">
    <img src="https://img.shields.io/badge/||_‎_‎_‎_‎_OPEN_WEBSITE_‎_‎_‎_‎||-0969DA?style=for-the-badge&logoColor=white" alt="Open Maria-tutor">
  </a>
</div>

## Overview

This is a complex Django project that serves as a website with dynamic rendering from tutor content templates and personally for chimestry tutor for Maria Seredinskaya. It includes a basic homepage and is set up for further development.

---

## Features

- Basic Django setup
- Main homepage (index page)
- Ready for customization and expansion

- **🎯 Project Board:** [View project board](https://github.com/users/ErnestoAizenberg/projects/3)
---

## Screenshots
![image_2025-10-19_16-20-39](https://github.com/user-attachments/assets/20d15b2f-0911-47bd-b8c1-222f5cb5c63c)


## Getting Started

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/ErnestoAizenberg/maria-tutor.git
cd maria-tutor
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment:

```bash
cp .env.example .env
```

5. Apply migrations and run the development server:

```bash
python manage.py migrate
python manage.py runserver
```

6. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the homepage.

---

## Project Structure

- `manage.py` — Django's command-line utility
- `run.sh` — custom utility for project management
- `requirements.txt` — Dependencies
- `README.md` — Project description
- `LICENSE` — License info
- `.gitignore` — Files to ignore in version control
- `main` — App directory with tutor pages
- `telegram_bot` - Telegram bot for display application UI as Telegram Mini App

---

## License

This project is licensed under the Apache License. See the LICENSE file for details.

---
