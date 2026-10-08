import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

prompt_path = "prompts/thanvi/edtech_task5.txt"

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

answer = response.text

os.makedirs("outputs/thanvi/gemini", exist_ok=True)

output_path = "outputs/thanvi/gemini/edtech_task5.txt"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(answer)

print(answer)
print(f"\nSaved to: {output_path}")