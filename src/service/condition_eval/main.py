from .llm import llm
from src.schema import ResConditionEval
import json


def main(answer: str, condition: str) -> ResConditionEval:
    """
    Verifies whether the answer satisfies the given condition using llm
    """
    try:
        user_message = {"answer": answer, "condition": condition}
        strMsg = json.dumps(user_message)
        result = llm(strMsg)
        if "result" in result and "reason" in result:
            return ResConditionEval(result=result["result"], reason=result["reason"])
        else:
            raise Exception("Something went wront with llm validator")
    except Exception as e:
        raise e
