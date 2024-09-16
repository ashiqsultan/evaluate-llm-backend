from fastapi import FastAPI
from src.schema import (
    StrictCompareReq,
    StrictCompareRes,
    ConditionVerifyReq,
    ConditionVerifyRes,
)

from service.strict_compare import strict_compare as strict_compare_controller
from service.conditional_verify.main import main as condition_verify_controller

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


@app.post("/verify/conditional")
def verify_condition(req_body: ConditionVerifyReq) -> ConditionVerifyRes:
    """
    Verifies whether an answer satisfies a given condition
    """
    test_result = condition_verify_controller(req_body.answer, req_body.condition)
    return test_result


@app.post("/verify/strict-compare")
def strict_compare(request: StrictCompareReq) -> StrictCompareRes:
    return StrictCompareRes(
        result=strict_compare_controller(request.expected, request.actual)
    )
