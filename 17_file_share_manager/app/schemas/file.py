from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator
from fastapi import File, HTTPException, UploadFile

class FileBase(BaseModel):
    id: int
    is_directory: bool
    mime_type: Optional[str] = None
    modified_time: datetime
    name: str
    owner_id: int
    parent_id: Optional[int] = None
    path: str
    size: float
    upload_time: datetime

    
class FileResponseSchemas(BaseModel):
    files: List[FileBase]
    path: str
    total: int
    page: int
    pages: int


class FileUpdate(BaseModel):
    name: str

    @field_validator("name")
    def name_valid(cls, value):
        teshufuhao =  ["/", ":", "*", "?", "<", ">"] 
        for n in value:
            if n in teshufuhao:
                raise HTTPException(status_code=400, detail="文件名称存在特殊符号")
        if len(value) > 255:
            raise HTTPException(status_code=400, detail="文件名称过长")
        return value
    

class FileUpload(BaseModel):
    file: List[UploadFile] = File(...)
    path: str = "/"


class DirCreate(BaseModel):
    dirname: str
    path: str = "/"
    
    @field_validator("dirname")
    def dirname_valid(cls, value):
        teshufuhao =  ["/", ":", "*", "?", "<", ">"] 
        for n in value:
            if n in teshufuhao:
                raise HTTPException(status_code=400, detail="文件夹名称存在特殊符号")
        if len(value) > 255:
            raise HTTPException(status_code=400, detail="文件夹名称过长")
        return value