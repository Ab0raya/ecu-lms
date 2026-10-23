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
  bool _isLoading = true;
  String? _detectedSession;

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
            setState(() => _isLoading = true);
          },
          onPageFinished: (url) async {
            setState(() => _isLoading = false);
            await _checkCookies();
          },
          onUrlChange: (change) async {
            await _checkCookies();
          },
        ),
      )
      ..loadRequest(Uri.parse('https://lms.ecu.edu.eg/auth/oidc/'));
  }

  Future<void> _checkCookies() async {
    try {
      // Evaluate document.cookie
      final result = await _controller.runJavaScriptReturningResult('document.cookie');
      final cookieStr = result.toString();

      if (cookieStr.contains('MoodleSession')) {
        final match = RegExp(r'MoodleSession=([a-zA-Z0-9]+)').firstMatch(cookieStr);
        if (match != null) {
          final token = match.group(1);
          if (token != null && token.isNotEmpty && token != _detectedSession) {
            _detectedSession = token;
            await ApiService().setSessionToken(token);
            if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('✅ تم تسجيل الدخول تلقائياً!'),
                  backgroundColor: Color(0xFF10B981),
                ),
              );
              Navigator.of(context).pop(true);
            }
          }
        }
      }
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF080C14),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F1626),
        title: const Text(
          'تسجيل دخول جامعة ECU',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
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
            const Center(
              child: CircularProgressIndicator(color: Color(0xFF4F46E5)),
            ),
        ],
      ),
    );
  }
}
