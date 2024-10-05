from fastapi import APIRouter
from src.schema import (
    ReqConditionEval,
    ReqStrictCompare,
    ResConditionEval,
    ResStrictCompare,
)
from src.service.strict_compare import strict_compare as strict_compare_service
from src.service.condition_eval import main as condition_eval_service

router = APIRouter()


@router.post("/evaluate/condition")
def condition_evaluation(req_body: ReqConditionEval) -> ResConditionEval:
    """
    Verifies whether an answer satisfies a given condition.
    """
    test_result = condition_eval_service(req_body.answer, req_body.condition)
    return test_result


@router.post("/evaluate/strict-compare")
def strict_compare(request: ReqStrictCompare) -> ResStrictCompare:
    """
    Strict Compare two strings and return true or false
    """
    return ResStrictCompare(
        result=strict_compare_service(request.expected, request.actual)
    )
