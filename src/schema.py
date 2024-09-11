from pydantic import BaseModel


class StrictCompareReq(BaseModel):
    expected: str
    actual: str


class StrictCompareRes(BaseModel):
    result: bool
