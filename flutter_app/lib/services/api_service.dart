import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import '../models/course.dart';
import '../models/assignment.dart';

class ApiService {
  static const String defaultCloudUrl =
      'https://markers-analog-buildings-thumbzilla.trycloudflare.com';
  static const String keyBaseUrl = 'ecu_api_base_url';
  static const String keySession = 'ecu_moodle_session';

  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  String _baseUrl = defaultCloudUrl;
  String? _moodleSession;

  String get baseUrl => _baseUrl;
  String? get moodleSession => _moodleSession;

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _baseUrl = prefs.getString(keyBaseUrl) ?? defaultCloudUrl;
    _moodleSession = prefs.getString(keySession);
  }

  Future<void> setBaseUrl(String url) async {
    _baseUrl = url.trim().replaceAll(RegExp(r'/+$'), '');
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(keyBaseUrl, _baseUrl);
  }

  Future<void> setSessionToken(String token) async {
    _moodleSession = token.trim();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(keySession, _moodleSession!);

    // Also notify backend
    try {
      final uri = Uri.parse('$_baseUrl/api/auth/session');
      await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'moodle_session': _moodleSession}),
      );
    } catch (_) {}
  }

  Future<void> logout() async {
    _moodleSession = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(keySession);
    try {
      final uri = Uri.parse('$_baseUrl/api/auth/logout');
      await http.post(uri);
    } catch (_) {}
  }

  Map<String, String> _getHeaders() {
    final headers = {'Content-Type': 'application/json'};
    if (_moodleSession != null && _moodleSession!.isNotEmpty) {
      headers['X-Moodle-Session'] = _moodleSession!;
      headers['Cookie'] = 'moodle_session=$_moodleSession';
    }
    return headers;
  }

  Future<UserProfile?> fetchProfile() async {
    try {
      final uri = Uri.parse('$_baseUrl/api/auth/me');
      final res = await http.get(uri, headers: _getHeaders()).timeout(
            const Duration(seconds: 12),
          );
      if (res.statusCode == 200) {
        final data = jsonDecode(utf8.decode(res.bodyBytes));
        if (data['user'] != null) {
          return UserProfile.fromJson(data['user']);
        }
      }
    } catch (e) {
      // ignore
    }
    return null;
  }

  Future<List<CourseSummary>> fetchCourses() async {
    try {
      final uri = Uri.parse('$_baseUrl/api/courses');
      final res = await http.get(uri, headers: _getHeaders()).timeout(
            const Duration(seconds: 15),
          );
      if (res.statusCode == 200) {
        final List data = jsonDecode(utf8.decode(res.bodyBytes));
        return data.map((e) => CourseSummary.fromJson(e)).toList();
      }
    } catch (e) {
      // ignore
    }
    return [];
  }

  Future<CourseDetail?> fetchCourseDetail(String courseId) async {
    try {
      final uri = Uri.parse('$_baseUrl/api/courses/$courseId');
      final res = await http.get(uri, headers: _getHeaders()).timeout(
            const Duration(seconds: 15),
          );
      if (res.statusCode == 200) {
        final data = jsonDecode(utf8.decode(res.bodyBytes));
        return CourseDetail.fromJson(data);
      }
    } catch (e) {
      // ignore
    }
    return null;
  }

  Future<List<AssignmentItem>> fetchAssignments() async {
    try {
      final uri = Uri.parse('$_baseUrl/api/assignments');
      final res = await http.get(uri, headers: _getHeaders()).timeout(
            const Duration(seconds: 15),
          );
      if (res.statusCode == 200) {
        final List data = jsonDecode(utf8.decode(res.bodyBytes));
        return data.map((e) => AssignmentItem.fromJson(e)).toList();
      }
    } catch (e) {
      // ignore
    }
    return [];
  }
}
