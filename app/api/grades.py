"""
Grades and academic evaluation routes.
"""
from fastapi import APIRouter, Header, Request, HTTPException
from typing import Optional
from app.scraper.client import ECULMSClient

router = APIRouter(prefix="/api/grades", tags=["Grades"])

@router.get("/{course_id}")
def get_grades(course_id: str, request: Request, x_moodle_session: Optional[str] = Header(None)):
    """
    Get grade breakdown and instructor feedback for a specific course.
    """
    token = x_moodle_session or request.cookies.get("moodle_session")
    client = ECULMSClient(moodle_session=token)
    grades = client.get_grades(course_id)
    if not grades:
        raise HTTPException(status_code=404, detail="Grades not available for this course")
    return grades
