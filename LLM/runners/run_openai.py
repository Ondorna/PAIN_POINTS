import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt_path = BASE_DIR / "prompts/swapnil/prompt5/note_task1_cot.txt"

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()

response = client.responses.create(
    model="gpt-6-luna",
    input=prompt,
    reasoning={"effort": "none"}
)

answer = response.output_text

os.makedirs(BASE_DIR / "outputs/swapnil/prompt5/openai", exist_ok=True)

output_path = BASE_DIR / "outputs/swapnil/prompt5/openai/note_task1_cot_3.txt"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(answer)

print(answer)
print(f"\nSaved to: {output_path}")