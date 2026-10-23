class AssignmentItem {
  final String id;
  final String courseId;
  final String courseName;
  final String? courseCode;
  final String title;
  final String? description;
  final String dueDate;
  final int? dueTimestamp;
  final String status; // 'submitted', 'pending', 'overdue'
  final String? grade;
  final String submissionUrl;
  final int? daysLeft;

  AssignmentItem({
    required this.id,
    required this.courseId,
    required this.courseName,
    this.courseCode,
    required this.title,
    this.description,
    required this.dueDate,
    this.dueTimestamp,
    required this.status,
    this.grade,
    required this.submissionUrl,
    this.daysLeft,
  });

  factory AssignmentItem.fromJson(Map<String, dynamic> json) {
    return AssignmentItem(
      id: json['id']?.toString() ?? '',
      courseId: json['course_id']?.toString() ?? '',
      courseName: json['course_name'] ?? '',
      courseCode: json['course_code'],
      title: json['title'] ?? 'Assignment',
      description: json['description'],
      dueDate: json['due_date'] ?? '',
      dueTimestamp: json['due_timestamp'],
      status: json['status'] ?? 'pending',
      grade: json['grade'],
      submissionUrl: json['submission_url'] ?? '',
      daysLeft: json['days_left'],
    );
  }
}
