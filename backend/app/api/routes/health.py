from fastapi import APIRouter

from app.config.settings import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    suspect = settings.role_ai_config("suspect")
    judge = settings.role_ai_config("judge")
    return {
        "status": "ok",
        "ai": {
            "suspect": {
                "provider": suspect["provider"],
                "model": suspect["model"],
                "configured": bool(suspect["api_key"]),
            },
            "judge": {
                "provider": judge["provider"],
                "model": judge["model"],
                "configured": bool(judge["api_key"]),
            },
        },
    }
