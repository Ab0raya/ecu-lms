# ECU LMS Mobile Companion & Scraper

A modern, fast, mobile-first companion app for the **Egyptian Chinese University (ECU) Learning Management System** (`https://lms.ecu.edu.eg/my/courses.php`), powered by [Scrapling](https://github.com/D4Vinci/Scrapling) and FastAPI.

---

## 🌟 Key Capabilities

1. **Cloudflare & Anti-Bot Bypass with Scrapling**:
   - `lms.ecu.edu.eg` is protected by Cloudflare (which blocks standard HTTP scrapers with 403 Forbidden).
   - Scrapling's `FetcherSession(impersonate='chrome')` delivers TLS fingerprinting and stealth browser headers to reliably communicate with the university server with zero overhead.

2. **Microsoft Entra ID (OIDC) Session Sync**:
   - ECU LMS delegates single sign-on to Microsoft Entra ID (`login.microsoftonline.com`).
   - The app provides a 1-tap Bookmarklet and session sync helper to import the student's authenticated `MoodleSession` cookie.

3. **Mobile-First Progressive Web App (PWA)**:
   - Installable directly to the home screen on iOS and Android.
   - Glassmorphic dark theme, sleek typography (Outfit & Plus Jakarta Sans), and smooth transitions.
   - **Enrolled Courses**: Real-time search, progress tracking, and lecture breakdown.
   - **Course Detail Modal**: Organized weekly topics, PDF lecture slides, downloadable files, and instructor announcements.
   - **Deadlines & Quizzes**: Urgency badges, countdown chips, and submission links.
   - **Academic Grades**: GPA card and assessment breakdown.
   - **Demo & Offline Mode**: Explore with realistic ECU course structures even before logging in.

---

## 🏗️ Architecture

```
                                  ┌───────────────────────────────┐
                                  │      lms.ecu.edu.eg           │
                                  │   (Cloudflare + Moodle + OIDC)│
                                  └───────────────▲───────────────┘
                                                  │
                                       Scrapling FetcherSession
                                     (TLS Fingerprint Impersonation)
                                                  │
┌───────────────────────────┐     ┌───────────────▼───────────────┐
│   Mobile Client (PWA)     │◄───►│  FastAPI Backend (Port 8000)  │
│   iOS / Android Browser   │     │  - Scrapling Parser & Engine  │
│   - Courses, Files, Tasks │     │  - REST API & PWA Server      │
└───────────────────────────┘     └───────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Launch the Server
```bash
./run.sh
```
Or manually:
```bash
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Open the Mobile App
Open your browser and navigate to:
```
http://localhost:8000
```
On mobile devices on the same Wi-Fi network, navigate to `http://<YOUR_LOCAL_IP>:8000`.

---

## 📱 Installing on Mobile Devices (PWA)

- **iOS (Safari)**:
  1. Open `http://<YOUR_LOCAL_IP>:8000` in Safari.
  2. Tap the **Share** button (`⎋`).
  3. Tap **Add to Home Screen**.
- **Android (Chrome)**:
  1. Open `http://<YOUR_LOCAL_IP>:8000` in Chrome.
  2. Tap the **Three Dots Menu** (`⋮`).
  3. Tap **Install App** / **Add to Home screen**.

---

## 🔐 How to Connect Your Live ECU LMS Account

1. Open `lms.ecu.edu.eg` in your desktop or mobile browser and log in with your university Microsoft account.
2. Open developer console or use the built-in 1-tap Bookmarklet provided in the app's **Connect Session** modal.
3. Paste your `MoodleSession` cookie.
4. Scrapling will verify the session and immediately pull your live courses, lecture materials, and deadlines.

---

## 🛠️ API Reference

| Endpoint | Method | Description |
|---|---|---|
| `GET /api/courses` | `GET` | List all enrolled courses |
| `GET /api/courses/{id}` | `GET` | Course syllabus, topics, and files |
| `GET /api/assignments` | `GET` | Deadlines, quizzes, and tasks |
| `GET /api/grades/{id}` | `GET` | Gradebook and instructor feedback |
| `GET /api/download` | `GET` | Authenticated proxy download for lecture PDFs |
| `POST /api/auth/session` | `POST` | Validate and store student MoodleSession cookie |
| `GET /api/auth/me` | `GET` | Current student profile & status |
| `GET /health` | `GET` | Service & Scrapling health check |
