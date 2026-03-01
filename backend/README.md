# CSV Data Ingestion Backend

A FastAPI backend for handling CSV data uploads, storage, and analysis with JWT-based authentication and PostgreSQL database.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Database](#database)
- [Assumptions](#assumptions)

## Prerequisites

- **Python 3.12+**
- **PostgreSQL 18+** (for database)
- **pip** or **uv** (Python package manager)
- **Git**

For Docker-based setup, see the root README.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using `pip`:

```bash
pip install -e ".[dev]"
```

### 3. Configure Environment

Create a `.env` file in the backend directory:

```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=csv_ingestion
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Security
SECRET_KEY=your-secret-key-here

# Server
API_HOST=0.0.0.0
API_PORT=8000
```

Or copy from example:

```bash
cp ../.env.example .env
```

### 4. Initialize Database

Start PostgreSQL and run migrations:

```bash
# If using Docker
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:18-alpine

# Run migrations
alembic upgrade head
```

## Running the Server

### Development Mode

```bash
fastapi dev app/main.py
```

Server will start at `http://localhost:8000`

### Production Mode

```bash
fastapi run --port 8000 app/main.py
```

### Using Docker

```bash
docker build -t csv-backend .
docker run -p 8000:8000 --env-file .env csv-backend
```

## API Documentation

### Interactive API Docs

Once the server is running, visit:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

### Endpoints Overview

#### Health Check

```
GET /api/health
```

Returns service health status.

#### Authentication

**Register User**

```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}

Response: 201 Created
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe"
}
```

**Login**

```
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secure_password

Response: 200 OK
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

**Refresh Token**

```
POST /api/auth/refresh
Authorization: Bearer {token}

Response: 200 OK
{
  "access_token": "new_jwt_token",
  "token_type": "bearer"
}
```

#### Datasets

**List All Datasets**

```
GET /api/datasets
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "id": "uuid",
    "name": "sales_data.csv",
    "created_at": "2024-02-28T10:30:00Z",
    "row_count": 5000,
    "columns": ["Order ID", "Product", "Quantity", ...]
  }
]
```

**Upload CSV File**

```
POST /api/datasets/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: <csv_file>

Response: 201 Created
{
  "id": "uuid",
  "name": "sales_data.csv",
  "row_count": 5000,
  "columns": [...],
  "created_at": "2024-02-28T10:30:00Z"
}
```

**Get Dataset Details**

```
GET /api/datasets/{dataset_id}
Authorization: Bearer {token}

Response: 200 OK
{
  "id": "uuid",
  "name": "sales_data.csv",
  "row_count": 5000,
  "columns": [...],
  "created_at": "2024-02-28T10:30:00Z"
}
```

**Get Dataset Records**

```
GET /api/datasets/{dataset_id}/data?limit=100&offset=0
Authorization: Bearer {token}

Response: 200 OK
{
  "total": 5000,
  "limit": 100,
  "offset": 0,
  "data": [
    {"Order ID": "1001", "Product": "Widget", ...},
    ...
  ]
}
```

**Get Dataset Analytics Summary**

```
GET /api/datasets/{dataset_id}/summary
Authorization: Bearer {token}

Response: 200 OK
{
  "total_rows": 5000,
  "columns": ["Order ID", "Product", ...],
  "numeric_columns": {
    "Quantity": {
      "min": 1,
      "max": 100,
      "mean": 25.5,
      "median": 25
    }
  },
  "categorical_columns": {
    "Product": {
      "unique_values": 45,
      "top_values": ["Widget", "Gadget", ...]
    }
  }
}
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
```

### Run Tests Matching Pattern

```bash
pytest -k "login" -v
```

### Run with Coverage

```bash
pytest --cov=app
```

### Test Structure

Tests are organized by feature:

```
tests/
├── test_auth.py          # Authentication tests
├── test_datasets.py      # Dataset operation tests
├── test_api.py          # General API tests
└── conftest.py          # Shared test fixtures
```

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application setup
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   └── datasets.py        # Dataset endpoints
│   ├── models/
│   │   ├── user.py            # User database model
│   │   ├── dataset.py         # Dataset database model
│   │   └── schemas.py         # Pydantic request/response schemas
│   ├── services/
│   │   ├── auth_service.py    # Authentication logic
│   │   ├── dataset_service.py # Dataset processing logic
│   │   └── csv_processor.py   # CSV parsing and analysis
│   ├── db/
│   │   └── session.py         # Database session management
│   └── core/
│       ├── config.py          # Configuration management
│       └── security.py        # JWT and password utilities
├── migrations/                 # Alembic database migrations
├── tests/                      # Test suite
├── pyproject.toml             # Python dependencies
├── alembic.ini                # Alembic configuration
└── .env                       # Environment variables
```

