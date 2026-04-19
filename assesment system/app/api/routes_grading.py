from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.services.grading_service import grading_service
from app.core.logging import logger
from app.db.database import get_db
from app.models.models import Submission

router = APIRouter()


class GradingRequest(BaseModel):
    question: Dict[str, Any]
    student_answer: str
    student_id: str


@router.post("/evaluate")
async def evaluate_answer(
    request: GradingRequest,
    db: Session = Depends(get_db)
):
    try:
        result = grading_service.grade_answer(
            question=request.question,
            student_answer=request.student_answer
        )

        # Persist to DB
        submission = Submission(
            student_id=request.student_id,
            answer=request.student_answer,
            evaluation=result
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)

        return {"evaluation": result}

    except Exception as e:
        logger.exception("Grading failed")
        raise HTTPException(status_code=500, detail=str(e))