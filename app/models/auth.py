from pydantic import BaseModel, Field
from typing import Optional

class SessionAuthRequest(BaseModel):
    moodle_session: str = Field(..., description="The MoodleSession cookie value from lms.ecu.edu.eg")
    name: Optional[str] = None
    email: Optional[str] = None

class SessionAuthResponse(BaseModel):
    success: bool
    message: str
    is_valid: bool
    user: Optional[dict] = None
