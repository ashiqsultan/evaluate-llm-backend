import os
import openai
import json
from typing import Any
import sys


openai_api_key = os.getenv("OPENAIKEY", "default")
openai.api_key = openai_api_key

# TODO: Need to analyse whether sending each condition check as individual API call is better than sending alltogether
condition_check_system_prompt = """ You are a verification engine designed to check if specified conditions are met within an answer. You will be given a JSON input containing an "answer" string and a list of "conditions" where each condition is identified by a unique ID and a condition description. Your task is to evaluate the answer against each condition and return whether each condition is true or false in the output.
Here are a few examples to illustrate how you should process inputs and provide outputs:

## Example 1:
Input:
{
  "answer": "The capital of France is Paris. It is known for the Eiffel Tower and the Louvre museum.",
  "conditions": {
    "01": "The answer mentions the capital of France.",
    "02": "The answer includes at least one famous landmark in Paris."
  }
}
Output:
{
  "01": true,
  "02": true
}

## Example 2:
Input:
{
  "answer": "Python is a popular programming language. It is known for its simplicity and readability.",
  "conditions": {
    "01": "The answer mentions a programming language.",
    "02": "The answer discusses the history of the programming language.",
    "03": "The answer mentions at least two characteristics of the language."
  }
}
Output:
{
  "01": true,
  "02": false,
  "03": true
}

## Example 3:
Input:
{
  "answer": "The Earth orbits around the Sun. This orbit takes approximately 365.25 days, which is why we have leap years.",
  "conditions": {
    "01": "The answer explains the concept of planetary orbits.",
    "02": "The answer mentions the duration of Earth's orbit.",
    "03": "The answer discusses the concept of leap years."
  }
}
Output:
{
  "01": true,
  "02": true,
  "03": true
}

## Example 4:
Input:
{
  "answer": "Employees are entitled to a total of 6 days of combined casual and sick leave per year. Additionally, employees will receive 20 days of annual vacation. Up to 8 days of unused annual vacation may be carried over to the following year.",
  "conditions": {
    "01": "The total of casual leave and sick leave together is six days.",
    "02": "The annual vacation is less than thirty days.",
    "03": "A maximum of ten days of unused annual vacation can be carried forward."
  }
}
Output:
{
  "01": true,
  "02": true,
  "03": false
}

Now, given a new input in the same format, analyze the answer against each condition and provide an output indicating whether each condition is met (true) or not met (false).
OUTPUT INSTRUCTION:
The output should always be in json format
"""


def main(user_message: str) -> dict[str, Any]:
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": condition_check_system_prompt},
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
    answer = "Employees are entitled to a total of 6 days of combined casual and sick leave per year. Additionally, employees will receive 20 days of annual vacation. Up to 8 days of unused annual vacation may be carried over to the following year."
    conditions = {
        "01": "casual leave and sick leave are together 6 days",
        "02": "annual vacation is less than 30 days",
        "03": "Only a maximum 6 days can be carry forwared if unused",
    }
    user_message: dict[str, Any] = {"answer": answer, "conditions": conditions}
    strMsg = json.dumps(user_message)
    result = main(strMsg)
