# ═══════════════════════════════════════════════
# prompts.py — All Permapod AI prompts
# ═══════════════════════════════════════════════
#
# NOTE: The master SYSTEM_PROMPT lives in handlers.py and is passed
# into every generate_text / generate_vision call via the system= kwarg.
# The SYSTEM_PROMPT constant below is kept as a fallback reference only
# and should NOT be used directly — handlers.py always overrides it.
# ═══════════════════════════════════════════════

# ── VOICE INSTRUCTIONS ──────────────────────────
VOICE_INSTRUCTIONS = {
    "protocol": (
        "Use Protocol Voice: grounded, clear, direct, transparent, quietly confident, "
        "data-led when possible, not overhyped. Short punchy lines. Vary rhythm — mix "
        "short lines with one slightly longer observation. No exclamation marks. No hype "
        "language. No em dashes. Do not sound too corporate, too cute, too degen, too "
        "formal, too technical, or too vague. Sound like a sharp human, not a bot."
    ),
    "blipblop": (
        "Use Blip Blop Voice: write as the Blip Blop character in third person. Warm, "
        "punchy, slightly robotic, builder-coded, short, lightly playful, not cringe. "
        "2-3 short punchy lines. No em dashes. Add 🤖 at the very end. "
        "Use approved Blip Blop phrases where natural: 'Blip Blop ran the numbers', "
        "'Blip Blop checked the leaderboard', 'Blip Blop checked the wiring', "
        "'systems nominal', 'back to building', 'beep', "
        "'Blip Blop sees the bigger picture', 'Blip Blop ran diagnostics'. "
        "Do NOT say 'Blip Blop is the onchain credit market'."
    ),
}

# ── PILLAR INSTRUCTIONS ──────────────────────────
PILLAR_INSTRUCTIONS = {
    "lending": (
        "Pillar focus: onchain lending markets, liquidity, productive capital deployment, "
        "lending infrastructure. Themes: what is onchain credit, why borrowing matters, "
        "how lending and borrowing work together, why utilization matters, "
        "why TVL alone is not the full story, how capital becomes productive. "
        "Example angle: Supply adds liquidity. Borrowing activates it. "
        "That balance is what keeps an onchain credit market healthy."
    ),
    "stablecoin": (
        "Pillar focus: stablecoins put to work in lending markets instead of sitting still. "
        "USDC should not sit in a wallet. Connect APY to real borrowing demand, not just the number. "
        "If referencing APY, always say 'up to ~X%' and note APY may change. "
        "Never use guaranteed yield language."
    ),
    "demand": (
        "Pillar focus: yield comes from real lending activity and market demand. "
        "The source of APY matters more than the number itself. "
        "APY reflects borrowing demand. TVL is a signal, credit is the story. "
        "Ranking validates market activity. Stablecoin capital is finding productive use."
    ),
    "credit": (
        "Pillar focus: Permapod as a financial primitive and credit infrastructure layer, "
        "bigger than a single app. Lending is the first layer, credit is the larger system. "
        "Strong ecosystems need more than assets — they need lending, liquidity, and financial infrastructure."
    ),
    "zigchain": (
        "Pillar focus: Permapod contributing lending and credit primitives to ZIGChain. "
        "Strong ecosystems need lending infrastructure. More liquidity means deeper markets. "
        "More assets onchain means more future utility. Credit markets become more important "
        "as asset bases grow. Do not overclaim direct integration with Ondo or RWAs unless confirmed live. "
        "For ZIGChain x Ondo content: be vague, talk about what more assets onchain can enable over time."
    ),
    "education": (
        "Pillar focus: explain one clear aspect of what Permapod does in simple terms. "
        "Themes: what is onchain credit, why borrowing matters, why supply caps exist, "
        "how lending and borrowing work together, what health factor means, "
        "why utilization matters, why TVL alone is not the full story, "
        "how capital becomes productive. "
        "Example: Supply adds liquidity. Borrowing activates it. "
        "That balance is what keeps an onchain credit market healthy."
    ),
    "benchmark": (
        "Pillar focus: reference lending activity, participation, rankings, or growth. "
        "Do not state specific APY unless confirmed current. "
        "Lending Benchmark is available in Analytics — lets users compare USDC lending markets "
        "across top protocols (Morpho and Maple excluded). Metrics: Base APY, TVL, 30D growth. "
        "Data from DeFiLlama. Narrative: better context, users should not need 12 tabs, "
        "compare before you supply. TVL is a signal. APY reflects borrowing demand. "
        "Ranking validates market activity."
    ),
    "blipblop": (
        "Pillar focus: use the Blip Blop mascot voice. Observational, playful, community-native. "
        "Suitable for: points reminders, leaderboard posts, community updates, light milestones, "
        "educational whiteboard posts, playful QRTs, ecosystem reactions. "
        "Blip Blop is a mascot, not the protocol itself."
    ),
}

