import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

prompt_path = BASE_DIR / "prompts/swapnil/prompt4/note_task1.txt"

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

answer = response.text

os.makedirs(BASE_DIR / "outputs/swapnil/prompt4/gemini", exist_ok=True)

output_path = BASE_DIR / "outputs/swapnil/prompt4/gemini/note_task1_3.txt"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(answer)

print(answer)
print(f"\nSaved to: {output_path}")