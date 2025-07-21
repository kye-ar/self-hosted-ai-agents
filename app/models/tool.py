from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from datetime import datetime
from database import Base

class Tool(Base):
    """
    Tool-Model - Represents a tool that can be used by an agent
    """

    __tablename__ = "tools"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Tool Identification - must be unique for tool registry
    name = Column(String(100), nullable=False, unique=True, index=True)
    display_name = Column(String(150), nullable=False) # Human-readable name
    description = Column(Text, nullable=False) # What the tool does

    # Tool Categorisation
    category = Column(String(50), default="general", index=True)

    # Tool Schema - Defines how the tool is used
    # This adheres to the JSON Schema for LLM function calling
    parameters_schema = Column(JSON, nullable=False)

    # Tool configuration
    version = Column(String(20), default="1.0.0")
    is_active = Column(Boolean, default=True, index=True)
    is_builtin = Column(Boolean, default=False, index=True) # Is it a default, or custom tool?

    # Security settings
    requires_confirmation = Column(Boolean, default=False)
    max_execution_time = Column(Integer, default=30) # Define tool timeout

    # Usage analytics
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime, nullable=True)

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Tool(id={self.id}, name='{self.name}', category='{self.category}')>"
