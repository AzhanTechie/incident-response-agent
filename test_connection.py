import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

# Test Hindsight
hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)
hindsight.retain(bank_id="test-bank", content="This is a connection test.")
result = hindsight.recall(bank_id="test-bank", query="connection test")
print("HINDSIGHT OK:", result.results[0].text if result.results else "no results yet")

# Test Groq
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
response = groq.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Say hello in exactly 3 words."}],
)
print("GROQ OK:", response.choices[0].message.content) 