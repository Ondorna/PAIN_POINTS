import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() 

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

with open("prompts/thanvi/edtech_task5.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {
            "role": "user",
            "content": prompt
        },

    ],
    stream=False,
    # reasoning_effort="high",
    # extra_body={"thinking": {"type": "enabled"}}
)

answer = response.choices[0].message.content

os.makedirs("outputs/thanvi/deepseek", exist_ok=True)

output_path = f"outputs/thanvi/deepseek/edtech_task5.txt"

with open(output_path, "w", encoding="utf-8") as f:

    f.write(answer)

print(answer)

print(f"\nSaved to: {output_path}")