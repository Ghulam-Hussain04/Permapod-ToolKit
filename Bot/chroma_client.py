# ═══════════════════════════════════════════════
# chroma_client.py — ChromaDB semantic search
# for approved tweet examples
# ═══════════════════════════════════════════════
#
# Uses ChromaDB's default local embedding model
# (all-MiniLM-L6-v2) — no extra API key needed.
# Data persists via Docker volume at /app/chroma_data
# ═══════════════════════════════════════════════

import logging
import os
from typing import Optional

import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

# ── Persist path (mapped to Docker volume) ────────
CHROMA_PATH = os.environ.get("CHROMA_PATH", "/app/chroma_data")
COLLECTION_NAME = "approved_tweets"

# ── Singleton client ──────────────────────────────
_client: Optional[chromadb.ClientAPI] = None
_collection = None


def _get_collection():
    """
    Lazy-init ChromaDB persistent client and collection.
    Called on first use, reused after that.
    """
    global _client, _collection

    if _collection is not None:
        return _collection

    try:
        _client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False),
        )
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},  # cosine similarity for tweet comparison
        )
        logger.info(f"✅ ChromaDB ready — collection: {COLLECTION_NAME}")
        return _collection
    except Exception as e:
        logger.error(f"❌ ChromaDB init error: {e}")
        return None


# ── Store ─────────────────────────────────────────

def embed_and_store(
    tweet_id:   int,
    tweet_text: str,
    brand:      str = "permapod",
    voice:      Optional[str] = None,
    pillar:     Optional[str] = None,
    flow:       Optional[str] = None,
    bucket:     Optional[str] = None,
):
    """
    Embed a tweet and store it in ChromaDB.
    Called immediately after save_approved_tweet() in db.py flow.

    tweet_id must be unique — use the PostgreSQL row id.
    """
    collection = _get_collection()
    if collection is None:
        logger.warning("ChromaDB unavailable — skipping embed.")
        return

    try:
        collection.upsert(
            ids=[str(tweet_id)],
            documents=[tweet_text],
            metadatas=[{
                "brand":  brand  or "permapod",
                "voice":  voice  or "",
                "pillar": pillar or "",
                "flow":   flow   or "",
                "bucket": bucket or "",
            }],
        )
        logger.info(f"✅ ChromaDB: embedded tweet id={tweet_id}")
    except Exception as e:
        logger.error(f"❌ ChromaDB embed error: {e}")


# ── Search ────────────────────────────────────────

def search_similar(
    query:  str,
    brand:  str = "permapod",
    voice:  Optional[str] = None,
    pillar: Optional[str] = None,
    n:      int = 3,
) -> list[str]:
    """
    Semantic search for approved tweets similar to the query.
    Optionally filter by voice and/or pillar metadata.

    Returns a list of tweet_text strings (up to n results).
    Falls back to empty list if ChromaDB is unavailable or
    collection has fewer than n items.
    """
    collection = _get_collection()
    if collection is None:
        return []

    # Need at least n items in collection to query
    try:
        count = collection.count()
    except Exception:
        return []

    if count == 0:
        return []

    # Build metadata filter
    filters = [{"brand": brand or "permapod"}]
    if voice:
        filters.append({"voice": voice})
    if pillar:
        filters.append({"pillar": pillar})
    where: Optional[dict] = filters[0] if len(filters) == 1 else {"$and": filters}

    # Clamp n to available count
    n_results = min(n, count)

    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where if where else None,
        )
        docs = results.get("documents", [[]])[0]
        return docs
    except Exception as e:
        logger.error(f"❌ ChromaDB search error: {e}")
        return []


# ── Count ─────────────────────────────────────────

def get_chroma_count() -> int:
    """Return total number of embedded tweets."""
    collection = _get_collection()
    if collection is None:
        return 0
    try:
        return collection.count()
    except Exception:
        return 0
