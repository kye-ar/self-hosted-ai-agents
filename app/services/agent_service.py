from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from fastapi import HTTPException, status

# Import our database model and schemas
from models.agent_model import Agent
from schemas.agent_schemas import AgentCreate, AgentUpdate, AgentResponse, AgentListResponse

class AgentService:
    """
    Service class for managing agent operations
    """

    def __init__(self, db: Session):
        self.db = db

    def create_agent(self, agent_data: AgentCreate) -> AgentResponse:
        """
        Creates a new agent in the database
        """
        # Business Rule: Check if the agent name already exists
        existing_agent = self.db.query(Agent).filter(Agent.name == agent_data.name).first()
        if existing_agent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Agent with name '{agent_data.name}' already exists"
            )

        # Convert Pydantic model to SQLAlchemy model
        agent_dict = agent_data.dict()
        db_agent = Agent(**agent_dict)

        # Save to database
        try:
            self.db.add(db_agent)
            self.db.commit()
            self.db.refresh(db_agent)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create agent: {str(e)}"
            )
        
        # Convert SQLAlchemy model to Pydantic model for response
        return AgentResponse.from_orm(db_agent)

    def get_agent(self, agent_id: int) -> AgentResponse:
        """
        Retrieves a single agent by ID
        """
        db_agent = self.db.query(Agent).filter(Agent.id == agent_id).first()

        if not db_agent:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )
        
        return AgentResponse.from_orm(db_agent)

    def get_agents(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> AgentListResponse:
        """
        Retrieves a paginated list of agents
        """
        query = self.db.query(Agent)
        if active_only:
            query = query.filter(Agent.is_active == True)
        
        # Get total count of agents
        total = query.count()

        # Apply pagination
        agents = query.offset(skip).limit(limit).all()

        # Convert response to response format
        agent_responses = [AgentResponse.from_orm(agent) for agent in agents]

        return AgentListResponse(
            agents=agent_responses,
            total=total,
            page=(skip // limit) + 1,
            per_page=limit
        )
    
    def update_agent(self, agent_id: int, agent_data: AgentUpdate) -> AgentResponse:
        """
        Updates an existing agent
        """
        # Find the agent
        db_agent = self.db.query(Agent).filter(Agent.id == agent_id).first()

        if not db_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )
        
        # Get only the fields that were provided (not None)
        update_data = agent_data.dict(exclude_unset=True)

        # Business Rule: Check for name conflicts (if name is being updated)
        if "name" in update_data:
            existing_agent = self.db.query(Agent).filter(
                Agent.name == update_data["name"],
                Agent.id != agent_id # don't count the current agent
            ).first()

            if existing_agent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Agent with name '{update_data['name']}' already exists"
                )
        
        # Update the agent
        try:
            for field, value in update_data.items():
                setattr(db_agent, field, value) # update each field
            
            self.db.commit()
            self.db.refresh(db_agent)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update agent: {str(e)}"
            )
        
        return AgentResponse.from_orm(db_agent)
    
    def delete_agent(self, agent_id: int) -> dict:
        """
        Deletes an agent from the database
        """
        db_agent = self.db.query(Agent).filter(Agent.id == agent_id).first()

        if not db_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )
        
        try:
            self.db.delete(db_agent)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete agent: {str(e)}"
            )
        
        return {"message": f"Agent {db_agent.name} (ID: {agent_id}) deleted successfully"}
        
    def get_agent_by_name(self, name: str) -> Optional[AgentResponse]:
        """
        Helper method to retrieve an agent by name
        """
        db_agent = self.db.query(Agent).filter(Agent.name == name).first()

        if db_agent:
            return AgentResponse.from_orm(db_agent)
        return None
        