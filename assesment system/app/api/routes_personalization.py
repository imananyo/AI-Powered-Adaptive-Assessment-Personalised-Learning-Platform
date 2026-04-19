from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.services.personalization_service import personalization_service
from app.core.logging import logger

router = APIRouter()


class PersonalizationRequest(BaseModel):
    question: Dict[str, Any]
    student_answer: str
    evaluation: Dict[str, Any]


@router.post("/recommend")
async def generate_recommendation(request: PersonalizationRequest):
    try:
        result = personalization_service.generate_personalized_plan(
            question=request.question,
            student_answer=request.student_answer,
            evaluation=request.evaluation
        )
        return result

    except Exception as e:
        logger.exception("Personalization error")
        raise HTTPException(status_code=500, detail=str(e))