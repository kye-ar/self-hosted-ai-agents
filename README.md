# Self-Hosted AI Agents

A local LLM-powered agent system with custom tool capabilities, built on FastAPI.

## Overview

This system allows you to create and manage AI agents that can have conversations and execute custom tools. It's designed to run locally with support for various LLM providers.

## Core Components

- **Agent Management**: Create and configure AI agents with different capabilities
- **Conversation Engine**: Handle agent conversations and message history
- **Tool Registry**: Extensible system for agent tools and actions
- **LLM Provider**: Support for local model providers (Ollama)

## Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   cd app
   alembic upgrade head
   ```

3. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

4. **View API documentation**
   - http://localhost:8000/docs

## Current Status

This project is in active development:

- ✅ Database models and core structure
- ✅ Modular configuration system with LLM provider support
- ✅ LLM provider base class and Llama/Ollama integration
- ✅ Agent management system with full CRUD operations
- ⏳ Conversation handling
- ⏳ Tool execution framework


## API Overview

- **Agent management**: `/agents` - Create, read, update, delete agents
  - `POST /agents` - Create new agent
  - `GET /agents` - List agents with pagination
  - `GET /agents/{id}` - Get specific agent
  - `PUT /agents/{id}` - Update agent
  - `DELETE /agents/{id}` - Delete agent
- **Conversations**: `/conversations` - (Coming soon)
- **Tools**: `/tools` - (Coming soon)

## Configuration

The system uses a modular configuration approach with environment variable support:

**Application Settings** (prefix: `APP__`):
- `APP__DATABASE_URL`: Database connection (defaults to SQLite)
- `APP__LLM_PROVIDER`: Selected LLM provider (ollama, openai, etc.)
- `APP__DEBUG`: Enable debug mode
- `APP__LOG_LEVEL`: Logging level

**LLM Provider Settings**:
Each LLM provider has its own configuration prefix and parameters. For example, Ollama uses `LLAMA__` prefix for settings like API base URL, model name, temperature, and provider-specific options.

**Logging** (prefix: `LOGGING__`):
- `LOGGING__LOG_LEVEL`: Logging level
- `LOGGING__LOG_FILE`: Log file location
- `LOGGING__LOG_TO_CONSOLE`: Enable console logging

The modular design allows easy addition of new LLM providers without affecting existing configurations.
