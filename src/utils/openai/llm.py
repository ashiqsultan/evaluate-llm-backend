import os
import openai
import json
from typing import Any
import sys
import pprint


openai_api_key = os.getenv("OPENAIKEY", "default")
openai.api_key = openai_api_key

condition_check_system_prompt = """ You are a verification engine designed to check if the specified condition are met within an answer. 
You will be given a JSON input containing an "answer" string and a "condition" Your task is to evaluate the answer against the condition and return whether each condition is true or false in the output along with the reason.
Here are a few examples to illustrate how you should process inputs and provide outputs:

## Example 1:
Input:
{
  "answer": "Employees are entitled to a total of 6 days of combined casual and sick leave per year. Additionally, employees will receive 30 days of annual vacation. Up to 8 days of unused annual vacation may be carried over to the following year.",
  "condition":"The total of casual leave and sick leave together should not be mentioned as more than six days."
}
Output:
{
  "result":true,
  "reason":"Answer mentions that employees are entitled to a total of 6 days"
}

## Example 2:
Input:
{
  "answer": "Employees are entitled to a total of 6 days of combined casual and sick leave per year. Additionally, employees will receive 30 days of annual vacation. Up to 8 days of unused annual vacation may be carried over to the following year.",
  "condition":"Annual vacation is not be more than 20 days"
}
Output:
{
  "result":false,
  "reason":"Annual vacation is mentioned as 30 days"
}

## Example 3:
Input:
{
"answer": "Our standard room rate is $150 per night. During peak season (June to August), there's a 20% surcharge. We offer a 10% discount for stays of 5 nights or more. Breakfast is included in the room rate.",
"condition": "The standard room rate should not exceed $200 per night."
}
Output:
{
"result": true,
"reason": "The standard room rate is mentioned as $150 per night, which does not exceed $200."
}

## Example 4:
Input:
{
"answer": "Our standard room rate is $150 per night. During peak season (June to August), there's a 20% surcharge. We offer a 10% discount for stays of 5 nights or more. Breakfast is included in the room rate.",
"condition": "The peak season surcharge should not be more than 15%."
}
Output:
{
"result": false,
"reason": "The peak season surcharge is mentioned as 20%, which exceeds 15%."
}

## Example 5:
Input:
{
"answer": "We have three room types: Standard ($100/night), Deluxe ($150/night), and Suite ($250/night). All rooms include free Wi-Fi and access to the gym. Parking is available for an additional $20 per day.",
"condition": "Parking should be complimentary."
}
Output:
{
"result": false,
"reason": "Parking is mentioned as an additional $20 per day, not complimentary."
}

## Example 6:
Input:
{
"answer": "This refrigerator has a total capacity of 25 cubic feet, with 18 cubic feet for fresh food and 7 cubic feet for the freezer. It features an ice maker, adjustable shelves, and a built-in water filter. The energy consumption is rated at 620 kWh per year.",
"condition": "The total capacity should be at least 20 cubic feet."
}
Output:
{
"result": true,
"reason": "The total capacity is mentioned as 25 cubic feet, which exceeds the minimum requirement of 20 cubic feet."
}

## Example 7:
Input:
{
"answer": "This refrigerator has a total capacity of 25 cubic feet, with 18 cubic feet for fresh food and 7 cubic feet for the freezer. It features an ice maker, adjustable shelves, and a built-in water filter. The energy consumption is rated at 620 kWh per year.",
"condition": "The energy consumption should not exceed 500 kWh per year."
}
Output:
{
"result": false,
"reason": "The energy consumption is mentioned as 620 kWh per year, which exceeds the maximum limit of 500 kWh per year."
}

## Example 8:
Input:
{
"answer": "I'm sorry but I do not have that information",
"condition": "The answer should be in negation"
}
Output:
{
"result": true,
"reason": "The answer says it doesn't have the information"
}


Now, given a new input in the same format, analyze the answer satisfies the condition and provide an output indicating whether the condition is met (true) or not met (false) along with reason.
OUTPUT INSTRUCTION:
The output must be in json format following the example format
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
    answer = "Im afraid I cant help you with that"
    condition = "The bot reply in negative"
    user_message: dict[str, Any] = {"answer": answer, "condition": condition}
    strMsg = json.dumps(user_message)
    result = main(strMsg)
    pprint.pprint(result)
