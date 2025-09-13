# Brecon Jazz Web App

A lightweight web application for the Brecon Jazz Festival.  
The app provides festival information such as **schedule, bands, and venues** in a clean, mobile-friendly interface.  

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) (Python backend)
- [Jinja2](https://jinja.palletsprojects.com/) (HTML templating)
- [HTMX](https://htmx.org/) + [Alpine.js](https://alpinejs.dev/) (frontend interactivity)
- [PostgreSQL](https://www.postgresql.org/) (database)

---

## 🚀 Features
- 📅 Festival schedule  
- 🎷 Bands listing  
- 🏟️ Venues page with map previews  

---
## Setup Instructions

### Database Initialization

This application uses a PostgreSQL database (or SQLite for local development). 

Before running the app for the first time on a new environment (such as a developer machine or a fresh server), **you must initialize the database schema and seed initial data** by running the included `init_db.py` script:

This script creates the database tables and inserts initial festival data such as bands, venues, and gigs.

You only need to run this script once per database. After the database has been initialized, you can start the app normally, without rerunning the script.

For production deployments, incorporate this initialization step into your deployment procedure or use database migration tools like Alembic for easier schema management.

---

**Note:** If you are using a different database or configuration, adjust the connection settings in `app/database.py` accordingly.
