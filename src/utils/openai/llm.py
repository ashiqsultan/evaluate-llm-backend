import os
import openai
import pprint
import json
from typing import Any
import sys


openai_api_key = os.getenv("OPENAIKEY", "default")
openai.api_key = openai_api_key


def main(user_message: str, context: str) -> dict[str, Any]:
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant responding to user messages using the context"
                        "Answer the user's question only using the provided context as knowledge. "
                        "If the question is outside the given context, apologize to the user for not having information about the question. "
                        f"Context: {context} "
                        "The output must be in JSON. "
                        'Output JSON Format: {"reply":""}'
                    ),
                },
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
    result = main("how old am i", "The user name is paul and he is 29 years old")
    pprint.pprint(result)
    print("END")
