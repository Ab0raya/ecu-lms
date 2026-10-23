"""
Course materials proxy and file download endpoints.
"""
from fastapi import APIRouter, Header, Request, Query, HTTPException, Response
from typing import Optional
from app.scraper.client import ECULMSClient

router = APIRouter(prefix="/api/download", tags=["Files"])

@router.get("")
def download_file(
    request: Request,
    url: Optional[str] = Query(None),
    file: Optional[str] = Query(None),
    x_moodle_session: Optional[str] = Header(None)
):
    """
    Download a lecture slide, syllabus, or course document via authenticated Scrapling session.
    """
    token = x_moodle_session or request.cookies.get("moodle_session")
    
    if file:
        # Mock / sample PDF generation for demo mode
        sample_pdf = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 51 >>\nstream\nBT /F1 24 Tf 100 700 Td (Egyptian Chinese University) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000117 00000 n\n0000000213 00000 n\ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n314\n%%EOF"
        return Response(
            content=sample_pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{file}"'}
        )

    if not url:
        raise HTTPException(status_code=400, detail="Missing resource url")

    client = ECULMSClient(moodle_session=token)
    try:
        content, content_type = client.download_resource(url)
        return Response(
            content=content,
            media_type=content_type,
            headers={"Content-Disposition": 'attachment; filename="course_material.pdf"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download material: {str(e)}")
