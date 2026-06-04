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
}


def get(user_id: int) -> dict:
    if user_id not in _sessions:
        _sessions[user_id] = DEFAULT.copy()
    return _sessions[user_id]


def update(user_id: int, **kwargs):
    s = get(user_id)
    s.update(kwargs)


def reset(user_id: int):
    _sessions[user_id] = DEFAULT.copy()


def set_flow(user_id: int, flow: str, step: str):
    s = get(user_id)
    s["flow"] = flow
    s["step"] = step
