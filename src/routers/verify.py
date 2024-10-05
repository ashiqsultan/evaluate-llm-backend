from fastapi import APIRouter
from src.schema import (
    ConditionVerifyReq,
    StrictCompareReq,
    ConditionVerifyRes,
    StrictCompareRes,
)
from src.service.strict_compare import strict_compare as strict_compare_service
from src.service.conditional_verify import main as condition_verify_service

router = APIRouter()


@router.post("/verify/conditional")
def verify_condition(req_body: ConditionVerifyReq) -> ConditionVerifyRes:
    """
    Verifies whether an answer satisfies a given condition.
    """
    test_result = condition_verify_service(req_body.answer, req_body.condition)
    return test_result


@router.post("/verify/strict-compare")
def strict_compare(request: StrictCompareReq) -> StrictCompareRes:
    return StrictCompareRes(
        result=strict_compare_service(request.expected, request.actual)
    )
