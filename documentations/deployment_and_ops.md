# Deployment & Operations Guide

The Mono Electric system is designed for high availability and easy scalability through Docker.

## 🐳 Docker Architecture

The project uses `docker-compose` to orchestrate 5 essential services:

1.  **Web (Django)**: The Gunicorn/Uvicorn-based application handling the Admin Panel and Web App API.
2.  **Bot (Aiogram)**: A dedicated container running the Telegram bot's polling/webhook loop.
3.  **DB (PostgreSQL)**: Persistently stores all relational data.
4.  **Redis**: Acts as the message broker for Celery and caching layer.
5.  **Worker (Celery)**: Processes long-running tasks:
    - Mass broadcasts.
    - PDF/Image generation.
    - Data synchronization.
6.  **Beat (Celery Beat)**: Schedules periodic tasks (e.g., cleaning old logs, stats updates).

## 🚀 Setting Up Production

1.  **Clone & Configure**:
    ```bash
    git clone <repo_url>
    cp .env.example .env
    # Set SECRET_KEY, TELEGRAM_BOT_TOKEN, and DB credentials
    ```
2.  **Build & Launch**:
    ```bash
    docker-compose -f docker-compose.prod.yml up -d --build
    ```
3.  **Bootstrap**:
    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

## 📈 Monitoring & Logging

- **Sentry**: Integrated in both the Django and Aiogram services to capture exceptions in real-time.
- **Logs**:
  - Container logs: `docker-compose logs -f web bot`
  - Internal Django logs: Located in the `logs/` directory.
- **Health Checks**: 
  - `GET /health/`: Returns the status of the DB and Redis connections.

## ⚙️ Key Environment Variables

| Variable | Requirement | Description |
| :--- | :--- | :--- |
| `DEBUG` | Optional | Set to `False` in production. |
| `TELEGRAM_BOT_TOKEN` | **Required** | The API token from @BotFather. |
| `WEB_APP_URL` | **Required** | The public HTTPS URL where the Web App is hosted. |
| `DATABASE_URL` | **Required** | PostgreSQL connection string. |
| `SENTRY_DSN` | Optional | For error tracking. |

## 🛠️ Maintenance Tasks

- **QR Generation**: Admins can generate and download ZIP archives of codes via the Django Admin.
- **Data Backup**: Use `pg_dump` on the PostgreSQL container:
    ```bash
    docker-compose exec db pg_dump -U user_name db_name > backup.sql
    ```
- **Updating the Bot**: A simple `docker-compose restart bot` is usually sufficient for minor changes.
