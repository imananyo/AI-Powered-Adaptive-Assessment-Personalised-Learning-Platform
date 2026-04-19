from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger

from app.api import (
    routes_health,
    routes_auth,
    routes_teacher,
    routes_assessment,
    routes_grading,
    routes_personalization,
)


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description="AI-powered academic assessment platform with JWT auth, Celery, OpenAI & PostgreSQL",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(routes_health.router, tags=["Health"])
    app.include_router(routes_auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(routes_teacher.router, prefix="/teacher", tags=["Teacher"])
    app.include_router(routes_assessment.router, prefix="/assessment", tags=["Assessment"])
    app.include_router(routes_grading.router, prefix="/grading", tags=["Grading"])
    app.include_router(routes_personalization.router, prefix="/personalization", tags=["Personalization"])

    @app.on_event("startup")
    async def on_startup():
        logger.info(f"🚀 {settings.APP_NAME} started in {settings.ENV} mode")

    return app


app = create_application()