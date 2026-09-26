from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.routes import health, cases, game, interrogation

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router, prefix="/api")
app.include_router(cases.router, prefix="/api")
app.include_router(game.router, prefix="/api")
app.include_router(interrogation.router, prefix="/api")

@app.get("/")
async def root():
    return {"name": settings.app_name, "status": "ok", "docs": "/docs"}
