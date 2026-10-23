"""
Scrapling Client for Egyptian Chinese University (ECU) LMS.
Manages HTTP session, Chrome TLS impersonation, Cloudflare bypass, and Moodle session state.
"""
from typing import List, Dict, Any, Optional
import logging
from scrapling.fetchers import FetcherSession
from app.config import (
    LMS_BASE_URL,
    LMS_COURSES_URL,
    LMS_DASHBOARD_URL,
    LMS_COURSE_VIEW_URL,
    LMS_ASSIGNMENT_VIEW_URL,
    LMS_GRADES_URL,
    DEMO_MODE
)
from app.scraper.parser import MoodleParser
from app.scraper.mock_data import (
    MOCK_USER,
    MOCK_COURSES,
    MOCK_COURSE_DETAILS,
    MOCK_ASSIGNMENTS,
    MOCK_GRADES
)

logger = logging.getLogger("ecu_lms")

class ECULMSClient:
    """Handles communication with ECU LMS using Scrapling."""

    def __init__(self, moodle_session: Optional[str] = None):
        self.moodle_session = moodle_session
        self._cached_profile = None

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        }
        if self.moodle_session:
            headers["Cookie"] = f"MoodleSession={self.moodle_session.strip()}"
        return headers

    def check_session(self) -> Dict[str, Any]:
        """Check if the provided MoodleSession is currently authenticated."""
        if not self.moodle_session:
            return {"authenticated": False, "reason": "No session cookie provided"}

        try:
            with FetcherSession(impersonate="chrome", headers=self._get_headers()) as session:
                res = session.get(LMS_COURSES_URL)
                # If redirected to Microsoft Entra ID login, session is not valid
                if "login.microsoftonline.com" in res.url or "/login/" in res.url:
                    return {"authenticated": False, "reason": "Session expired or invalid (redirected to Microsoft login)"}
                
                html = res.body.decode("utf-8", errors="ignore") if hasattr(res, "body") and res.body else ""
                profile = MoodleParser.parse_user_profile(html)
                self._cached_profile = profile
                return {"authenticated": True, "user": profile}
        except Exception as e:
            logger.error(f"Error checking session: {e}")
            return {"authenticated": False, "error": str(e)}

    def get_profile(self) -> Dict[str, Any]:
        """Get the current student profile."""
        if self.moodle_session:
            status = self.check_session()
            if status.get("authenticated") and status.get("user"):
                return status["user"]

        if DEMO_MODE:
            return MOCK_USER
        
        return {"id": "guest", "name": "Guest Student", "is_authenticated": False}

    def get_courses(self) -> List[Dict[str, Any]]:
        """Fetch list of enrolled courses using Moodle AJAX service or HTML fallback."""
        if self.moodle_session:
            try:
                import json
                import re

                with FetcherSession(impersonate="chrome", headers=self._get_headers()) as session:
                    res = session.get(LMS_COURSES_URL)
                    if "login.microsoftonline.com" not in res.url:
                        html = res.body.decode("utf-8", errors="ignore") if hasattr(res, "body") and res.body else ""
                        
                        # Extract sesskey to use Moodle's internal course timeline API
                        sesskey_match = re.search(r'sesskey=([a-zA-Z0-9]+)', html)
                        if sesskey_match:
                            sesskey = sesskey_match.group(1)
                            ajax_url = f"{LMS_BASE_URL}/lib/ajax/service.php?sesskey={sesskey}&info=core_course_get_enrolled_courses_by_timeline_classification"
                            payload = [{
                                "index": 0,
                                "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
                                "args": {
                                    "offset": 0,
                                    "limit": 0,
                                    "classification": "all",
                                    "sort": "fullname"
                                }
                            }]
                            try:
                                ajax_res = session.post(ajax_url, json=payload)
                                data = json.loads(ajax_res.body.decode("utf-8"))
                                raw_courses = data[0]["data"]["courses"]
                                
                                palette = ["#6366f1", "#0ea5e9", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6"]
                                courses = []
                                for c in raw_courses:
                                    cid = str(c["id"])
                                    color = palette[int(cid) % len(palette)] if cid.isdigit() else "#3b82f6"
                                    courses.append({
                                        "id": cid,
                                        "name": c.get("fullname") or f"Course {cid}",
                                        "code": c.get("shortname") or "",
                                        "term": "Spring 2026",
                                        "instructor": "Faculty Staff",
                                        "image_url": c.get("courseimage"),
                                        "progress": c.get("progress") or 0,
                                        "enrolled": True,
                                        "color": color,
                                        "url": c.get("viewurl") or f"{LMS_COURSE_VIEW_URL}?id={cid}"
                                    })
                                if courses:
                                    return courses
                            except Exception as ex:
                                logger.error(f"Error querying Moodle AJAX courses API: {ex}")

                        # Fallback to HTML parser
                        courses = MoodleParser.parse_courses(html)
                        if courses:
                            return courses
            except Exception as e:
                logger.error(f"Failed to fetch live courses: {e}")

        # Fallback to demo mode if allowed
        if DEMO_MODE:
            return MOCK_COURSES
        return []

    def get_course_details(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Fetch details, topics, and files for a specific course."""
        if self.moodle_session:
            try:
                target_url = f"{LMS_COURSE_VIEW_URL}?id={course_id}"
                with FetcherSession(impersonate="chrome", headers=self._get_headers()) as session:
                    res = session.get(target_url)
                    if "login.microsoftonline.com" not in res.url:
                        html = res.body.decode("utf-8", errors="ignore") if hasattr(res, "body") and res.body else ""
                        details = MoodleParser.parse_course_contents(html, course_id)
                        return details
            except Exception as e:
                logger.error(f"Failed to fetch live course {course_id}: {e}")

        if DEMO_MODE:
            return MOCK_COURSE_DETAILS.get(str(course_id)) or MOCK_COURSE_DETAILS.get("101")
        return None

    def get_assignments(self) -> List[Dict[str, Any]]:
        """Fetch assignments and upcoming deadlines from ECU LMS calendar."""
        if self.moodle_session:
            try:
                target_url = f"{LMS_BASE_URL}/calendar/view.php?view=upcoming"
                with FetcherSession(impersonate="chrome", headers=self._get_headers()) as session:
                    res = session.get(target_url)
                    if "login.microsoftonline.com" not in res.url:
                        html = res.body.decode("utf-8", errors="ignore") if hasattr(res, "body") and res.body else ""
                        assignments = MoodleParser.parse_calendar_assignments(html)
                        if assignments:
                            return assignments
            except Exception as e:
                logger.error(f"Failed to fetch live assignments: {e}")

        if DEMO_MODE:
            return MOCK_ASSIGNMENTS
        return []

    def get_grades(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Fetch grades for a course."""
        if DEMO_MODE:
            return MOCK_GRADES.get(str(course_id))
        return None

    def download_resource(self, resource_url: str):
        """Stream or download a protected LMS resource with the authenticated session."""
        try:
            with FetcherSession(impersonate="chrome", headers=self._get_headers()) as session:
                res = session.get(resource_url)
                body = res.body if hasattr(res, 'body') and res.body else b""
                content_type = res.headers.get("content-type", "application/pdf")
                return body, content_type
        except Exception as e:
            logger.error(f"Failed to download resource: {e}")
            raise
