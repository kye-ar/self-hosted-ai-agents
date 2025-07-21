from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from datetime import datetime
from database import Base

class PromptTemplate(Base):
    """
    PromptTemplate-Model - Represents reusable prompt templates for agents
    """

    __tablename__ = "prompt_templates"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Template identification
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Template categorisation
    template_type = Column(String(30), nullable=False, index=True)
    category = Column(String(50), default="general", index=True)

    # Template content
    content = Column(Text, nullable=False) # The actual prompt template, with variable placeholders

    # Template configuration
    variables = Column(JSON, default=list)
    default_values = Column(JSON, default=dict)

    # Template metadata
    version = Column(String(20), default="1.0.0")
    is_active = Column(Boolean, default=True, index=True)
    is_system = Column(Boolean, default=False, index=True) # User or System created

    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime, nullable=True)

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PromptTemplate(id={self.id}, name='{self.name}', type='{self.template_type}')>"

        