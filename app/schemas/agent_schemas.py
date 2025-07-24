from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class AgentBase(BaseModel):
    """
    Base schema for all agents - contains fields common to all agent operations
    """
    name: str = Field(..., min_length=3, max_length=100, description="Human readable name for the agent")
    description: Optional[str] = Field(None, description="Optional description of the agent's purpose")
    version: str = Field(default="1.0.0", description="Version string for tracking the agent iterations")
    llm_model: str = Field(..., description="The LLM model used by the agent")
    provider_config: Dict[str, Any] = Field(default_factory=dict, description="Provider-specific configuration")
    llm_params: Dict[str, Any] = Field(default_factory=dict, description="LLM-specific parameters")
    system_prompt: str = Field(..., min_length=1, description="The system prompt that defines the agent's personality & behaviour")
    available_tools: List[str] = Field(default_factory=list, description="List of tools available to the agent")
    is_active: bool = Field(default=True, description="Whether the agent is active or not")

    @validator("name")
    def validate_name(cls, v):
        """
        Custom validator for agent name
        """
        if not v.strip():
            raise ValueError("Agent name cannot be empty")
        
        # Check for problematic characters
        if any(char in v for char in ['<', '>', '&', '"', "'"]):
            raise ValueError("Agent name cannot contain HTML/XML special characters")
        
        return v.strip()

    @validator("system_prompt")
    def validate_system_prompt(cls, v):
        """
        Ensures system prompt provides meaningful guidance to the agent
        """
        if not v.strip():
            raise ValueError("System prompt cannot be empty")
        
        if len(v.strip()) < 10:
            raise ValueError("System prompt should be at least 10 characters long")
        
        # Basic safety checks
        harmful_terms = ['ignore previous instructions', 'harmful', 'dangerous']
        if any(term in v.lower() for term in harmful_terms):
            raise ValueError("System prompt cannot contain harmful instructions")
        
        return v.strip()

    @validator('llm_model')
    def validate_llm_model(cls, v):
        """
        Validates the LLM model name format
        """
        if not v.strip():
            raise ValueError("LLM model name cannot be empty")
        
        # Basic format validation
        if len(v.strip()) < 3:
            raise ValueError("LLM model name seems too short")
        
        return v.strip()

class AgentCreate(AgentBase):
    """
    Schema for creating a new agent
    """
    pass

class AgentUpdate(BaseModel):
    """
    Schema for updating an existing agent
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    version: Optional[str] = None
    llm_model: Optional[str] = None
    provider_config: Optional[Dict[str, Any]] = None
    llm_params: Optional[Dict[str, Any]] = None
    system_prompt: Optional[str] = Field(None, min_length=1)
    available_tools: Optional[List[str]] = None
    is_active: Optional[bool] = None

    @validator('name')
    def validate_name(cls, v):
        """Same validation as AgentBase, but only when name is provided"""
        if v is not None:
            if not v.strip():
                raise ValueError('Agent name cannot be empty or just whitespace')
            if any(char in v for char in ['<', '>', '&', '"', "'"]):
                raise ValueError('Agent name cannot contain HTML/XML special characters')
            return v.strip()
        return v

    @validator('system_prompt')
    def validate_system_prompt(cls, v):
        """Same validation as AgentBase, but only when system_prompt is provided"""
        if v is not None:
            if not v.strip():
                raise ValueError('System prompt cannot be empty')
            if len(v.strip()) < 10:
                raise ValueError('System prompt should be at least 10 characters long')
            harmful_terms = ['ignore previous instructions', 'harmful', 'dangerous']
            if any(term in v.lower() for term in harmful_terms):
                raise ValueError('System prompt cannot contain potentially harmful instructions')
            return v.strip()
        return v

    @validator('llm_model')
    def validate_llm_model(cls, v):
        """Same validation as AgentBase, but only when llm_model is provided"""
        if v is not None:
            if not v.strip():
                raise ValueError('LLM model cannot be empty')
            if len(v.strip()) < 3:
                raise ValueError('LLM model name seems too short')
            return v.strip()
        return v

class AgentResponse(AgentBase):
    """
    Schema for returning agent data from the API
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Pydantic configuration for working with SQLAlchemy models
        """
        from_attributes = True

class AgentListResponse(BaseModel):
    """
    Schema for returning a paginated list of agents.
    """
    agents: List[AgentResponse]
    total: int = Field(..., description="Total number of agents in the database")
    page: int = Field(..., description="Current page number (starting from 1)")
    per_page: int = Field(..., description="Number of agents per page")
    
    class Config:
        from_attributes = True