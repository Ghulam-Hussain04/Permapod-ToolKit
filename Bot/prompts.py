BRAND_NAMES = {
    "permapod": "Permapod",
    "nawa": "Nawa",
}


VOICE_INSTRUCTIONS = {
    "permapod": {
        "protocol": (
            "Use Protocol Voice: grounded, clear, direct, transparent, quietly confident, "
            "data-led when possible, not overhyped. Short punchy lines. Vary rhythm. "
            "No exclamation marks. No hype language. No em dashes. Do not sound too corporate, "
            "too cute, too degen, too formal, too technical, or too vague."
        ),
        "blipblop": (
            "Use Blip Blop Voice: write as the Blip Blop character in third person. Warm, "
            "punchy, slightly robotic, builder-coded, short, lightly playful, not cringe. "
            "2-3 short punchy lines. No em dashes. Add the robot emoji at the very end. "
            "Use approved Blip Blop phrases where natural: 'Blip Blop ran the numbers', "
            "'Blip Blop checked the leaderboard', 'Blip Blop checked the wiring', "
            "'systems nominal', 'back to building', 'beep'. "
            "Do NOT say 'Blip Blop is the onchain credit market'."
        ),
    },
    "nawa": {
        "brand": (
            "Use Nawa Brand Voice: calm, premium, semi-institutional, human, sharp, "
            "values-driven, and structured. Sound like a thoughtful financial operator "
            "explaining why the structure behind yield matters. Never sound hypey, degen, "
            "preachy, overly religious, or like a bank advertisement."
        ),
        "educational": (
            "Use Nawa Educational Voice: clear, measured, and useful. Explain one idea "
            "about yield source, Shariah-certified structure, real activity, traceability, "
            "RWAs, or ethical capital. Do not over-explain or sound academic."
        ),
        "conversion": (
            "Use Nawa Conversion Voice: calm and direct. Encourage action without pressure. "
            "Focus on the Nawa USDC Vault, stablecoin productivity, certified strategies, "
            "asset-backed yield, real-world economic activity, and liquidity from the start. "
            "Never imply guaranteed, risk-free, safe, or passive returns."
        ),
        "qrt": (
            "Use Nawa QRT Voice: interpret the source post through Nawa's lens without "
            "copying the announcement or making everything about Nawa. Connect the topic "
            "to access, structure, RWAs, real-world yield, source transparency, and aligned capital."
        ),
    },
}


PILLAR_INSTRUCTIONS = {
    "permapod": {
        "lending": (
            "Pillar focus: onchain lending markets, liquidity, productive capital deployment, "
            "lending infrastructure. Themes: what is onchain credit, why borrowing matters, "
            "how lending and borrowing work together, why utilization matters, why TVL alone "
            "is not the full story, how capital becomes productive."
        ),
        "stablecoin": (
            "Pillar focus: stablecoins put to work in lending markets instead of sitting still. "
            "USDC should not sit in a wallet. Connect APY to real borrowing demand, not just the number. "
            "If referencing APY, always say 'up to ~X%' and note APY may change."
        ),
        "demand": (
            "Pillar focus: yield comes from real lending activity and market demand. "
            "The source of APY matters more than the number itself. APY reflects borrowing demand. "
            "TVL is a signal, credit is the story."
        ),
        "credit": (
            "Pillar focus: Permapod as a financial primitive and credit infrastructure layer. "
            "Lending is the first layer, credit is the larger system."
        ),
        "zigchain": (
            "Pillar focus: Permapod contributing lending and credit primitives to ZIGChain. "
            "Strong ecosystems need lending infrastructure. Do not overclaim direct RWA integrations."
        ),
        "education": (
            "Pillar focus: explain one clear aspect of what Permapod does in simple terms. "
            "Themes: onchain credit, borrowing, supply caps, health factor, utilization, TVL, and productive capital."
        ),
        "benchmark": (
            "Pillar focus: reference lending activity, participation, rankings, or growth. "
            "Do not state specific APY unless confirmed current. Lending Benchmark is available in Analytics."
        ),
        "blipblop": (
            "Pillar focus: use the Blip Blop mascot voice for points reminders, leaderboard posts, "
            "community updates, light milestones, educational whiteboard posts, and playful QRTs."
        ),
    },
    "nawa": {
        "stablecoin": (
            "Pillar focus: Stablecoin Productivity. Stablecoins helped ethical investors preserve value. "
            "Nawa helps USDC become productive through Shariah-certified, asset-backed yield structures. "
            "Ethical investors should not have to choose between productivity and principles."
        ),
        "yield_source": (
            "Pillar focus: Yield Source Education. APY is only half the story. The source, mechanics, "
            "structure, asset backing, and connection to real activity matter before yield becomes attractive."
        ),
        "shariah_structure": (
            "Pillar focus: Shariah Compliance Is Structure, Not A Label. Compliance cannot be added at the end. "
            "The strategy, assets, return mechanics, risk treatment, and review process must shape the vault before capital moves."
        ),
        "rwa": (
            "Pillar focus: RWAs And Ethical Finance. RWAs are not automatically ethical, but assets, activity, "
            "and traceable return sources naturally align with Islamic finance principles when structured properly."
        ),
        "access": (
            "Pillar focus: Access Is Not Enough. Ethical capital needs aligned access. Investors were not missing "
            "from onchain yield because they lacked interest. The infrastructure did not match their standards."
        ),
        "transparency": (
            "Pillar focus: Onchain Transparency And Ethical Finance. Blockchain matters for ethical capital because "
            "capital movement, vault mechanics, review, and yield sources can become more traceable."
        ),
        "ethical_capital": (
            "Pillar focus: Ethical Capital As A Distinct Market. Some capital has mandates, values, and principles. "
            "Nawa exists because ethical capital needs infrastructure built around how it is allowed to move."
        ),
    },
}


