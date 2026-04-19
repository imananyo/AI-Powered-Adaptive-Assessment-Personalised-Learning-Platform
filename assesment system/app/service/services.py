import json
from typing import Any, Dict

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging import logger


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
    def generate(self, prompt: str, temperature: float = 0.3) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a precise and structured AI assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            raise

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        response_text = self.generate(prompt, temperature=0.2)

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON from LLM. Retrying with lower temperature...")
            response_text = self.generate(prompt, temperature=0.1)
            try:
                return json.loads(response_text)
            except Exception as e:
                logger.error(f"Failed to parse JSON after retry: {e}")
                raise ValueError("LLM did not return valid JSON")


llm_service = LLMService()