# ── REPLY BUCKET ANGLES ──────────────────────────
BUCKET_ANGLES = {
    "stablecoin": (
        "Replying under a stablecoin post. Angle: stablecoin supply is only one side of the story. "
        "The stronger question is where lending demand comes from. "
        "Connect to the onchain credit market and productive capital."
    ),
    "defi": (
        "Replying under a Defi yield post. Angle: the APY number gets attention but the source "
        "of yield determines long-term sustainability. "
        "Always write 'Defi' or 'defi' — never 'DeFi'."
    ),
    "zig": (
        "Replying under a ZIGChain ecosystem post. Angle: strong ecosystems need lending primitives "
        "and financial infrastructure. More liquidity means deeper markets. "
        "More assets onchain means more future utility for the credit market."
    ),
    "mention": (
        "Replying to a direct Permapod mention. Angle: appreciate the mention, stay focused. "
        "Reinforce that Permapod is building useful onchain credit infrastructure. "
        "Keep it grounded and product-led."
    ),
}

# ── WEEKLY CADENCE ───────────────────────────────
WEEKLY_CADENCE = {
    "mon": ("Market Thesis",     "protocol", "lending"),
    "tue": ("Product Education", "protocol", "education"),
    "wed": ("Blip Blop Post",    "blipblop", "blipblop"),
    "thu": ("Ecosystem",         "protocol", "zigchain"),
    "fri": ("Benchmark",         "protocol", "benchmark"),
    "sat": ("Community",         "blipblop", "blipblop"),
    "sun": ("Narrative",         "protocol", "credit"),
}

# ── MESSAGE BUILDERS ─────────────────────────────

def build_post_prompt(voice, pillar, context="", hook="ai", closing="ai"):
    hook_line = (
        f'Opening hook: start Tweet 1 and Tweet 2 each with a DIFFERENT approach, '
        f'but Tweet 1 must open with exactly this line: "{hook}"'
        if hook != "ai"
        else "Opening hook: write a fresh, original opening line for each tweet. Do NOT copy from the hooks library word for word."
    )
    closing_line = (
        f'Closing line: end Tweet 1 with exactly this line: "{closing}" — Tweet 2 should use a different closer.'
        if closing != "ai"
        else "Closing line: write a fresh, original closing line for each tweet. Do NOT copy from the closers library word for word."
    )
    parts = [
        "Write exactly 2 different X (Twitter) posts for Permapod.",
        "Label them Tweet 1: and Tweet 2: with a blank line between them.",
        "Each tweet must be distinct in angle, rhythm, or framing. Both must fit within 280 characters.",
        "",
        VOICE_INSTRUCTIONS[voice],
        "",
        PILLAR_INSTRUCTIONS[pillar],
        "",
        hook_line,
        closing_line,
    ]
    if context:
        parts.append(f"\nAdditional context to incorporate: {context}")
    parts.append(
        "\nFormat: max 280 characters each. No hashtags. No quotes around output. "
        "No em dashes. No 'DeFi' (use Defi/defi). No 'on-chain' (use onchain). "
        "Output only the two labeled tweets, nothing else."
    )
    return "\n".join(parts)


def build_reply_prompt(voice, bucket, tweet="", context=""):
    parts = [
        "Write exactly 2 different replies to this tweet for the Permapod X account.",
        "Label them Tweet 1: and Tweet 2: with a blank line between them.",
        "",
        f'Tweet being replied to: "{tweet or "(no tweet provided — write a general on-brand reply)"}"',
        "",
        VOICE_INSTRUCTIONS[voice],
        "",
        BUCKET_ANGLES[bucket],
    ]
    if context:
        parts.append(f"\nAdditional context: {context}")
    parts.append(
        "\nFormat: 1-3 short lines each. Sharp, adds value. No hashtags. "
        "No em dashes. No 'DeFi'. No 'on-chain'. Output only the two labeled replies, nothing else."
    )
    return "\n".join(parts)


def build_repost_prompt(voice, pillar, tweet="", context=""):
    parts = [
        "Write exactly 2 different quote-repost comments for the Permapod X account.",
        "Label them Tweet 1: and Tweet 2: with a blank line between them.",
        "",
        f'Tweet being quote-reposted: "{tweet or "(no tweet provided)"}"',
        "",
        VOICE_INSTRUCTIONS[voice],
        "",
        f"Content angle: {PILLAR_INSTRUCTIONS[pillar]}",
    ]
    if context:
        parts.append(f"\nSpecific take to incorporate: {context}")
    parts.append(
        "\nFormat: 1-2 lines each. Sharp, opinionated. No hashtags. "
        "No em dashes. No 'DeFi'. No 'on-chain'. Output only the two labeled comments, nothing else."
    )
    return "\n".join(parts)


def build_trend_prompt(voice, pillar, trend="", output_type="tweet", context=""):
    out_map = {
        "tweet":   "original tweet",
        "reply":   "reply",
        "repost":  "quote-repost comment",
    }
    out_label = out_map.get(output_type, "tweet")
    parts = [
        f'Trending topic or tweet: "{trend or "(no trend provided)"}"',
        "",
        f"Generate exactly 2 different Permapod {out_label}s that connect this trend to Permapod's narrative.",
        "Label them Tweet 1: and Tweet 2: with a blank line between them.",
        "",
        VOICE_INSTRUCTIONS[voice],
        "",
        f"Content angle: {PILLAR_INSTRUCTIONS[pillar]}",
    ]
    if context:
        parts.append(f"\nExtra context: {context}")
    parts.append(
        "\nFormat: max 280 characters each. No hashtags. "
        "No em dashes. No 'DeFi'. No 'on-chain'. Output only the two labeled posts, nothing else."
    )
    return "\n".join(parts)