from telegram import InlineKeyboardButton, InlineKeyboardMarkup


BRAND_LABELS = {
    "permapod": "Permapod",
    "nawa": "Nawa",
}


VOICE_OPTIONS = {
    "permapod": [
        ("🏛️ Protocol voice", "protocol"),
        ("🤖 Blip Blop voice", "blipblop"),
    ],
    "nawa": [
        ("🏛️ Brand voice", "brand"),
        ("📚 Educational voice", "educational"),
        ("🎯 Conversion voice", "conversion"),
        ("🔁 QRT voice", "qrt"),
    ],
}


PILLAR_OPTIONS = {
    "permapod": [
        ("🏦 Onchain Lending", "lending"),
        ("💵 Stablecoin Utility", "stablecoin"),
        ("📈 Lending Demand", "demand"),
        ("🏗️ Credit Infrastructure", "credit"),
        ("⛓️ ZIGChain Ecosystem", "zigchain"),
        ("📚 Product Education", "education"),
        ("📊 Benchmark", "benchmark"),
        ("🤖 Blip Blop", "blipblop"),
    ],
    "nawa": [
        ("💵 Stablecoin Productivity", "stablecoin"),
        ("🔎 Yield Source Education", "yield_source"),
        ("🏛️ Shariah Structure", "shariah_structure"),
        ("🏦 RWAs & Ethical Finance", "rwa"),
        ("🔑 Access Is Not Enough", "access"),
        ("⛓️ Onchain Transparency", "transparency"),
        ("🌿 Ethical Capital", "ethical_capital"),
    ],
}


BUCKET_OPTIONS = {
    "permapod": [
        ("💵 Under stablecoin posts", "stablecoin"),
        ("📈 Under Defi yield posts", "defi"),
        ("⛓️ Under ZIGChain posts", "zig"),
        ("📣 Under Permapod mentions", "mention"),
    ],
    "nawa": [
        ("💵 Under stablecoin posts", "stablecoin"),
        ("🏦 Under RWA posts", "rwa"),
        ("📈 Under Defi yield posts", "defi"),
        ("⛓️ Under ZIGChain posts", "zig"),
        ("🌿 Under ethical finance posts", "ethical"),
        ("📣 Under Nawa mentions", "mention"),
    ],
}





CADENCE_OPTIONS = {
    "permapod": [
        ("Mon - 📈 Market", "mon"),
        ("Tue - 📚 Product", "tue"),
        ("Wed - 🤖 Blip Blop", "wed"),
        ("Thu - ⛓️ Ecosystem", "thu"),
        ("Fri - 📊 Benchmark", "fri"),
        ("Sat - 💬 Community", "sat"),
        ("Sun - 🧭 Narrative", "sun"),
    ],
    "nawa": [
        ("Mon - 🔎 Yield Source", "mon"),
        ("Tue - 💵 Stablecoins", "tue"),
        ("Wed - 🏛️ Shariah Structure", "wed"),
        ("Thu - 🏦 RWAs", "thu"),
        ("Fri - 🎯 USDC Vault", "fri"),
        ("Sat - 🌿 Ethical Capital", "sat"),
        ("Sun - 🧭 Narrative", "sun"),
    ],
}


def _back():
    return [InlineKeyboardButton("⬅️ Back", callback_data="back_step")]


def _rows(options, prefix, per_row=2):
    buttons = [
        InlineKeyboardButton(label, callback_data=f"{prefix}{value}")
        for label, value in options
    ]
    return [buttons[i:i + per_row] for i in range(0, len(buttons), per_row)]


def brand_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟣 Permapod", callback_data="brand_permapod")],
        [InlineKeyboardButton("🌿 Nawa", callback_data="brand_nawa")],
    ])


def main_menu(brand="permapod"):
    label = BRAND_LABELS.get(brand, "Content")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ New Post", callback_data="flow_post")],
        [InlineKeyboardButton("💬 Reply", callback_data="flow_reply")],
        [InlineKeyboardButton("🔁 Repost + Comment", callback_data="flow_repost")],
        [InlineKeyboardButton("🔥 Trend / Image", callback_data="flow_trend")],
        [InlineKeyboardButton("🛡️ Brand Rules", callback_data="flow_rules")],
        [InlineKeyboardButton("📅 Weekly Cadence", callback_data="flow_cadence")],
        [InlineKeyboardButton("📋 My Approvals", callback_data="flow_history")],
        [InlineKeyboardButton("🔄 Switch Brand", callback_data="switch_brand")],
    ])


def voice_keyboard(prefix="", brand="permapod"):
    return InlineKeyboardMarkup(_rows(VOICE_OPTIONS.get(brand, VOICE_OPTIONS["permapod"]), f"{prefix}voice_") + [_back()])


def pillar_keyboard(prefix="", brand="permapod"):
    return InlineKeyboardMarkup(_rows(PILLAR_OPTIONS.get(brand, PILLAR_OPTIONS["permapod"]), f"{prefix}pillar_") + [_back()])


def bucket_keyboard(brand="permapod"):
    return InlineKeyboardMarkup(_rows(BUCKET_OPTIONS.get(brand, BUCKET_OPTIONS["permapod"]), "bucket_", per_row=1) + [_back()])





def trend_mode_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📝 Text trend", callback_data="timode_trend"),
            InlineKeyboardButton("🖼️ Screenshot/Image", callback_data="timode_image"),
        ],
        _back(),
    ])


def output_type_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🐦 Original tweet", callback_data="outtype_tweet"),
            InlineKeyboardButton("💬 Reply", callback_data="outtype_reply"),
            InlineKeyboardButton("🔁 Repost comment", callback_data="outtype_repost"),
        ],
        _back(),
    ])


def skip_keyboard(skip_data="skip_context"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏭️ Skip (no context)", callback_data=skip_data)],
        _back(),
    ])


def after_gen_keyboard(flow: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve Tweet 1", callback_data=f"approve_1_{flow}"),
            InlineKeyboardButton("✅ Approve Tweet 2", callback_data=f"approve_2_{flow}"),
        ],
        [
            InlineKeyboardButton("🔄 Regenerate", callback_data=f"regen_{flow}"),
            InlineKeyboardButton("🏠 Main menu", callback_data="back_menu"),
        ],
    ])


def after_approval_keyboard(flow: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Generate another", callback_data=f"regen_{flow}"),
            InlineKeyboardButton("🏠 Main menu", callback_data="back_menu"),
        ],
    ])


def cadence_keyboard(brand="permapod"):
    return InlineKeyboardMarkup(_rows(CADENCE_OPTIONS.get(brand, CADENCE_OPTIONS["permapod"]), "cadence_") + [_back()])
