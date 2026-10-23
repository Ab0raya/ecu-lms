"""
Moodle HTML and DOM parser powered by Scrapling.
Extracts courses, sections, materials, assignments, and grades from ECU LMS pages.
"""
from typing import List, Dict, Any, Optional
import re
from scrapling.parser import Selector

class MoodleParser:
    """Parses Moodle pages using Scrapling CSS/XPath selectors."""

    @staticmethod
    def parse_user_profile(html_content: str) -> Dict[str, Any]:
        """Extract user profile information from navigation bar or profile block."""
        page = Selector(html_content)
        
        # User display name
        name = None
        for sel in [
            '#user-menu-toggle',
            '.usermenu .dropdown-toggle',
            '.logininfo a',
            '.usertext',
            '.profile-name',
            '.userpicture ~ span',
            '.usernav .usertext'
        ]:
            el = page.css(f"{sel}::text").get()
            if el and el.strip() and "log out" not in el.lower() and "login" not in el.lower():
                name = el.strip()
                break
        
        if not name:
            # Try xpath
            name_el = page.xpath("//span[contains(@class, 'usertext')]/text()").get()
            name = name_el.strip() if name_el else "ECU Student"

        # Avatar
        avatar = None
        for sel in ['.userpicture', '.avatar img', '.user-menu img']:
            src = page.css(f"{sel}::attr(src)").get()
            if src:
                avatar = src
                break

        # User ID if found in profile link
        user_id = None
        profile_links = page.css("a[href*='/user/profile.php']::attr(href)").getall()
        for link in profile_links:
            match = re.search(r'id=(\d+)', link)
            if match:
                user_id = match.group(1)
                break

        return {
            "id": user_id or "ecu_student",
            "name": name,
            "avatar_url": avatar,
            "role": "Student",
            "university": "Egyptian Chinese University (ECU)",
            "faculty": "Faculty of Engineering & Technology",
            "is_authenticated": True
        }

    @staticmethod
    def parse_courses(html_content: str) -> List[Dict[str, Any]]:
        """Parse list of enrolled courses from /my/courses.php or /my/"""
        page = Selector(html_content)
        courses = []
        seen_ids = set()

        # Modern Moodle cards (Moodle 3.11+, 4.x)
        cards = page.css(".dashboard-card, .course-info-container, [data-region='course-content'], .coursename")
        
        # Check standard course list items
        links = page.css("a[href*='/course/view.php?id=']")
        for link in links:
            href = link.attrib.get('href', '')
            match = re.search(r'id=(\d+)', href)
            if not match:
                continue
            course_id = match.group(1)
            if course_id in seen_ids:
                continue
            seen_ids.add(course_id)

            title = link.text.strip() if link.text else ""
            if not title:
                # Look for span or nested text inside link
                nested = link.css(".coursename::text, .multiline::text, span::text").get()
                title = nested.strip() if nested else f"Course #{course_id}"

            # Filter out non-course navigation links
            if title.lower() in ["home", "dashboard", "my courses", "site home"]:
                continue

            # Look for progress if available in parent container
            parent = link.parent
            progress = 0
            if parent:
                prog_el = parent.css(".progress-bar::attr(aria-valuenow), [data-percentage]::attr(data-percentage)").get()
                if prog_el:
                    try:
                        progress = int(float(prog_el))
                    except ValueError:
                        pass

            # Image
            img_src = None
            if parent:
                img_el = parent.css(".dashboard-card-img::attr(src), .course-image::attr(src)").get()
                if img_el:
                    img_src = img_el

            # Palette color generator based on ID
            palette = ["#6366f1", "#0ea5e9", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6"]
            color = palette[int(course_id) % len(palette)] if course_id.isdigit() else "#3b82f6"

            courses.append({
                "id": course_id,
                "name": title,
                "code": title.split(":")[0].strip() if ":" in title else None,
                "term": "Current Semester",
                "instructor": "Faculty Member",
                "image_url": img_src,
                "progress": progress,
                "enrolled": True,
                "color": color,
                "url": href
            })

        return courses

    @staticmethod
    def parse_course_contents(html_content: str, course_id: str) -> Dict[str, Any]:
        """Parse topics, sections, files, and assignments from /course/view.php?id={course_id}"""
        page = Selector(html_content)
        
        # Course title
        course_name = page.css("h1.page-header-headings::text, .page-header-headings h1::text, header h1::text, .course-header h1::text").get()
        if not course_name:
            course_name = page.css("title::text").get() or f"Course {course_id}"
        course_name = course_name.replace("Course:", "").strip()

        sections = []
        announcements = []

        # Find all Moodle sections (topics or weeks)
        section_nodes = page.css("li.section, div.course-section, div[data-for='section']")
        for idx, sec in enumerate(section_nodes):
            sec_id = sec.attrib.get('id', f"section-{idx}")
            title = sec.css(".sectionname a::text, .sectionname::text, h3 a::text, h3::text, [data-for='section_title'] a::text, [data-for='section_title']::text").get()
            if not title:
                title = f"Topic {idx}" if idx > 0 else "General Information"
            title = title.strip()

            summary = sec.css(".summary::text, .contentwithoutlink::text").get()
            summary = summary.strip() if summary else None

            items = []
            activity_nodes = sec.css("li.activity, div.activity-item")
            for act in activity_nodes:
                act_link = act.css("a[href*='/mod/']::attr(href)").get()
                if not act_link:
                    continue

                act_name = (
                    act.attrib.get('data-activityname') or 
                    act.css('.activity-item::attr(data-activityname)').get() or
                    act.css('[data-activityname]::attr(data-activityname)').get() or
                    act.css('.instancename::text, .activityname .media-body::text, a::text').get()
                )
                if not act_name:
                    continue
                act_name = act_name.strip()

                # Determine type
                act_type = "link"
                act_classes = act.attrib.get("class", "")
                if "resource" in act_classes or ".pdf" in act_name.lower():
                    act_type = "pdf"
                elif "assign" in act_classes:
                    act_type = "assignment"
                elif "quiz" in act_classes:
                    act_type = "quiz"
                elif "forum" in act_classes:
                    act_type = "announcement"
                elif "folder" in act_classes:
                    act_type = "folder"
                elif "url" in act_classes:
                    act_type = "link"

                # Info/details
                info = act.css(".resourcelinkdetails::text, .dimmed_text::text, .text-muted::text").get()
                info = info.strip() if info else None

                item_id = act.attrib.get('id', f"item-{idx}-{len(items)}")

                item_obj = {
                    "id": item_id,
                    "name": act_name,
                    "type": act_type,
                    "url": act_link,
                    "download_url": f"/api/download?url={act_link}" if act_type == "pdf" else None,
                    "file_size": None,
                    "info": info
                }

                if act_type == "announcement":
                    announcements.append(item_obj)
                else:
                    items.append(item_obj)

            if items or summary:
                sections.append({
                    "id": sec_id,
                    "title": title,
                    "summary": summary,
                    "items": items
                })

        return {
            "id": course_id,
            "name": course_name,
            "code": course_name.split(":")[0].strip() if ":" in course_name else None,
            "term": "Current Semester",
            "enrolled": True,
            "url": f"https://lms.ecu.edu.eg/course/view.php?id={course_id}",
            "sections": sections,
            "announcements": announcements
        }

    @staticmethod
    def parse_assignment_details(html_content: str, assignment_id: str) -> Dict[str, Any]:
        """Parse assignment details and submission status from /mod/assign/view.php?id=X"""
        page = Selector(html_content)
        title = page.css("h2::text, .page-header-headings h1::text").get() or "Assignment"
        description = page.css(".intro::text, [data-region='activity-information']::text").get()
        
        status = "pending"
        due_date = "Check LMS"
        grade = None

        # Look in general table
        rows = page.css("table.generaltable tr")
        for row in rows:
            header = row.css("th::text, td.c0::text").get()
            val = row.css("td::text, td.c1::text").get()
            if not header or not val:
                continue
            header = header.lower().strip()
            val = val.strip()

            if "submission status" in header:
                if "submitted" in val.lower():
                    status = "submitted"
            elif "due date" in header:
                due_date = val
            elif "grade" in header and val != "-":
                grade = val
                status = "graded"

        return {
            "id": assignment_id,
            "title": title.strip(),
            "description": description.strip() if description else None,
            "due_date": due_date,
            "status": status,
            "grade": grade,
            "submission_url": f"https://lms.ecu.edu.eg/mod/assign/view.php?id={assignment_id}"
        }

    @staticmethod
    def parse_calendar_assignments(html_content: str) -> List[Dict[str, Any]]:
        """Parse upcoming assignments and deadlines from /calendar/view.php?view=upcoming"""
        import time
        page = Selector(html_content)
        assignments = []
        now = time.time()
        for ev in page.css('.event'):
            title = ev.attrib.get('data-event-title') or ev.css('.name::text').get() or 'Assignment'
            title = title.replace(' is due', '').strip()
            course_id = ev.attrib.get('data-course-id') or ''
            course_name = ev.css(".description a[href*='/course/view.php']::text").get() or f"Course {course_id}"
            due_date = ev.css('.date::text').get() or 'Check LMS'
            due_date = due_date.strip()
            timestamp_str = ev.css('.date::attr(data-timestamp)').get()
            timestamp = int(timestamp_str) if timestamp_str and timestamp_str.isdigit() else None
            
            days_left = None
            if timestamp:
                days_left = max(0, int((timestamp - now) / 86400))
            
            url = ev.css(".card-footer a[href*='/mod/assign/']::attr(href)").get() or ''
            match = re.search(r'id=(\d+)', url)
            assign_id = match.group(1) if match else ev.attrib.get('data-event-id', '0')

            assignments.append({
                'id': assign_id,
                'course_id': course_id,
                'course_name': course_name.strip(),
                'course_code': course_name.split('-')[0].strip() if '-' in course_name else None,
                'title': title,
                'description': None,
                'due_date': due_date,
                'due_timestamp': timestamp,
                'status': 'pending',
                'submission_url': url or f"https://lms.ecu.edu.eg/mod/assign/view.php?id={assign_id}",
                'days_left': days_left
            })
        return assignments
