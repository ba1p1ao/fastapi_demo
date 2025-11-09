from pydantic import BaseModel, field_validator
from typing import Optional


class CommentCreate(BaseModel):
    movie_id: int
    content: str
    rating: float
