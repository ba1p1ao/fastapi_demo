from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str = None 
    is_completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None