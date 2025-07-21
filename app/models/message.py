from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Message(Base):
    """
    Message-model - Represents individual messages within conversations.
    """

    __tablename__ = "messages"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to conversation
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    
    # Message metadata
    role = Column(String(20), nullable=False, index=True) # user, assistant, system, tool
    content = Column(Text, nullable=False)

    # Message ordering within conversation
    sequence_number = Column(Integer, nullable=False, index=True)

    # Tool-related fields (for future phases)
    tool_calls = Column(JSON, nullable=True)
    tool_call_id = Column(String(100), nullable=True)

    # Message metadata
    metadata = Column(JSON, default=dict)

    # Processing status
    is_processed = Column(Boolean, default=True)

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', conversation_id={self.conversation_id})>"