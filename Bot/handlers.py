# ═══════════════════════════════════════════════
# handlers.py — All flow and callback handlers
# ═══════════════════════════════════════════════

import base64
import aiohttp

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import session
import keyboards as kb
from prompts import (
    build_post_prompt, build_reply_prompt,
    build_repost_prompt, build_trend_prompt,
    WEEKLY_CADENCE,
)
from ai_client import generate_text, generate_vision

BRAND_RULES = """🛡️ *Brand Rules — Permapod*

✅ *Always say:*
• Onchain lending
• Credit infrastructure
• Stablecoin utility
• Lending demand
• Productive capital
• ZIGChain ecosystem
• Capital efficiency

❌ *Never say:*
• Guaranteed yield
• Risk-free returns
• Fixed APY (unconfirmed)
• RWA / tokenized equities
• No loss possible
• Collateralized markets as live
• Unconfirmed roadmap as live

🪝 *Strong hooks:*
• Idle capital is a missed opportunity.
• The APY matters. The source matters more.
• Capital should work, not wait.
• Stablecoins deserve better utility.
• Lending infrastructure matters.

💬 *Strong closers:*
• That is the market Permapod is building.
• Capital should be productive.
• Onchain lending is only getting started.
• Permapod is building that layer on ZIGChain.

⚠️ *Risk language:*
• Never say fixed APY → say "APY may change"
• Never say no risk → say "lending carries risk"
• Always refer to docs for live data: permapod.gitbook.io/home"""

HOOK_MAP = {
    "hook_ai": "ai",
    "hook_1":  "Idle capital is a missed opportunity.",
    "hook_2":  "Stablecoins deserve better utility.",
    "hook_3":  "The APY matters. The source matters more.",
    "hook_4":  "Productive capital builds stronger markets.",
    "hook_5":  "Capital should work, not wait.",
    "hook_6":  "Lending infrastructure matters.",
}

CLOSING_MAP = {
    "closing_ai": "ai",
    "closing_1":  "That is the market Permapod is building.",
    "closing_2":  "Capital should be productive.",
    "closing_3":  "Onchain lending is only getting started.",
    "closing_4":  "Stablecoins deserve better markets.",
    "closing_5":  "Permapod is building that layer on ZIGChain.",
}

# ── HELPERS ──────────────────────────────────────

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Main menu", callback_data="back_menu")]
    ])

