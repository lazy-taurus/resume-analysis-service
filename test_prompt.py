import os
from google import genai
from dotenv import load_dotenv  # <--- You were missing this
from pathlib import Path

# 1. Force load the .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# 2. Get Key
api_key = os.getenv("GEMINI_API_KEY")
has_key = bool(api_key)

print(f"DEBUG: Reading .env from: {env_path}")
print(f"DEBUG: Key found? {has_key}")

if has_key:
    # Print the start of the key to verify it matches your NEW one
    print(f"DEBUG: Key starts with: {api_key[:10]}...") 
else:
    print("❌ ERROR: No key found.")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)

try:
    print("Attempting to call Gemini...")
    # Switched to 1.5-flash as it is the most stable for testing keys
    resp = client.models.generate_content(model="gemini-2.5-flash", contents="Explain how eggs works in a few words")
    print("\n✅ SUCCESS!")
    print("Response:", resp.text)
except Exception as e:
    print("\n❌ FAILURE:")
    print(e)