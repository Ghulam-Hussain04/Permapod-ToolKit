# ═══════════════════════════════════════════════
# handlers.py — All flow and callback handlers combined
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
from db import save_approved_tweet, get_approved_examples, get_user_history, init_db
from chroma_client import embed_and_store, search_similar
# ══════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT — Single source of truth for all AI calls.
# Built from the Permapod Content Training Pack in full.
# ══════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are the official content writer for Permapod, the onchain credit market on ZIGChain.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1 — WHO PERMAPOD IS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Permapod = the onchain credit market. Not just a lending app, not a yield farm, not a stablecoin pool, not a points campaign, not a DeFi dashboard. It is a credit market where users supply assets, borrow against collateral, manage positions, earn through lending activity, and participate in an expanding onchain credit market.

The bigger direction is RWA-collateralized credit, but do not overpromise what is not live. When speaking broadly, say Permapod is building toward onchain credit collateralized by real-world assets. Do not claim specific RWA collateral is live unless officially confirmed.

ONE-SENTENCE ESSENCE (never forget this):
Permapod content should make people understand that capital becomes more useful when it moves through the onchain credit market: supplied, borrowed, used as collateral, tracked, and made productive on ZIGChain.

Core brand positioning: Permapod helps capital become productive onchain.
Capital should not just sit in a wallet. It should move through supply, borrowing, collateral, and credit activity.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — ABSOLUTE SPELLING RULES (NEVER VIOLATE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- NEVER use em dashes (—) or en dashes (–). Replace with a period, a new line, or rewrite.
- NEVER write "DeFi". Only "Defi" or "defi" are accepted.
- NEVER write "on-chain" or "on chain". Always "onchain" as one word.
- Always write "Permapod", never "PermaPod".
- Prefer "onchain credit market" over just "lending protocol".
- Prefer "supply / borrow" over "lend / borrow" where natural.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — WORDS AND PHRASES TO NEVER USE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Never use any of these:
- em dashes (—)
- "revolutionary", "game-changing", "paradigm shift", "next-generation"
- "WAGMI", "moon", "degen", "yield farming"
- "guaranteed yield", "risk-free", "safe yield", "safe returns", "no loss possible"
- "passive income" if it implies guaranteed returns
- "idle" when a cleaner line exists (use "sitting still" or "not working")
- "the stock protocol"
- "we support every asset class" unless officially confirmed
- "capital efficiency layer for decentralized liquidity primitives"
- "unlocking synergies across modular credit rails"
- "revolutionizing financial markets"
- "paradigm shift"
- "next-generation DeFi super app"
- "maximize your passive income"
- "best yield" (use "up to ~X% APY" instead)
- "guaranteed", "risk-free", "best yield" in any banner copy
- stacked filler rhythm: "more X, more Y, more Z" three or more times in a row
- overly abstract AI-style writing
- "borrow more or caps won't raise"
- "we can't raise caps because nobody is borrowing"
- "uncapping deposits hurts everyone"
- "vanity metrics"
- "Blip Blop is the onchain credit market" (Blip Blop is a mascot, not the protocol)
- "Ondo assets can now be used as collateral on Permapod" (unless officially confirmed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 — APPROVED WORDING PATTERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use these naturally, do not force all at once:
- "stablecoin capital should not sit still"
- "put your capital to work"
- "make your assets productive"
- "supply builds liquidity, borrowing activates it"
- "the onchain credit market keeps taking shape"
- "liquidity becomes more useful when it moves through credit activity"
- "productive capital starts when supplied liquidity meets real borrowing demand"
- "the onchain credit market"
- "productive capital"
- "real borrowing demand"
- "market balance"
- "capital moving through lending, borrowing, and credit activity"
- "stablecoin capital, USDC, capital, liquidity, collateral"
- "productive capital, credit activity, market depth"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5 — APPROVED NARRATIVE LINES (reuse freely)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- The onchain credit market is taking shape
- Stablecoin capital should not sit still
- Your USDC has somewhere better to be
- Put your capital to work
- Supply builds depth, borrowing creates motion
- More room opens as the market grows
- Better markets need better context
- See where the market stands before you put capital to work
- TVL is the signal, credit is the story
- Where liquidity becomes credit
- The curve is early, the direction is clear
- The market gets deeper when capital starts working
- Lending is the first layer, credit is the larger system
- Access is step one, utility comes next
- More assets onchain means more systems to build around them over time
- Back to building
- Beep

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6 — BRAND VOICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROTOCOL VOICE — use for product announcements, milestone posts, analytics, serious updates, wallet migration posts, risk/cap management, partnership posts:
Grounded, clear, direct, transparent, quietly confident, data-led when possible, not overhyped.
Do NOT sound: too corporate, too cute, too degen, too formal, too technical, too vague.

BLIP BLOP VOICE — use only for points reminders, leaderboard posts, community updates, light milestones, educational whiteboard posts, playful QRTs, ecosystem reactions, social-friendly announcements:
Warm, punchy, slightly robotic, builder-coded, short, lightly playful, not cringe. Write Blip Blop in third person. Add 🤖 at the end of Blip Blop posts.
Do NOT overuse Blip Blop in formal posts. Blip Blop enhances the brand, it does not replace it.

Blip Blop approved phrases (use these, do not invent random ones):
- Blip Blop ran the numbers
- Blip Blop checked the leaderboard
- Blip Blop checked the wiring
- systems nominal
- back to building
- beep
- Blip Blop sees the bigger picture
- Blip Blop ran diagnostics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 7 — TONE RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Write grounded, clear, direct, quietly confident. No hype. No CT slang. Human and clean.
- Every line must earn its place. Cut filler.
- Vary sentence rhythm. Mix short punchy lines with one slightly longer observation.
- Avoid generic crypto clichés.
- Make the reader feel something or think something they did not before.
- The best posts sound like a sharp human wrote them, not a bot.
- Always connect features, metrics, and ecosystem news back to: onchain credit, productive capital, lending, borrowing, collateral, liquidity, or market activity.
- Never overclaim features that are not live.
- Use "up to" or "~" for all APY figures.
- Never say yields are guaranteed.
- If APY is mentioned, note "APY may change". Say "lending carries risk". Refer users to docs for live data.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 8 — TWEET STRUCTURES THAT WORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A. Metric post: (1) Metric or rank (2) Context (3) Meaning (4) CTA
B. Blip Blop countdown: (1) Deadline (2) Blip Blop reaction (3) What users can do (4) CTA
C. Product feature: (1) Feature is live (2) What it does (3) Why it matters (4) CTA
D. Ecosystem QRT: (1) Acknowledge ecosystem move (2) Connect to Permapod (3) Avoid overclaiming (4) Optional CTA
E. Educational mechanic: (1) State user context (2) Explain mechanic simply (3) Why it matters (4) CTA or close

The best Permapod tweets: strong hook, specific metric or feature, one clear meaning, CTA.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 9 — FEATURE CANON (what exists, how to write about it)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CURRENT ASSETS: $ZIG, stZIG, USDC
solvBTC: Only say live if confirmed. Narrative: BTC-backed capital entering the onchain credit market. Use: supply, borrow, collateral. Avoid saying "coming" on a live post. Avoid overexplaining wrapped token mechanics.

stZIG SUPPLY CAPS: Full cap = strong signal. Never say "there is no borrowing demand". Explain caps through market balance. Caps expand responsibly when utilization, liquidity, borrowing activity, and risk stay balanced. Never say: "borrow more or caps won't raise", "we can't raise caps because nobody is borrowing", "uncapping deposits hurts everyone", "vanity metrics".

USDC YIELD/APY: Always use "up to" or "~". Never guaranteed yield language. Connect APY to borrowing demand and onchain credit activity. If quoting ~15% APY, verify it is still current before using.

LENDING BENCHMARK: Available in Analytics. Compares USDC lending markets across top protocols. Morpho and Maple are excluded (derivative and non-verifiable native USDC reserves). Metrics: Base APY, TVL, 30D growth. Data from DeFiLlama. Narrative: better context for credit decisions, users should not need 12 tabs, compare before you supply. CTA: app.permapod.xyz/analytics

SKILLS: Skills tab in app redirects to GitHub. Lets users access Permapod Skills for Claude and OpenClaw. Helps fetch protocol data and understand the market. Narrative: onchain credit should not require 12 tabs, risk/activity/opportunity should be easier to understand.

PARA / SOCIAL LOGIN: Only mention when confirmed live. Powered by @get_para. Users connect with X, Google, Discord, or Apple. Fewer wallet setup steps.

LEAP WALLET SUNSET: Leap is being sunset. User funds remain safe. Positions remain onchain. Nothing changes on protocol side. Users need to migrate wallet access. Supported wallets: Keplr, MetaMask, IBC Wallet.

POINTS / REFERRALS: Referrals earn up to 10% of referred wallet points, capped at 50% of your own points. Season 1 final stretch energy. Blip Blop can lead points posts.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 10 — CTA LINES TO USE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

General: app.permapod.xyz / Start here: app.permapod.xyz / Explore now: app.permapod.xyz / Put your capital to work: app.permapod.xyz / Make your assets productive: app.permapod.xyz
USDC: Put your USDC to work: app.permapod.xyz / Make your stablecoin capital productive: app.permapod.xyz / Turn stablecoins into productive capital: app.permapod.xyz
Points: Make your last moves count: app.permapod.xyz / Keep stacking before Season 1 closes: app.permapod.xyz / Final stretch starts now: app.permapod.xyz
Analytics: Try it now: app.permapod.xyz/analytics / Explore Lending Benchmark: app.permapod.xyz/analytics / See where the market stands: app.permapod.xyz/analytics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 11 — BANNER COPY RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Banner copy: short, clean, one idea only, no full stops, not too wordy, visually strong.
Never use: long sentences, "revolutionary", "maximize your passive income", "guaranteed", "risk-free", "best yield", too much punctuation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 12 — WHAT TO AVOID (WITH EXAMPLES)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Too generic: "We are excited to announce a groundbreaking milestone" → rewrite as a specific fact.
Too AI-ish: "More liquidity, more activity, more growth, more opportunity" → "Liquidity is the base layer. Borrowing turns it into credit activity."
Too harsh: "Unproductive stablecoin capital is a waste" → "Stablecoin capital should not sit still."
Too direct on missing demand: "We cannot raise stZIG caps because not enough people are borrowing" → "Caps are managed with market balance in mind: liquidity, borrowing activity, utilization, and risk all moving together."
Overclaiming RWA: "Ondo assets can now be used as collateral on Permapod" → "More assets onchain means more possibilities for what can be built around them over time."
Overusing Blip Blop: "Blip Blop is the onchain credit market" → "Blip Blop ran the numbers. The onchain credit market is getting deeper."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 13 — OUTPUT FORMAT (MANDATORY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Always generate exactly 2 tweet options. Label them exactly as shown below. Nothing else outside the two tweets — no preamble, no explanation, no commentary.

Tweet 1:
[tweet text here]

Tweet 2:
[tweet text here]

Both tweets must be distinct in angle or hook but aligned to the same brief. No hashtags unless specifically requested. No quotes around output."""

# ══════════════════════════════════════════════════════════════════════════
# BRAND RULES DISPLAY (shown in-bot via Brand Rules button)
# ══════════════════════════════════════════════════════════════════════════

BRAND_RULES = """🛡️ *Brand Rules — Permapod*

✅ *Always write:*
• onchain (not on-chain or on chain)
• Defi or defi (never DeFi)
• Permapod (never PermaPod)
• onchain credit market (not just "lending protocol")
• supply / borrow (preferred over lend / borrow)

✅ *Always connect to:*
• Onchain credit, productive capital
• Lending, borrowing, collateral, liquidity
• Market activity, credit activity

❌ *Never say:*
• Guaranteed yield / risk-free / safe yield
• Fixed APY unless confirmed live
• RWA / tokenized equities as live features
• No loss possible / no risk
• Collateralized markets as live (if not)
• Unconfirmed roadmap as live
• Em dashes (—)
• "idle" (use "sitting still" instead)
• "the stock protocol"
• "we support every asset class" unless confirmed
• "Blip Blop is the onchain credit market"

📊 *Feature canon:*
• Assets live: $ZIG, stZIG, USDC
• solvBTC: only if confirmed live
• USDC APY: always "up to ~X%", never guaranteed
• stZIG caps: explain via market balance, never blame borrowers
• Lending Benchmark: Morpho + Maple excluded

🪝 *Strong hooks:*
• Idle capital is a missed opportunity.
• The APY matters. The source matters more.
• Capital should work, not wait.
• Stablecoins deserve better utility.

💬 *Strong closers:*
• That is the market Permapod is building.
• Capital should be productive.
• Onchain lending is only getting started.
• Permapod is building that layer on ZIGChain.

⚠️ *Risk language:*
• Never fixed APY → say "APY may change"
• Never no risk → say "lending carries risk"
• Refer to docs: permapod.gitbook.io/home

📣 *CTA lines:*
• General: app.permapod.xyz
• USDC: Put your USDC to work: app.permapod.xyz
• Points: Make your last moves count: app.permapod.xyz
• Analytics: Try it now: app.permapod.xyz/analytics"""

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

def _parse_tweets(result: str) -> tuple[str, str]:
    """
    Parse AI output into (tweet1_text, tweet2_text).
    Handles 'Tweet 1:' and 'Tweet 2:' labels.
    Returns empty string for a tweet if not found.
    """
    tweet1 = ""
    tweet2 = ""

    if "Tweet 2:" in result:
        parts = result.split("Tweet 2:", 1)
        tweet2 = parts[1].strip()
        t1_raw = parts[0]
        if "Tweet 1:" in t1_raw:
            tweet1 = t1_raw.split("Tweet 1:", 1)[1].strip()
        else:
            tweet1 = t1_raw.strip()
    elif "Tweet 1:" in result:
        tweet1 = result.split("Tweet 1:", 1)[1].strip()

    return tweet1, tweet2


def _format_result(result: str, flow: str) -> tuple[str, object]:
    """
    Format AI result for display.
    Shows both tweets with approve buttons and total character count.
    """
    char_count = len(result)
    text = f"✨ *Generated:*\n\n{result}\n\n_{char_count} chars total_"
    return text, kb.after_gen_keyboard(flow)


def _build_dynamic_system_prompt(voice: str = None, pillar: str = None) -> str:
    """
    Build the final system prompt by appending approved tweet examples.
    Uses ChromaDB semantic search when available, falls back to SQL query.
    Always returns a valid prompt even if no examples exist yet.
    """
    base = SYSTEM_PROMPT

    query = f"{voice or ''} {pillar or ''} Permapod tweet".strip()
    examples = search_similar(query=query, voice=voice, pillar=pillar, n=3)

    if not examples:
        examples = get_approved_examples(voice=voice, pillar=pillar, limit=3)

    if not examples:
        return base

    example_block = "\n".join(f"- {t}" for t in examples)
    injection = (
        "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "SECTION 14 — PREVIOUSLY APPROVED TWEET EXAMPLES\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "These tweets have been reviewed and approved by the Permapod team. "
        "Use them as quality and style references — match this standard:\n\n"
        f"{example_block}"
    )
    return base + injection


async def _handle_approve(update: Update, tweet_number: int, flow: str):
    """
    Called when user taps Approve Tweet 1 or Approve Tweet 2.
    Parses the correct tweet from session, saves to DB and ChromaDB.
    """
    query = update.callback_query
    uid = update.effective_user.id
    user = update.effective_user
    s = session.get(uid)

    raw_result = s.get("last_result", "")
    if not raw_result:
        await query.answer("No generated tweet found. Please generate first.", show_alert=True)
        return

    tweet1, tweet2 = _parse_tweets(raw_result)
    tweet_text = tweet1 if tweet_number == 1 else tweet2

    if not tweet_text:
        await query.answer("Could not parse tweet text. Please regenerate.", show_alert=True)
        return

    row_id = save_approved_tweet(
        user_id=uid,
        username=user.username or user.first_name or str(uid),
        flow=flow,
        tweet_number=tweet_number,
        tweet_text=tweet_text,
        voice=s.get("voice"),
        pillar=s.get("pillar"),
        bucket=s.get("bucket"),
        hook=s.get("hook"),
        closing=s.get("closing"),
        output_type=s.get("output_type"),
        context=s.get("context"),
        source_tweet=s.get("tweet"),
        trend_input=s.get("trend"),
    )

    if row_id is None:
        await query.answer("DB error — could not save. Try again.", show_alert=True)
        return

    embed_and_store(
        tweet_id=row_id,
        tweet_text=tweet_text,
        voice=s.get("voice"),
        pillar=s.get("pillar"),
        flow=flow,
        bucket=s.get("bucket"),
    )

    username_display = f"@{user.username}" if user.username else user.first_name
    confirmation = (
        f"✅ *Tweet {tweet_number} approved and saved!*\n\n"
        f"_{tweet_text}_\n\n"
        f"Saved by {username_display} · flow: {flow} · "
        f"voice: {s.get('voice', 'n/a')} · pillar: {s.get('pillar', 'n/a')}"
    )
    await query.edit_message_text(
        confirmation,
        reply_markup=kb.after_approval_keyboard(flow),
        parse_mode=ParseMode.MARKDOWN,
    )

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

    # ── Approve callbacks ──────────────────────────
    if data.startswith("approve_"):
        parts = data.split("_", 2)
        if len(parts) == 3:
            tweet_number = int(parts[1])
            flow = parts[2]
            await _handle_approve(update, tweet_number, flow)
        return

    # ── ADD THIS BLOCK: Intercept Back Button ──
    if data == "back_step":
        flow, step = s.get("flow"), s.get("step")
        
        if flow == "post":
            # Reverse lookup for the hook map
            rev_hook = {v: k for k, v in HOOK_MAP.items()}
            hook_key = rev_hook.get(s.get("hook"), "hook_ai")
            
            if step == "pillar":  data = "flow_post"
            elif step == "hook":  data = f"post_voice_{s.get('voice')}"
            elif step == "closing": data = f"post_pillar_{s.get('pillar')}"
            elif step == "context": data = hook_key
            else: data = "back_menu"
            
        elif flow == "reply":
            if step == "voice":   data = "flow_reply"
            elif step == "tweet": data = f"bucket_{s.get('bucket')}"
            elif step == "context": data = f"reply_voice_{s.get('voice')}"
            else: data = "back_menu"
            
        elif flow == "repost":
            if step == "pillar":  data = "flow_repost"
            elif step == "tweet": data = f"repost_voice_{s.get('voice')}"
            elif step == "context": data = f"repost_pillar_{s.get('pillar')}"
            else: data = "back_menu"
            
        elif flow == "trend":
            if step in ("output_type", "image_output_type"): data = "flow_trend"
            elif step == "voice_trend": data = "timode_trend"
            elif step == "voice_image": data = "timode_image"
            elif step in ("pillar_trend", "pillar_image"): data = f"outtype_{s.get('output_type')}"
            elif step in ("trend_input", "awaiting_image"): data = f"trend_voice_{s.get('voice')}"
            elif step in ("context", "context_image"): data = f"trend_pillar_{s.get('pillar')}"
            else: data = "back_menu"
            
        else:
            data = "back_menu"
    # ──────────────────────────────────────────

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

    elif data == "flow_history":
        rows = get_user_history(uid, limit=5)
        if not rows:
            text = "📋 *Your Approvals*\n\nNo approved tweets yet."
        else:
            lines = ["📋 *Your Recent Approvals*\n"]
            for r in rows:
                dt = r["approved_at"].strftime("%d %b %Y") if r["approved_at"] else "n/a"
                lines.append(
                    f"*{dt}* · {r['flow']} · {r.get('voice','') or 'n/a'} · {r.get('pillar','') or 'n/a'}\n"
                    f"_{r['tweet_text'][:120]}{'...' if len(r['tweet_text']) > 120 else ''}_\n"
                )
            text = "\n".join(lines)
        await query.edit_message_text(
            text, reply_markup=back_keyboard(), parse_mode=ParseMode.MARKDOWN,
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
        await query.edit_message_text("⏳ Generating 2 tweet options...")
        result = await generate_text(
            build_post_prompt(s["voice"], s["pillar"], "", s["hook"], s["closing"]),
            system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
        )
        session.update(uid, step="done", last_result=result)
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
            await query.edit_message_text("⏳ Generating 2 reply options...")
            result = await generate_text(
                build_reply_prompt(s["voice"], s["bucket"], s["tweet"], ""),
                system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
            )
        elif flow == "repost":
            await query.edit_message_text("⏳ Generating 2 repost comment options...")
            result = await generate_text(
                build_repost_prompt(s["voice"], s["pillar"], s["tweet"], ""),
                system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
            )
        elif flow == "trend":
            await query.edit_message_text("⏳ Generating 2 options from trend...")
            result = await generate_text(
                build_trend_prompt(s["voice"], s["pillar"], s["trend"], s["output_type"], ""),
                system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
            )
        else:
            result = "Unknown flow."
        session.update(uid, step="done", last_result=result)
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
        await query.edit_message_text("⏳ Generating 2 options from image...")
        s = session.get(uid)
        result = await generate_vision(
            build_trend_prompt(s["voice"], s["pillar"], "", s["output_type"], ""),
            s["image_b64"], s["image_mime"],
            system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
        )
        session.update(uid, step="done", last_result=result)
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
        await query.edit_message_text("⏳ Regenerating 2 options...")
        if flow == "post":
            result = await generate_text(
                build_post_prompt(s["voice"], s["pillar"], s["context"], s["hook"], s["closing"]),
                system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
            )
        elif flow == "reply":
            result = await generate_text(
                build_reply_prompt(s["voice"], s["bucket"], s["tweet"], s["context"]),
                system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
            )
        elif flow == "repost":
            result = await generate_text(
                build_repost_prompt(s["voice"], s["pillar"], s["tweet"], s["context"]),
                system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
            )
        elif flow == "trend":
            if s.get("image_b64"):
                result = await generate_vision(
                    build_trend_prompt(s["voice"], s["pillar"], "", s["output_type"], s["context"]),
                    s["image_b64"], s["image_mime"],
                    system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
                )
            else:
                result = await generate_text(
                    build_trend_prompt(s["voice"], s["pillar"], s["trend"], s["output_type"], s["context"]),
                    system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
                )
        else:
            result = "Unknown flow."
        session.update(uid, last_result=result)
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
        msg = await update.message.reply_text("⏳ Generating 2 tweet options...")
        s = session.get(uid)
        result = await generate_text(
            build_post_prompt(s["voice"], s["pillar"], s["context"], s["hook"], s["closing"]),
            system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
        )
        session.update(uid, step="done", last_result=result)
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
        msg = await update.message.reply_text("⏳ Generating 2 reply options...")
        s = session.get(uid)
        result = await generate_text(
            build_reply_prompt(s["voice"], s["bucket"], s["tweet"], s["context"]),
            system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
        )
        session.update(uid, step="done", last_result=result)
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
        msg = await update.message.reply_text("⏳ Generating 2 repost comment options...")
        s = session.get(uid)
        result = await generate_text(
            build_repost_prompt(s["voice"], s["pillar"], s["tweet"], s["context"]),
            system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
        )
        session.update(uid, step="done", last_result=result)
        txt, markup = _format_result(result, "repost")
        await msg.edit_text(txt, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        return

    # Image — context input after image received
    if flow == "trend" and step == "context_image":
        session.update(uid, context="" if text.lower() == "skip" else text)
        msg = await update.message.reply_text("⏳ Generating 2 options from image...")
        s = session.get(uid)
        result = await generate_vision(
            build_trend_prompt(s["voice"], s["pillar"], "", s["output_type"], s["context"]),
            s["image_b64"], s["image_mime"],
            system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
        )
        session.update(uid, step="done", last_result=result)
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
        msg = await update.message.reply_text("⏳ Generating 2 options from trend...")
        s = session.get(uid)
        result = await generate_text(
            build_trend_prompt(s["voice"], s["pillar"], s["trend"], s["output_type"], s["context"]),
            system=_build_dynamic_system_prompt(s.get("voice"), s.get("pillar")),
        )
        session.update(uid, step="done", last_result=result)
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

    if s.get("step") != "awaiting_image":
        await update.message.reply_text("Please start a Trend/Image flow first. Use /menu.")
        return

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






