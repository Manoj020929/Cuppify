# ☕ Cuppify – Cafe Management System

A full-stack cafe management web application built with Django and deployed online on PythonAnywhere. Customers enter their details and place orders from the menu, and the cafe admin manages products and orders from a dedicated admin panel.

**Live demo:** https://manoj09.pythonanywhere.com

## Features
- Customer entry screen (name and phone number)
- Menu browsing and order placement
- Order management through Django models and views
- Admin panel to add, edit and delete products and manage orders
- Clean HTML/CSS interface
- Built on Django's MVT (Model–View–Template) architecture
- Deployed live on PythonAnywhere

## Tech stack
| Layer | Technology |
|---|---|
| Frontend | HTML, CSS |
| Backend | Python, Django |
| Database | [MySQL / SQLite] (Django ORM) |
| Hosting | PythonAnywhere |

## Deployment (PythonAnywhere)
1. Uploaded the project to PythonAnywhere by cloning it from GitHub in a Bash console.
2. Created a virtualenv and installed `requirements.txt`.
3. Created a web app (manual configuration) and pointed the WSGI file at the Django project.
4. Set `ALLOWED_HOSTS` to include `[your-username].pythonanywhere.com`.
5. Configured the database [and ran `python manage.py migrate`].
6. Mapped `/static/` to the collected static files folder (`python manage.py collectstatic`).
7. Reloaded the web app from the Web tab.


<img width="1360" height="768" alt="image" src="https://github.com/user-attachments/assets/7699fb3c-f4e2-4027-a61b-e4adaf172d07" />
<img width="1360" height="768" alt="image" src="https://github.com/user-attachments/assets/04ac4094-f9db-4aca-b786-38e78a9183d4" />


