from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.services.llm_service import llm_service
from app.core.security import require_role
from app.models.user import UserRole

router = APIRouter()


class ContentRequest(BaseModel):
    topic: str


@router.post("/content")
async def get_content(
    request: ContentRequest,
    current_user: dict = Depends(require_role(UserRole.teacher))   # Only teachers & admins
):
    try:
        prompt = f"""
        Recommend high-quality learning resources for the topic: {request.topic}
        Return JSON format with videos and articles.
        """

        result = llm_service.generate_json(prompt)

        return {
            "topic": request.topic,
            "resources": result,
            "generated_for": current_user['email'],
            "role": current_user['role']
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))