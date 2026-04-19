from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


@celery_app.task
def async_generate_questions(topic, difficulty, num_students):
    from app.services.question_generator import question_generator
    return question_generator.generate_for_students(
        topic, difficulty, num_students
    )