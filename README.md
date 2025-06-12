# maria-tutor
Personal website for Maria Seredinskaya.

---

## Overview

This is a simple Django project that serves as a personal website for Maria Seredinskaya. It includes a basic homepage and is set up for further development.

---

## Features

- Basic Django setup
- Main homepage (index page)
- Ready for customization and expansion

---

## Getting Started

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
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

4. Apply migrations and run the development server:

```bash
python manage.py migrate
python manage.py runserver
```

5. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the homepage.

---

## Project Structure

- `manage.py` — Django's command-line utility
- `requirements.txt` — Dependencies
- `README.md` — Project description
- `LICENSE` — License info
- `.gitignore` — Files to ignore in version control
- `main` (or similar) — App directory with main code

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---
