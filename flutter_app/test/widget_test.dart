import 'package:flutter_test/flutter_test.dart';
import 'package:ecu_lms/main.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const EcuLmsApp());
  });
}
