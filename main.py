from openai import AsyncOpenAI
import asyncio
import json

print("welcome to the quiz\n")

client = AsyncOpenAI(
    api_key="api_key",
    base_url="https://openrouter.ai/api/v1",
)


SYSTEM_PROMPT = """
You are a quiz question generator.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{
    "question": "What is the capital of Australia?",
    "options": {
        "A": "Sydney",
        "B": "Melbourne",
        "C": "Canberra",
        "D": "Brisbane"
    },
    "correct_answer": "C"
}

Rules:

1. Generate exactly one multiple-choice question.
2. Provide exactly four options.
3. Options must be A, B, C, and D.
4. correct_answer must be exactly A, B, C, or D.
5. Return only the JSON object.
6. Do not use Markdown.
7. Do not wrap the JSON in ```json.
"""


async def getQuestion():

    response = await client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Generate a new quiz question."},
        ],
    )

    if not response.choices:
        print("The model did not return any choices.")
        print(response)
        return None

    content = response.choices[0].message.content

    if not content:
        print("The model returned empty content.")
        print(response)
        return None

    return content


def checkAnswer(answer: str, option: str):
    if not answer:
        print("you havent entered your answerd")
        return
    print(option)
    print(answer)
    if option.lower() != answer.lower():
        print("you have entered the wrong answer")
        print(f"the correnct answer is {option}")
        return False
    else:
        return True


async def main():

    ready = input("are you ready: ")
    if ready.lower() != "yes":
        print("sure maybe next time")
        return

    print("\nHere we go!\n")
    while True:
        question = json.loads(await getQuestion())
        print(question["question"])
        for option, text in question["options"].items():
            print(f"{option}: {text}")
        answer = input("enter your answer ")

        result = checkAnswer(answer, question["correct_answer"])

        if not result:
            print("game over")
            break


if __name__ == "__main__":
    asyncio.run(main())
