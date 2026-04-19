from typing import Dict, Any
import json

from app.services.llm_service import llm_service
from app.core.logging import logger


class PersonalizationService:
    def extract_weak_concepts(
        self,
        question: Dict[str, Any],
        student_answer: str,
        evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        prompt = f"""
        Analyze the student's performance.

        QUESTION:
        {json.dumps(question, indent=2)}

        STUDENT ANSWER:
        {student_answer}

        EVALUATION:
        {json.dumps(evaluation, indent=2)}

        Identify weak concepts and improvement areas.

        Return JSON:
        {{
            "weak_concepts": ["..."],
            "improvement_areas": ["..."]
        }}
        """

        return llm_service.generate_json(prompt)

    def recommend_resources(self, weak_concepts: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Recommend learning resources for:

        {json.dumps(weak_concepts, indent=2)}

        Return JSON:
        {{
            "videos": [{{"title": "...", "url": "..."}}],
            "articles": [{{"title": "...", "url": "..."}}]
        }}
        """

        return llm_service.generate_json(prompt)

    def generate_personalized_plan(
        self,
        question: Dict[str, Any],
        student_answer: str,
        evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        logger.info("Starting personalization pipeline")

        weak_concepts = self.extract_weak_concepts(question, student_answer, evaluation)
        resources = self.recommend_resources(weak_concepts)

        logger.info("Personalization completed")
        return {
            "weak_analysis": weak_concepts,
            "recommended_resources": resources
        }


personalization_service = PersonalizationService()