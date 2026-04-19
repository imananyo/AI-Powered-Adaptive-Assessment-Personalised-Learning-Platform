import random
from typing import List, Dict

from app.services.llm_service import llm_service


class QuestionGenerator:
    def _generate_single_question(self, topic: str, difficulty: str, seed: int) -> Dict:
        random.seed(seed)

        contexts = [
            "housing prices dataset",
            "car sales dataset",
            "student exam scores dataset",
            "stock market dataset",
            "salary prediction dataset"
        ]

        selected_context = random.choice(contexts)

        prompt = f"""
        Generate a {difficulty} level question on {topic}.

        Context: {selected_context}

        The question must include:
        1. main_question
        2. logic_check (short answer)
        3. conceptual_why (deep reasoning)

        Return JSON format:
        {{
            "main_question": "...",
            "logic_check": "...",
            "conceptual_why": "..."
        }}
        """

        return llm_service.generate_json(prompt)

    def generate_for_students(
        self,
        topic: str,
        difficulty: str,
        num_students: int,
        base_seed: int = 42
    ) -> List[Dict]:
        questions = []

        for i in range(num_students):
            seed = base_seed + i
            question = self._generate_single_question(
                topic=topic,
                difficulty=difficulty,
                seed=seed
            )
            questions.append({
                "student_id": f"student_{i+1}",
                "seed": seed,
                "question": question
            })

        return questions


question_generator = QuestionGenerator()