BUCKET_ANGLES = {
    "permapod": {
        "stablecoin": "Replying under a stablecoin post. Angle: stablecoin supply is only one side of the story. Connect to onchain credit and productive capital.",
        "defi": "Replying under a Defi yield post. Angle: the APY number gets attention but the source of yield determines sustainability.",
        "zig": "Replying under a ZIGChain ecosystem post. Angle: strong ecosystems need lending primitives and financial infrastructure.",
        "mention": "Replying to a direct Permapod mention. Appreciate the mention and reinforce useful onchain credit infrastructure.",
    },
    "nawa": {
        "stablecoin": "Replying under a stablecoin post. Angle: stablecoins can become productive only when the yield path aligns with ethical capital.",
        "rwa": "Replying under an RWA post. Angle: RWAs move the market toward assets and activity, but structure still decides suitability for ethical capital.",
        "defi": "Replying under a Defi yield post. Angle: APY is not enough. Source, mechanics, leverage, and structure matter.",
        "zig": "Replying under a ZIGChain post. Angle: access matters, but aligned infrastructure lets ethical capital participate without compromising how it moves.",
        "ethical": "Replying under ethical or Islamic finance content. Angle: principles need modern rails, but compliance has to shape the product before capital moves.",
        "mention": "Replying to a direct Nawa mention. Stay calm, helpful, and focused on certified structure, real activity, and traceable yield sources.",
    },
}


WEEKLY_CADENCE = {
    "permapod": {
        "mon": ("Market Thesis", "protocol", "lending"),
        "tue": ("Product Education", "protocol", "education"),
        "wed": ("Blip Blop Post", "blipblop", "blipblop"),
        "thu": ("Ecosystem", "protocol", "zigchain"),
        "fri": ("Benchmark", "protocol", "benchmark"),
        "sat": ("Community", "blipblop", "blipblop"),
        "sun": ("Narrative", "protocol", "credit"),
    },
    "nawa": {
        "mon": ("Yield Source Education", "educational", "yield_source"),
        "tue": ("Stablecoin Productivity", "brand", "stablecoin"),
        "wed": ("Shariah Structure", "educational", "shariah_structure"),
        "thu": ("RWAs And Ethical Finance", "qrt", "rwa"),
        "fri": ("USDC Vault Conversion", "conversion", "stablecoin"),
        "sat": ("Ethical Capital", "brand", "ethical_capital"),
        "sun": ("Principle-Led Narrative", "brand", "access"),
    },
}





def brand_name(brand):
    return BRAND_NAMES.get(brand, BRAND_NAMES["permapod"])


def get_weekly_cadence(brand):
    return WEEKLY_CADENCE.get(brand, WEEKLY_CADENCE["permapod"])





def _voice(brand, voice):
    return VOICE_INSTRUCTIONS.get(brand, VOICE_INSTRUCTIONS["permapod"])[voice]


