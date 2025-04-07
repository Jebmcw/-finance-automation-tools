# assistant/prompt_router.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_action_from_prompt(user_prompt):
    """Use GPT to classify the user's request as a known action label."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or "gpt-4"
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a classifier. Only respond with one of the following action labels:\n"
                    "- bank_vs_book\n"
                    "- gl_vs_ap\n"
                    "- unknown"
                )
            },
            {"role": "user", "content": user_prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip().lower()

if __name__ == "__main__":
    while True:
        prompt = input("Prompt: ")
        label = get_action_from_prompt(prompt)
        print(f"Action: {label}")
