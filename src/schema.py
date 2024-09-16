from pydantic import BaseModel


class StrictCompareReq(BaseModel):
    expected: str
    actual: str


class StrictCompareRes(BaseModel):
    result: bool


class ConditionVerifyReq(BaseModel):
    answer: str
    condition: str


class ConditionVerifyRes(BaseModel):
    result: bool
    reason: str
