# FastAPI Project Template

A modern, production-ready FastAPI template designed for rapid prototyping and API development. Features clean architecture, built-in authentication, SQLAlchemy ORM, and Docker containerization.

## Features

- ⚡ **FastAPI** - High-performance Python web framework
- 🔐 **API Key Authentication** - Simple Bearer token authentication
- 🗄️ **SQLAlchemy ORM** - Database abstraction with SQLite default
- 🐳 **Docker Ready** - Containerized development and deployment
- 📋 **Auto-Generated API Docs** - Interactive Swagger UI
- 🔄 **Hot Reload** - Development server with automatic code reloading
- ⚙️ **Configurable** - Environment-based configuration with Pydantic
- 🧪 **Testing Ready** - Pytest integration for comprehensive testing

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (recommended)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-project-template
   ```

2. **Option A: Using Docker (Recommended)**
   ```bash
   docker-compose up
   ```

3. **Option B: Local Development**
   ```bash
   pip install -r requirements.txt
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///./app.db

# Authentication - JSON format for lists
API_KEYS=["dev-key-123", "dev-key-456", "your-custom-key"]
ENABLE_AUTH=true

# API Settings  
DEBUG=true
LOG_LEVEL=INFO
ENABLE_SWAGGER=true

# CORS - JSON format for lists
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

### Key Settings

- **`API_KEYS`**: JSON array of valid API keys
- **`ENABLE_AUTH`**: Toggle authentication on/off
- **`DEBUG`**: Enable debug mode
- **`ENABLE_SWAGGER`**: Show/hide API documentation
- **`DATABASE_URL`**: Database connection string

## API Usage

### Authentication

All protected endpoints require an API key in the Authorization header:

```bash
curl -H "Authorization: Bearer dev-key-123" http://localhost:8000/protected
```

### Example Requests

**Health Check** (no auth required):
```bash
curl http://localhost:8000/health
```

**Protected Endpoint**:
```bash
curl -H "Authorization: Bearer dev-key-123" http://localhost:8000/protected
```

**Root Endpoint**:
```bash
curl http://localhost:8000/
```

## Project Structure

```
fastapi-project-template/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Application configuration
│   ├── auth.py              # Authentication middleware
│   ├── database.py          # Database setup and session management
│   ├── model_config.py      # Model configuration utilities
│   ├── models/              # SQLAlchemy models (empty)
│   ├── schemas/             # Pydantic request/response schemas (empty)
│   ├── crud/                # Database operations (empty)
│   └── scripts/             # Custom scripts and utilities (empty)
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Container image definition
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md               # This file
```

## Development

### Adding New Features

1. **Models**: Add SQLAlchemy models in `app/models/`
2. **Schemas**: Define Pydantic schemas in `app/schemas/`
3. **CRUD Operations**: Implement database operations in `app/crud/`
4. **Endpoints**: Add new routes in `app/main.py` or separate route files

### Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py
```

### Database Migrations

This template comes with Alembic pre-configured for database migrations. An example model (`ExampleItem`) and its migration are included to demonstrate the workflow.

```bash
# Apply existing migrations (includes example table)
cd app && alembic upgrade head

# Create new migration after adding/modifying models
cd app && alembic revision --autogenerate -m "Add new table"

# Apply new migrations
cd app && alembic upgrade head

# View migration history
cd app && alembic history

# Rollback to previous migration
cd app && alembic downgrade -1
```

**Remove the example model when starting your project:**
```bash
# Delete the example model file
rm app/models/example_item.py

# Create migration to remove the table
cd app && alembic revision --autogenerate -m "Remove example table"

# Apply the migration
cd app && alembic upgrade head
```

## Deployment

### Docker Deployment

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d
```

### Production Considerations

1. **Security**: Change default API keys
2. **Database**: Switch to PostgreSQL for production
3. **Environment**: Set `DEBUG=false` and configure proper logging
4. **HTTPS**: Use reverse proxy (nginx) with SSL certificates
5. **Monitoring**: Add health checks and logging

## Customization

### Authentication

The template uses simple API key authentication. To upgrade to JWT:

1. Install `python-jose[cryptography]`
2. Modify `app/auth.py` to handle JWT tokens
3. Update endpoints to use JWT dependencies

### Database

To switch from SQLite to PostgreSQL:

1. Update `DATABASE_URL` in your `.env` file
2. Install `psycopg2-binary` in requirements.txt
3. Update SQLAlchemy connection settings if needed

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the [Issues](../../issues) section
- Review the API documentation at `/docs`
- Check the health endpoint at `/health`