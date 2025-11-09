from pydantic import BaseModel
from typing import Optional



class FileSearch(BaseModel):
    page: int = 1
    keyword: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    