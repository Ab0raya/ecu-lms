"""
Configuration and settings for ECU LMS Converter.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ECU LMS Endpoints
LMS_BASE_URL = os.getenv("LMS_BASE_URL", "https://lms.ecu.edu.eg")
LMS_COURSES_URL = f"{LMS_BASE_URL}/my/courses.php"
LMS_DASHBOARD_URL = f"{LMS_BASE_URL}/my/"
LMS_COURSE_VIEW_URL = f"{LMS_BASE_URL}/course/view.php"
LMS_ASSIGNMENT_VIEW_URL = f"{LMS_BASE_URL}/mod/assign/view.php"
LMS_GRADES_URL = f"{LMS_BASE_URL}/grade/report/user/index.php"
LMS_CALENDAR_URL = f"{LMS_BASE_URL}/calendar/view.php"
LMS_AJAX_SERVICE_URL = f"{LMS_BASE_URL}/lib/ajax/service.php"

# Server Settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

# Demo / Offline Preview Mode (allows exploring the app with rich sample courses when no live student session is provided)
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
