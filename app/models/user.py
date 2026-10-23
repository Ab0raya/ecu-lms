from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    id: Optional[str] = None
    name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = "Student"
    university: str = "Egyptian Chinese University (ECU)"
    faculty: Optional[str] = "Engineering & Technology"
    is_authenticated: bool = True
