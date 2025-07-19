from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class ExampleItem(Base):
    """
    EXAMPLE MODEL - DELETE THIS WHEN STARTING YOUR PROJECT

    This model demonstrates:
    - Basic column type (Integer, String, Boolean, DateTime)
    - Primary key (id)
    - Nullable vs non-nullable fields
    - Default values


    To remove: Delete this file, then run:
    alembic revision --autogenerate -m "remove example table"
    alembic upgrade head
    """
    __tablename__ = "example_items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=1)