async def send_main_menu(update: Update, text="What would you like to create?"):
    content = f"🏠 *Permapod Content Manager*\n\n{text}"
    if update.callback_query:
        await update.callback_query.edit_message_text(
            content, reply_markup=kb.main_menu(), parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await update.message.reply_text(
            content, reply_markup=kb.main_menu(), parse_mode=ParseMode.MARKDOWN,
        )

def _format_result(result: str, flow: str) -> tuple[str, object]:
    char_count = len(result)
    warn = " ⚠️ over 280 chars" if char_count > 280 else ""
    text = f"✨ *Generated:*\n\n{result}\n\n_{char_count}/280 chars{warn}_"
    return text, kb.after_gen_keyboard(flow)

# ── START / MENU ──────────────────────────────────

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    session.reset(update.effective_user.id)
    await send_main_menu(update, "Welcome to the Permapod X Content Manager.\nChoose what you want to create:")

async def menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    session.reset(update.effective_user.id)
    await send_main_menu(update)

# ── CALLBACK ROUTER ───────────────────────────────

async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid  = update.effective_user.id
    s    = session.get(uid)

    # ── Main flows ──
    if data == "flow_post":
        session.set_flow(uid, "post", "voice")
        await query.edit_message_text(
            "✏️ *New Post — Step 1/5*\n\nChoose brand voice:",
            reply_markup=kb.voice_keyboard("post_"), parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "flow_reply":
        session.set_flow(uid, "reply", "bucket")
        await query.edit_message_text(
            "💬 *Reply — Step 1/4*\n\nWhich type of post are you replying under?",
            reply_markup=kb.bucket_keyboard(), parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "flow_repost":
        session.set_flow(uid, "repost", "voice")
        await query.edit_message_text(
            "🔁 *Repost + Comment — Step 1/4*\n\nChoose brand voice:",
            reply_markup=kb.voice_keyboard("repost_"), parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "flow_trend":
        session.set_flow(uid, "trend", "mode")
        await query.edit_message_text(
            "🔥 *Trend / Image — Step 1/5*\n\nChoose input mode:",
            reply_markup=kb.trend_mode_keyboard(), parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "flow_rules":
        await query.edit_message_text(
            BRAND_RULES, reply_markup=back_keyboard(), parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "flow_cadence":
        await query.edit_message_text(
            "📅 *Weekly Content Cadence*\n\nPick a day to auto-set voice and pillar:",
            reply_markup=kb.cadence_keyboard(), parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "back_menu":
        session.reset(uid)
        await send_main_menu(update)

    # ── POST flow ──
    elif data.startswith("post_voice_"):
        v = data.replace("post_voice_", "")
        session.update(uid, voice=v, flow="post", step="pillar")
        await query.edit_message_text(
            "✏️ *New Post — Step 2/5*\n\nChoose content pillar:",
            reply_markup=kb.pillar_keyboard("post_"), parse_mode=ParseMode.MARKDOWN,
        )

    elif data.startswith("post_pillar_"):
        p = data.replace("post_pillar_", "")
        session.update(uid, pillar=p, step="hook")
        await query.edit_message_text(
            "✏️ *New Post — Step 3/5*\n\nChoose opening hook:",
            reply_markup=kb.hook_keyboard(), parse_mode=ParseMode.MARKDOWN,
        )

    elif data.startswith("hook_"):
        session.update(uid, hook=HOOK_MAP.get(data, "ai"), step="closing")
        await query.edit_message_text(
            "✏️ *New Post — Step 4/5*\n\nChoose closing line:",
            reply_markup=kb.closing_keyboard(), parse_mode=ParseMode.MARKDOWN,
        )

    elif data.startswith("closing_"):
        session.update(uid, closing=CLOSING_MAP.get(data, "ai"), step="context")
        await query.edit_message_text(
            "✏️ *New Post — Step 5/5*\n\nAny additional context? (optional)\n\nType it or skip:",
            reply_markup=kb.skip_keyboard("skip_post_context"), parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "skip_post_context":
        session.update(uid, context="")
        await query.edit_message_text("⏳ Generating your post...")
        result = await generate_text(
            build_post_prompt(s["voice"], s["pillar"], "", s["hook"], s["closing"])
        )
        session.update(uid, step="done")
        txt, markup = _format_result(result, "post")
        await query.edit_message_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

    # ── REPLY flow ──
    elif data.startswith("bucket_"):
        b = data.replace("bucket_", "")
        session.update(uid, bucket=b, step="voice")
        await query.edit_message_text(
            "💬 *Reply — Step 2/4*\n\nChoose brand voice:",
            reply_markup=kb.voice_keyboard("reply_"), parse_mode=ParseMode.MARKDOWN,
        )

    elif data.startswith("reply_voice_"):
        v = data.replace("reply_voice_", "")
        session.update(uid, voice=v, step="tweet")
        await query.edit_message_text(
            "💬 *Reply — Step 3/4*\n\nPaste the tweet you're replying to:\n_(or type 'skip')_",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "skip_context":
        session.update(uid, context="")
        flow = s.get("flow")
        if flow == "reply":
            await query.edit_message_text("⏳ Generating reply...")
            result = await generate_text(
                build_reply_prompt(s["voice"], s["bucket"], s["tweet"], "")
            )
        elif flow == "repost":
            await query.edit_message_text("⏳ Generating repost comment...")
            result = await generate_text(
                build_repost_prompt(s["voice"], s["pillar"], s["tweet"], "")
            )
        elif flow == "trend":
            await query.edit_message_text("⏳ Generating from trend...")
            result = await generate_text(
                build_trend_prompt(s["voice"], s["pillar"], s["trend"], s["output_type"], "")
            )
        else:
            result = "Unknown flow."
        session.update(uid, step="done")
        txt, markup = _format_result(result, flow)
        await query.edit_message_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

    # ── REPOST flow ──
    elif data.startswith("repost_voice_"):
        v = data.replace("repost_voice_", "")
        session.update(uid, voice=v, step="pillar")
        await query.edit_message_text(
            "🔁 *Repost + Comment — Step 2/4*\n\nChoose content angle:",
            reply_markup=kb.pillar_keyboard("repost_"), parse_mode=ParseMode.MARKDOWN,
        )

    elif data.startswith("repost_pillar_"):
        p = data.replace("repost_pillar_", "")
        session.update(uid, pillar=p, step="tweet")
        await query.edit_message_text(
            "🔁 *Repost + Comment — Step 3/4*\n\nPaste the tweet you want to repost:\n_(or type 'skip')_",
            parse_mode=ParseMode.MARKDOWN,
        )

    # ── TREND flow ──
    elif data == "timode_trend":
        session.update(uid, step="output_type")
        await query.edit_message_text(
            "🔥 *Trend — Step 2/5*\n\nWhat type of content to generate?",
            reply_markup=kb.output_type_keyboard(), parse_mode=ParseMode.MARKDOWN,
        )

    elif data == "timode_image":
        session.update(uid, step="image_output_type")
        await query.edit_message_text(
            "🖼️ *Image — Step 2/5*\n\nWhat type of content to generate?",
            reply_markup=kb.output_type_keyboard(), parse_mode=ParseMode.MARKDOWN,
        )

    elif data.startswith("outtype_"):
        ot = data.replace("outtype_", "")
        session.update(uid, output_type=ot)
        step = s.get("step", "")
        if "image" in step:
            session.update(uid, step="voice_image")
            await query.edit_message_text(
                "🖼️ *Image — Step 3/5*\n\nChoose brand voice:",
                reply_markup=kb.voice_keyboard("trend_"), parse_mode=ParseMode.MARKDOWN,
            )
        else:
            session.update(uid, step="voice_trend")
            await query.edit_message_text(
                "🔥 *Trend — Step 3/5*\n\nChoose brand voice:",
                reply_markup=kb.voice_keyboard("trend_"), parse_mode=ParseMode.MARKDOWN,
            )

    elif data.startswith("trend_voice_"):
        v = data.replace("trend_voice_", "")
        session.update(uid, voice=v)
        step = s.get("step", "")
        session.update(uid, step="pillar_image" if "image" in step else "pillar_trend")
        await query.edit_message_text(
            "🔥 *Trend — Step 4/5*\n\nChoose content angle:",
            reply_markup=kb.pillar_keyboard("trend_"), parse_mode=ParseMode.MARKDOWN,
        )

    elif data.startswith("trend_pillar_"):
        p = data.replace("trend_pillar_", "")
        session.update(uid, pillar=p)
        step = s.get("step", "")
        if "image" in step:
            session.update(uid, step="awaiting_image")
            await query.edit_message_text(
                "🖼️ *Image — Step 5/5*\n\nSend me the screenshot now:\n_(send as photo or file)_",
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            session.update(uid, step="trend_input")
            await query.edit_message_text(
                "🔥 *Trend — Step 5/5*\n\nPaste the trending topic or tweet:",
                parse_mode=ParseMode.MARKDOWN,
            )

    # ── IMAGE context skip ──
    elif data == "skip_image_context":
        session.update(uid, context="")
        await query.edit_message_text("⏳ Generating from image...")
        s = session.get(uid)
        result = await generate_vision(
            build_trend_prompt(s["voice"], s["pillar"], "", s["output_type"], ""),
            s["image_b64"], s["image_mime"]
        )
        session.update(uid, step="done")
        txt, markup = _format_result(result, "trend")
        await query.edit_message_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

    # ── CADENCE ──
    elif data.startswith("cadence_"):
        day = data.replace("cadence_", "")
        if day in WEEKLY_CADENCE:
            label, voice, pillar = WEEKLY_CADENCE[day]
            session.update(uid, voice=voice, pillar=pillar, flow="post", step="hook")
            await query.edit_message_text(
                f"📅 *{label}* — voice and pillar set!\n\nNow choose opening hook:",
                reply_markup=kb.hook_keyboard(), parse_mode=ParseMode.MARKDOWN,
            )

    # ── REGENERATE ──
    elif data.startswith("regen_"):
        flow = data.replace("regen_", "")
        s = session.get(uid)
        await query.edit_message_text("⏳ Regenerating...")
        if flow == "post":
            result = await generate_text(build_post_prompt(s["voice"], s["pillar"], s["context"], s["hook"], s["closing"]))
        elif flow == "reply":
            result = await generate_text(build_reply_prompt(s["voice"], s["bucket"], s["tweet"], s["context"]))
        elif flow == "repost":
            result = await generate_text(build_repost_prompt(s["voice"], s["pillar"], s["tweet"], s["context"]))
        elif flow == "trend":
            if s.get("image_b64"):
                result = await generate_vision(
                    build_trend_prompt(s["voice"], s["pillar"], "", s["output_type"], s["context"]),
                    s["image_b64"], s["image_mime"]
                )
            else:
                result = await generate_text(build_trend_prompt(s["voice"], s["pillar"], s["trend"], s["output_type"], s["context"]))
        else:
            result = "Unknown flow."
        txt, markup = _format_result(result, flow)
        await query.edit_message_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)


# ── MESSAGE HANDLER ───────────────────────────────

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    s    = session.get(uid)
    text = update.message.text.strip()
    step = s.get("step")
    flow = s.get("flow")

    # Post context
    if flow == "post" and step == "context":
        session.update(uid, context="" if text.lower() == "skip" else text)
        msg = await update.message.reply_text("⏳ Generating your post...")
        s = session.get(uid)
        result = await generate_text(build_post_prompt(s["voice"], s["pillar"], s["context"], s["hook"], s["closing"]))
        session.update(uid, step="done")
        txt, markup = _format_result(result, "post")
        await msg.edit_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        return

    # Reply — tweet input
    if flow == "reply" and step == "tweet":
        session.update(uid, tweet="" if text.lower() == "skip" else text, step="context")
        await update.message.reply_text(
            "💬 *Reply — Step 4/4*\n\nAny additional context? (optional)\n\nType it or skip:",
            reply_markup=kb.skip_keyboard("skip_context"), parse_mode=ParseMode.MARKDOWN,
        )
        return

    # Reply — context input
    if flow == "reply" and step == "context":
        session.update(uid, context="" if text.lower() == "skip" else text)
        msg = await update.message.reply_text("⏳ Generating reply...")
        s = session.get(uid)
        result = await generate_text(build_reply_prompt(s["voice"], s["bucket"], s["tweet"], s["context"]))
        session.update(uid, step="done")
        txt, markup = _format_result(result, "reply")
        await msg.edit_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        return

    # Repost — tweet input
    if flow == "repost" and step == "tweet":
        session.update(uid, tweet="" if text.lower() == "skip" else text, step="context")
        await update.message.reply_text(
            "🔁 *Repost — Step 4/4*\n\nYour specific take? (optional)\n\nType it or skip:",
            reply_markup=kb.skip_keyboard("skip_context"), parse_mode=ParseMode.MARKDOWN,
        )
        return

    # Repost — context input
    if flow == "repost" and step == "context":
        session.update(uid, context="" if text.lower() == "skip" else text)
        msg = await update.message.reply_text("⏳ Generating repost comment...")
        s = session.get(uid)
        result = await generate_text(build_repost_prompt(s["voice"], s["pillar"], s["tweet"], s["context"]))
        session.update(uid, step="done")
        txt, markup = _format_result(result, "repost")
        await msg.edit_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        return

    # Image — context input after image received
    if flow == "trend" and step == "context_image":
        session.update(uid, context="" if text.lower() == "skip" else text)
        msg = await update.message.reply_text("⏳ Generating from image...")
        s = session.get(uid)
        result = await generate_vision(
            build_trend_prompt(s["voice"], s["pillar"], "", s["output_type"], s["context"]),
            s["image_b64"], s["image_mime"]
        )
        session.update(uid, step="done")
        txt, markup = _format_result(result, "trend")
        await msg.edit_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        return

    # Trend — trend text input
    if flow == "trend" and step == "trend_input":
        session.update(uid, trend=text, step="context")
        await update.message.reply_text(
            "🔥 Any extra context? (optional)\n\nType it or skip:",
            reply_markup=kb.skip_keyboard("skip_context"), parse_mode=ParseMode.MARKDOWN,
        )
        return

    # Trend — context input
    if flow == "trend" and step == "context":
        session.update(uid, context="" if text.lower() == "skip" else text)
        msg = await update.message.reply_text("⏳ Generating from trend...")
        s = session.get(uid)
        result = await generate_text(build_trend_prompt(s["voice"], s["pillar"], s["trend"], s["output_type"], s["context"]))
        session.update(uid, step="done")
        txt, markup = _format_result(result, "trend")
        await msg.edit_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        return

    # Default
    await update.message.reply_text(
        "Use /menu to start.", reply_markup=kb.main_menu(),
    )


# ── PHOTO / DOCUMENT HANDLER ──────────────────────

async def handle_photo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    s   = session.get(uid)

    print(f"DEBUG handle_photo called — step: {s.get('step')} flow: {s.get('flow')}")
    print(f"DEBUG has photo: {bool(update.message.photo)}")
    print(f"DEBUG has document: {bool(update.message.document)}")

    if s.get("step") != "awaiting_image":
        await update.message.reply_text("Please start a Trend/Image flow first. Use /menu.")
        return

    # Handle both photo and pasted document
    if update.message.photo:
        tg_file  = await ctx.bot.get_file(update.message.photo[-1].file_id)
        img_mime = "image/jpeg"
    elif update.message.document:
        tg_file  = await ctx.bot.get_file(update.message.document.file_id)
        img_mime = update.message.document.mime_type or "image/jpeg"
    else:
        await update.message.reply_text("Please send an image.")
        return

    # SSL disabled to handle VPN certificate interception
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as http:
        async with http.get(tg_file.file_path) as resp:
            img_bytes = await resp.read()

    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    session.update(uid, image_b64=img_b64, image_mime=img_mime, step="context_image")

    await update.message.reply_text(
        "🖼️ Image received!\n\nAny extra context? (optional)\n\nType it or skip:",
        reply_markup=kb.skip_keyboard("skip_image_context"),
        parse_mode=ParseMode.MARKDOWN,
    )
