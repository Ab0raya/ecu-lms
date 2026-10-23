class UserProfile {
  final String id;
  final String name;
  final String? email;
  final String? avatarUrl;
  final String role;
  final String university;
  final String faculty;
  final bool isAuthenticated;

  UserProfile({
    required this.id,
    required this.name,
    this.email,
    this.avatarUrl,
    required this.role,
    required this.university,
    required this.faculty,
    required this.isAuthenticated,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id']?.toString() ?? 'ecu_student',
      name: json['name'] ?? 'ECU Student',
      email: json['email'],
      avatarUrl: json['avatar_url'],
      role: json['role'] ?? 'Student',
      university: json['university'] ?? 'Egyptian Chinese University (ECU)',
      faculty: json['faculty'] ?? 'Engineering & Technology',
      isAuthenticated: json['is_authenticated'] ?? true,
    );
  }
}
