from pydantic import BaseModel
from typing import List, Optional

class ResourceItem(BaseModel):
    id: str
    name: str
    type: str  # 'pdf', 'slide', 'doc', 'link', 'folder', 'video', 'announcement', 'quiz', 'assignment'
    url: str
    download_url: Optional[str] = None
    file_size: Optional[str] = None
    icon: Optional[str] = None
    info: Optional[str] = None

class CourseSection(BaseModel):
    id: str
    title: str
    summary: Optional[str] = None
    items: List[ResourceItem] = []

class CourseSummary(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    term: Optional[str] = "Spring 2026"
    instructor: Optional[str] = None
    image_url: Optional[str] = None
    progress: Optional[int] = 0
    enrolled: bool = True
    color: Optional[str] = "#3b82f6"
    url: str

class CourseDetail(CourseSummary):
    sections: List[CourseSection] = []
    announcements: List[ResourceItem] = []
