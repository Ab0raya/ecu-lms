import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/course.dart';
import '../services/api_service.dart';

class CourseDetailScreen extends StatefulWidget {
  final CourseSummary course;

  const CourseDetailScreen({super.key, required this.course});

  @override
  State<CourseDetailScreen> createState() => _CourseDetailScreenState();
}

class _CourseDetailScreenState extends State<CourseDetailScreen> {
  CourseDetail? _detail;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadCourseDetail();
  }

  Future<void> _loadCourseDetail() async {
    setState(() => _isLoading = true);
    final detail = await ApiService().fetchCourseDetail(widget.course.id);
    if (mounted) {
      setState(() {
        _detail = detail;
        _isLoading = false;
      });
    }
  }

  Future<void> _openUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF080C14),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F1626),
        title: Text(
          widget.course.code ?? widget.course.name,
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: _isLoading
          ? const Center(
              child: CircularProgressIndicator(color: Color(0xFF4F46E5)),
            )
          : _detail == null
              ? const Center(
                  child: Text('فشل تحميل محتوى المادة',
                      style: TextStyle(color: Colors.white70)),
                )
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Header Card
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: const Color(0xFF101726),
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: Colors.white.withValues(alpha: 0.08),
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _detail!.name,
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Row(
                              children: [
                                const Icon(Icons.school,
                                    size: 16, color: Color(0xFF818CF8)),
                                const SizedBox(width: 6),
                                Text(
                                  _detail!.instructor ?? 'Faculty Staff',
                                  style: const TextStyle(
                                      color: Colors.white70, fontSize: 13),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 20),

                      // Sections
                      const Text(
                        'Weekly Topics & Materials',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 12),
                      ..._detail!.sections.map((section) {
                        return Container(
                          margin: const EdgeInsets.only(bottom: 12),
                          decoration: BoxDecoration(
                            color: const Color(0xFF101726),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: Colors.white.withValues(alpha: 0.08),
                            ),
                          ),
                          child: ExpansionTile(
                            initiallyExpanded: true,
                            iconColor: const Color(0xFF818CF8),
                            collapsedIconColor: Colors.white54,
                            title: Text(
                              section.title.isEmpty ? 'General' : section.title,
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                                color: Colors.white,
                              ),
                            ),
                            children: section.items.map((item) {
                              final isPdf = item.type == 'pdf' ||
                                  item.name.toLowerCase().contains('.pdf');
                              final isAssign = item.type == 'assignment';

                              return ListTile(
                                leading: Container(
                                  padding: const EdgeInsets.all(8),
                                  decoration: BoxDecoration(
                                    color: isPdf
                                        ? const Color(0xFFF43F5E).withValues(alpha: 0.15)
                                        : (isAssign
                                            ? const Color(0xFFF59E0B).withValues(alpha: 0.15)
                                            : const Color(0xFF06B6D4).withValues(alpha: 0.15)),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Icon(
                                    isPdf
                                        ? Icons.picture_as_pdf
                                        : (isAssign
                                            ? Icons.assignment
                                            : Icons.link),
                                    color: isPdf
                                        ? const Color(0xFFF43F5E)
                                        : (isAssign
                                            ? const Color(0xFFF59E0B)
                                            : const Color(0xFF06B6D4)),
                                    size: 20,
                                  ),
                                ),
                                title: Text(
                                  item.name,
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 13,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                                subtitle: item.info != null
                                    ? Text(
                                        item.info!,
                                        style: const TextStyle(
                                            color: Colors.white54, fontSize: 11),
                                      )
                                    : null,
                                trailing: IconButton(
                                  icon: const Icon(Icons.download,
                                      color: Color(0xFF818CF8)),
                                  onPressed: () {
                                    final url = item.downloadUrl != null
                                        ? '${ApiService().baseUrl}${item.downloadUrl}'
                                        : item.url;
                                    _openUrl(url);
                                  },
                                ),
                              );
                            }).toList(),
                          ),
                        );
                      }),
                    ],
                  ),
                ),
    );
  }
}
