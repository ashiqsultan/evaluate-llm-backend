from src.utils.openai.llm import main as llm
from src.schema import TestConditionRes
import json


def test_condition(answer: str, condition: str) -> TestConditionRes:
    """
    Test if the answer satisfies the condition
    """
    try:
        user_message = {"answer": answer, "condition": condition}
        strMsg = json.dumps(user_message)
        result = llm(strMsg)
        if "result" in result and "reason" in result:
            return TestConditionRes(result=result["result"], reason=result["reason"])
        else:
            raise Exception("Something went wront with llm validator")
    except Exception as e:
        raise e
