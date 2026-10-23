"""
Authentication and session management routes for ECU LMS.
"""
from fastapi import APIRouter, Header, Response, Request
from typing import Optional
from app.models.auth import SessionAuthRequest, SessionAuthResponse
from app.scraper.client import ECULMSClient
from app.config import DEMO_MODE
from app.scraper.mock_data import MOCK_USER

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# In-memory session store (keyed by token or global active session)
ACTIVE_SESSIONS = {}

@router.post("/session", response_model=SessionAuthResponse)
def set_session(auth_req: SessionAuthRequest, response: Response):
    """
    Validate and save a MoodleSession cookie from ECU LMS.
    """
    token = auth_req.moodle_session.strip()
    client = ECULMSClient(moodle_session=token)
    check = client.check_session()
    
    if check.get("authenticated"):
        user = check.get("user")
        ACTIVE_SESSIONS[token] = user
        response.set_cookie(key="moodle_session", value=token, httponly=True, samesite="lax")
        return SessionAuthResponse(
            success=True,
            message="Successfully authenticated with ECU LMS",
            is_valid=True,
            user=user
        )
    elif DEMO_MODE:
        # If running in development/demo mode, accept the token or use demo profile
        user = MOCK_USER.copy()
        if auth_req.name:
            user["name"] = auth_req.name
        ACTIVE_SESSIONS[token] = user
        response.set_cookie(key="moodle_session", value=token, httponly=True, samesite="lax")
        return SessionAuthResponse(
            success=True,
            message="Connected to ECU LMS (Demo / Fallback Mode enabled)",
            is_valid=True,
            user=user
        )
    else:
        return SessionAuthResponse(
            success=False,
            message=check.get("reason", "Invalid or expired session cookie"),
            is_valid=False
        )

@router.get("/me")
def get_current_user(
    request: Request,
    x_moodle_session: Optional[str] = Header(None)
):
    """
    Return the current active student profile.
    """
    token = x_moodle_session or request.cookies.get("moodle_session")
    if token and token in ACTIVE_SESSIONS:
        return {"authenticated": True, "user": ACTIVE_SESSIONS[token]}
    
    client = ECULMSClient(moodle_session=token)
    profile = client.get_profile()
    return {"authenticated": profile.get("is_authenticated", False), "user": profile}

@router.post("/logout")
def logout(response: Response):
    """
    Clear stored session.
    """
    response.delete_cookie(key="moodle_session")
    return {"success": True, "message": "Logged out successfully"}
