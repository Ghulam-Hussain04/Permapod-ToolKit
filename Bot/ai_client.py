import asyncio
import base64
import os
from io import BytesIO

from dotenv import load_dotenv
from openai import OpenAI

try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    Image = None
    UnidentifiedImageError = OSError

from prompts import SYSTEM_PROMPT

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_VISION_MODEL = os.environ.get("OPENAI_VISION_MODEL", OPENAI_MODEL)


def _client() -> OpenAI | None:
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


def _extract_response_text(response) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    parts = []
    for item in getattr(response, "output", []) or []:
        for block in getattr(item, "content", []) or []:
            text = getattr(block, "text", None)
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def _openai_error_message(error: Exception) -> str:
    text = str(error)
    lower = text.lower()

    if "incorrect api key" in lower or "invalid api key" in lower or "401" in lower:
        return "Invalid OpenAI API key. Check OPENAI_API_KEY in .env."
    if "rate limit" in lower or "429" in lower:
        return "OpenAI rate limit hit. Wait a moment and try again."
    if "model" in lower and ("not found" in lower or "does not exist" in lower or "404" in lower):
        return f"OpenAI model issue. Check that {OPENAI_MODEL} is available for your API key."
    return f"OpenAI error: {text}"


def _normalize_image_data_url(image_base64: str, image_mime: str) -> str | None:
    try:
        raw_bytes = base64.b64decode(image_base64)
        mime = image_mime or "image/jpeg"

        if Image is not None:
            with Image.open(BytesIO(raw_bytes)) as img:
                img.thumbnail((1568, 1568))
                if img.mode != "RGB":
                    img = img.convert("RGB")
                output = BytesIO()
                img.save(output, format="JPEG", quality=90, optimize=True)
                raw_bytes = output.getvalue()
                mime = "image/jpeg"

        encoded = base64.b64encode(raw_bytes).decode("utf-8")
        return f"data:{mime};base64,{encoded}"
    except (UnidentifiedImageError, OSError, ValueError):
        return None


async def generate_text(user_prompt: str) -> str:
    """Send a text prompt to OpenAI and return the response."""
    client = _client()
    if client is None:
        return "Missing OpenAI API key. Set OPENAI_API_KEY in .env."

    try:
        response = await asyncio.to_thread(
            client.responses.create,
            model=OPENAI_MODEL,
            input=[
                {
                    "role": "developer",
                    "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": user_prompt}],
                },
            ],
            max_output_tokens=700,
            temperature=0.9,
        )
        return _extract_response_text(response) or "Empty text response from OpenAI."
    except Exception as e:
        return _openai_error_message(e)


async def generate_vision(user_prompt: str, image_base64: str, image_mime: str) -> str:
    """Send an image plus prompt to OpenAI and return the response."""
    client = _client()
    if client is None:
        return "Missing OpenAI API key. Set OPENAI_API_KEY in .env."

    image_url = _normalize_image_data_url(image_base64, image_mime)
    if not image_url:
        return "Could not read the uploaded image. Send a normal PNG, JPG, or WebP file."

    try:
        response = await asyncio.to_thread(
            client.responses.create,
            model=OPENAI_VISION_MODEL,
            input=[
                {
                    "role": "developer",
                    "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user_prompt},
                        {"type": "input_image", "image_url": image_url, "detail": "auto"},
                    ],
                },
            ],
            max_output_tokens=700,
            temperature=0.9,
        )
        return _extract_response_text(response) or "Empty vision response from OpenAI."
    except Exception as e:
        return _openai_error_message(e)
