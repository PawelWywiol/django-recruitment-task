## Django Recruitment Task

```
! Work in Progress !
```

This repository is a Django version of the [NextJS recruitment task](https://github.com/PawelWywiol/nextjs-recruitment-task). It implements a complete REST API for managing users and their addresses with Django REST Framework.

## Features

- **REST API** with full CRUD operations for users and addresses
- **Swagger/OpenAPI documentation** at `/api/`
- **Django Admin interface** for easy data management
- **PostgreSQL/SQLite database support**
- **Modern Python tooling** with uv package manager
- **Code quality** with Ruff linting and formatting

## API Endpoints

- **GET/POST** `/api/users/` - List/create users
- **GET/PUT/PATCH/DELETE** `/api/users/{id}/` - User operations
- **Swagger UI** `/api/` - Interactive API documentation
- **Django Admin** `/admin/` - Administrative interface

## Development Commands

Environment setup

```bash
cp .env.example .env
uv venv
source .venv/bin/activate
uv sync
```

Database operations

```bash
uv run manage.py migrate
uv run manage.py createsuperuser
```

Development server

```bash
uv run manage.py runserver
```

Code quality

```bash
ruff check .
ruff format .
```

Django management

```bash
uv run manage.py makemigrations
uv run manage.py shell
```

## Architecture Overview

This Django recruitment task implements a user address management system with PostgreSQL backend. The application is designed to be modular and extensible for future CRUD components.

## API Usage

### List Users
```bash
curl http://localhost:8000/api/users/
```

### Create User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com", "status": "ACTIVE"}'
```

### Access Documentation
- **Swagger UI**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

### Key Architectural Decisions

#### Modern Python Tooling
- Uses `uv` instead of pip for faster dependency management
- Modern `pyproject.toml` configuration
- Comprehensive Ruff configuration with 120 character line length and all linting rules enabled except documentation

#### API-First Design
- Swagger/OpenAPI documentation configured via drf-yasg
- API documentation available at `/api/` (Swagger UI) and `/redoc/`
- Django REST Framework ready for API implementation

#### Database Design Patterns
- Composite primary keys for address versioning
- CASCADE delete for address cleanup when users are removed
- Proper model choices for status and address types
- Automatic timestamp management

## Task

Create a NextJS application which allows you to manage users' addresses. The database schema with sample records is provided for you, you can set it up by running:

```bash
docker compose up
```

## ~~UI Requirements~~

1. ~~The UI should only include what's required in task's description. There is no need to build authentication, menus or any features besides what's required.~~
2. ~~The UI should consist of:~~

-   ~~A paginated users' list. Add a mocked button to **Create** a new user above the list and in each record, a context menu with mocked **Edit** and **Delete** buttons.~~
-   ~~A paginated users' addresses list. The list should be visible after clicking a user record in the users' list.~~
-   ~~In the addresses list, include a context menu where you can **Edit** and **Delete** an address record.~~
-   ~~Add the ability to **Create** a new user address.~~
-   ~~**Create** and **Edit** forms should be implemented in modals.~~
-   ~~When inputting address fields, display a preview of the full address in the realtime in the following format:~~

```
<street> <building_number>
<post_code> <city>
<country_code>
```

3. ~~You may use any UI library: MUI, AntD, etc.~~
4. ~~Handle data validation errors coming from the server.~~

## Server Requirements

1. Use the database schema provided. Do not modify it.
2. ~~Implement ["Server Actions"](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations) which the frontend should use to interact with the database.~~
3. You may use any ORM or Query Builder.
4. Introduce simple data validation. Nothing fancy, you can use constraints from the database schema. Country codes use ISO3166-1 alpha-3 standard.

## General Requirements

1. Expect the application to eventually include many similar CRUD components (i.e. "users_tasks", "users_permissions", etc.), make your code modular, extensible and generic so that similar modules can be developed with less overhead.
2. Keep the code clean, scalable, follow known conding conventions, paradigms, patterns, etc.
3. Use TypeScript.
4. You do not have to deploy the application, but prepare the codebase for deployment to an environment of your choice.
