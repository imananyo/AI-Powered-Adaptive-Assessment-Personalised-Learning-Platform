from typing import Dict, Any

from app.services.llm_service import llm_service
from app.core.logging import logger


class GradingService:
    def grade_answer(
        self,
        question: Dict[str, Any],
        student_answer: str
    ) -> Dict[str, Any]:
        prompt = f"""
        You are an expert evaluator.

        QUESTION:
        {question}

        STUDENT ANSWER:
        {student_answer}

        Evaluate based on:
        1. Correctness (0-100)
        2. Depth of understanding (0-100)
        3. Identify mistake types: conceptual, logical, syntax (if code)

        Return ONLY valid JSON:
        {{
            "score": int,
            "depth_score": int,
            "mistakes": [],
            "feedback": "detailed constructive feedback"
        }}
        """

        try:
            result = llm_service.generate_json(prompt)
            logger.info("Grading completed successfully")
            return result
        except Exception as e:
            logger.error(f"Grading failed: {e}")
            raise


grading_service = GradingService()