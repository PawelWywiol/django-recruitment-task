# Django Recruitment Task

```
! Work in Progress !
```

This repository is a Django version of the [NextJS recruitment task](https://github.com/PawelWywiol/nextjs-recruitment-task). It implements a complete REST API for managing users and their addresses using Django REST Framework. It provides a robust backend solution with comprehensive API documentation, health monitoring, and modern development tooling.

## Features

- **Complete REST API** with full CRUD operations for users and addresses
- **Health Check Endpoint** for monitoring application status
- **Swagger/OpenAPI Documentation** with interactive UI
- **Django Admin Interface** for data management
- **Comprehensive Test Suite** with CRUD functionality tests
- **PostgreSQL/SQLite Database Support**
- **Modern Python Tooling** with uv package manager
- **Code Quality Tools** with Ruff linting and formatting

## Quick Start

### Environment Setup

```bash
# Copy environment configuration
cp .env.example .env

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv sync
```

### Database Setup

```bash
# Run database migrations
uv run python manage.py migrate

# Create superuser account (optional)
uv run python manage.py createsuperuser
```

### Development Server

```bash
# Start development server
uv run python manage.py runserver

# Access the application
# API Documentation: http://localhost:8000/api/
# Django Admin: http://localhost:8000/admin/
# Health Check: http://localhost:8000/health/
```

## API Endpoints

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/users/` | List all users (paginated) |
| `POST` | `/api/users/` | Create a new user |
| `GET` | `/api/users/{id}/` | Retrieve specific user with addresses |
| `PUT` | `/api/users/{id}/` | Update user (full update) |
| `PATCH` | `/api/users/{id}/` | Partially update user |
| `DELETE` | `/api/users/{id}/` | Delete user and all addresses |

### User Address Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/users/{id}/address/` | List addresses for specific user |
| `POST` | `/api/users/{id}/address/` | Create new address for user |
| `GET` | `/api/users/{id}/address/{address_id}/` | Retrieve specific address |
| `PUT` | `/api/users/{id}/address/{address_id}/` | Update address (full update) |
| `PATCH` | `/api/users/{id}/address/{address_id}/` | Partially update address |
| `DELETE` | `/api/users/{id}/address/{address_id}/` | Delete address |

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health/` | Application health check |
| `GET` | `/api/` | Swagger UI documentation |
| `GET` | `/redoc/` | ReDoc API documentation |
| `GET` | `/admin/` | Django admin interface |

## Health Check

The health check endpoint (`/health/`) monitors application status and database connectivity:

```bash
curl http://localhost:8000/health/
```

**Response Format:**
```json
{
  "status": "UP|DOWN",
  "checks": [
    {
      "name": "databaseReady",
      "status": "UP|DOWN"
    }
  ]
}
```

- Returns **HTTP 200** when healthy
- Returns **HTTP 503** when unhealthy (database connection issues)

## API Usage Examples

### Create User

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "status": "ACTIVE"
  }'
```

### Create User Address

```bash
curl -X POST http://localhost:8000/api/users/1/address/ \
  -H "Content-Type: application/json" \
  -d '{
    "address_type": "HOME",
    "valid_from": "2025-09-26T10:00:00Z",
    "post_code": "12345",
    "city": "New York",
    "country_code": "USA",
    "street": "Main Street",
    "building_number": "123"
  }'
```

### Update Address

```bash
curl -X PATCH http://localhost:8000/api/users/1/address/1/ \
  -H "Content-Type: application/json" \
  -d '{"city": "Updated City"}'
```

## Testing

### Run Tests

```bash
# Run all tests
uv run python manage.py test

# Run specific app tests
uv run python manage.py test users

# Run with verbose output
uv run python manage.py test --verbosity=2

# Run with coverage (if coverage is installed)
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage

The test suite includes:
- **User CRUD Operations**: Create, read, update, delete users
- **Address CRUD Operations**: Manage user addresses with proper relationships
- **Validation Testing**: Email uniqueness, required fields
- **API Response Testing**: Status codes, response formats
- **Database Relationship Testing**: Foreign key constraints, cascading deletes

## Code Quality

### Linting and Formatting

```bash
# Check code quality
ruff check .

# Fix auto-fixable issues
ruff check . --fix

# Format code
ruff format .

# Check specific files
ruff check users/models.py
```

## Project Structure

```
├── app/                    # Main Django project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # Root URL configuration
│   ├── views.py          # Application-level views (health check)
│   └── wsgi.py           # WSGI application
├── users/                 # Users app
│   ├── models.py         # User and UserAddress models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views and ViewSets
│   ├── urls.py           # App URL configuration
│   ├── admin.py          # Django admin configuration
│   └── tests.py          # Test suite
├── docker/               # Docker configuration
├── pyproject.toml        # Project dependencies and configuration
├── manage.py            # Django management script
└── README.md            # This file
```

## Architecture Decisions

### API-First Design
- Swagger/OpenAPI documentation automatically generated
- RESTful endpoint design with proper HTTP methods
- Consistent error handling and validation
- Nested resources for logical data relationships

### Modern Python Tooling
- **uv** for fast dependency management
- **Ruff** for linting and formatting (120 char line length)
- **Type hints** throughout the codebase
- **pyproject.toml** for modern project configuration

### Database Design
- Proper foreign key relationships with CASCADE deletes
- Unique constraints for business logic
- Choice fields for controlled vocabularies
- Automatic timestamp management

### Scalability Considerations
- Modular app structure for easy extension
- Generic ViewSets for consistent CRUD patterns
- Proper database indexing on foreign keys
- Pagination support for large datasets
