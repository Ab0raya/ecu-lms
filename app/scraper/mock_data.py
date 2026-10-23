"""
Realistic demo data representing ECU (Egyptian Chinese University) Moodle LMS courses.
Used for offline development, preview, and fallback when no live session is active.
"""

MOCK_USER = {
    "id": "ecu_student_2026",
    "name": "Ahmed Mansour",
    "email": "ahmed.mansour@ecu.edu.eg",
    "role": "Undergraduate Student",
    "university": "Egyptian Chinese University (ECU)",
    "faculty": "Faculty of Engineering & Technology",
    "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
    "is_authenticated": True
}

MOCK_COURSES = [
    {
        "id": "101",
        "name": "CSE 312: Artificial Intelligence & Machine Learning",
        "code": "CSE 312",
        "term": "Spring 2026",
        "instructor": "Dr. Tarek Hegazy",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&auto=format&fit=crop&q=80",
        "progress": 72,
        "enrolled": True,
        "color": "#6366f1",
        "url": "https://lms.ecu.edu.eg/course/view.php?id=101"
    },
    {
        "id": "102",
        "name": "CSE 214: Database Systems & Cloud Architecture",
        "code": "CSE 214",
        "term": "Spring 2026",
        "instructor": "Dr. Mona El-Shenawy",
        "image_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&auto=format&fit=crop&q=80",
        "progress": 60,
        "enrolled": True,
        "color": "#0ea5e9",
        "url": "https://lms.ecu.edu.eg/course/view.php?id=102"
    },
    {
        "id": "103",
        "name": "ECE 320: Digital Signal Processing & Embedded Systems",
        "code": "ECE 320",
        "term": "Spring 2026",
        "instructor": "Prof. Mahmoud Zahran",
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=80",
        "progress": 45,
        "enrolled": True,
        "color": "#10b981",
        "url": "https://lms.ecu.edu.eg/course/view.php?id=103"
    },
    {
        "id": "104",
        "name": "CSE 331: Computer Networks & Distributed Systems",
        "code": "CSE 331",
        "term": "Spring 2026",
        "instructor": "Dr. Hany Mostafa",
        "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&auto=format&fit=crop&q=80",
        "progress": 85,
        "enrolled": True,
        "color": "#f59e0b",
        "url": "https://lms.ecu.edu.eg/course/view.php?id=104"
    },
    {
        "id": "105",
        "name": "ENG 201: Technical Writing & Academic Communication",
        "code": "ENG 201",
        "term": "Spring 2026",
        "instructor": "Dr. Salma Adel",
        "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600&auto=format&fit=crop&q=80",
        "progress": 90,
        "enrolled": True,
        "color": "#ec4899",
        "url": "https://lms.ecu.edu.eg/course/view.php?id=105"
    }
]