def _pillar(brand, pillar):
    return PILLAR_INSTRUCTIONS.get(brand, PILLAR_INSTRUCTIONS["permapod"])[pillar]


def _bucket(brand, bucket):
    return BUCKET_ANGLES.get(brand, BUCKET_ANGLES["permapod"])[bucket]


def _brand_format_rules(brand):
    if brand == "nawa":
        return (
            "No hashtags unless specifically requested. No quotes around output. No em dashes. "
            "Never say guaranteed, risk-free, safe returns, easy money, passive income, halal yield farming, "
            "yield farming made halal, game changer, revolutionary, insane APY, or massive gains. "
            "Never imply all RWAs are ethical or that yield has no risk. Do not use Quranic or religious references "
            "unless specifically requested. Keep it calm, premium, human, and clear."
        )
    return (
        "No hashtags. No quotes around output. No em dashes. No 'DeFi' (use Defi/defi). "
        "No 'on-chain' (use onchain). Never imply guaranteed or risk-free yield."
    )


def build_post_prompt(voice, pillar, context="", brand="permapod"):
    name = brand_name(brand)
    hook_line = "Opening hook: write a fresh, original opening line for each tweet. Do not use predefined hooks."
    closing_line = "Closing line: write a fresh, original closing line for each tweet. Do not use predefined closers."
    parts = [
        f"Write exactly 2 different X (Twitter) posts for {name}.",
        "Label them Tweet 1: and Tweet 2: with a blank line between them.",
        "Each tweet must be distinct in angle, rhythm, or framing. Both must fit within 280 characters.",
        "",
        _voice(brand, voice),
        "",
        _pillar(brand, pillar),
        "",
        hook_line,
        closing_line,
    ]
    if context:
        parts.append(f"\nAdditional context to incorporate: {context}")
    parts.append(f"\nFormat rules: {_brand_format_rules(brand)} Output only the two labeled tweets, nothing else.")
    return "\n".join(parts)


def build_reply_prompt(voice, bucket, tweet="", context="", brand="permapod"):
    name = brand_name(brand)
    parts = [
        f"Write exactly 2 different replies to this tweet for the {name} X account.",
        "Label them Tweet 1: and Tweet 2: with a blank line between them.",
        "",
        f'Tweet being replied to: "{tweet or "(no tweet provided. Write a general on-brand reply)"}"',
        "",
        _voice(brand, voice),
        "",
        _bucket(brand, bucket),
    ]
    if context:
        parts.append(f"\nAdditional context: {context}")
    parts.append(f"\nFormat: 1-3 short lines each. Sharp and adds value. {_brand_format_rules(brand)} Output only the two labeled replies, nothing else.")
    return "\n".join(parts)


def build_repost_prompt(voice, pillar, tweet="", context="", brand="permapod"):
    name = brand_name(brand)
    parts = [
        f"Write exactly 2 different quote-repost comments for the {name} X account.",
        "Label them Tweet 1: and Tweet 2: with a blank line between them.",
        "",
        f'Tweet being quote-reposted: "{tweet or "(no tweet provided)"}"',
        "",
        _voice(brand, voice),
        "",
        f"Content angle: {_pillar(brand, pillar)}",
    ]
    if context:
        parts.append(f"\nSpecific take to incorporate: {context}")
    parts.append(f"\nFormat: 1-2 lines each. Sharp and interpretive. {_brand_format_rules(brand)} Output only the two labeled comments, nothing else.")
    return "\n".join(parts)


def build_trend_prompt(voice, pillar, trend="", output_type="tweet", context="", brand="permapod"):
    name = brand_name(brand)
    out_map = {
        "tweet": "original tweet",
        "reply": "reply",
        "repost": "quote-repost comment",
    }
    out_label = out_map.get(output_type, "tweet")
    parts = [
        f'Trending topic or tweet: "{trend or "(no trend provided)"}"',
        "",
        f"Generate exactly 2 different {name} {out_label}s that connect this trend to {name}'s narrative.",
        "Label them Tweet 1: and Tweet 2: with a blank line between them.",
        "",
        _voice(brand, voice),
        "",
        f"Content angle: {_pillar(brand, pillar)}",
    ]
    if context:
        parts.append(f"\nExtra context: {context}")
    parts.append(f"\nFormat: max 280 characters each. {_brand_format_rules(brand)} Output only the two labeled posts, nothing else.")
    return "\n".join(parts)
