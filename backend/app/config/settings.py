from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Detective Game"
    debug: bool = True
    cors_origins: str = "http://localhost:5173"

    suspect_ai_provider: str = "openrouter"
    suspect_ai_api_key: str = ""
    suspect_ai_base_url: str = "https://openrouter.ai/api/v1"
    suspect_ai_model: str = "minimax/minimax-m3:free"
    suspect_ai_fallback_models: str = "thinkingmachines/inkling:free,google/gemma-4-31b-it:free"
    suspect_ai_temperature: float = 0.75

    judge_ai_provider: str = "openrouter"
    judge_ai_api_key: str = ""
    judge_ai_base_url: str = "https://openrouter.ai/api/v1"
    judge_ai_model: str = "z-ai/glm-5.2:free"
    judge_ai_fallback_models: str = "nvidia/nemotron-3-ultra-550b-a55b:free,google/gemma-4-31b-it:free"
    judge_ai_temperature: float = 0.15

    ai_timeout_seconds: float = 35.0
    ai_retry_count: int = 1
    ai_retry_delay_seconds: float = 1.5
    max_questions: int = 10
    starting_confidence: int = 100
    starting_confession_progress: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

    @staticmethod
    def _csv(value: str) -> list[str]:
        return [item.strip() for item in value.split(",") if item.strip()]

    def role_ai_config(self, role: str) -> dict:
        prefix = role.lower().strip()
        if prefix == "suspect":
            return {
                "provider": self.suspect_ai_provider,
                "api_key": self.suspect_ai_api_key,
                "base_url": self.suspect_ai_base_url,
                "model": self.suspect_ai_model,
                "fallback_models": self._csv(self.suspect_ai_fallback_models),
                "temperature": self.suspect_ai_temperature,
            }
        if prefix == "judge":
            return {
                "provider": self.judge_ai_provider,
                "api_key": self.judge_ai_api_key,
                "base_url": self.judge_ai_base_url,
                "model": self.judge_ai_model,
                "fallback_models": self._csv(self.judge_ai_fallback_models),
                "temperature": self.judge_ai_temperature,
            }
        raise ValueError(f"Unknown AI role: {role}")


settings = Settings()
