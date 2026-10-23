from pydantic import BaseModel
from typing import Optional

class AssignmentItem(BaseModel):
    id: str
    course_id: str
    course_name: str
    course_code: Optional[str] = None
    title: str
    description: Optional[str] = None
    due_date: str
    due_timestamp: Optional[int] = None
    status: str  # 'submitted', 'pending', 'overdue', 'graded'
    grade: Optional[str] = None
    submission_url: str
    attachment_name: Optional[str] = None
    attachment_url: Optional[str] = None
    days_left: Optional[int] = None
