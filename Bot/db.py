# ═══════════════════════════════════════════════
# db.py — PostgreSQL storage for approved tweets
# ═══════════════════════════════════════════════

import os
import logging
from datetime import datetime
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ── Connection config ─────────────────────────────

DB_CONFIG = {
    "host":     os.environ.get("POSTGRES_HOST", "db"),
    "port":     int(os.environ.get("POSTGRES_PORT", 5432)),
    "dbname":   os.environ.get("POSTGRES_DB", "permapod"),
    "user":     os.environ.get("POSTGRES_USER", "permapod"),
    "password": os.environ.get("POSTGRES_PASSWORD", ""),
}


def get_connection():
    """Return a new psycopg2 connection."""
    return psycopg2.connect(**DB_CONFIG)


# ── Table creation ────────────────────────────────

def init_db():
    """
    Create the approved_tweets table if it does not exist.
    Called once at bot startup.
    """
    create_sql = """
    CREATE TABLE IF NOT EXISTS approved_tweets (
        id              SERIAL PRIMARY KEY,
        user_id         BIGINT          NOT NULL,
        username        TEXT,

        -- flow metadata
        flow            TEXT            NOT NULL,   -- post | reply | repost | trend
        voice           TEXT,                       -- protocol | blipblop
        pillar          TEXT,                       -- lending | stablecoin | demand | credit | zigchain | education | benchmark | blipblop
        bucket          TEXT,                       -- reply bucket: stablecoin | defi | zig | mention (reply flow only)
        hook            TEXT,                       -- selected hook text or "ai"
        closing         TEXT,                       -- selected closing text or "ai"
        output_type     TEXT,                       -- tweet | reply | repost (trend flow only)

        -- content
        tweet_number    INTEGER,                    -- 1 or 2 (which option was approved)
        tweet_text      TEXT            NOT NULL,   -- the approved tweet text
        context         TEXT,                       -- extra context user typed
        source_tweet    TEXT,                       -- original tweet for reply/repost flows
        trend_input     TEXT,                       -- trend text for trend flow

        -- status
        status          TEXT            NOT NULL DEFAULT 'approved',  -- approved | posted | archived
        approved_at     TIMESTAMP       NOT NULL DEFAULT NOW(),
        posted_at       TIMESTAMP
    );

    -- indexes for fast filtering
    CREATE INDEX IF NOT EXISTS idx_approved_tweets_voice   ON approved_tweets(voice);
    CREATE INDEX IF NOT EXISTS idx_approved_tweets_pillar  ON approved_tweets(pillar);
    CREATE INDEX IF NOT EXISTS idx_approved_tweets_flow    ON approved_tweets(flow);
    CREATE INDEX IF NOT EXISTS idx_approved_tweets_status  ON approved_tweets(status);
    CREATE INDEX IF NOT EXISTS idx_approved_tweets_user    ON approved_tweets(user_id);
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_sql)
            conn.commit()
        logger.info("✅ DB: approved_tweets table ready.")
    except Exception as e:
        logger.error(f"❌ DB init error: {e}")
        raise


# ── Insert ────────────────────────────────────────

def save_approved_tweet(
    user_id:      int,
    username:     Optional[str],
    flow:         str,
    tweet_number: int,
    tweet_text:   str,
    voice:        Optional[str] = None,
    pillar:       Optional[str] = None,
    bucket:       Optional[str] = None,
    hook:         Optional[str] = None,
    closing:      Optional[str] = None,
    output_type:  Optional[str] = None,
    context:      Optional[str] = None,
    source_tweet: Optional[str] = None,
    trend_input:  Optional[str] = None,
) -> Optional[int]:
    """
    Insert one approved tweet into the DB.
    Returns the new row id, or None on failure.
    """
    sql = """
    INSERT INTO approved_tweets (
        user_id, username,
        flow, voice, pillar, bucket, hook, closing, output_type,
        tweet_number, tweet_text, context, source_tweet, trend_input
    ) VALUES (
        %(user_id)s, %(username)s,
        %(flow)s, %(voice)s, %(pillar)s, %(bucket)s, %(hook)s, %(closing)s, %(output_type)s,
        %(tweet_number)s, %(tweet_text)s, %(context)s, %(source_tweet)s, %(trend_input)s
    )
    RETURNING id;
    """
    params = dict(
        user_id=user_id,
        username=username,
        flow=flow,
        voice=voice,
        pillar=pillar,
        bucket=bucket,
        hook=hook,
        closing=closing,
        output_type=output_type,
        tweet_number=tweet_number,
        tweet_text=tweet_text,
        context=context or "",
        source_tweet=source_tweet or "",
        trend_input=trend_input or "",
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                row_id = cur.fetchone()[0]
            conn.commit()
        logger.info(f"✅ DB: tweet saved (id={row_id}, user={user_id}, flow={flow})")
        return row_id
    except Exception as e:
        logger.error(f"❌ DB save error: {e}")
        return None


# ── Query: fetch examples for prompt injection ────

def get_approved_examples(
    voice:  Optional[str] = None,
    pillar: Optional[str] = None,
    limit:  int = 3,
) -> list[str]:
    """
    Fetch recent approved tweets filtered by voice and/or pillar.
    Used to inject real approved examples into the generation prompt.
    Returns a list of tweet_text strings.
    """
    conditions = ["status = 'approved'"]
    params: dict = {}

    if voice:
        conditions.append("voice = %(voice)s")
        params["voice"] = voice
    if pillar:
        conditions.append("pillar = %(pillar)s")
        params["pillar"] = pillar

    where = " AND ".join(conditions)
    sql = f"""
    SELECT tweet_text
    FROM approved_tweets
    WHERE {where}
    ORDER BY approved_at DESC
    LIMIT %(limit)s;
    """
    params["limit"] = limit

    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
        return [r["tweet_text"] for r in rows]
    except Exception as e:
        logger.error(f"❌ DB query error: {e}")
        return []


# ── Query: recent history for a user ─────────────

def get_user_history(user_id: int, limit: int = 5) -> list[dict]:
    """
    Fetch recent approved tweets for a specific user.
    """
    sql = """
    SELECT id, flow, voice, pillar, tweet_text, approved_at, status
    FROM approved_tweets
    WHERE user_id = %(user_id)s
    ORDER BY approved_at DESC
    LIMIT %(limit)s;
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, {"user_id": user_id, "limit": limit})
                return cur.fetchall()
    except Exception as e:
        logger.error(f"❌ DB history error: {e}")
        return []


# ── Query: total approved count ───────────────────

def get_total_approved() -> int:
    """Return total number of approved tweets across all users."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM approved_tweets WHERE status = 'approved';")
                return cur.fetchone()[0]
    except Exception as e:
        logger.error(f"❌ DB count error: {e}")
        return 0
