# ═══════════════════════════════════════════════
# groq_client.py — Groq API wrapper
# ═══════════════════════════════════════════════

import os
from groq import Groq
from prompts import SYSTEM_PROMPT
import os
import base64
from dotenv import load_dotenv

# Load .env before anything else
load_dotenv()

TEXT_MODEL   = "llama-3.3-70b-versatile"
# VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
VISION_MODEL = "llama-3.2-11b-vision-preview"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


async def generate_text(user_prompt: str) -> str:
    """Send a text prompt to Groq and return the response."""
    try:
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            max_tokens=350,
            temperature=0.9,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error = str(e)
        if "401" in error or "invalid_api_key" in error.lower():
            return "❌ Invalid Groq API key. Check your .env file."
        elif "429" in error or "rate_limit" in error.lower():
            return "⏳ Rate limit hit. Wait a moment and try again."
        elif "503" in error or "unavailable" in error.lower():
            return "🔄 Model busy. Wait 30 seconds and try again."
        else:
            return f"❌ Error: {error}"


async def generate_vision(user_prompt: str, image_base64: str, image_mime: str) -> str:
    """Send an image + prompt to Groq vision model."""
    try:
        response = client.chat.completions.create(
            model=VISION_MODEL,
            max_tokens=350,
            temperature=0.9,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{image_mime};base64,{image_base64}"
                            },
                        },
                        {"type": "text", "text": user_prompt},
                    ],
                },
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Vision error: {str(e)}"
