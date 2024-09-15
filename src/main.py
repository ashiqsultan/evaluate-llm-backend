from fastapi import FastAPI
from src.schema import StrictCompareReq, StrictCompareRes
from src.utils.strict_compare import strict_compare as strict_compare_controller
import src.utils.openai.llm as llm

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


@app.get("/test-llm")
def testllm():
    test_result = llm.main(
        "What is my name", "The user name is paul and he is 29 years old"
    )
    return test_result


@app.post("/strict-compare")
def strict_compare(request: StrictCompareReq) -> StrictCompareRes:
    return StrictCompareRes(
        result=strict_compare_controller(request.expected, request.actual)
    )
