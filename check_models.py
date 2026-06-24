"""
check_models.py
Run this once to find out EXACTLY which Gemini models your API key can
use right now. Don't guess model names -- ask the API directly.

Uses ONLY the current `google-genai` package (the `from google import genai`
import). If you see an import error here, you still have the old
`google-generativeai` package interfering -- run:
    pip uninstall google-generativeai -y
"""
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found -- check your .env file.")

client = genai.Client(api_key=API_KEY)

print("Models your key can use for generate_content:\n")

try:
    for model in client.models.list():
        actions = getattr(model, "supported_actions", None)
        # Different SDK versions expose this slightly differently;
        # print everything so we can see the real shape of the data.
        print(f"- {model.name}  (supported_actions={actions})")
except Exception as e:
    print(f"Error listing models: {e}")