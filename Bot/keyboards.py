# ═══════════════════════════════════════════════
# keyboards.py — All inline keyboard definitions
# ═══════════════════════════════════════════════

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ── MAIN MENU ────────────────────────────────────
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ New Post",          callback_data="flow_post")],
        [InlineKeyboardButton("💬 Reply",              callback_data="flow_reply")],
        [InlineKeyboardButton("🔁 Repost + Comment",  callback_data="flow_repost")],
        [InlineKeyboardButton("🔥 Trend / Image",     callback_data="flow_trend")],
        [InlineKeyboardButton("🛡️ Brand Rules",       callback_data="flow_rules")],
        [InlineKeyboardButton("📅 Weekly Cadence",    callback_data="flow_cadence")],
    ])

# ── VOICE ────────────────────────────────────────
def voice_keyboard(prefix=""):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏛️ Protocol voice", callback_data=f"{prefix}voice_protocol"),
            InlineKeyboardButton("🤖 Blip Blop voice", callback_data=f"{prefix}voice_blipblop"),
        ]
    ])

# ── PILLARS ──────────────────────────────────────
def pillar_keyboard(prefix=""):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏦 Onchain Lending",      callback_data=f"{prefix}pillar_lending"),
            InlineKeyboardButton("💵 Stablecoin Utility",   callback_data=f"{prefix}pillar_stablecoin"),
        ],
        [
            InlineKeyboardButton("📈 Lending Demand",       callback_data=f"{prefix}pillar_demand"),
            InlineKeyboardButton("🏗️ Credit Infrastructure",callback_data=f"{prefix}pillar_credit"),
        ],
        [
            InlineKeyboardButton("⛓️ ZIGChain Ecosystem",   callback_data=f"{prefix}pillar_zigchain"),
            InlineKeyboardButton("📚 Product Education",    callback_data=f"{prefix}pillar_education"),
        ],
        [
            InlineKeyboardButton("📊 Benchmark",            callback_data=f"{prefix}pillar_benchmark"),
            InlineKeyboardButton("🤖 Blip Blop",            callback_data=f"{prefix}pillar_blipblop"),
        ],
    ])

# ── REPLY BUCKETS ────────────────────────────────
def bucket_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💵 Under stablecoin posts",   callback_data="bucket_stablecoin")],
        [InlineKeyboardButton("📈 Under DeFi yield posts",   callback_data="bucket_defi")],
        [InlineKeyboardButton("⛓️ Under ZIGChain posts",     callback_data="bucket_zig")],
        [InlineKeyboardButton("📣 Under Permapod mentions",  callback_data="bucket_mention")],
    ])

# ── HOOK OPTIONS ─────────────────────────────────
def hook_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ AI picks freely",                              callback_data="hook_ai")],
        [InlineKeyboardButton("Idle capital is a missed opportunity.",           callback_data="hook_1")],
        [InlineKeyboardButton("Stablecoins deserve better utility.",             callback_data="hook_2")],
        [InlineKeyboardButton("The APY matters. The source matters more.",       callback_data="hook_3")],
        [InlineKeyboardButton("Productive capital builds stronger markets.",     callback_data="hook_4")],
        [InlineKeyboardButton("Capital should work, not wait.",                  callback_data="hook_5")],
        [InlineKeyboardButton("Lending infrastructure matters.",                 callback_data="hook_6")],
    ])

# ── CLOSING OPTIONS ──────────────────────────────
def closing_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ AI picks freely",                              callback_data="closing_ai")],
        [InlineKeyboardButton("That is the market Permapod is building.",        callback_data="closing_1")],
        [InlineKeyboardButton("Capital should be productive.",                   callback_data="closing_2")],
        [InlineKeyboardButton("Onchain lending is only getting started.",        callback_data="closing_3")],
        [InlineKeyboardButton("Stablecoins deserve better markets.",             callback_data="closing_4")],
        [InlineKeyboardButton("Permapod is building that layer on ZIGChain.",   callback_data="closing_5")],
    ])

# ── TREND INPUT MODE ─────────────────────────────
def trend_mode_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📝 Text trend",        callback_data="timode_trend"),
            InlineKeyboardButton("🖼️ Screenshot/Image",  callback_data="timode_image"),
        ]
    ])

# ── TREND OUTPUT TYPE ────────────────────────────
def output_type_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🐦 Original tweet",    callback_data="outtype_tweet"),
            InlineKeyboardButton("💬 Reply",              callback_data="outtype_reply"),
            InlineKeyboardButton("🔁 Repost comment",    callback_data="outtype_repost"),
        ]
    ])

# ── SKIP / GENERATE ──────────────────────────────
def skip_keyboard(skip_data="skip_context"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏭️ Skip (no context)",  callback_data=skip_data)],
    ])

# ── AFTER GENERATION ────────────────────────────
def after_gen_keyboard(flow):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Regenerate",    callback_data=f"regen_{flow}"),
            InlineKeyboardButton("🏠 Main menu",     callback_data="back_menu"),
        ]
    ])

# ── WEEKLY CADENCE ───────────────────────────────
def cadence_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mon — Market",     callback_data="cadence_mon"),
            InlineKeyboardButton("Tue — Product",    callback_data="cadence_tue"),
        ],
        [
            InlineKeyboardButton("Wed — Blip Blop",  callback_data="cadence_wed"),
            InlineKeyboardButton("Thu — Ecosystem",  callback_data="cadence_thu"),
        ],
        [
            InlineKeyboardButton("Fri — Benchmark",  callback_data="cadence_fri"),
            InlineKeyboardButton("Sat — Community",  callback_data="cadence_sat"),
        ],
        [InlineKeyboardButton("Sun — Narrative",     callback_data="cadence_sun")],
    ])
