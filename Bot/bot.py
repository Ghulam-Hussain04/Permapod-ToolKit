# ═══════════════════════════════════════════════
# bot.py — Permapod Telegram Bot entry point
# ═══════════════════════════════════════════════

import os
import logging
import asyncio
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from handlers import (
    start, menu,
    handle_callback,
    handle_message,
    handle_photo,
)

# ── Load env ─────────────────────────────────────
load_dotenv()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_KEY  = os.environ.get("GROQ_API_KEY")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in .env")
if not GROQ_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")

# ── Logging ──────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu",  menu))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Permapod bot is running...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    # Run forever until Ctrl+C
    await asyncio.Event().wait()

    await app.updater.stop()
    await app.stop()
    await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())