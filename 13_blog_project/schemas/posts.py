from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Optional


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):

    @field_validator("title")
    def title_not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()

    @field_validator("content")
    def content_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip() if v else v


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    @field_validator("title")
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v

    @field_validator("content")
    def content_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip() if v else v


class PostResponse(PostBase):
    id: int
    author_id: int
    author_name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total: int

class PostDeleteResponse(BaseModel):
    message: str
    post_id: int