## Database

### Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

Downgrade migrations:

```bash
alembic downgrade -1
```

View migration history:

```bash
alembic history
```

### Current Schema

**users** table

- `id` (UUID) - Primary key
- `email` (VARCHAR) - Unique email address
- `password_hash` (VARCHAR) - Hashed password
- `full_name` (VARCHAR) - User's full name
- `created_at` (TIMESTAMP) - Account creation timestamp

**datasets** table

- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to users
- `name` (VARCHAR) - Original CSV filename
- `data` (JSONB) - CSV data stored as JSON
- `row_count` (INTEGER) - Number of rows
- `columns` (TEXT[]) - Array of column names
- `created_at` (TIMESTAMP) - Upload timestamp

### Database Connection

The application uses SQLModel (SQLAlchemy + Pydantic) for ORM operations. Connection pooling is configured for production deployments.

## Assumptions

1. **CSV Format**: Uploaded files must be valid CSV with:
   - A header row containing column names
   - Consistent number of columns across all rows
   - UTF-8 encoding

2. **File Size**: CSV files are loaded entirely into memory for processing. Maximum practical file size depends on available server memory. Consider implementing streaming for production deployments with large files.

3. **Authentication**:
   - JWT tokens expire after a configurable period (default: 24 hours)
   - Tokens are validated on every protected endpoint
   - Users must have an account to upload and view datasets

4. **Data Storage**:
   - CSV data is stored as JSON in the database
   - This approach works well for datasets up to ~10,000 rows
   - For larger datasets, consider storing CSV files in object storage (S3, GCS) instead

5. **Column Names**: Column names from CSV headers are used as-is:
   - Special characters are preserved
   - Duplicate column names will cause issues during processing
   - Consider normalizing column names in production

6. **Error Handling**:
   - CSV parsing errors are returned with 400 Bad Request
   - Database errors return 500 Internal Server Error
   - Invalid credentials return 401 Unauthorized

7. **CORS**: Currently configured to accept requests from all origins (`*`). Update `CORSMiddleware` configuration in `app/main.py` for production.

8. **Security**:
   - Passwords are hashed using bcrypt
   - HTTPS should be enforced in production (configure in reverse proxy)
   - `SECRET_KEY` must be changed in production

9. **Timezone**: All timestamps are stored and returned in UTC. The client is responsible for timezone conversion.

10. **Concurrency**: The application uses async/await patterns and can handle multiple concurrent requests. Database connection pooling is configured for optimal performance.

## Development Tips

### Debug Mode

Enable FastAPI debug mode:

```python
app = FastAPI(debug=True)
```

### Database Shell

Access PostgreSQL directly:

```bash
psql -U postgres -d csv_ingestion
```

### Check Logs

View application logs:

```bash
# Within Docker
docker compose logs backend -f

# Local development
# Logs appear in terminal running fastapi dev
```

### Reset Database

Drop all tables and recreate schema:

```bash
alembic downgrade base  # Remove all migrations
alembic upgrade head    # Reapply all migrations
```

## Deployment Checklist

- [ ] Set `SECRET_KEY` to a secure random value
- [ ] Update database credentials
- [ ] Set `POSTGRES_PASSWORD` to a strong password
- [ ] Enable HTTPS in production
- [ ] Configure CORS for specific frontend domain
- [ ] Set up proper logging and monitoring
- [ ] Configure database backups
- [ ] Test migrations on production database
