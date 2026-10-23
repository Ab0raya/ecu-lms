"""
Assignments, quizzes, and deadline tracking routes.
"""
from fastapi import APIRouter, Header, Request
from typing import List, Optional
from app.models.assignment import AssignmentItem
from app.scraper.client import ECULMSClient

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])

@router.get("", response_model=List[AssignmentItem])
def list_assignments(request: Request, x_moodle_session: Optional[str] = Header(None)):
    """
    Get all active assignments and upcoming submission deadlines across all courses.
    """
    token = x_moodle_session or request.cookies.get("moodle_session")
    client = ECULMSClient(moodle_session=token)
    return client.get_assignments()
