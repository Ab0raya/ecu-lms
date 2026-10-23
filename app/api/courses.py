"""
Course catalog and course content routes.
"""
from fastapi import APIRouter, Header, Request, HTTPException
from typing import List, Optional
from app.models.course import CourseSummary, CourseDetail
from app.scraper.client import ECULMSClient

router = APIRouter(prefix="/api/courses", tags=["Courses"])

def _get_client(request: Request, x_moodle_session: Optional[str]) -> ECULMSClient:
    token = x_moodle_session or request.cookies.get("moodle_session")
    return ECULMSClient(moodle_session=token)

@router.get("", response_model=List[CourseSummary])
def list_courses(request: Request, x_moodle_session: Optional[str] = Header(None)):
    """
    Get all enrolled courses for the authenticated ECU student.
    """
    client = _get_client(request, x_moodle_session)
    courses = client.get_courses()
    return courses

@router.get("/{course_id}", response_model=CourseDetail)
def get_course_detail(course_id: str, request: Request, x_moodle_session: Optional[str] = Header(None)):
    """
    Get full section outline, lecture slides, assignments, and announcements for a specific course.
    """
    client = _get_client(request, x_moodle_session)
    detail = client.get_course_details(course_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Course not found or no access")
    return detail
