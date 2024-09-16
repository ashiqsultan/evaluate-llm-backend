from fastapi import FastAPI
from src.schema import (
    StrictCompareReq,
    StrictCompareRes,
    TestConditionReq,
    TestConditionRes,
)
from src.utils.strict_compare import strict_compare as strict_compare_controller
from src.utils.test_condition import test_condition as test_condition_controller

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


@app.post("/test/condition")
def test_condition(req_body: TestConditionReq) -> TestConditionRes:
    test_result = test_condition_controller(req_body.answer, req_body.condition)
    return test_result


@app.post("/strict-compare")
def strict_compare(request: StrictCompareReq) -> StrictCompareRes:
    return StrictCompareRes(
        result=strict_compare_controller(request.expected, request.actual)
    )
