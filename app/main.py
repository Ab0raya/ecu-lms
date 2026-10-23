"""
ECU LMS Mobile Converter & Companion Backend.
Powered by Scrapling (Anti-bot Cloudflare bypass & Moodle HTML extraction).
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import BASE_DIR, LMS_BASE_URL, DEMO_MODE
from app.api.auth import router as auth_router
from app.api.courses import router as courses_router
from app.api.assignments import router as assignments_router
from app.api.grades import router as grades_router
from app.api.files import router as files_router

app = FastAPI(
    title="ECU LMS Mobile Companion API",
    description="Mobile App & REST API Bridge for Egyptian Chinese University LMS powered by Scrapling",
    version="1.0.0"
)

# Enable CORS for mobile webview and cross-origin clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(auth_router)
app.include_router(courses_router)
app.include_router(assignments_router)
app.include_router(grades_router)
app.include_router(files_router)

# Mount static directory for the mobile PWA
static_dir = BASE_DIR / "app" / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "ECU LMS Mobile Backend",
        "scrapling_engine": "active",
        "target_lms": LMS_BASE_URL,
        "demo_mode": DEMO_MODE
    }

@app.get("/download-apk")
def download_apk():
    apk_path = BASE_DIR / "ecu-lms.apk"
    if apk_path.exists():
        return FileResponse(
            apk_path,
            media_type="application/vnd.android.package-archive",
            filename="ECU-LMS.apk"
        )
    return {"error": "APK not found"}

@app.get("/")
def serve_index():
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "ECU LMS Mobile Backend is running. Static UI not found."}

@app.get("/manifest.json")
def serve_manifest():
    manifest_path = static_dir / "manifest.json"
    if manifest_path.exists():
        return FileResponse(manifest_path, media_type="application/manifest+json")
    return {}

@app.get("/sw.js")
def serve_service_worker():
    sw_path = static_dir / "sw.js"
    if sw_path.exists():
        return FileResponse(sw_path, media_type="application/javascript")
    return {}
