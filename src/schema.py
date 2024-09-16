from pydantic import BaseModel


class StrictCompareReq(BaseModel):
    expected: str
    actual: str


class StrictCompareRes(BaseModel):
    result: bool


class TestConditionReq(BaseModel):
    answer: str
    condition: str


class TestConditionRes(BaseModel):
    result: bool
    reason: str
