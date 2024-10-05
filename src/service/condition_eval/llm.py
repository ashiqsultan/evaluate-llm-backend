import os
import openai
import json
from typing import Any
import sys
import pprint
from .system_prompt import system_prompt

openai_api_key = os.getenv("OPENAIKEY", "default")
openai.api_key = openai_api_key


def llm(user_message: str) -> dict[str, Any]:
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        response_content = response.choices[0].message.content
        if isinstance(response_content, str):
            try:
                output_json = json.loads(response_content)
                return output_json
            except json.JSONDecodeError:
                raise Exception(
                    "response message content from llm is a string but not valid JSON"
                )
        raise ValueError("response message content from llm is not a string")
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": "Error with OpenAI LLM API"}


if __name__ == "__main__":
    print("START")
    answer = "Im afraid I cant help you with that"
    condition = "The bot reply in negative"
    user_message: dict[str, Any] = {"answer": answer, "condition": condition}
    strMsg = json.dumps(user_message)
    result = llm(strMsg)
    pprint.pprint(result)
