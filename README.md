# Self-Hosted AI Agents

A flexible, local LLM-powered agent system with custom tool capabilities, built on FastAPI.

## Overview

This system provides a complete infrastructure for creating, managing, and deploying AI agents that can interact with users through conversations and execute custom tools. It's designed to run locally with support for various LLM providers including Ollama, Mistral, and OpenAI-compatible APIs.

## Architecture

The system follows a modular architecture with the following core components:

- **API Endpoints**: FastAPI-based REST API with authentication and request validation
- **Conversation Engine**: Central orchestrator managing message processing and context
- **Agent Management**: Agent storage, configuration, and capability management
- **Tool Registry**: Tool discovery, execution, and permission management
- **Prompt Template Component**: Context assembly and template rendering
- **LLM Provider**: Abstract interface supporting multiple model providers
- **Database**: SQLAlchemy-based persistence layer with SQLite/PostgreSQL support

## Features

- **Multi-Agent Support**: Create and manage multiple AI agents with different capabilities
- **Custom Tools**: Extensible tool system for agent actions
- **Local LLM Support**: Works with Ollama and other local model providers
- **Conversation Management**: Persistent conversation history and context
- **Template System**: Flexible prompt templating with variable substitution
- **REST API**: Complete HTTP API for integration with external systems
- **Docker Support**: Containerised deployment ready

## Quick Start

### Development Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   cd app
   alembic upgrade head
   ```

3. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Docker Deployment

```bash
docker-compose up -d
```

## Implementation Status

This project is currently in development following a phased implementation approach:

- ✅ **Phase 1**: Foundation (Database models, basic configuration)
- 🚧 **Phase 2**: Agent Management (CRUD operations for agents)
- ⏳ **Phase 3**: Basic Conversation System (Message handling)
- ⏳ **Phase 4**: Tool System Integration (Tool execution framework)
- ⏳ **Phase 5**: Enhanced Features (Multiple LLM providers, monitoring)
- ⏳ **Phase 6**: Advanced Features (Real-time, streaming, plugins)

## API Endpoints

### Agents
- `GET /agents` - List all agents
- `POST /agents` - Create new agent
- `GET /agents/{id}` - Get specific agent
- `PUT /agents/{id}` - Update agent
- `DELETE /agents/{id}` - Delete agent

### Conversations
- `POST /conversations` - Start new conversation
- `POST /conversations/{id}/messages` - Send message
- `GET /conversations/{id}/messages` - Get conversation history

### Tools
- `GET /tools` - List available tools
- `POST /tools/{tool_name}/execute` - Execute tool directly

## Configuration

The system uses environment variables for configuration:

- `DATABASE_URL`: Database connection string
- `LLM_PROVIDER`: Primary LLM provider (ollama, openai, mistral)
- `LLM_MODEL`: Model name to use
- `API_KEY`: Authentication key for API access

## Contributing

1. Review the implementation roadmap in `plan/implementation-roadmap.txt`
2. Follow the existing code patterns and architecture
3. Add tests for new functionality
4. Update documentation for API changes

## License

MIT License - see LICENSE file for details.