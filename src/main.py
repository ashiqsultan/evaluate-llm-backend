from fastapi import FastAPI
from src.schema import StrictCompareReq, StrictCompareRes

from src.utils.strict_compare import strict_compare as strict_compare_controller

app = FastAPI(
    title="evaluate-llm-backend",
    description="description",
    summary="Docs Summary",
    version="1.0",
)


@app.get("/ping")
def health_check():
    """
    Health check endpoint just for testing.
    """
    return {"message": "pong"}


@app.post("/strict-compare")
def strict_compare(request: StrictCompareReq) -> StrictCompareRes:
    return StrictCompareRes(
        result=strict_compare_controller(request.expected, request.actual)
    )
