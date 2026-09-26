from app.config.settings import settings

def ai_settings(role: str = "suspect"):
    cfg = settings.role_ai_config(role)
    return {
        "provider": cfg["provider"],
        "base_url": cfg["base_url"],
        "model": cfg["model"],
        "temperature": cfg["temperature"],
        "timeout": settings.ai_timeout_seconds,
    }
