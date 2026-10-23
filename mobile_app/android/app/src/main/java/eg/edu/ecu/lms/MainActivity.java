package eg.edu.ecu.lms;

import android.os.Bundle;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.app.Dialog;
import android.view.ViewGroup;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Expose a native JavaScript bridge to our frontend
        this.getBridge().getWebView().addJavascriptInterface(new Object() {
            @JavascriptInterface
            public void openInAppLogin() {
                runOnUiThread(() -> showLoginDialog());
            }

            @JavascriptInterface
            public boolean isNativeAvailable() {
                return true;
            }
        }, "ECUNativeAuth");
    }

    private void showLoginDialog() {
        Dialog dialog = new Dialog(this, android.R.style.Theme_Black_NoTitleBar_Fullscreen);
        WebView loginWebView = new WebView(this);
        WebSettings settings = loginWebView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setUserAgentString("Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36");

        CookieManager cookieManager = CookieManager.getInstance();
        cookieManager.setAcceptCookie(true);
        cookieManager.setAcceptThirdPartyCookies(loginWebView, true);

        loginWebView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                
                String cookies = CookieManager.getInstance().getCookie(url);
                if (cookies != null && cookies.contains("MoodleSession")) {
                    for (String cookie : cookies.split(";")) {
                        String[] parts = cookie.trim().split("=");
                        if (parts.length >= 2 && parts[0].trim().equals("MoodleSession")) {
                            String token = parts[1].trim();
                            if (!token.isEmpty()) {
                                dialog.dismiss();
                                getBridge().getWebView().post(() -> {
                                    getBridge().getWebView().evaluateJavascript(
                                        "window.onNativeLoginSuccess('" + token + "')", null
                                    );
                                });
                                return;
                            }
                        }
                    }
                }
            }
        });

        loginWebView.loadUrl("https://lms.ecu.edu.eg/auth/oidc/");
        dialog.setContentView(loginWebView, new ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT
        ));
        dialog.show();
    }
}
