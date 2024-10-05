from pydantic import BaseModel


class ReqStrictCompare(BaseModel):
    expected: str
    actual: str


class ResStrictCompare(BaseModel):
    result: bool


class ReqConditionEval(BaseModel):
    answer: str
    condition: str


class ResConditionEval(BaseModel):
    result: bool
    reason: str


class ReqSimilarity(BaseModel):
    expected: str
    actual: str


class ResSimilarity(BaseModel):
    score: float
