import 'dart:async';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../services/api_service.dart';

class LoginWebViewScreen extends StatefulWidget {
  const LoginWebViewScreen({super.key});

  @override
  State<LoginWebViewScreen> createState() => _LoginWebViewScreenState();
}

class _LoginWebViewScreenState extends State<LoginWebViewScreen> {
  late final WebViewController _controller;
  final WebViewCookieManager _cookieManager = WebViewCookieManager();
  bool _isLoading = true;
  bool _isCapturing = false;
  String? _detectedSession;
  String _currentUrl = 'https://lms.ecu.edu.eg/auth/oidc/';
  Timer? _pollingTimer;

  @override
  void initState() {
    super.initState();

    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setUserAgent(
          "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36")
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (url) {
            setState(() {
              _isLoading = true;
              _currentUrl = url;
            });
            _checkCookies(url);
          },
          onPageFinished: (url) async {
            setState(() {
              _isLoading = false;
              _currentUrl = url;
            });
            await _checkCookies(url);
          },
          onUrlChange: (change) async {
            if (change.url != null) {
              setState(() => _currentUrl = change.url!);
              await _checkCookies(change.url!);
            }
          },
        ),
      )
      ..loadRequest(Uri.parse('https://lms.ecu.edu.eg/auth/oidc/'));

    // Periodic check every 1.2s to auto-detect login completion seamlessly
    _pollingTimer = Timer.periodic(const Duration(milliseconds: 1200), (_) {
      if (mounted && !_isCapturing) {
        _checkCookies(_currentUrl);
      }
    });
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    super.dispose();
  }

  Future<void> _checkCookies([String? url]) async {
    if (_isCapturing) return;

    try {
      final targets = [
        Uri.parse('https://lms.ecu.edu.eg'),
        Uri.parse('https://lms.ecu.edu.eg/my/courses.php'),
        Uri.parse('https://lms.ecu.edu.eg/my/'),
      ];

      for (final uri in targets) {
        final cookies = await _cookieManager.getCookies(domain: uri);
        for (final c in cookies) {
          if (c.name == 'MoodleSession' && c.value.isNotEmpty) {
            await _onSessionFound(c.value);
            return;
          }
        }
      }

      // Check document.cookie as fallback
      final result =
          await _controller.runJavaScriptReturningResult('document.cookie');
      final cookieStr = result.toString();
      if (cookieStr.contains('MoodleSession')) {
        final match =
            RegExp(r'MoodleSession=([a-zA-Z0-9]+)').firstMatch(cookieStr);
        if (match != null && match.group(1) != null) {
          await _onSessionFound(match.group(1)!);
          return;
        }
      }

      // If user is visibly on Moodle dashboard (/my or /my/courses.php)
      final activeUrl = url ?? _currentUrl;
      if (activeUrl.contains('lms.ecu.edu.eg') &&
          (activeUrl.contains('/my') || activeUrl.contains('course')) &&
          !activeUrl.contains('/auth/oidc/')) {
        // Try to read all cookies once more
        final allCookies = await _cookieManager.getCookies(
          domain: Uri.parse('https://lms.ecu.edu.eg'),
        );
        for (final c in allCookies) {
          if (c.name.toLowerCase().contains('moodle') ||
              c.name == 'MoodleSession') {
            await _onSessionFound(c.value);
            return;
          }
        }
      }
    } catch (_) {}
  }

  Future<void> _onSessionFound(String token) async {
    if (_isCapturing || token == _detectedSession) return;
    setState(() {
      _isCapturing = true;
      _detectedSession = token;
    });

    _pollingTimer?.cancel();

    await ApiService().setSessionToken(token);

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Row(
            children: [
              Icon(Icons.check_circle, color: Colors.white),
              SizedBox(width: 10),
              Text('✅ تم تسجيل الدخول بنجاح ومزامنة الكورسات!'),
            ],
          ),
          backgroundColor: Color(0xFF10B981),
          duration: Duration(seconds: 2),
        ),
      );
      Navigator.of(context).pop(true);
    }
  }

  Future<void> _manualFinish() async {
    setState(() => _isLoading = true);
    await _checkCookies();
    if (_detectedSession == null) {
      // Try fetching cookies directly
      final cookies = await _cookieManager.getCookies(
        domain: Uri.parse('https://lms.ecu.edu.eg'),
      );
      for (final c in cookies) {
        if (c.name == 'MoodleSession' && c.value.isNotEmpty) {
          await _onSessionFound(c.value);
          return;
        }
      }

      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
              'برجاء إتمام تسجيل الدخول في الموقع أولاً (أدخل بريدك وكلمة المرور)',
            ),
            backgroundColor: Color(0xFFEF4444),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF080C14),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F1626),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'تسجيل دخول جامعة ECU',
              style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
            ),
            Text(
              _currentUrl.contains('microsoft')
                  ? 'Microsoft Entra ID (University Login)'
                  : 'ECU LMS Moodle Portal',
              style: const TextStyle(fontSize: 10, color: Colors.white54),
            ),
          ],
        ),
        leading: IconButton(
          icon: const Icon(Icons.close),
          onPressed: () => Navigator.of(context).pop(false),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => _controller.reload(),
          ),
        ],
      ),
      body: Stack(
        children: [
          WebViewWidget(controller: _controller),
          if (_isLoading)
            Container(
              color: Colors.black.withValues(alpha: 0.3),
              child: const Center(
                child: CircularProgressIndicator(color: Color(0xFF4F46E5)),
              ),
            ),
        ],
      ),
      bottomNavigationBar: SafeArea(
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: const Color(0xFF0F172A),
            border: Border(
              top: BorderSide(
                color: Colors.white.withValues(alpha: 0.08),
                width: 1,
              ),
            ),
          ),
          child: Row(
            children: [
              const Expanded(
                child: Text(
                  'أكمل تسجيل الدخول في الصفحة، وسيتم نقلك للتطبيق تلقائياً',
                  style: TextStyle(fontSize: 12, color: Colors.white70),
                ),
              ),
              const SizedBox(width: 8),
              ElevatedButton.icon(
                onPressed: _manualFinish,
                icon: const Icon(Icons.arrow_forward, size: 16),
                label: const Text('دخول للتطبيق'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF4F46E5),
                  foregroundColor: Colors.white,
                  padding:
                      const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
