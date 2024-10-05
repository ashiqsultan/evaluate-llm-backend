from pydantic import BaseModel


class StrictCompareReq(BaseModel):
    expected: str
    actual: str


class StrictCompareRes(BaseModel):
    result: bool


class ReqConditionEval(BaseModel):
    answer: str
    condition: str


class ResConditionEval(BaseModel):
    result: bool
    reason: str
