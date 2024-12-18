from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Document(BaseModel):
    id: int
    title: str
    author: str
    content: str
    tags: List[str]
    uploaded_date: datetime
    version: int = 1

class DocumentMetadata(BaseModel):
    id: int
    title: str
    author: str
    tags: List[str]
    uploaded_date: datetime
    version: int

class DocumentPermission(BaseModel):
    user_id: str
    permission: str  # "read", "edit", or "admin"

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