MOCK_COURSE_DETAILS = {
    "101": {
        "id": "101",
        "name": "CSE 312: Artificial Intelligence & Machine Learning",
        "code": "CSE 312",
        "term": "Spring 2026",
        "instructor": "Dr. Tarek Hegazy",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&auto=format&fit=crop&q=80",
        "progress": 72,
        "enrolled": True,
        "color": "#6366f1",
        "url": "https://lms.ecu.edu.eg/course/view.php?id=101",
        "announcements": [
            {
                "id": "ann-1",
                "name": "Midterm Exam Coverage & Practice Questions Posted",
                "type": "announcement",
                "url": "https://lms.ecu.edu.eg/mod/forum/discuss.php?d=101",
                "info": "Posted yesterday by Dr. Tarek Hegazy"
            }
        ],
        "sections": [
            {
                "id": "sec-0",
                "title": "Course Information & Syllabus",
                "summary": "General guidelines, grading policy, office hours, and textbook references.",
                "items": [
                    {
                        "id": "item-101-1",
                        "name": "CSE312_Course_Syllabus_Spring2026.pdf",
                        "type": "pdf",
                        "url": "https://lms.ecu.edu.eg/mod/resource/view.php?id=1001",
                        "download_url": "/api/download?file=CSE312_Course_Syllabus_Spring2026.pdf",
                        "file_size": "1.4 MB",
                        "info": "Course policies and weekly schedule"
                    },
                    {
                        "id": "item-101-2",
                        "name": "Instructor Office Hours & Zoom Link",
                        "type": "link",
                        "url": "https://lms.ecu.edu.eg/mod/url/view.php?id=1002",
                        "info": "Tuesdays & Thursdays 12:00 PM - 2:00 PM"
                    }
                ]
            },
            {
                "id": "sec-1",
                "title": "Week 1: Intelligent Agents & Problem Formulation",
                "summary": "Introduction to AI agents, environments, search formulation, and uninformed search.",
                "items": [
                    {
                        "id": "item-101-3",
                        "name": "Lecture 01 - Intelligent Agents.pdf",
                        "type": "pdf",
                        "url": "https://lms.ecu.edu.eg/mod/resource/view.php?id=1003",
                        "download_url": "/api/download?file=Lecture_01_Intelligent_Agents.pdf",
                        "file_size": "3.8 MB",
                        "info": "Presentation slides"
                    },
                    {
                        "id": "item-101-4",
                        "name": "Tutorial Sheet 1 - Search Algorithms.pdf",
                        "type": "pdf",
                        "url": "https://lms.ecu.edu.eg/mod/resource/view.php?id=1004",
                        "download_url": "/api/download?file=Tutorial_Sheet_1.pdf",
                        "file_size": "850 KB",
                        "info": "Problem set & questions"
                    }
                ]
            },
            {
                "id": "sec-2",
                "title": "Week 2: Heuristic Search & A* Algorithm",
                "summary": "Informed search strategies, admissible heuristics, and graph search guarantees.",
                "items": [
                    {
                        "id": "item-101-5",
                        "name": "Lecture 02 - Heuristic Search & A*.pdf",
                        "type": "pdf",
                        "url": "https://lms.ecu.edu.eg/mod/resource/view.php?id=1005",
                        "download_url": "/api/download?file=Lecture_02_A_Star.pdf",
                        "file_size": "4.2 MB",
                        "info": "Lecture slides with trace examples"
                    },
                    {
                        "id": "item-101-6",
                        "name": "Lab 1: Python A* Pathfinding Implementation",
                        "type": "assignment",
                        "url": "https://lms.ecu.edu.eg/mod/assign/view.php?id=1006",
                        "info": "Due: Oct 28, 2026 (Submitted)"
                    }
                ]
            },
            {
                "id": "sec-3",
                "title": "Week 3: Neural Networks & Backpropagation",
                "summary": "Perceptrons, multi-layer networks, activation functions, loss gradients.",
                "items": [
                    {
                        "id": "item-101-7",
                        "name": "Lecture 03 - Deep Learning Foundations.pdf",
                        "type": "pdf",
                        "url": "https://lms.ecu.edu.eg/mod/resource/view.php?id=1007",
                        "download_url": "/api/download?file=Lecture_03_Deep_Learning.pdf",
                        "file_size": "5.6 MB",
                        "info": "Backprop derivations"
                    },
                    {
                        "id": "item-101-8",
                        "name": "Project 1: PyTorch Classifier on Fashion-MNIST",
                        "type": "assignment",
                        "url": "https://lms.ecu.edu.eg/mod/assign/view.php?id=1008",
                        "info": "Due: Oct 31, 2026 - 11:59 PM (Pending)"
                    }
                ]
            }
        ]
    },
    "102": {
        "id": "102",
        "name": "CSE 214: Database Systems & Cloud Architecture",
        "code": "CSE 214",
        "term": "Spring 2026",
        "instructor": "Dr. Mona El-Shenawy",
        "image_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&auto=format&fit=crop&q=80",
        "progress": 60,
        "enrolled": True,
        "color": "#0ea5e9",
        "url": "https://lms.ecu.edu.eg/course/view.php?id=102",
        "announcements": [],
        "sections": [
            {
                "id": "sec-102-1",
                "title": "Relational Algebra & Advanced SQL",
                "summary": "Complex queries, window functions, and indexing strategies.",
                "items": [
                    {
                        "id": "item-102-1",
                        "name": "Lecture 4 - SQL Optimization & Indexes.pdf",
                        "type": "pdf",
                        "url": "https://lms.ecu.edu.eg/mod/resource/view.php?id=1021",
                        "download_url": "/api/download?file=Lecture_04_SQL_Optimization.pdf",
                        "file_size": "2.9 MB",
                        "info": "B-Tree vs Hash index explanation"
                    },
                    {
                        "id": "item-102-2",
                        "name": "Assignment 2: Schema Normalization (BCNF)",
                        "type": "assignment",
                        "url": "https://lms.ecu.edu.eg/mod/assign/view.php?id=1022",
                        "info": "Due: Nov 04, 2026 - 11:59 PM (Pending)"
                    }
                ]
            }
        ]
    }
}

