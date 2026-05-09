import os
from dotenv import load_dotenv
load_dotenv()

from google import genai

key = os.getenv("GEMINI_API_KEY")
print(f"Key present: {bool(key)}")
print(f"Key prefix: {key[:8] if key else 'MISSING'}")

client = genai.Client(api_key=key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents='Say hello in JSON: {"msg": "hello"}'
)
print(f"Response: {response.text}")
