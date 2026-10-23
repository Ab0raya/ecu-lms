class ResourceItem {
  final String id;
  final String name;
  final String type; // pdf, link, assignment, announcement, quiz
  final String url;
  final String? downloadUrl;
  final String? fileSize;
  final String? info;

  ResourceItem({
    required this.id,
    required this.name,
    required this.type,
    required this.url,
    this.downloadUrl,
    this.fileSize,
    this.info,
  });

  factory ResourceItem.fromJson(Map<String, dynamic> json) {
    return ResourceItem(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      type: json['type'] ?? 'link',
      url: json['url'] ?? '',
      downloadUrl: json['download_url'],
      fileSize: json['file_size'],
      info: json['info'],
    );
  }
}

class CourseSection {
  final String id;
  final String title;
  final String? summary;
  final List<ResourceItem> items;

  CourseSection({
    required this.id,
    required this.title,
    this.summary,
    required this.items,
  });

  factory CourseSection.fromJson(Map<String, dynamic> json) {
    var rawItems = json['items'] as List? ?? [];
    return CourseSection(
      id: json['id']?.toString() ?? '',
      title: json['title'] ?? 'Section',
      summary: json['summary'],
      items: rawItems.map((e) => ResourceItem.fromJson(e)).toList(),
    );
  }
}

class CourseSummary {
  final String id;
  final String name;
  final String? code;
  final String term;
  final String? instructor;
  final String? imageUrl;
  final int progress;
  final String color;
  final String url;

  CourseSummary({
    required this.id,
    required this.name,
    this.code,
    required this.term,
    this.instructor,
    this.imageUrl,
    required this.progress,
    required this.color,
    required this.url,
  });

  factory CourseSummary.fromJson(Map<String, dynamic> json) {
    return CourseSummary(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      code: json['code'],
      term: json['term'] ?? 'Spring 2026',
      instructor: json['instructor'],
      imageUrl: json['image_url'],
      progress: json['progress'] ?? 0,
      color: json['color'] ?? '#4f46e5',
      url: json['url'] ?? '',
    );
  }
}

class CourseDetail extends CourseSummary {
  final List<CourseSection> sections;
  final List<ResourceItem> announcements;

  CourseDetail({
    required super.id,
    required super.name,
    super.code,
    required super.term,
    super.instructor,
    super.imageUrl,
    required super.progress,
    required super.color,
    required super.url,
    required this.sections,
    required this.announcements,
  });

  factory CourseDetail.fromJson(Map<String, dynamic> json) {
    var rawSections = json['sections'] as List? ?? [];
    var rawAnnounce = json['announcements'] as List? ?? [];

    return CourseDetail(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      code: json['code'],
      term: json['term'] ?? 'Spring 2026',
      instructor: json['instructor'],
      imageUrl: json['image_url'],
      progress: json['progress'] ?? 0,
      color: json['color'] ?? '#4f46e5',
      url: json['url'] ?? '',
      sections: rawSections.map((e) => CourseSection.fromJson(e)).toList(),
      announcements: rawAnnounce.map((e) => ResourceItem.fromJson(e)).toList(),
    );
  }
}
