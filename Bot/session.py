# ═══════════════════════════════════════════════
# session.py — Per-user session state
# Tracks which step each user is on in a flow
# ═══════════════════════════════════════════════

# session store: { user_id: { ...state } }
_sessions = {}

DEFAULT = {
    "flow":        None,    # current flow: post|reply|repost|trend
    "step":        None,    # current step within the flow
    "voice":       "protocol",
    "pillar":      "lending",
    "bucket":      "stablecoin",
    "output_type": "tweet",
    "hook":        "ai",
    "closing":     "ai",
    "tweet":       "",
    "context":     "",
    "trend":       "",
    "image_b64":   None,
    "image_mime":  None,
    "nav_stack":   [],      # list of {"text": str, "markup": InlineKeyboardMarkup} for back navigation
}


def get(user_id: int) -> dict:
    if user_id not in _sessions:
        s = DEFAULT.copy()
        s["nav_stack"] = []
        _sessions[user_id] = s
    return _sessions[user_id]


def update(user_id: int, **kwargs):
    s = get(user_id)
    s.update(kwargs)


def reset(user_id: int):
    s = DEFAULT.copy()
    s["nav_stack"] = []
    _sessions[user_id] = s


def set_flow(user_id: int, flow: str, step: str):
    s = get(user_id)
    s["flow"] = flow
    s["step"] = step

# ── NAV STACK helpers ──────────────────────────────
# Each entry: {"text": str, "markup": InlineKeyboardMarkup}
# Push the CURRENT screen before advancing so Back can replay it.

def nav_push(user_id: int, text: str, markup):
    s = get(user_id)
    s["nav_stack"].append({"text": text, "markup": markup})


def nav_pop(user_id: int):
    """Return the previous screen dict and remove it, or None if stack is empty."""
    s = get(user_id)
    if s["nav_stack"]:
        return s["nav_stack"].pop()
    return None


def nav_clear(user_id: int):
    s = get(user_id)
    s["nav_stack"] = []