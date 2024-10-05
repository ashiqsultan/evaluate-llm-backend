from fastapi import FastAPI
from src.routers import evaluate
from src.routers import health

app = FastAPI(
    title="evaluate-llm-backend",
    description="description",
    summary="Docs Summary",
    version="1.0",
)

app.include_router(health.router)
app.include_router(evaluate.router)
