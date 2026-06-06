import os
from pathlib import Path

from aiohttp import web
from dotenv import load_dotenv

from ai_client import generate_text, generate_vision

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT_DIR / "Frontend"


async def health(_request):
    return web.json_response({"ok": True})


async def generate(request):
    try:
        payload = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid JSON body."}, status=400)

    prompt = (payload.get("prompt") or "").strip()
    image_base64 = payload.get("imageBase64")
    image_mime = payload.get("imageMime")

    if not prompt:
        return web.json_response({"error": "Missing prompt."}, status=400)

    if image_base64:
        text = await generate_vision(prompt, image_base64, image_mime or "")
    else:
        text = await generate_text(prompt)

    return web.json_response({"text": text})


async def index(_request):
    return web.FileResponse(FRONTEND_DIR / "index.html")


def create_app():
    app = web.Application(client_max_size=12 * 1024**2)
    app.router.add_get("/api/health", health)
    app.router.add_post("/api/generate", generate)
    app.router.add_static("/src", FRONTEND_DIR / "src", name="src")
    app.router.add_get("/", index)
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"Starting Permapod frontend bot at http://127.0.0.1:{port}")
    web.run_app(create_app(), host="127.0.0.1", port=port)
