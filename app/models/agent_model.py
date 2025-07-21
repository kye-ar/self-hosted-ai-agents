from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from datetime import datetime
from database import Base


class Agent(Base):
    """
    Agent-Model - Represents an AI agent with its configuration and metadata.
    """

    __tablename__ = "agents"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Basic agent information
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    version = Column(String(20), default="1.0.0")

    # LLM configuration
    llm_model = Column(String(100), nullable=False)

    # JSON field for provider-specific configuration
    provider_config = Column(JSON, default=dict)

    # JSON field for LLM parameters such as temp, max tokens, etc..
    llm_params = Column(JSON, default=dict)

    # Agent behaviour configuration
    system_prompt = Column(Text, nullable=False)

    # JSON Array of tool names this agent can utilise
    available_tools = Column(JSON, default=list)
    
    # Control flags
    is_active = Column(Boolean, default=True, index=True)

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', provider='{self.llm_model}')>"
