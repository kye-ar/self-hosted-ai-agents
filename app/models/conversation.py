from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Conversation(Base):
    """ 
    Conversation-Model - Represents a conversation between an agent and a user
    """

    __tablename__ = "conversations"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to the agent handling this conversation
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)

    # User identifier - User ID or Session ID (For anonymous users)
    user_id = Column(String(100), nullable=False, index=True)

    # Conversation metadata
    title = Column(String(200), nullable=True)
    status = Column(String(20), default="active", index=True)

    # Conversation settings
    max_messages = Column(Integer, default=100)

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    agent = relationship("Agent", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, agent_id={self.agent_id})>"