MOCK_ASSIGNMENTS = [
    {
        "id": "assign-101",
        "course_id": "101",
        "course_name": "CSE 312: Artificial Intelligence & Machine Learning",
        "course_code": "CSE 312",
        "title": "Project 1: PyTorch Classifier on Fashion-MNIST",
        "description": "Implement a Convolutional Neural Network with at least 88% test accuracy. Submit your .ipynb and exported report.",
        "due_date": "Oct 31, 2026 - 11:59 PM",
        "due_timestamp": 1793404740,
        "status": "pending",
        "submission_url": "https://lms.ecu.edu.eg/mod/assign/view.php?id=1008",
        "attachment_name": "Project_1_Instructions.pdf",
        "days_left": 8
    },
    {
        "id": "assign-102",
        "course_id": "102",
        "course_name": "CSE 214: Database Systems & Cloud Architecture",
        "course_code": "CSE 214",
        "title": "Assignment 2: Schema Normalization & BCNF Decomposition",
        "description": "Decompose the provided enterprise relations into Boyce-Codd Normal Form with functional dependencies proof.",
        "due_date": "Nov 04, 2026 - 11:59 PM",
        "due_timestamp": 1793750340,
        "status": "pending",
        "submission_url": "https://lms.ecu.edu.eg/mod/assign/view.php?id=1022",
        "attachment_name": "HW2_Normalization.pdf",
        "days_left": 12
    },
    {
        "id": "assign-103",
        "course_id": "103",
        "course_name": "ECE 320: Digital Signal Processing & Embedded Systems",
        "course_code": "ECE 320",
        "title": "MATLAB Lab 2: Fast Fourier Transform (FFT) Filter Design",
        "description": "Design an FIR low-pass filter with Hamming window and analyze the frequency response.",
        "due_date": "Oct 25, 2026 - 08:00 PM",
        "due_timestamp": 1792886400,
        "status": "pending",
        "submission_url": "https://lms.ecu.edu.eg/mod/assign/view.php?id=1033",
        "attachment_name": "Lab2_FIR_Filter.mlx",
        "days_left": 2
    },
    {
        "id": "assign-104",
        "course_id": "101",
        "course_name": "CSE 312: Artificial Intelligence & Machine Learning",
        "course_code": "CSE 312",
        "title": "Lab 1: Python A* Pathfinding Implementation",
        "description": "Implement grid search with Manhattan and Euclidean distance heuristics.",
        "due_date": "Oct 18, 2026 - 11:59 PM",
        "due_timestamp": 1792281540,
        "status": "submitted",
        "grade": "98 / 100",
        "submission_url": "https://lms.ecu.edu.eg/mod/assign/view.php?id=1006",
        "days_left": 0
    }
]

MOCK_GRADES = {
    "101": {
        "course_name": "CSE 312: Artificial Intelligence & Machine Learning",
        "total_grade": "94.5%",
        "letter_grade": "A",
        "items": [
            {"item": "Lab 1: A* Search", "grade": "98 / 100", "weight": "10%", "feedback": "Great algorithmic structure and clean code."},
            {"item": "Quiz 1: Heuristics & Search Spaces", "grade": "19 / 20", "weight": "15%", "feedback": "Solid understanding."},
            {"item": "Tutorial Participation", "grade": "10 / 10", "weight": "5%", "feedback": "Excellent attendance."}
        ]
    },
    "102": {
        "course_name": "CSE 214: Database Systems",
        "total_grade": "88.0%",
        "letter_grade": "B+",
        "items": [
            {"item": "Assignment 1: ER Diagrams", "grade": "88 / 100", "weight": "10%", "feedback": "Cardinality ratios corrected."},
            {"item": "Quiz 1: SQL Queries", "grade": "18 / 20", "weight": "15%", "feedback": "Good join logic."}
        ]
    }
}
