from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Import the database session
from database import get_db

# Import the schemas and service
from schemas.agent_schemas import AgentCreate, AgentUpdate, AgentResponse, AgentListResponse
from services.agent_service import AgentService

# Create the router
router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}}
)

def get_agent_service(db: Session = Depends(get_db)) -> AgentService:
    """
    Dependency function to get the agent service
    """
    return AgentService(db)

@router.post("", response_model=AgentResponse, status_code=201)
@router.post("/", response_model=AgentResponse, status_code=201)
async def create_agent(
    agent_data: AgentCreate,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Create a new agent
    
    - **name**: Unique name for the agent (required)
    - **system_prompt**: The prompt that defines agent behavior (required)
    - **llm_model**: The LLM model to use (required)
    - **description**: Optional description of the agent's purpose
    - **available_tools**: List of tools this agent can use
    """
    return agent_service.create_agent(agent_data)

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Get an agent by ID
    """
    return agent_service.get_agent(agent_id)

@router.get("", response_model=AgentListResponse)
@router.get("/", response_model=AgentListResponse)
async def get_agents(
    skip: int = Query(0, ge=0, description="Number of agents to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of agents to return"),
    active_only: bool = Query(True, description="Whether to return only active agents"),
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Retrieve a paginated list of agents

    - **skip**: Number of agents to skip (for pagination)
    - **limit**: Maximum number of agents to return
    - **active_only**: Filter to show only active agents
    """
    return agent_service.get_agents(skip=skip, limit=limit, active_only=active_only)

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Update an existing agent
    
    Only provided fields will be updated.
    """
    return agent_service.update_agent(agent_id, agent_data)

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Delete an agent by ID
    """
    return agent_service.delete_agent(agent_id)

@router.get("/search/by-name/{agent_name}", response_model=AgentResponse)
async def search_agent_by_name(
    agent_name: str,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Search for an agent by name
    """
    agent = agent_service.get_agent_by_name(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with name '{agent_name}' not found")
    return agent