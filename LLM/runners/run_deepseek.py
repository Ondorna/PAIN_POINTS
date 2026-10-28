import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env") 

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

with open(BASE_DIR / "prompts/swapnil/prompt5/note_task1_cot.txt", "r", encoding="utf-8") as f:
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

os.makedirs(BASE_DIR / "outputs/swapnil/prompt5/deepseek", exist_ok=True)

output_path = BASE_DIR / "outputs/swapnil/prompt5/deepseek/note_task1_cot_3.txt"

with open(output_path, "w", encoding="utf-8") as f:

    f.write(answer)

print(answer)

print(f"\nSaved to: {output_path}")