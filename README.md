# CSV Data Ingestion Platform

A full-stack application for uploading, analyzing, and visualizing CSV data with a modern dashboard and comprehensive analytics.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Assumptions](#assumptions)

## Tech Stack

### 🔙 Backend

- **🚀 FastAPI** - Modern, fast web framework for building APIs
- **🐘 PostgreSQL 18** - Robust relational database
- **📚 SQLModel** - SQLAlchemy + Pydantic for type-safe ORM
- **🔄 Alembic** - Database migration management
- **🐼 Pandas** - Data manipulation and CSV processing
- **🧪 Pytest** - Comprehensive testing framework
- **🔐 Python-Jose** - JWT authentication with cryptographic signing
- **🔑 Bcrypt** - Secure password hashing
- **📦 Uvicorn** - ASGI web server

### 🎨 Frontend

- **💚 Vue 3.5** - Progressive JavaScript framework
- **⚡ Vite 7** - Next-generation build tool with instant HMR
- **🟦 TypeScript 5.9** - Type-safe JavaScript
- **🍍 Pinia** - State management with Colada for server-state
- **🎨 UnoCSS** - Atomic CSS engine (Tailwind-like utilities)
- **🎭 Radix Vue + Reka UI** - Headless, accessible component libraries
- **📊 Unovis Vue** - Interactive data visualization library
- **📋 TanStack Vue Table** - Headless, feature-rich data table
- **📦 Bun** - Fast JavaScript runtime and package manager
- **🧪 Vitest** - Unit testing powered by Vite
- **🔍 ESLint** - Code quality and linting

### 🐳 DevOps & Infrastructure

- **🐳 Docker** - Containerization
- **🐙 Docker Compose** - Multi-container orchestration
- **🌐 Nginx** - Reverse proxy and static file server
- **🔗 CORS Middleware** - Cross-origin resource sharing

### 🛠️ Development Tools

- **📝 Makefile** - Development command shortcuts
- **📦 uv** - Fast Python package manager
- **🔄 Hot Module Replacement (HMR)** - Instant code refresh
- **🧠 Auto imports** - Automatic component/utility imports
- **📐 File-based routing** - Convention over configuration

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** and **Docker Compose** (v2.0+)
  - [Docker Installation Guide](https://docs.docker.com/get-docker/)
  - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)
- **Make** (for convenience commands)
- **Bun** (for frontend development) - Optional, used for development
- **Python 3.12+** (for backend development) - Optional, used for development
- **A CSV file** with sales data
  - Example file: `example/sales_data_sample.csv`
  - Expected format: Headers with columns like Order ID, Product, Quantity, Price, etc.

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd csv-data-ingestion
   ```

2. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` if needed (default values work for local development)

3. **Build and start services**

   ```bash
   docker compose up -d
   ```

4. **Access the application**
   - **Frontend**: <http://localhost:8080>
   - **Backend API**: <http://localhost:8000>
   - **API Swagger Docs**: <http://localhost:8000/docs>

5. **Stop services**

   ```bash
   docker compose down
   ```

### Local Development

#### Setup Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
make migrate  # Run from root
```

#### Setup Frontend

```bash
cd frontend
bun install
```

#### Run Development Servers

From the root directory:

```bash
make dev
```

Or run individually:

```bash
# Terminal 1: Start database
make db

# Terminal 2: Start backend (FastAPI dev server)
make backend

# Terminal 3: Start frontend (Vite dev server)
make frontend
```

**Development URLs**:

- Frontend: <http://localhost:5173>
- Backend API: <http://localhost:8000>
- API Swagger: <http://localhost:8000/docs>

## Development

### Available Make Commands

```bash
make setup          # Initial project setup (install dependencies, setup database)
make dev            # Start all dev servers
make db             # Start database container
make backend        # Start backend dev server
make frontend       # Start frontend dev server
make migrate        # Run database migrations
make prod           # Build and run production containers
make prod-build     # Build production Docker images
make prod-stop      # Stop production containers
```

### Project Structure

```
csv-data-ingestion/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI application setup
│   │   ├── routers/        # API route handlers
│   │   │   ├── auth.py     # Authentication endpoints
│   │   │   └── datasets.py # Dataset management endpoints
│   │   └── ...
│   ├── migrations/         # Alembic database migrations
│   ├── tests/              # Backend tests
│   └── pyproject.toml      # Python dependencies
├── frontend/               # Vue 3 + Vite application
│   ├── src/
│   │   ├── pages/          # Page components (file-based routing)
│   │   ├── components/     # Reusable components
│   │   └── stores/         # Pinia state management
│   ├── test/               # Frontend tests
│   └── package.json        # Node dependencies
├── example/                # Example CSV data
├── compose.yaml            # Docker Compose configuration
├── .env.example            # Environment variables template
└── Makefile               # Development commands
```

## Production Deployment

### Build Production Images

```bash
docker compose -f compose.yaml build
```

### Environment Variables

Create a `.env` file with production values:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<secure-password>
POSTGRES_DB=csv_ingestion
SECRET_KEY=<secure-random-key>
PORT=80
```

### Run Production Stack

```bash
docker compose up -d
```

The application will be available at the configured `PORT` (default: 80).

## API Documentation

The backend provides interactive API documentation via Swagger UI at `/docs`.

### Key Endpoints

**Authentication**

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token
- `POST /api/auth/refresh` - Refresh authentication token

**Datasets**

- `GET /api/datasets` - List all datasets
- `POST /api/datasets/upload` - Upload and process CSV file
- `GET /api/datasets/{dataset_id}` - Get dataset details
- `GET /api/datasets/{dataset_id}/data` - Get dataset records
- `GET /api/datasets/{dataset_id}/summary` - Get dataset analytics

**Health**

- `GET /api/health` - Service health check

For detailed request/response schemas, visit the Swagger UI at <http://localhost:8000/docs>

## Testing

### Backend Tests

```bash
cd backend
pytest                    # Run all tests
pytest -v               # Run with verbose output
pytest tests/test_api.py # Run specific test file
pytest -k test_name     # Run tests matching pattern
```

### Frontend Tests

```bash
cd frontend
bun test                # Run all tests
bun test -- --watch    # Run in watch mode
bun test -- --ui       # Run with UI
```

## Assumptions

1. **CSV Format**: The uploaded CSV files are expected to have a header row with column names. Data consistency is not validated at upload time - errors may be caught during processing.

2. **Authentication**: The application uses JWT-based authentication stored in secure httpOnly cookies. Authentication is required for all data operations.

3. **Database**: PostgreSQL 18 is used as the primary database. The database schema is automatically initialized via Alembic migrations on first run.

4. **File Upload Limits**: Large CSV files are processed in memory. File size limits may apply depending on server memory availability.

5. **CORS**: In development, CORS is permissive (`allow_origins=["*"]`). For production, update this in `backend/app/main.py`.

6. **Frontend Build**: The frontend is served as static files from an Nginx container. The API URL for the frontend is configured during build time.

7. **Data Privacy**: All data is stored in a local PostgreSQL container. No data is sent to external services. For production, ensure proper backup and security measures are in place.

8. **Timezone**: All timestamps are stored in UTC. Client-side timezone handling depends on the frontend implementation.

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL container is healthy: `docker compose ps`
- Check logs: `docker compose logs db`

### Port Already in Use

- Change `PORT` in `.env` file
- Or kill existing process: `lsof -i :8080` and `kill -9 <PID>`

### Migration Failures

- Check database logs: `docker compose logs migrate`
- Manually verify database: `docker compose exec db psql -U postgres -d csv_ingestion`

### Frontend Build Issues

- Clear node_modules: `cd frontend && rm -rf node_modules bun.lock && bun install`
- Clear build cache: `rm -rf frontend/dist`

## Support

For issues or questions, check the individual README files in the `backend/` and `frontend/` directories for component-specific details.
