# Django Recruitment Task

## Setup Instructions

Copy the `.env.example` file to `.env` and set your environment variables:

```bash
cp .env.example .env
```

Install dependencies and set up the virtual environment:

```bash
uv venv
source .venv/bin/activate
uv sync
```

Run migrations:

```bash
uv run manage.py migrate
```

Create a superuser:

```bash
uv run manage.py createsuperuser
```

Run the development server:

```bash
uv run manage.py runserver
```
