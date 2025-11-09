from pydantic import BaseModel
from typing import List, Optional



class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None

class MovieDetail(BaseModel):
    id: int
    title: str
    cover_url: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    rating: Optional[float] = None
    director: Optional[str] = None

class MovieList(BaseModel):
    total: int
    page: int
    size: int
    movies: List[MovieDetail]

