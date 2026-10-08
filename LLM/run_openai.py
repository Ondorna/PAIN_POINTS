import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt_path = "prompts/thanvi/edtech_task5.txt"

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()

response = client.responses.create(
    model="gpt-6-luna",
    input=prompt,
    reasoning={"effort": "none"}
)

answer = response.output_text

os.makedirs("outputs/thanvi/openai", exist_ok=True)

output_path = "outputs/thanvi/openai/edtech_task5.txt"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(answer)

print(answer)
print(f"\nSaved to: {output_path}")