from fastapi import APIRouter
from app.schemas.base import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", app_name="AI Assessment Platform")