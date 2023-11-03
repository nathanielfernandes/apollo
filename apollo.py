import openai
import random


fortune_words = []
with open("catalysts.txt", "r") as f:
    fortune_words = [w.rstrip("\n") for w in f.readlines()]


def get_lucky_numbers():
    return random.sample(range(1, 100), 6)


def get_catalyst():
    return random.choice(fortune_words)


async def generate_fortune():
    try:
        catalyst = get_catalyst()
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "I want you to answer as a fortune cookie. When I ask you a question I want you to respond in the form of fortune cookie wisdom. Answers should be short, cryptic and sound somewhat profound.",
                },
                {"role": "user", "content": catalyst},
            ],
        )

        return completion.choices[0].message["content"], catalyst
    except Exception as e:
        print("Error generating fortune: ", e)
        return "No fortune for you >:)"
